#!/usr/bin/env python3
"""
pwd_auditor_online.py

Vérificateur de robustesse de mot de passe (offline + vérification en ligne de compromissions).

Fonctionnalités principales :
 - Estimation d'entropie (local)
 - Détection de motifs faibles, répétitions, séquences (local)
 - Détection de mots du dictionnaire et "leet" (local, optionnel)
 - Vérification en ligne auprès de l'API "Pwned Passwords" (k-anonymity) pour savoir
   si un mot de passe apparaît dans des fuites publiques connues, sans envoyer le mot de passe complet.
 - Option JSON pour sortie machine-readable.

Notes de sécurité :
 - Le script n'envoie **jamais** le mot de passe en clair au réseau.
 - Il utilise le modèle k-anonymity (envoie les 5 premiers caractères du SHA-1).
 - Vous devez toujours prendre en compte la confidentialité et le contexte d'utilisation.
"""

import argparse
import hashlib
import math
import json
import re
import sys
import time
from typing import List, Tuple
from urllib import request, error

# --- Configuration réseau / API ---
HIBP_RANGE_API = "https://api.pwnedpasswords.com/range/{}"
USER_AGENT = "pwd_auditor_online/1.0 (contact: local)"  # adapter si nécessaire
HTTP_TIMEOUT = 10  # secondes

# --- Utilitaires locaux (mêmes que précédemment, adaptés) ---
BUILTIN_COMMON = {
    "123456", "password", "12345678", "qwerty", "abc123", "football",
    "monkey", "letmein", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "1234567", "sunshine", "master", "welcome", "shadow",
    "ashley", "password1", "admin", "passw0rd"
}

LEET_MAP = str.maketrans({
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a',
    '$': 's', '+': 't', '8': 'b', '9': 'g', '2': 'z'
})

def char_classes(password: str) -> Tuple[int, dict]:
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_space = any(c.isspace() for c in password)
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
        pool += 32
        breakdown['symbols'] = 32
    if has_space:
        pool += 1
        breakdown['space'] = 1

    return pool, breakdown

def estimate_entropy(password: str) -> float:
    pool, _ = char_classes(password)
    if pool <= 1 or not password:
        return 0.0
    return len(password) * math.log2(pool)

