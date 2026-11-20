#!/usr/bin/env bash
# VM IDS optionnelle : Suricata en ecoute sur le reseau interne
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get install -y --no-install-recommends suricata
suricata-update || true
