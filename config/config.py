# config/config.py

# ---PostgreSQL settings ---
# core/logger.py ve core/db_utils.py bu sözlüğü (dictionary) kullanacak
POSTGRES_DB = {
    'dbname': 'netmonitor_db',
    'user': 'netmonitor_user',
    'password': '982134_32fb', # password
    'host': 'localhost',             # Server run in local host
    'port': '5432'                   # Default PostgreSQL port
}


LOG_FILE = "data/dns_sorgulari.txt"
SUSPICIOUS_PORTS = {21, 23, 6667}
KEYWORDS_TO_HUNT = [b'user', b'pass', b'username', b'password', b'login', b'kullanici', b'sifre']

# BPF filter
BPF_FILTER = "udp port 53 or tcp port 21 or tcp port 23 or tcp port 6667 or tcp port 80"

# Consol colors
RENK_KIRMIZI = "\033[91m"
RENK_SARI = "\033[93m"
RENK_RESET = "\033[0m"

# API KEY
ABUSEIPDB_API_KEY = "c5e68847e6eb22315a9ae4086cfc592193e33563aa1c33d62d5c6225f9e023511712e566efbdb221"
