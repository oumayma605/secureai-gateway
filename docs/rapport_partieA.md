# Rapport - Partie A : cryptographie (C1) et mots de passe (C2)

> Partie de l'étudiant A. Chiffres issus de `results/` (moyennes de 5 répétitions, VM
> Lubuntu 22.04, 2 vCPU). Restent à ajouter : les captures d'écran dans `docs/captures/`.

## 1. Introduction et problématique

Quelles solutions de sécurité faut-il choisir pour protéger une communication réseau, en
fonction de la sécurité apportée, des performances et de la complexité de configuration ?
Cette partie traite deux briques : les **algorithmes cryptographiques** (C1) et le
**hachage de mots de passe** (C2). L'objectif n'est pas d'utiliser des solutions toutes
faites mais de les configurer, les mesurer, les attaquer et les comparer.

## 2. Méthode de comparaison

- Critères fixés à l'avance : **sécurité** (ce que peut faire un attaquant), **performance**
  (débit, opérations par seconde, temps de calcul), **complexité** (réglages, pièges),
  **cas d'usage conseillé**.
- Mêmes conditions pour tous les tests : même VM client (Lubuntu/Ubuntu, 2 Go, 2 vCPU),
  même durée de mesure (3 s par test `openssl speed`), autres applications fermées.
- **5 répétitions** par mesure, moyenne et écart-type (`algorithms/bench_utils.py`).
- Résultats en CSV dans `results/`, un script par comparaison, graphiques avec
  pandas/matplotlib, un seul lancement : `bash run_all_A.sh`.
- Éthique : tout le craquage se fait sur des mots de passe de test créés pour le projet,
  dans le réseau virtuel isolé.

## 3. C1 - Algorithmes cryptographiques

### 3.1 Configuration
`algorithms/bench_c1.py` appelle `openssl speed` (blocs de 8 Ko) pour AES-128/256 en CBC
et GCM, SHA-256 et SHA3-256, puis RSA-2048, RSA-4096, ECDSA P-256 et Ed25519 (signatures
et vérifications par seconde). Il génère aussi une clé par algorithme pour relever la
taille réelle des clés et des signatures.

### 3.2 Résultats
- Débit symétrique et hachage : `results/c1_symetrique.csv`, `results/c1_symetrique.png`.
  Moyennes sur 5 répétitions (VM client, 2 vCPU) :

  | Algorithme | Débit (Mo/s) |
  |---|---|
  | AES-128-GCM | 5432 |
  | AES-256-GCM | 3484 |
  | AES-128-CBC | 1652 |
  | AES-256-CBC | 1117 |
  | SHA-256 | 349 |
  | SHA3-256 | 265 |
- Asymétrique : `results/c1_asymetrique.csv`, `results/c1_asymetrique.png` (opérations par seconde) :

  | Algorithme | Signatures/s | Vérifications/s |
  |---|---|---|
  | RSA-2048 | 1423 | 49 019 |
  | RSA-4096 | 293 | 19 830 |
  | ECDSA P-256 | 48 967 | 18 262 |
  | Ed25519 | 26 815 | 9 994 |
- Tailles (`results/c1_tailles.csv`, mesurées) : signature RSA-2048 = 256 octets,
  RSA-4096 = 512, Ed25519 = 64, ECDSA P-256 = 71 (encodage DER) ; clé publique RSA-2048 =
  294 octets, RSA-4096 = 550, ECDSA = 91, Ed25519 = 44.

### 3.3 Analyse
- **AES-GCM vs AES-CBC** : GCM fournit confidentialité *et* intégrité (chiffrement
  authentifié) et se parallélise ; CBC ne fournit que la confidentialité, exige un MAC
  séparé et est exposé aux attaques de type *padding oracle* si mal utilisé. Mesuré : GCM
  est environ 3,3 fois plus rapide que CBC (5432 contre 1652 Mo/s en AES-128), car le
  chiffrement CBC est séquentiel alors que GCM se parallélise.
- **AES-128 vs AES-256** : 256 bits coûte plus de calcul (14 tours au lieu de 10) : mesuré,
  AES-256-GCM est environ 36 % plus lent qu'AES-128-GCM (3484 contre 5432 Mo/s) ;
  128 bits reste jugé sûr aujourd'hui.
- **RSA vs ECDSA vs Ed25519** : à niveau de sécurité comparable (RSA-3072 ≈ P-256 ≈
  Ed25519), les courbes elliptiques ont des clés et signatures bien plus petites et la
  signature est nettement plus rapide ; RSA vérifie très vite mais signe lentement
  (surtout 4096). Ed25519 est déterministe, ce qui évite la fragilité d'ECDSA face à un
  mauvais nonce. RSA-2048 correspond à ≈ 112 bits de sécurité.
