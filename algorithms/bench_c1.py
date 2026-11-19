#!/usr/bin/env python3
"""C1 - Algorithmes cryptographiques (Etudiant A).

Mesure avec `openssl speed` (5 repetitions, meme duree pour tous les algos) :
  - AES-128/256 (CBC, GCM), SHA-256, SHA3-256  -> debit en Mo/s
  - RSA-2048, RSA-4096, ECDSA P-256, Ed25519    -> signatures/s et verifications/s
et releve la taille reelle des cles et des signatures.

Sorties (dossier results/) :
  c1_symetrique.csv   algo, run, mo_par_s
  c1_asymetrique.csv  algo, run, signatures_par_s, verifications_par_s
  c1_tailles.csv      algo, cle_privee_octets, cle_publique_octets, signature_octets

Usage : python3 algorithms/bench_c1.py [--duree 3] [--rep 5]
Variable OPENSSL pour choisir le binaire (sinon `openssl` du PATH).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench_utils import REPETITIONS, ecrire_csv, resume  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

SYMETRIQUE = ["aes-128-cbc", "aes-256-cbc", "aes-128-gcm", "aes-256-gcm",
              "sha256", "sha3-256"]
# nom openssl speed -> (prefixe -mr, colonne signature, colonne verification)
ASYMETRIQUE = {
    "rsa2048": ("+F2:", 3, 4),
    "rsa4096": ("+F2:", 3, 4),
    "ecdsap256": ("+F4:", 3, 4),
    "ed25519": ("+F6:", 4, 5),
}


def trouver_openssl():
    cand = os.environ.get("OPENSSL") or shutil.which("openssl")
    if not cand:
        git = Path(r"C:\Program Files\Git\usr\bin\openssl.exe")
        cand = str(git) if git.exists() else None
    if not cand:
        sys.exit("openssl introuvable (definir la variable OPENSSL)")
    return cand


def run(openssl, *args, **kw):
    return subprocess.run([openssl, *args], capture_output=True, text=True,
                          check=kw.pop("check", True), **kw)


def debit_symetrique(openssl, algo, duree):
    """Mo/s sur des blocs de 8192 octets (ligne machine '+F:<n>:<ALGO>:<octets/s>')."""
    out = run(openssl, "speed", "-seconds", str(duree), "-bytes", "8192",
              "-mr", "-evp", algo).stdout
    for ligne in out.splitlines():
        if ligne.startswith("+F:"):
            return float(ligne.split(":")[3]) / 1e6
    raise RuntimeError(f"sortie inattendue pour {algo}:\n{out}")


def debit_asymetrique(openssl, algo, duree):
    prefixe, c_sign, c_verif = ASYMETRIQUE[algo]
    out = run(openssl, "speed", "-seconds", str(duree), "-mr", algo).stdout
    bits = {"rsa2048": "2048", "rsa4096": "4096"}.get(algo)
    for ligne in out.splitlines():
        if not ligne.startswith(prefixe):
            continue
        p = ligne.split(":")
        if bits and p[2] != bits:
            continue
        return float(p[c_sign]), float(p[c_verif])
    raise RuntimeError(f"sortie inattendue pour {algo}:\n{out}")


def taille(path):
    return os.path.getsize(path)


def tailles(openssl):
    """Genere une cle par algo, signe un message et renvoie les tailles (octets)."""
    lignes = []
    specs = [
        ("rsa2048", ["genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048"], False),
        ("rsa4096", ["genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:4096"], False),
        ("ecdsap256", ["genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256"], False),
        ("ed25519", ["genpkey", "-algorithm", "ED25519"], True),
    ]
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        msg = d / "msg.txt"
        msg.write_bytes(b"message de test C1")
        for nom, gen, rawin in specs:
            priv, pub, sig = d / f"{nom}.der", d / f"{nom}.pub.der", d / f"{nom}.sig"
            run(openssl, *gen, "-outform", "DER", "-out", str(priv))
            run(openssl, "pkey", "-inform", "DER", "-in", str(priv),
                "-pubout", "-outform", "DER", "-out", str(pub))
            if rawin:
                run(openssl, "pkeyutl", "-sign", "-rawin", "-inkey", str(priv),
                    "-keyform", "DER", "-in", str(msg), "-out", str(sig))
            else:
                run(openssl, "dgst", "-sha256", "-sign", str(priv),
                    "-keyform", "DER", "-out", str(sig), str(msg))
            lignes.append([nom, taille(priv), taille(pub), taille(sig)])
    return lignes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duree", type=int, default=3, help="secondes par mesure")
    ap.add_argument("--rep", type=int, default=REPETITIONS)
    a = ap.parse_args()
    ossl = trouver_openssl()
    print("openssl :", run(ossl, "version").stdout.strip())

    sym, mesures = [], {}
    for algo in SYMETRIQUE:
        vals = []
        for r in range(1, a.rep + 1):
            v = debit_symetrique(ossl, algo, a.duree)
            sym.append([algo, r, round(v, 2)])
            vals.append(v)
        mesures[algo] = vals
        m, e = resume(vals)
        print(f"{algo:12s} {m:10.1f} Mo/s  (+/- {e:.1f})")
    ecrire_csv(RESULTS / "c1_symetrique.csv", sym, ["algo", "run", "mo_par_s"])

    asym = []
    for algo in ASYMETRIQUE:
        sig, ver = [], []
        for r in range(1, a.rep + 1):
            s, v = debit_asymetrique(ossl, algo, a.duree)
            asym.append([algo, r, round(s, 1), round(v, 1)])
            sig.append(s); ver.append(v)
        print(f"{algo:12s} sign {resume(sig)[0]:9.1f}/s   verif {resume(ver)[0]:9.1f}/s")
    ecrire_csv(RESULTS / "c1_asymetrique.csv", asym,
               ["algo", "run", "signatures_par_s", "verifications_par_s"])

    ecrire_csv(RESULTS / "c1_tailles.csv", tailles(ossl),
               ["algo", "cle_privee_octets", "cle_publique_octets", "signature_octets"])
    print("OK ->", RESULTS)


if __name__ == "__main__":
    main()
