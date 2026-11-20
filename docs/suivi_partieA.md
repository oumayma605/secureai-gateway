# Suivi - Étudiant A

| Jour | Tâche | Livrable | État |
|---|---|---|---|
| J1 | Dépôt, squelette | `algorithms/bench_utils.py`, `requirements.txt` | Fait |
| J2 | C1 : AES, SHA | `algorithms/bench_c1.py` | Script fait, **mesures à lancer en VM** |
| J3 | C1 : RSA, ECDSA, Ed25519, tailles, graphiques | `bench_c1.py`, `plot_c1.py` | Script fait, **mesures à lancer en VM** |
| J4 | C2 : hachage, liste de test | `passwords/gen_data.py`, `bench_c2.py` | Script fait, **mesures à lancer en VM** |
| J5 | C2 : craquage John the Ripper | `passwords/crack_c2.sh` | Script fait, **non testé (John absent du PC)** |
| J6 | Graphiques, sections du rapport | `plot_c1.py`, `plot_c2.py`, `docs/rapport_partieA.md` | Brouillon fait, chiffres à insérer |
| J7 | Synthèse avec B | `docs/grille_synthese_A.md` | Brouillon fait |
| J8 | Relecture, relance d'un coup | `run_all_A.sh` | Script fait |

## À faire dans la VM client
```bash
git clone https://github.com/oumayma605/secureai-gateway.git && cd secureai-gateway
git checkout partie-A
sudo apt install -y john python3-pip openssl
bash run_all_A.sh
```
Puis : captures d'écran dans `docs/captures/` (une par mesure), remplacer les `[MESURE]`
du rapport et de la grille, commit et push de `results/` et `docs/`.
