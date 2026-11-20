#!/usr/bin/env bash
# Relance toute la partie A d'un seul coup (C1 puis C2) - a lancer dans la VM client.
# Usage : bash run_all_A.sh
set -euo pipefail
cd "$(dirname "$0")"
pip3 install --quiet -r requirements.txt
echo "== C1 : algorithmes =="
python3 algorithms/bench_c1.py
echo "== C2 : temps de hachage =="
python3 passwords/bench_c2.py
echo "== C2 : donnees + craquage John the Ripper =="
python3 passwords/gen_data.py
bash passwords/crack_c2.sh
echo "== Graphiques =="
python3 algorithms/plot_c1.py
python3 passwords/plot_c2.py
echo "Termine : voir results/"
