#!/usr/bin/env bash
# Commun a toutes les VMs. Idempotent : peut etre relance (vagrant provision).
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y --no-install-recommends \
  openssl iperf3 tcpdump nmap net-tools iproute2 curl git \
  nftables john python3 python3-pip python3-venv

# Bureau Lubuntu (leger, base LXQt) uniquement si demande
if [ "${WITH_GUI:-0}" = "1" ] && ! dpkg -s lubuntu-desktop >/dev/null 2>&1; then
  apt-get install -y lubuntu-desktop sddm wireshark
  # Wireshark : autoriser l'utilisateur vagrant a capturer
  echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
  dpkg-reconfigure -f noninteractive wireshark-common || true
  usermod -aG wireshark vagrant || true
fi

# Bibliotheques Python du projet (Etudiant A)
if [ -f /home/vagrant/project/requirements.txt ]; then
  pip3 install --quiet -r /home/vagrant/project/requirements.txt
fi