- **SHA-256 vs SHA3-256** : même taille de sortie, constructions différentes (Merkle-Damgård
  vs éponge). SHA-2 est souvent accéléré matériellement donc plus rapide ; SHA-3 n'est pas
  vulnérable à l'extension de longueur.

## 4. C2 - Hachage de mots de passe

### 4.1 Configuration
- `passwords/bench_c2.py` : temps de calcul par hash pour SHA-256 simple (sans sel), PBKDF2-HMAC-SHA256
  (10 000 / 100 000 / 600 000 itérations), bcrypt (coûts 8, 10, 12, 14), Argon2id (3 profils).
- `passwords/gen_data.py` : liste de candidats fixe (graine 42) et 10 mots de passe de test
  (6 présents dans la liste, 4 absents), hachés avec chaque algorithme au format John.
- `passwords/crack_c2.sh` : John the Ripper sur CPU, même liste pour tous, pot vidé à chaque essai.
- Coûts utilisés pour le craquage (volontairement modestes, sinon la mesure est trop
  longue sur CPU) : PBKDF2 = 10 000 itérations, bcrypt = coût 8, Argon2id = t=1, m=8 Mio, p=1.

### 4.2 Résultats
- Temps de hachage : `results/c2_temps_hash.csv`, `results/c2_temps_hash.png`.
- Craquage : `results/c2_craquage.csv`, `results/c2_craquage.png`
  (temps total, mots de passe trouvés, temps par tentative).
- Temps de calcul d'un hash (moyenne sur 5 répétitions) : SHA-256 simple 0,007 ms ;
  PBKDF2 : 5,2 ms (10 000 it.), 49 ms (100 000), 291 ms (600 000) ; bcrypt : 13 ms (coût 8),
  51 ms (10), 203 ms (12), 827 ms (14) ; Argon2id : 7 ms (t=1, 8 Mio), 29 ms (t=2, 19 Mio),
  185 ms (t=3, 64 Mio).
- Craquage John the Ripper (1000 candidats, 10 comptes, 5 répétitions ; les 6 mots de passe
  présents dans la liste sont retrouvés pour chaque algorithme) :

  | Algorithme (coût du test) | Temps moyen | ms par tentative |
  |---|---|---|
  | SHA-256 simple | 0,41 s | 0,04 |
  | PBKDF2 (10 000 it.) | 4,7 s | 0,47 |
  | Argon2id (t=1, 8 Mio) | 10,2 s | 1,02 |
  | bcrypt (coût 8) | 17,0 s | 1,69 |

  Une « tentative » est un mot de la liste essayé contre un compte. Avec ces coûts modestes,
  SHA-256 simple se casse environ 40 fois plus vite que bcrypt ; avec les coûts recommandés
  (PBKDF2 600 000 it., bcrypt 12, Argon2id 19 Mio), l'écart serait bien plus grand.
  Limite : un test sur 1000 mots et 10 comptes est petit, les écarts sont à lire en ordre
  de grandeur.

### 4.3 Analyse
- Un hash rapide non salé (SHA-256 simple) est inadapté aux mots de passe : l'attaquant
  teste des millions de candidats par seconde, et deux utilisateurs au même mot de passe
  ont le même hash.
- Les trois autres sont **lents et salés**, et leur coût est réglable. Recommandations
  OWASP : Argon2id (m=19 Mio, t=2, p=1 au minimum), sinon bcrypt (coût ≥ 10) ou
  PBKDF2-HMAC-SHA256 (≥ 600 000 itérations).
- **Argon2id** est *memory-hard* : il résiste mieux aux GPU/ASIC. **bcrypt** est éprouvé mais
  ignore les octets d'un mot de passe au-delà de 72. **PBKDF2** est standardisé (FIPS) mais peu
  résistant au matériel parallèle.
- Limite : le craquage ne porte que sur des mots de passe du dictionnaire ; un mot de passe
  absent de la liste n'est pas trouvé quel que soit l'algorithme, ce qui montre le rôle de
  la robustesse du mot de passe lui-même.

## 5. Conclusion partielle et limites
`[À rédiger en J7 avec B]` : recommandations par besoin. Limites : mesures faites dans des
VMs (virtualisation), un seul CPU, liste de mots de passe courte, coûts de craquage réduits
par rapport à la production.
