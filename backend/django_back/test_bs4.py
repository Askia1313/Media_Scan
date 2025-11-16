import requests
from bs4 import BeautifulSoup

url = 'https://lepays.bf'
print(f"Test BeautifulSoup sur {url}\n")

r = requests.get(url, timeout=30)
print(f"HTML récupéré: {len(r.content)} bytes\n")

soup = BeautifulSoup(r.content, 'html.parser')

all_tags = list(soup.descendants)
print(f"Total tags: {len(all_tags)}")

a_tags = soup.find_all('a')
print(f"Balises <a>: {len(a_tags)}")

if len(a_tags) > 0:
    print("\nPremiers 5 liens:")
    for i, a in enumerate(a_tags[:5], 1):
        print(f"   {i}. {a.get('href', 'NO HREF')}")
else:
    print("\n❌ Aucune balise <a> trouvée!")
    print("\nPremiers tags trouvés:")
    for tag in list(soup.find_all())[:10]:
        print(f"   • <{tag.name}>")
