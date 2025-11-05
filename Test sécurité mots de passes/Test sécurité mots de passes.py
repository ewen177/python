#!/usr/bin/env python3
"""
pwd_auditor.py

Vérificateur de robustesse de mot de passe (offline, éducatif / défensif).

Fonctionnalités :
- Estimation d'entropie (bits) basée sur les classes de caractères détectées.
- Détection de mots de passe dans une liste de "common passwords" intégrée.
- Détection de mots/dérivés par normalisation leet (ex: p4ssw0rd -> password).
- Détection de séquences (abcd, 1234), répétitions et motifs courts répétés.
- Rapport textuel et option JSON.
- CLI interactif et possibilité de fournir un fichier de mots communs / dictionnaire.
"""

import argparse
import math
import json
import re
from typing import List, Tuple

# Petite liste intégrée de mots de passe trop courants (exemples, non exhaustive)
BUILTIN_COMMON = {
    "123456", "password", "12345678", "qwerty", "abc123", "football",
    "monkey", "letmein", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "1234567", "sunshine", "master", "welcome", "shadow",
    "ashley", "password1", "admin", "passw0rd"
}

# Map pour "leet" simple
LEET_MAP = str.maketrans({
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a',
    '$': 's', '+': 't', '8': 'b', '9': 'g', '2': 'z'
})

def load_wordlist(path: str) -> set:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return {line.strip().lower() for line in f if line.strip()}
    except Exception:
        return set()

def char_classes(password: str) -> Tuple[int, dict]:
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_space = any(c.isspace() for c in password)
    # punctuation / symbols
    has_symbol = any((not c.isalnum() and not c.isspace()) for c in password)

    pool = 0
    breakdown = {}
    if has_lower:
        pool += 26
        breakdown['lower'] = 26
    if has_upper:
        pool += 26
        breakdown['upper'] = 26
    if has_digits:
        pool += 10
        breakdown['digits'] = 10
    if has_symbol:
        # approximation: printable ASCII punctuation set (common)
        pool += 32
        breakdown['symbols'] = 32
    if has_space:
        pool += 1
        breakdown['space'] = 1

    return pool, breakdown

def estimate_entropy(password: str) -> float:
    pool, breakdown = char_classes(password)
    if pool <= 1 or not password:
        return 0.0
    # entropy bits = length * log2(pool)
    entropy = len(password) * math.log2(pool)
    return entropy

def is_common(password: str, extra_common:set) -> bool:
    p = password.lower()
    if p in BUILTIN_COMMON:
        return True
    if p in extra_common:
        return True
    return False

def leet_normalize(s: str) -> str:
    return s.translate(LEET_MAP)

def contains_dictionary_word(password: str, dictset:set, min_len=4) -> Tuple[bool, List[str]]:
    lowered = password.lower()
    leeted = leet_normalize(lowered)
    found = []
    for w in dictset:
        if len(w) < min_len:
            continue
        if w in lowered or w in leeted:
            found.append(w)
    return (len(found) > 0), found

