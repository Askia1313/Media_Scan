#!/usr/bin/env python3
"""Script pour nettoyer complètement la base de données"""

import os
import sqlite3

db_path = "data/media_scan.db"

print("🔧 Nettoyage complet de la base de données...\n")

if os.path.exists(db_path):
    print(f"📂 Suppression de {db_path}...")
    os.remove(db_path)
    print("✅ Base de données supprimée\n")
else:
    print("ℹ️ Aucune base de données existante\n")

# Réinitialiser la base
from database.db_manager import DatabaseManager

print("🔧 Création d'une nouvelle base de données...")
db = DatabaseManager()
print("✅ Nouvelle base de données créée\n")

print("📊 Vérification:")
stats = db.get_scraping_stats()
print(f"   • Total articles: {stats['total_articles']}")
print(f"   • Total médias: {len(stats['articles_par_media'])}")

print("\n✅ Base de données prête pour le scraping HTML!")
