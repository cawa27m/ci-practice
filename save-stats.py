#!/usr/bin/env python3
import sqlite3
import re
from datetime import datetime

LOG_FILE = "access.log"
DB_FILE = "stats.db"

def parse_log_line(line):
    # Регулярка для Common Log Format
    pattern = r'(\S+) \S+ \S+ \[([\w:/+\s]+)\] "(\S+) (\S+) \S+" (\d+)'
    match = re.search(pattern, line)
    if match:
        ip, timestamp, method, endpoint, status = match.groups()
        return {
            "ip": ip,
            "timestamp": timestamp,
            "method": method,
            "endpoint": endpoint,
            "status": int(status)
        }
    return None

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            timestamp TEXT,
            method TEXT,
            endpoint TEXT,
            status INTEGER,
            analyzed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_stats():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    with open(LOG_FILE, "r") as f:
        for line in f:
            data = parse_log_line(line)
            if data:
                cursor.execute('''
                    INSERT INTO requests (ip, timestamp, method, endpoint, status, analyzed_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data["ip"],
                    data["timestamp"],
                    data["method"],
                    data["endpoint"],
                    data["status"],
                    datetime.now().isoformat()
                ))
    
    conn.commit()
    conn.close()
    print(f"✅ Статистика сохранена в {DB_FILE}")

if __name__ == "__main__":
    save_stats()
