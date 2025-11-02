# config/config.example.py

# please update this variables with your own values
POSTGRES_DB = {
    'dbname': 'monitor_db',
    'user': 'user_name', # user name for PostgreSQL
    'password': hsfjsdjksd, # Example password
    'host': 'localhost',             
    'port': '5432'                   
}

# --- Threat intelligence settings ---
# AbuseIPDB key
ABUSEIPDB_API_KEY = "Add your key here"


# Suspicious port that sniffer listen
SUSPICIOUS_PORTS = {21, 23, 6667}

# HTTP keywords for unencrypted packet
KEYWORDS_TO_HUNT = [b'user', b'pass', b'username', b'password', b'login', b'kullanici', b'sifre']

# BPF FİLTER
BPF_FILTER = "udp port 53 or tcp port 21 or tcp port 23 or tcp port 6667 or tcp port 80"

LOG_FILE = "data/dns_sorgulari.txt"

# CONSOL COLORS
RENK_KIRMIZI = "\033[91m"
RENK_SARI = "\033[93m"
RENK_RESET = "\033[0m"