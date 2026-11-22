# secureai-gateway

Mini-projet sécurité : évaluation comparative de solutions de sécurité (algorithmes,
hachage de mots de passe, protocoles, IDS/firewall).

## Livrables
- Rapport : `docs/rapport_final.pdf` (source LaTeX : `docs/latex/rapport_final.tex` ; partie A détaillée dans `docs/rapport_partieA.md`)
- Résultats : `results/` ; captures : `docs/captures/`

## Labo (VMs)
Le plan prévoit un client (10.0.0.10) et un serveur (10.0.0.20). Pour recréer le labo avec
Vagrant (Lubuntu) : `cd vagrant && vagrant up client` (partie A) ou `vagrant up` (client + serveur).

## Partie A (C1 algorithmes, C2 mots de passe)
Dans la VM client, depuis la racine du dépôt :
```bash
sudo apt install -y python3-pip openssl && sudo snap install john-the-ripper   # John "jumbo" requis
bash run_all_A.sh        # C1 + C2 + graphiques -> results/
```
Détails : `docs/suivi_partieA.md`.

## Partie B (C3 protocoles, C4 IDS/firewall)
Voir `config/`, `protocols/`, `ids/`.
