#!/usr/bin/env python3
"""C2 - Prepare les donnees de test (J4) : liste de mots de passe + fichiers de hash.

Genere, de facon reproductible (graine fixe) :
  passwords/data/wordlist.txt         liste de candidats (dictionnaire)
  passwords/data/test_passwords.txt   mots de passe a hacher (certains sont dans la liste, d'autres non)
  passwords/hashes/<algo>.txt         une ligne "utilisateur:hash" par mot de passe, format John the Ripper

Les parametres de cout sont volontairement modestes pour que le craquage reste
faisable sur CPU dans une VM : ils sont reportes dans le rapport.
Usage : python3 passwords/gen_data.py [--mots 1000] [--hashes 10]
"""
import argparse
import base64
import hashlib
import os
import random
from pathlib import Path

import bcrypt
from argon2 import PasswordHasher
from argon2.low_level import Type

ROOT = Path(__file__).resolve().parent
DATA, HASHES = ROOT / "data", ROOT / "hashes"

# Parametres de cout utilises pour le craquage (voir docs/rapport_partieA.md)
PBKDF2_ITER = int(os.environ.get("PBKDF2_ITER", 10_000))
BCRYPT_COST = int(os.environ.get("BCRYPT_COST", 8))
ARGON2_T, ARGON2_M_KIB, ARGON2_P = 1, 8192, 1

BASES = """password admin welcome login master dragon monkey shadow sunshine princess
football baseball letmein trustno1 iloveyou secret azerty qwerty soleil bonjour
marseille paris tunisie maroc algerie camille nicolas thomas julie chocolat
football123 orange banane cerise hello world computer internet security
cyber hacker network server client linux ubuntu student projet ieee
summer winter spring autumn michael jessica jordan harley ranger""".split()
SUFFIXES = ["", "1", "12", "123", "1234", "!", "2024", "2025", "@1", "#1", "007", "99"]


def wordlist(n):
    mots = sorted({b + s for b in BASES for s in SUFFIXES} |
                  {b.capitalize() + s for b in BASES for s in SUFFIXES})
    random.Random(42).shuffle(mots)
    return mots[:n]


def test_passwords(mots, k):
    """~60 % presents dans la liste (faciles), le reste absents (robustes)."""
    dans = int(round(k * 0.6))
    presents = mots[: dans * 7 : 7][:dans]
    absents = ["Zx9#qLm2!vTb", "r7$Kp0wE_nA4", "Tr0ub4dor&3xyz", "j#8Fq!2mZ+Lc",
               "9vB^eR1t@Hy5", "uC6%dN3$kWp0", "Qm4&zX8!aLs2", "h2*Pf7#vYb9T"]
    return presents + absents[: k - len(presents)]


def ecrire(nom, lignes):
    HASHES.mkdir(parents=True, exist_ok=True)
    (HASHES / nom).write_text("\n".join(lignes) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mots", type=int, default=1000)
    ap.add_argument("--hashes", type=int, default=10)
    a = ap.parse_args()

    mots = wordlist(a.mots)
    pwds = test_passwords(mots, a.hashes)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "wordlist.txt").write_text("\n".join(mots) + "\n")
    (DATA / "test_passwords.txt").write_text("\n".join(pwds) + "\n")

    rng = random.Random(7)
    ph = PasswordHasher(time_cost=ARGON2_T, memory_cost=ARGON2_M_KIB,
                        parallelism=ARGON2_P, type=Type.ID)
    sha, pb, bc, ar = [], [], [], []
    for i, p in enumerate(pwds, 1):
        u, b = f"user{i}", p.encode()
        sha.append(f"{u}:{hashlib.sha256(b).hexdigest()}")
        salt = bytes(rng.getrandbits(8) for _ in range(16))
        dk = hashlib.pbkdf2_hmac("sha256", b, salt, PBKDF2_ITER)
        # format passlib lu par John : base64 "adapte" (+ -> ., sans =)
        ab64 = lambda x: base64.b64encode(x).decode().rstrip("=").replace("+", ".")
        pb.append(f"{u}:$pbkdf2-sha256${PBKDF2_ITER}${ab64(salt)}${ab64(dk)}")
        bc.append(f"{u}:{bcrypt.hashpw(b, bcrypt.gensalt(rounds=BCRYPT_COST)).decode()}")
        ar.append(f"{u}:{ph.hash(p)}")
    ecrire("sha256.txt", sha)
    ecrire("pbkdf2.txt", pb)
    ecrire("bcrypt.txt", bc)
    ecrire("argon2.txt", ar)
    print(f"OK : {len(mots)} mots, {len(pwds)} mots de passe, 4 fichiers dans passwords/hashes/")


if __name__ == "__main__":
    main()
