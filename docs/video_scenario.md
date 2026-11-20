# Vidéo du projet - scénario et checklist

Durée conseillée : **6 à 8 minutes** (vérifier la consigne exacte du professeur : durée, format,
dépôt de la vidéo). Les deux étudiants parlent.
Enregistrer l'écran avec **OBS Studio** (gratuit) ou, sur Windows, **Win + G** (Xbox Game Bar) ;
dans la VM, l'enregistrement se fait depuis Windows en capturant la fenêtre VirtualBox.

## Plan minuté

| Temps | Contenu | Qui | À l'écran |
|---|---|---|---|
| 0:00-0:40 | Présentation, problématique, objectifs | A | Diapo titre + problématique |
| 0:40-1:20 | Architecture du labo (VMs, IP, réseau isolé), méthode (5 répétitions, mêmes conditions) | B | Schéma + tableau des VMs |
| 1:20-2:50 | **Démo C1** : `bench_c1.py`, lecture des débits AES-GCM / CBC, RSA / ECDSA / Ed25519, tailles de clés | A | Terminal de la VM client + graphiques |
| 2:50-4:20 | **Démo C2** : temps de hachage, craquage John the Ripper (SHA-256 vs bcrypt vs Argon2), mots de passe trouvés | A | Terminal + `c2_craquage.png` |
| 4:20-5:20 | **Démo C3** : iperf3 / ping en clair vs TLS vs WireGuard, Wireshark (illisible vs lisible) | B | Terminal + Wireshark |
| 5:20-6:20 | **Démo C4** : Nmap/Hydra sur le serveur, alertes Suricata, effet des règles nftables | B | Terminal + `eve.json` / alertes |
| 6:20-7:30 | Synthèse et recommandations (tableau final), limites | A + B | Grille de synthèse |
| 7:30-8:00 | Conclusion, remerciements | B | Diapo de fin |

## Préparation (la veille)
- [ ] Toutes les mesures faites, CSV et graphiques dans `results/`.
- [ ] VMs à jour, snapshot pris, autres applications fermées.
- [ ] Commandes de démo **courtes** (par ex. `python3 algorithms/bench_c1.py --duree 1 --rep 2`)
  : la démo en direct ne doit pas durer des minutes ; montrer ensuite les vrais résultats.
- [ ] Démo de secours : captures d'écran et mini-vidéo déjà enregistrées.
- [ ] Texte lu ou notes devant soi, micro testé, police du terminal agrandie (Ctrl +).
- [ ] Attaques uniquement dans le réseau virtuel du projet (le dire à l'oral).

## Commandes de démo (partie A)
```bash
cd ~/secureai-gateway
python3 algorithms/bench_c1.py --duree 1 --rep 2      # C1 en version courte
python3 passwords/bench_c2.py --rep 2                  # temps de hachage
bash passwords/crack_c2.sh                              # craquage John (REPS=1 pour aller vite)
```

## Texte d'ouverture (exemple)
« Bonjour, notre projet compare des solutions de sécurité pour protéger une communication
réseau : algorithmes de chiffrement, hachage de mots de passe, protocoles TLS, WireGuard et
IPsec, et détection d'intrusion avec Suricata. Nous ne nous contentons pas de les utiliser :
nous les configurons, les attaquons dans un réseau virtuel isolé, les mesurons, puis nous
recommandons un choix argumenté. »

## Après l'enregistrement
- [ ] Voir la vidéo en entier (son, texte lisible, pas de mot de passe ou d'information
  personnelle visible).
- [ ] Exporter en MP4, vérifier la taille, la déposer là où le professeur le demande.
