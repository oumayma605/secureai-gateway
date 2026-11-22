# Grille de synthèse - lignes de la partie A (à finaliser en J7)

Les colonnes **Performance** sont à remplir avec les mesures de `results/`.

| Solution | Sécurité | Performance | Complexité | Recommandée pour |
|---|---|---|---|---|
| AES-GCM | Chiffrement authentifié (confidentialité + intégrité) | 5432 (128) / 3484 (256) Mo/s | Faible, mais ne jamais réutiliser un nonce | Protection de flux et de données par défaut |
| AES-CBC | Confidentialité seule, MAC séparé requis, risque de padding oracle | 1652 (128) / 1117 (256) Mo/s | Moyenne (IV, padding, MAC) | Compatibilité avec l'existant |
| RSA-2048 / 4096 | ≈ 112 bits (2048) ; clés et signatures volumineuses | signature 1423 /s (2048), 293 /s (4096) ; vérif. 49 019 /s, 19 830 /s | Faible | Compatibilité large ; 4096 si exigence forte et signatures rares |
| ECDSA P-256 | ≈ 128 bits ; sensible à un mauvais nonce | signature 48 967 /s, vérif. 18 262 /s | Moyenne | Certificats TLS usuels |
| Ed25519 | ≈ 128 bits, déterministe, petites clés (signature 64 o) | signature 26 815 /s, vérif. 9 994 /s | Faible | Signatures modernes, SSH |
| SHA-256 / SHA3-256 | Intégrité ; inadaptés seuls aux mots de passe | 349 / 265 Mo/s | Faible | Empreintes, signatures |
| SHA-256 simple (mdp) | Très faible : rapide, sans sel | 0,007 ms/hash (craquage : 0,04 ms/tentative) | Très faible | À éviter |
| PBKDF2 | Correct si ≥ 600 000 itérations ; peu résistant au GPU | 291 ms/hash à 600 000 it. | Faible | Exigence de conformité (FIPS) |
| bcrypt | Bon ; limite de 72 octets | 203 ms/hash (coût 12) | Faible | Compatibilité large, applications existantes |
| Argon2id | Très bon, memory-hard | 185 ms/hash (t=3, 64 Mio) | Moyenne (3 paramètres) | Nouvelles applications |