def load_wordlist(path: str) -> set:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return {line.strip().lower() for line in f if line.strip()}
    except Exception:
        return set()

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
    n = len(password)
    for l in range(min_repeat_len, n//2 + 1):
        if n % l != 0:
            continue
        chunk = password[:l]
        if chunk * (n // l) == password:
            return True
    return False

def has_long_repeat_char(password: str, threshold=4) -> bool:
    return any(len(m) >= threshold for m in re.findall(r'(.)\1*', password))

def has_sequential(password: str, seq_len=4) -> bool:
    if len(password) < seq_len:
        return False
    s = password.lower()
    for i in range(len(s) - seq_len + 1):
        chunk = s[i:i+seq_len]
        vals = []
        valid = True
        for c in chunk:
            if 'a' <= c <= 'z':
                vals.append(ord(c) - ord('a'))
            elif '0' <= c <= '9':
                vals.append(26 + ord(c) - ord('0'))
            else:
                valid = False
                break
        if not valid:
            continue
        ascending = all(vals[j+1] - vals[j] == 1 for j in range(len(vals)-1))
        descending = all(vals[j] - vals[j+1] == 1 for j in range(len(vals)-1))
        if ascending or descending:
            return True
    return False

# --- Vérification en ligne (k-anonymity avec Pwned Passwords) ---
def sha1_hex_upper(s: str) -> str:
    h = hashlib.sha1(s.encode('utf-8')).hexdigest().upper()
    return h

def query_hibp_range(prefix5: str) -> dict:
    """
    Interroge l'API range de Pwned Passwords pour un préfixe SHA1 de 5 caractères.
    Retourne un dict mapping suffix (40-5=35 chars) -> count (int).
    """
    url = HIBP_RANGE_API.format(prefix5)
    req = request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = {}
    try:
        with request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            body = r.read().decode('utf-8', errors='ignore')
            # lines au format: SUFFIX:COUNT
            for line in body.splitlines():
                parts = line.split(':')
                if len(parts) == 2:
                    suffix = parts[0].strip().upper()
                    try:
                        cnt = int(parts[1].strip())
                    except ValueError:
                        cnt = 0
                    resp[suffix] = cnt
    except error.HTTPError as e:
        # API peut renvoyer 429 (trop de requêtes) ou autres erreurs
        raise RuntimeError(f"Erreur HTTP lors de la requête HIBP: {e.code} {e.reason}")
    except Exception as e:
        raise RuntimeError(f"Erreur réseau lors de la requête HIBP: {e}")
    return resp

def check_pwned_password(password: str, max_retries=2, backoff=1.0) -> Tuple[bool, int]:
    """
    Retourne (pwned_boolean, count).
    Si pwned_boolean == True, count est le nombre d'occurrences retournées par HIBP (>=1).
    Si pwned_boolean == False, count == 0.
    Peut lever RuntimeError en cas d'erreur réseau/API.
    """
    sha1 = sha1_hex_upper(password)
    prefix = sha1[:5]
    suffix = sha1[5:]
    attempt = 0
    while True:
        try:
            table = query_hibp_range(prefix)
            cnt = table.get(suffix, 0)
            return (cnt > 0, cnt)
        except RuntimeError as e:
            attempt += 1
            if attempt > max_retries:
                raise
            time.sleep(backoff * attempt)

# --- Scoring et rapport ---
def score_password(password: str, dictset:set, extra_common:set, online_check:bool=True) -> dict:
    res = {}
    res['length'] = len(password)
    res['entropy_bits'] = round(estimate_entropy(password), 2)
    res['char_pool_breakdown'] = char_classes(password)[1]
    res['is_common_local'] = password.lower() in BUILTIN_COMMON or password.lower() in extra_common

    dict_found, dict_words = contains_dictionary_word(password, dictset) if dictset else (False, [])
    res['dictionary_words_found'] = dict_words
    res['has_leet_vuln'] = bool(dict_words)
    res['has_repeated_sequence'] = has_repeated_sequence(password)
    res['has_long_repeated_char'] = has_long_repeat_char(password)
    res['has_sequential'] = has_sequential(password)

    # Online check (pwned)
    res['pwned_checked'] = False
    res['pwned_occurrences'] = 0
    res['pwned_note'] = None
    if online_check:
        try:
            pwned, cnt = check_pwned_password(password)
            res['pwned_checked'] = True
            res['pwned_occurrences'] = int(cnt)
            if pwned:
                res['pwned_note'] = f"Mot de passe trouvé dans des fuites publiques ({cnt} occurrences rapportées)."
            else:
                res['pwned_note'] = "Aucune occurrence trouvée dans la base publique Pwned Passwords (à la date de la requête)."
        except Exception as e:
            res['pwned_checked'] = False
            res['pwned_note'] = f"Erreur lors de la vérification en ligne: {e}"

    # heuristique de score (conservatrice)
    score = 0
    eb = res['entropy_bits']
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

    if res['length'] >= 16:
        score += 20
    elif res['length'] >= 12:
        score += 12
    elif res['length'] >= 8:
        score += 6

    if res['is_common_local']:
        score -= 40
    if dict_found:
        score -= 20
    if res['has_repeated_sequence']:
        score -= 10
    if res['has_long_repeated_char']:
        score -= 8
    if res['has_sequential']:
        score -= 8
    # penalty for being pwned
    if res.get('pwned_checked') and res.get('pwned_occurrences', 0) > 0:
        # penalité très forte si le mot de passe est dans des fuites
        score -= 60

    score = max(0, min(100, score))
    res['score'] = int(score)
    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Weak"
    else:
        rating = "Very weak"
    res['rating'] = rating

    recs = []
    if res['length'] < 12:
        recs.append("Augmentez la longueur à ≥ 12 caractères (idéal ≥ 16).")
    if res['entropy_bits'] < 60:
        recs.append("Ajoutez diversité de caractères (minuscules, MAJ, chiffres, symboles).")
    if res['is_common_local']:
        recs.append("N'utilisez pas un mot de passe couramment utilisé ou réutilisé.")
    if dict_found:
        recs.append("Évitez d'utiliser des mots du dictionnaire même avec substitutions simples.")
    if res['has_long_repeated_char'] or res['has_repeated_sequence']:
        recs.append("Évitez les répétitions et motifs simples (aaaa, 12341234, abcabc).")
    if res['has_sequential']:
        recs.append("Évitez suites séquentielles (abcd, 1234).")
    if res.get('pwned_checked') and res.get('pwned_occurrences', 0) > 0:
        recs.append("Ce mot de passe figure dans des fuites publiques — changez-le immédiatement et n'utilisez pas ce mot de passe ailleurs.")
    if not recs:
        recs.append("Aucune recommandation critique — bonne pratique maintenue.")

    res['recommendations'] = recs
    return res

def pretty_report(res: dict) -> str:
    lines = []
    lines.append(f"Analyse du mot de passe (longueur {res['length']}):")
    lines.append(f" - Entropie estimée : {res['entropy_bits']} bits")
    lines.append(f" - Pool caractères détecté : {res['char_pool_breakdown']}")
    lines.append(f" - Note (0-100) : {res['score']} → {res['rating']}")
    lines.append(f" - Mot de passe localement reconnu comme très commun : {'Oui' if res['is_common_local'] else 'Non'}")
    if res['dictionary_words_found']:
        lines.append(f" - Mots du dictionnaire détectés : {res['dictionary_words_found']}")
    if res['has_repeated_sequence']:
        lines.append(" - Motif répété détecté (ex: abcabc, 1212).")
    if res['has_long_repeated_char']:
        lines.append(" - Séquence de caractères identiques détectée (ex: aaaa).")
    if res['has_sequential']:
        lines.append(" - Séquence ascendante/descendante détectée (ex: abcd, 1234).")
    if res.get('pwned_checked') is True:
        if res.get('pwned_occurrences', 0) > 0:
            lines.append(f" - COMPROMIS : trouvé dans des fuites ({res['pwned_occurrences']} occurrences).")
        else:
            lines.append(" - Vérification en ligne (Pwned Passwords) : aucune occurrence trouvée.")
    else:
        lines.append(f" - Vérification en ligne : non effectuée ou erreur ({res.get('pwned_note')}).")
    lines.append("\nRecommandations :")
    for r in res['recommendations']:
        lines.append(f" * {r}")
    lines.append("\nRemarque technique : la vérification en ligne utilise la méthode k-anonymity (SHA-1 prefix 5 caractères).")
    lines.append("Ainsi, le mot de passe en clair et le hash complet ne sont jamais transmis au service.")
    return "\n".join(lines)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Vérificateur local + en ligne de robustesse de mot de passe.")
    parser.add_argument("password", nargs='?', help="Mot de passe à analyser (si absent, mode interactif).")
    parser.add_argument("--no-online", action="store_true", help="Désactiver la vérification en ligne (mode offline uniquement).")
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
            pwd = input("Entrez le mot de passe à analyser : ")
        except KeyboardInterrupt:
            print("\nInterrompu.")
            return

    online_check = not args.no_online
    try:
        result = score_password(pwd, dictset, extra_common, online_check=online_check)
    except Exception as e:
        # Capture d'erreurs réseau: retourner un rapport partiel mais informatif
        result = {
            'length': len(pwd),
            'entropy_bits': round(estimate_entropy(pwd), 2),
            'char_pool_breakdown': char_classes(pwd)[1],
            'score': 0,
            'rating': 'Unknown',
            'recommendations': [f"Erreur lors de la vérification en ligne: {e}"]
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(pretty_report(result))

if __name__ == "__main__":
    main()
