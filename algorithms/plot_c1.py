#!/usr/bin/env python3
"""Graphiques C1 a partir des CSV de results/ (moyenne +/- ecart-type)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RESULTS = Path(__file__).resolve().parent.parent / "results"


def barres(ax, df, col, titre, ylabel, log=False):
    g = df.groupby("algo")[col].agg(["mean", "std"]).fillna(0)
    ax.bar(g.index, g["mean"], yerr=g["std"], capsize=3)
    ax.set_title(titre); ax.set_ylabel(ylabel)
    if log:
        ax.set_yscale("log")
    ax.tick_params(axis="x", rotation=40)


sym = pd.read_csv(RESULTS / "c1_symetrique.csv")
fig, ax = plt.subplots(figsize=(8, 4.5))
barres(ax, sym, "mo_par_s", "C1 - AES et hachage (blocs de 8 Ko)", "Mo/s")
plt.tight_layout(); fig.savefig(RESULTS / "c1_symetrique.png", dpi=150)

asy = pd.read_csv(RESULTS / "c1_asymetrique.csv")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
barres(axes[0], asy, "signatures_par_s", "Signatures par seconde", "ops/s", log=True)
barres(axes[1], asy, "verifications_par_s", "Verifications par seconde", "ops/s", log=True)
plt.tight_layout(); fig.savefig(RESULTS / "c1_asymetrique.png", dpi=150)
print("OK -> results/c1_symetrique.png, c1_asymetrique.png")
