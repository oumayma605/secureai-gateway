#!/usr/bin/env python3
"""C2 - Temps de calcul d'un hash (J4) : SHA-256 simple, PBKDF2, bcrypt, Argon2.

5 repetitions par configuration (bench_utils). Sortie :
  results/c2_temps_hash.csv   algo, parametres, run, ms_par_hash
Usage : python3 passwords/bench_c2.py [--rep 5]
"""
import argparse
import hashlib
import os
import sys
from pathlib import Path

import bcrypt
from argon2 import PasswordHasher
from argon2.low_level import Type

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "algorithms"))
from bench_utils import REPETITIONS, ecrire_csv, mesurer, resume  # noqa: E402

RESULTS = Path(__file__).resolve().parent.parent / "results"
PWD = b"MotDePasseTest123!"
SALT = os.urandom(16)


def sha256():
    return hashlib.sha256(PWD).hexdigest()


def pbkdf2(it):
    return lambda: hashlib.pbkdf2_hmac("sha256", PWD, SALT, it)


def bcrypt_cost(c):
    return lambda: bcrypt.hashpw(PWD, bcrypt.gensalt(rounds=c))


def argon2(t, m, p):
    ph = PasswordHasher(time_cost=t, memory_cost=m, parallelism=p, type=Type.ID)
    return lambda: ph.hash(PWD.decode())


CAS = [("sha256", "sans sel", sha256)]
CAS += [("pbkdf2-sha256", f"{i} iterations", pbkdf2(i)) for i in (10_000, 100_000, 600_000)]
CAS += [("bcrypt", f"cout {c}", bcrypt_cost(c)) for c in (8, 10, 12, 14)]
CAS += [("argon2id", f"t={t} m={m // 1024}Mio p=1", argon2(t, m, 1))
        for t, m in ((1, 8192), (2, 19456), (3, 65536))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=REPETITIONS)
    a = ap.parse_args()
    lignes = []
    for algo, params, fn in CAS:
        durees = mesurer(fn, a.rep)
        for r, d in enumerate(durees, 1):
            lignes.append([algo, params, r, round(d * 1000, 4)])
        m, e = resume(durees)
        print(f"{algo:14s} {params:22s} {m * 1000:10.3f} ms  (+/- {e * 1000:.3f})")
    ecrire_csv(RESULTS / "c2_temps_hash.csv", lignes,
               ["algo", "parametres", "run", "ms_par_hash"])
    print("OK -> results/c2_temps_hash.csv")


if __name__ == "__main__":
    main()