def has_repeated_sequence(password: str, min_repeat_len=2) -> bool:
    # detect patterns like "abcabc", "1212", "aaaa"
    n = len(password)
    for l in range(min_repeat_len, n//2 + 1):
        if n % l != 0:
            continue
        chunk = password[:l]
        if chunk * (n // l) == password:
            return True
    return False

def has_long_repeat_char(password: str, threshold=4) -> bool:
    # same char repeated >= threshold
    return any(len(m) >= threshold for m in re.findall(r'(.)\1*', password))

def has_sequential(password: str, seq_len=4) -> bool:
    if len(password) < seq_len:
        return False
    s = password.lower()
    # check alnum sequential ascending or descending
    for i in range(len(s) - seq_len + 1):
        chunk = s[i:i+seq_len]
        # map characters to ordinal positions for letters/digits, others get None
        vals = []
        valid = True
        for c in chunk:
            if 'a' <= c <= 'z':
                vals.append(ord(c) - ord('a'))
            elif '0' <= c <= '9':
                vals.append(26 + ord(c) - ord('0'))  # digits after letters
            else:
                valid = False
                break
        if not valid:
            continue
        # check ascending
        ascending = all(vals[j+1] - vals[j] == 1 for j in range(len(vals)-1))
        descending = all(vals[j] - vals[j+1] == 1 for j in range(len(vals)-1))
        if ascending or descending:
            return True
    return False

def score_password(password: str, dictset:set, extra_common:set) -> dict:
    result = {}
    result['length'] = len(password)
    result['entropy_bits'] = round(estimate_entropy(password), 2)
    result['char_pool_breakdown'] = char_classes(password)[1]
    result['is_common'] = is_common(password, extra_common)

    dict_found, dict_words = contains_dictionary_word(password, dictset) if dictset else (False, [])
    result['dictionary_words_found'] = dict_words
    result['has_leet_vuln'] = bool(dict_words)

    result['has_repeated_sequence'] = has_repeated_sequence(password)
    result['has_long_repeated_char'] = has_long_repeat_char(password)
    result['has_sequential'] = has_sequential(password)

    # simple heuristic score (0-100). This is intentionally conservative and explainable.
    score = 0
    # base by entropy
    eb = result['entropy_bits']
    if eb >= 80:
        score += 50
    elif eb >= 60:
        score += 40
    elif eb >= 40:
        score += 30
    elif eb >= 28:
        score += 20
    else:
        score += 10

    # length bonus
    if result['length'] >= 16:
        score += 20
    elif result['length'] >= 12:
        score += 12
    elif result['length'] >= 8:
        score += 6

    # penalties
    if result['is_common']:
        score -= 40
    if dict_found:
        score -= 20
    if result['has_repeated_sequence']:
        score -= 10
    if result['has_long_repeated_char']:
        score -= 8
    if result['has_sequential']:
        score -= 8

    # clamp
    score = max(0, min(100, score))
    result['score'] = int(score)

    # qualitative rating
    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Weak"
    else:
        rating = "Très faible"
    result['rating'] = rating

    # recommendations
    recs = []
    if result['length'] < 12:
        recs.append("Augmentez la longueur à ≥ 12 caractères (idéal ≥ 16).")
    if result['entropy_bits'] < 60:
        recs.append("Ajoutez diversité de caractères (minuscules, MAJ, chiffres, symboles).")
    if result['is_common']:
        recs.append("N'utilisez pas un mot de passe commun ou réutilisé.")
    if dict_found:
        recs.append("Évitez d'utiliser des mots du dictionnaire même avec substitutions simples (leet).")
    if result['has_long_repeated_char'] or result['has_repeated_sequence']:
        recs.append("Évitez les répétitions et motifs simples (aaaa, 12341234, abcabc).")
    if result['has_sequential']:
        recs.append("Évitez suites séquentielles (abcd, 1234).")
    if not recs:
        recs.append("Aucune recommandation critique — bonne pratique maintenue.")

    result['recommendations'] = recs

    return result

def pretty_report(res: dict, password: str) -> str:
    lines = []
    lines.append(f"Analyse du mot de passe (longueur {res['length']}):")
    lines.append(f" - Entropie estimée : {res['entropy_bits']} bits")
    lines.append(f" - Pool caractères détecté : {res['char_pool_breakdown']}")
    lines.append(f" - Note (0-100) : {res['score']} → {res['rating']}")
    lines.append(f" - Mot de passe commun connu : {'Oui' if res['is_common'] else 'Non'}")
    if res['dictionary_words_found']:
        lines.append(f" - Mots du dictionnaire détectés (après normalisation leet) : {res['dictionary_words_found']}")
    if res['has_repeated_sequence']:
        lines.append(" - Motif répété détecté (ex: abcabc, 1212).")
    if res['has_long_repeated_char']:
        lines.append(" - Séquence de caractères identiques détectée (ex: aaaa).")
    if res['has_sequential']:
        lines.append(" - Séquence ascendante/descendante détectée (ex: abcd, 1234).")
    lines.append("\nRecommandations :")
    for r in res['recommendations']:
        lines.append(f" * {r}")
    lines.append("\nMéthode (résumé) : entropie calculée = longueur × log2(pool_est.) ;")
    lines.append("vérifications supplémentaires : mots fréquents, mots du dictionnaire (avec dé-léetspeak), motifs répétitifs et séquences.")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Vérificateur local de robustesse de mot de passe (offline).")
    parser.add_argument("password", nargs='?', help="Mot de passe à analyser. Si absent, passe en mode interactif.")
    parser.add_argument("--common", "-c", help="Chemin vers un fichier de mots de passe communs (un par ligne).")
    parser.add_argument("--dict", "-d", help="Chemin vers un dictionnaire de mots (un par ligne) pour détection.")
    parser.add_argument("--json", action="store_true", help="Sortie JSON.")
    args = parser.parse_args()

    extra_common = set()
    dictset = set()

    if args.common:
        extra_common = load_wordlist(args.common)

    if args.dict:
        dictset = load_wordlist(args.dict)

    if args.password:
        pwd = args.password
    else:
        try:
            pwd = input("Entrez le mot de passe à analyser (entrée non affichée possible selon votre terminal) : ")
        except KeyboardInterrupt:
            print("\nInterrompu.")
            return

    result = score_password(pwd, dictset, extra_common)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(pretty_report(result, pwd))

if __name__ == "__main__":
    main()
