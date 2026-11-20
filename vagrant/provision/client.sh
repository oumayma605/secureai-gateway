#!/usr/bin/env bash
# Client / Attaquant : outils d'attaque (uniquement dans le reseau interne du projet)
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get install -y --no-install-recommends hydra hping3
