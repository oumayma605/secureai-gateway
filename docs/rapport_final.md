# Évaluation comparative de solutions de sécurité

Mini-projet sécurité - rapport final (4 à 5 pages minimum)
Étudiants : A (cryptographie, mots de passe) et B (réseau, protocoles, IDS) - `[noms et date]`

> Document commun. Les parties A sont reprises de `docs/rapport_partieA.md` ; les parties B
> sont à compléter par B à partir de `config/`, `results/` et `docs/captures/`.
> Remplacer tous les `[MESURE]` / `[B]` avant export en PDF.
> Export PDF : coller dans Word/Google Docs, ou `pandoc rapport_final.md -o rapport_final.pdf`.

## 1. Introduction et problématique
Quelles solutions de sécurité (protocoles, algorithmes, hachage de mots de passe, système de
détection d'intrusion) faut-il choisir pour protéger une communication réseau, en fonction de
la sécurité apportée, des performances et de la complexité de configuration ?
Le projet consiste à **configurer, attaquer, mesurer et comparer** plusieurs solutions, puis
à recommander un choix argumenté selon le besoin. Quatre comparaisons : C1 algorithmes
cryptographiques, C2 hachage de mots de passe, C3 protocoles de protection du trafic,
C4 IDS et firewall.

## 2. Architecture du laboratoire `[B]`
Réseau virtuel interne (VirtualBox), sans accès extérieur pendant les attaques ; une carte NAT
temporaire sert uniquement à installer les paquets.

| VM | Rôle | IP | RAM |
|---|---|---|---|
| Client / Attaquant | génère le trafic, lance Nmap, Hydra, hping3, iperf3 | 10.0.0.10 | 2 Go |
| Serveur | SSH, web, iperf3, endpoints TLS / WireGuard / IPsec | 10.0.0.20 | 2 Go |
| IDS (optionnelle) | Suricata en écoute (sinon sur le serveur) | 10.0.0.30 | 2 Go |

`[B]` Insérer le schéma du réseau et les captures `docs/captures/client_ip.png`,
`serveur_ip.png`, `ping.png`. Le dossier `vagrant/` permet de recréer le labo (Lubuntu).

## 3. Méthode de comparaison
- Critères fixés à l'avance : sécurité, performance (débit, latence, CPU, temps de calcul),
  complexité de configuration, cas d'usage conseillé.
- Mêmes conditions pour toutes les solutions : mêmes VMs, même durée, même charge.
- 5 répétitions par mesure, moyenne et écart-type, résultats en CSV dans `results/`.
- Un script par comparaison, graphiques avec pandas/matplotlib, capture de preuve pour chaque
  configuration et chaque attaque.
- Éthique : toutes les attaques se font uniquement dans le réseau virtuel du projet.

## 4. C1 et C2 : algorithmes et mots de passe (partie A)
Reprendre les sections 3 et 4 de `docs/rapport_partieA.md` (configuration, résultats,
analyse) avec les graphiques `results/c1_*.png` et `results/c2_*.png`.

## 5. C3 : protocoles de protection du trafic `[B]`
- Configurations : clair (référence), TLS avec stunnel (`config/stunnel.conf`), WireGuard,
  IPsec (strongSwan) ou SSH/OpenVPN en secours.
- Mesures : iperf3 (débit), ping (latence), CPU, temps d'établissement.
- Références déjà relevées dans le dépôt : en clair 864 Mbit/s et 1,54 ms (à confirmer avec
  `results/clair_iperf.csv` et `clair_ping.txt`).
- Captures Wireshark : en clair le contenu est lisible, avec TLS/WireGuard/IPsec il ne l'est pas
  (`docs/captures/wireshark_clair_*.png`, `tls_*.png`).

## 6. C4 : IDS et firewall `[B]`
Suricata (interface, règles, `suricata-update`, `eve.json`, `suricata -T`), attaques Nmap
et Hydra, alertes obtenues, faux positifs, règles nftables (politique DROP, limitation de
débit), comparaison avant / après.

## 7. Synthèse comparative et recommandations
Tableau final (lignes de A dans `docs/grille_synthese_A.md`, lignes de B à ajouter) :

| Solution | Sécurité | Performance | Complexité | Recommandée pour |
|---|---|---|---|---|
| AES-GCM / AES-CBC | | | | |
| RSA / ECDSA / Ed25519 | | | | |
| SHA-256 / PBKDF2 / bcrypt / Argon2 | | | | |
| Clair / TLS / WireGuard / IPsec | | | | |
| Suricata + nftables | | | | |

Conclusions argumentées : `[à rédiger ensemble en J7]`, une recommandation par besoin
(chiffrer des données, signer, stocker des mots de passe, protéger un flux, détecter).

## 8. Conclusion, limites et extensions
- Limites : mesures en VM (virtualisation), un seul CPU, liste de mots de passe courte,
  coûts de craquage réduits, scénarios d'attaque simulés.
- Extensions possibles : OpenVPN, PKI avec révocation (CRL), attaque man-in-the-middle,
  comparaison de plusieurs firewalls.

## Annexes
Captures (`docs/captures/`), configurations commentées (`config/`), scripts
(`algorithms/`, `passwords/`, `run_all_A.sh`), résultats (`results/`).
