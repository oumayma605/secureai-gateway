# Grille de synthèse - lignes de la partie A (à finaliser en J7)

Les colonnes **Performance** sont à remplir avec les mesures de `results/`.

| Solution | Sécurité | Performance | Complexité | Recommandée pour |
|---|---|---|---|---|
| AES-GCM | Chiffrement authentifié (confidentialité + intégrité) | `[MESURE]` Mo/s | Faible, mais ne jamais réutiliser un nonce | Protection de flux et de données par défaut |
| AES-CBC | Confidentialité seule, MAC séparé requis, risque de padding oracle | `[MESURE]` Mo/s | Moyenne (IV, padding, MAC) | Compatibilité avec l'existant |
| RSA-2048 / 4096 | ≈ 112 bits (2048) ; clés et signatures volumineuses | signature `[MESURE]` /s, vérif. `[MESURE]` /s | Faible | Compatibilité large ; 4096 si exigence forte et signatures rares |
| ECDSA P-256 | ≈ 128 bits ; sensible à un mauvais nonce | `[MESURE]` | Moyenne | Certificats TLS usuels |
| Ed25519 | ≈ 128 bits, déterministe, petites clés (signature 64 o) | `[MESURE]` | Faible | Signatures modernes, SSH |
| SHA-256 / SHA3-256 | Intégrité ; inadaptés seuls aux mots de passe | `[MESURE]` Mo/s | Faible | Empreintes, signatures |
| SHA-256 simple (mdp) | Très faible : rapide, sans sel | `[MESURE]` ms/hash | Très faible | À éviter |
| PBKDF2 | Correct si ≥ 600 000 itérations ; peu résistant au GPU | `[MESURE]` ms/hash | Faible | Exigence de conformité (FIPS) |
| bcrypt | Bon ; limite de 72 octets | `[MESURE]` ms/hash | Faible | Compatibilité large, applications existantes |
| Argon2id | Très bon, memory-hard | `[MESURE]` ms/hash | Moyenne (3 paramètres) | Nouvelles applications |
