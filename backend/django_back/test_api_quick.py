#!/usr/bin/env python3
"""Test rapide de l'API WordPress"""

import requests
from datetime import datetime, timedelta

# Sites à tester
sites = [
    'https://www.sidwaya.info',
    'https://www.aib.media',
    'https://www.burkina24.com',
    'https://www.lepays.bf',
    'https://www.lobservateur.bf'
]

print("="*60)
print("🧪 TEST RAPIDE DES API WORDPRESS")
print("="*60)

for site in sites:
    print(f"\n🔍 Test: {site}")
    
    # Test 1: Détection WordPress
    try:
        api_root = f"{site}/wp-json/"
        response = requests.get(api_root, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'namespaces' in data and 'wp/v2' in data.get('namespaces', []):
                print(f"   ✅ WordPress détecté")
                
                # Test 2: Récupération d'articles (sans filtre de date)
                posts_url = f"{site}/wp-json/wp/v2/posts?per_page=5"
                posts_response = requests.get(posts_url, timeout=10)
                
                if posts_response.status_code == 200:
                    posts = posts_response.json()
                    print(f"   ✅ API accessible: {len(posts)} articles récupérés")
                    
                    if len(posts) > 0:
                        # Afficher la date du premier article
                        first_post = posts[0]
                        print(f"   📅 Dernier article: {first_post.get('date', 'N/A')}")
                        print(f"   📰 Titre: {first_post.get('title', {}).get('rendered', 'N/A')[:50]}...")
                
                elif posts_response.status_code == 401:
                    error_data = posts_response.json()
                    print(f"   ❌ API bloquée (401): {error_data.get('message', 'Accès refusé')}")
                
                else:
                    print(f"   ❌ Erreur API: Status {posts_response.status_code}")
            else:
                print(f"   ❌ Pas WordPress")
        else:
            print(f"   ❌ Erreur: Status {response.status_code}")
    
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Timeout")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

print("\n" + "="*60)
print("✅ Test terminé")
print("="*60)
