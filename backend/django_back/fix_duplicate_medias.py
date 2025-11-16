#!/usr/bin/env python3
"""Script pour fusionner les médias dupliqués"""

from database.db_manager import DatabaseManager

db = DatabaseManager()

print("🔧 Fusion des médias dupliqués...\n")

# Récupérer tous les médias
conn = db.get_connection()
cursor = conn.cursor()

# Trouver les doublons (même nom, URLs différentes)
cursor.execute("""
    SELECT nom, GROUP_CONCAT(id) as ids, GROUP_CONCAT(url) as urls, COUNT(*) as count
    FROM medias
    GROUP BY nom
    HAVING count > 1
""")

duplicates = cursor.fetchall()

if not duplicates:
    print("✅ Aucun doublon trouvé")
else:
    print(f"📋 {len(duplicates)} médias avec doublons:\n")
    
    for dup in duplicates:
        nom = dup['nom']
        ids = dup['ids'].split(',')
        urls = dup['urls'].split(',')
        
        print(f"📺 {nom}:")
        for i, (id, url) in enumerate(zip(ids, urls)):
            # Compter les articles
            cursor.execute("SELECT COUNT(*) as count FROM articles WHERE media_id = ?", (id,))
            count = cursor.fetchone()['count']
            print(f"   • ID {id}: {url} ({count} articles)")
        
        # Garder le média avec le plus d'articles
        article_counts = []
        for id in ids:
            cursor.execute("SELECT COUNT(*) as count FROM articles WHERE media_id = ?", (id,))
            article_counts.append(cursor.fetchone()['count'])
        
        # ID à garder (celui avec le plus d'articles)
        keep_id = ids[article_counts.index(max(article_counts))]
        
        # Migrer les articles des autres IDs vers keep_id
        for id in ids:
            if id != keep_id:
                print(f"   → Migration des articles de ID {id} vers ID {keep_id}...")
                cursor.execute("""
                    UPDATE articles 
                    SET media_id = ? 
                    WHERE media_id = ?
                """, (keep_id, id))
                
                # Supprimer le média dupliqué
                cursor.execute("DELETE FROM medias WHERE id = ?", (id,))
        
        conn.commit()
        print(f"   ✅ Fusion terminée pour {nom}\n")

conn.close()

print("\n✅ Nettoyage terminé!")
print("\n📊 Vérification:")

# Afficher les stats
db2 = DatabaseManager()
stats = db2.get_scraping_stats()

print(f"\n📰 Total articles: {stats['total_articles']}")
print(f"\n📺 Articles par média:")
for media, count in stats['articles_par_media'].items():
    print(f"   • {media}: {count} articles")
