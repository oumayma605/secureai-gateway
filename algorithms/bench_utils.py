import csv
import statistics
import time
from pathlib import Path

REPETITIONS = 5


def mesurer(fonction, repetitions=REPETITIONS):
    """Lance fonction() plusieurs fois et renvoie la liste des durées (secondes)."""
    durees = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction()
        durees.append(time.perf_counter() - debut)
    return durees


def resume(durees):
    """Renvoie (moyenne, écart-type) d'une liste de durées."""
    moyenne = statistics.mean(durees)
    ecart = statistics.stdev(durees) if len(durees) > 1 else 0.0
    return moyenne, ecart


def ecrire_csv(chemin, lignes, entetes):
    """Écrit un fichier CSV, en créant le dossier si besoin."""
    Path(chemin).parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(entetes)
        w.writerows(lignes)
