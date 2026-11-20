#!/usr/bin/env bash
# Serveur : SSH, web, iperf3, TLS / WireGuard / IPsec, Suricata (si pas de VM IDS)
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get install -y --no-install-recommends \
  openssh-server nginx stunnel4 wireguard-tools strongswan suricata
systemctl enable --now ssh nginx
# Serveur iperf3 en service
cat >/etc/systemd/system/iperf3.service <<'EOF'
[Unit]
Description=iperf3 server
After=network.target
[Service]
ExecStart=/usr/bin/iperf3 -s
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now iperf3
