import requests
from bs4 import BeautifulSoup

url = 'https://lepays.bf'

# Test 1: Sans session
print("Test 1: Sans session")
r1 = requests.get(url, timeout=30)
soup1 = BeautifulSoup(r1.content, 'html.parser')
print(f"   Liens trouvés: {len(soup1.find_all('a', href=True))}\n")

# Test 2: Avec session et headers
print("Test 2: Avec session et headers")
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
})
r2 = session.get(url, timeout=30)
soup2 = BeautifulSoup(r2.content, 'html.parser')
print(f"   Liens trouvés: {len(soup2.find_all('a', href=True))}\n")

# Test 3: Avec le scraper
print("Test 3: Avec le scraper")
from scrapers.smart_html_scraper import SmartHTMLScraper
scraper = SmartHTMLScraper(url)
soup3 = scraper.get_page(url)
if soup3:
    links = soup3.find_all('a', href=True)
    print(f"   Liens trouvés: {len(links)}")
    if len(links) > 0:
        print(f"   Premier lien: {links[0].get('href')}")
else:
    print("   ❌ Erreur récupération page")
