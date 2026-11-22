#!/usr/bin/env bash
# C2 - Craquage avec John the Ripper (CPU) sur une liste fixe (J5).
# A lancer UNIQUEMENT dans la VM du projet, sur les hashes generes par gen_data.py.
# Sortie : results/c2_craquage.csv
#   algo, run, secondes, trouves, total, ms_par_tentative
# Usage : bash passwords/crack_c2.sh        (REPS=5 par defaut)
set -euo pipefail
cd "$(dirname "$0")/.."
REPS=${REPS:-5}
WL=passwords/data/wordlist.txt
OUT=results/c2_craquage.csv
JOHN=${JOHN:-john}
command -v "$JOHN" >/dev/null || { echo "john introuvable (sudo apt install john)"; exit 1; }
[ -f "$WL" ] && [ -f passwords/hashes/bcrypt.txt ] || python3 passwords/gen_data.py
mkdir -p results
NMOTS=$(wc -l < "$WL")
echo "algo,run,secondes,trouves,total,ms_par_tentative" > "$OUT"

# nom_fichier:format John
for spec in sha256:raw-sha256 pbkdf2:PBKDF2-HMAC-SHA256 bcrypt:bcrypt argon2:argon2; do
  algo=${spec%%:*}; fmt=${spec##*:}
  f=passwords/hashes/$algo.txt
  total=$(wc -l < "$f")
  if ! "$JOHN" --list=formats 2>/dev/null | tr ',' '\n' | tr -d ' ' | grep -qix "$fmt"; then
    echo "format $fmt non supporte par cette version de john : $algo ignore" >&2
    continue
  fi
  for run in $(seq 1 "$REPS"); do
    pot=$(mktemp)                    # pot vide a chaque essai = meme travail
    t0=$(date +%s.%N)
    "$JOHN" --format="$fmt" --wordlist="$WL" --pot="$pot" "$f" >/dev/null 2>&1 || true
    t1=$(date +%s.%N)
    trouves=$("$JOHN" --show --format="$fmt" --pot="$pot" "$f" 2>/dev/null \
              | awk '/password hash(es)? cracked/ {print $1}')
    rm -f "$pot"
    awk -v a="$algo" -v r="$run" -v t0="$t0" -v t1="$t1" -v f="${trouves:-0}" \
        -v tot="$total" -v n="$NMOTS" 'BEGIN {
          s = t1 - t0; tent = tot * n;
          printf "%s,%d,%.3f,%d,%d,%.4f\n", a, r, s, f, tot, s * 1000 / tent }' >> "$OUT"
  done
  echo "$algo : termine"
done
echo "OK -> $OUT"
