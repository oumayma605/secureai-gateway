#!/usr/bin/env python3
"""Graphiques C2 a partir des CSV de results/ (moyenne +/- ecart-type)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path(__file__).resolve().parent.parent / "results"

t = pd.read_csv(RESULTS / "c2_temps_hash.csv")
t["etiquette"] = t["algo"] + "\n" + t["parametres"]
g = t.groupby("etiquette", sort=False)["ms_par_hash"].agg(["mean", "std"]).fillna(0)
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(g.index, g["mean"], yerr=g["std"], capsize=3)
ax.set_yscale("log"); ax.set_ylabel("ms par hash (echelle log)")
ax.set_title("C2 - temps de calcul d'un hash")
ax.tick_params(axis="x", rotation=60, labelsize=7)
plt.tight_layout(); fig.savefig(RESULTS / "c2_temps_hash.png", dpi=150)

c = RESULTS / "c2_craquage.csv"
d = pd.read_csv(c) if c.exists() else pd.DataFrame()
if len(d):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    s = d.groupby("algo")["secondes"].agg(["mean", "std"]).fillna(0)
    axes[0].bar(s.index, s["mean"], yerr=s["std"], capsize=3)
    axes[0].set_yscale("log"); axes[0].set_ylabel("secondes"); axes[0].set_title("Temps de craquage")
    f = d.groupby("algo")[["trouves", "total"]].mean()
    axes[1].bar(f.index, f["trouves"]); axes[1].set_ylim(0, f["total"].max())
    axes[1].set_ylabel("mots de passe trouves"); axes[1].set_title("Mots de passe craques")
    plt.tight_layout(); fig.savefig(RESULTS / "c2_craquage.png", dpi=150)
print("OK -> results/c2_*.png")
