#!/usr/bin/env python3
"""Test du HTML brut"""

import requests

url = "https://lepays.bf"

print(f"🔍 Récupération du HTML brut: {url}\n")

response = requests.get(url, timeout=30)
html = response.text

print(f"✅ Page récupérée: {len(html)} caractères\n")
print("📄 Premiers 2000 caractères:\n")
print(html[:2000])
print("\n...")
print("\n📄 Recherche de liens <a href:")
import re
links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', html[:5000])
print(f"\nLiens trouvés dans les 5000 premiers caractères: {len(links)}")
for link in links[:10]:
    print(f"   • {link}")
