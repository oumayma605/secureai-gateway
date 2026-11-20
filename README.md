# secureai-gateway

Mini-projet sécurité : évaluation comparative de solutions de sécurité (algorithmes,
hachage de mots de passe, protocoles, IDS/firewall).

## Partie A (C1 algorithmes, C2 mots de passe)
Dans la VM client, depuis la racine du dépôt :
```bash
sudo apt install -y john python3-pip openssl
bash run_all_A.sh        # C1 + C2 + graphiques -> results/
```
Détails : `docs/suivi_partieA.md`, brouillon du rapport : `docs/rapport_partieA.md`.

## Partie B (C3 protocoles, C4 IDS/firewall)
Voir `config/`, `protocols/`, `ids/`.
