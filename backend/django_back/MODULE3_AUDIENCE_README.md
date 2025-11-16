# 📊 Module 3 - Analyse d'Audience par Plateforme

## 🎯 Objectif

Analyser l'audience des médias burkinabè **séparément par plateforme** :
- 📰 **Web** : Volume d'articles, fréquence de publication
- 📘 **Facebook** : Posts, engagement (likes, commentaires, partages)
- 🐦 **Twitter** : Tweets, engagement (retweets, replies, likes, quotes)

## ✅ Fonctionnalités implémentées

### 1. Analyse Web ✅
- Volume de publications (articles)
- Fréquence de publication (articles/jour)
- Dernière publication
- Jours depuis la dernière publication
- Statut d'activité (actif, récent, inactif)

### 2. Analyse Facebook ✅
- Volume de posts
- Fréquence de publication (posts/jour)
- Métriques d'engagement : likes, commentaires, partages
- Engagement total et moyen
- Statut d'activité

### 3. Analyse Twitter ✅
- Volume de tweets
- Fréquence de publication (tweets/jour)
- Métriques d'engagement : retweets, replies, likes, quotes, impressions
- Engagement total et moyen
- Statut d'activité

### 4. Classement global ✅
- Score d'influence composite (40% volume + 60% engagement)
- Comparaison multi-plateformes
- Publications totales
- Engagement total

### 5. Détection d'inactivité ✅
- Médias n'ayant pas publié depuis X jours
- Analyse par plateforme
- Identification des médias silencieux

## 📁 Fichiers créés

```
backend/django_back/
├── analysis/
│   └── audience_analyzer.py         # Analyseur d'audience
├── show_audience.py                 # Script d'affichage
└── MODULE3_AUDIENCE_README.md       # Ce fichier
```

## 🚀 Utilisation

### Analyse Web

```powershell
# Audience web sur 30 jours
python show_audience.py --platform web --days 30

# Audience web sur 7 jours
python show_audience.py --platform web --days 7
```

**Résultat** :
```
📰 AUDIENCE WEB - ARTICLES (30 derniers jours)

1. 📺 Lefaso
   🌐 URL: https://lefaso.net
   📊 Volume: 56 articles
   📈 Fréquence: 1.87 articles/jour
   📅 Dernière publication: 2025-11-16
   ⏱️ Il y a 0 jour(s)
   🟢 Actif (aujourd'hui)
```

### Analyse Facebook

```powershell
python show_audience.py --platform facebook --days 30
```

**Résultat** :
```
📘 AUDIENCE FACEBOOK (30 derniers jours)

1. 📺 AIB
   📘 Page: aib.infos
   📊 Volume: 5 posts
   👍 Likes: 8,920
   💬 Commentaires: 542
   🔄 Partages: 1,680
   📊 Engagement total: 11,142
   📈 Engagement moyen: 2,228 par post
```

### Analyse Twitter

```powershell
python show_audience.py --platform twitter --days 30
```

**Résultat** :
```
🐦 AUDIENCE TWITTER (30 derniers jours)

1. 📺 AIB
   🐦 Compte: @aibburkina
   📊 Volume: 5 tweets
   🔄 Retweets: 0
   💬 Réponses: 2
   ❤️ Likes: 16
   📊 Engagement total: 18
```

### Classement global

```powershell
python show_audience.py --platform global --days 30
```

**Résultat** :
```
🏆 CLASSEMENT GLOBAL PAR INFLUENCE (30 derniers jours)

🥇 📺 AIB
   🎯 Score d'influence: 15.64
   
   📰 Web: 20 articles
      Fréquence: 0.67 articles/jour
   📘 Facebook: 5 posts
      Engagement: 11,142
   🐦 Twitter: 5 tweets
      Engagement: 18
   📊 Publications totales: 30
   📈 Engagement total: 11,160
```

### Toutes les plateformes

```powershell
python show_audience.py --platform all --days 30
```

### Médias inactifs

```powershell
# Médias sans publication depuis 7 jours
python show_audience.py --platform web --inactive 7

# Médias sans publication depuis 30 jours
python show_audience.py --platform all --inactive 30
```

**Résultat** :
```
🔴 MÉDIAS INACTIFS (>7 jours sans publication)

📰 WEB (2 médias):
   • Faso7: 999 jours
   • Evenement-bf: 999 jours

📘 FACEBOOK (0 médias):
✅ Tous actifs

🐦 TWITTER (0 médias):
✅ Tous actifs
```

## 📊 Métriques par plateforme

### Web
| Métrique | Description |
|----------|-------------|
| **Volume** | Nombre d'articles publiés |
| **Fréquence** | Articles par jour |
| **Dernière publication** | Date du dernier article |
| **Jours depuis** | Nombre de jours sans publication |
| **Statut** | Actif, Récent, Modéré, Inactif |

### Facebook
| Métrique | Description |
|----------|-------------|
| **Volume** | Nombre de posts |
| **Fréquence** | Posts par jour |
| **Likes** | Total des likes (réactions) |
| **Commentaires** | Total des commentaires |
| **Partages** | Total des partages |
| **Engagement total** | Likes + Commentaires + Partages |
| **Engagement moyen** | Engagement par post |

### Twitter
| Métrique | Description |
|----------|-------------|
| **Volume** | Nombre de tweets |
| **Fréquence** | Tweets par jour |
| **Retweets** | Total des retweets |
| **Replies** | Total des réponses |
| **Likes** | Total des likes |
| **Quotes** | Total des citations |
| **Impressions** | Total des vues (niveau payant) |
| **Engagement total** | Retweets + Replies + Likes + Quotes |
| **Engagement moyen** | Engagement par tweet |

## 🎨 Statuts d'activité

| Statut | Icône | Condition |
|--------|-------|-----------|
| **Actif (aujourd'hui)** | 🟢 | Publication aujourd'hui |
| **Actif (hier)** | 🟢 | Publication hier |
| **Récent (3 jours)** | 🟡 | Publication il y a 1-3 jours |
| **Récent (1 semaine)** | 🟡 | Publication il y a 4-7 jours |
| **Modéré (2 semaines)** | 🟠 | Publication il y a 8-14 jours |
| **Modéré (1 mois)** | 🟠 | Publication il y a 15-30 jours |
| **Inactif** | 🔴 | Publication il y a >30 jours |
| **Aucune publication** | ❌ | Jamais publié |

## 📈 Score d'influence composite

Le score d'influence est calculé ainsi :

```
Score = (0.4 × Score_Volume) + (0.6 × Score_Engagement)

Où :
- Score_Volume = Total_Publications / 10
- Score_Engagement = Total_Engagement / 100
```

**Pondération** :
- 40% pour le volume de publications
- 60% pour l'engagement social

## 💡 Cas d'usage

### 1. Identifier les médias les plus actifs

```powershell
python show_audience.py --platform web --days 7
```

→ Voir qui publie le plus d'articles cette semaine

### 2. Trouver les médias avec le meilleur engagement

```powershell
python show_audience.py --platform facebook --days 30
```

→ Classement par engagement Facebook

### 3. Détecter les médias inactifs

```powershell
python show_audience.py --platform all --inactive 14
```

→ Médias sans publication depuis 2 semaines

### 4. Comparer les performances

```powershell
python show_audience.py --platform global --days 30
```

→ Classement global multi-plateformes

### 5. Analyser une période spécifique

```powershell
# Dernière semaine
python show_audience.py --platform all --days 7

# Dernier mois
python show_audience.py --platform all --days 30

# Dernier trimestre
python show_audience.py --platform all --days 90
```

## 🔧 Intégration dans le workflow

### Après le scraping

```powershell
# 1. Scraper tous les médias
python scrape_with_social.py --all

# 2. Analyser l'audience
python show_audience.py --platform all --days 30

# 3. Identifier les inactifs
python show_audience.py --platform all --inactive 7
```

### Automatisation quotidienne

Créez un script PowerShell :

```powershell
# daily_analysis.ps1
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back
env\Scripts\activate

# Scraping
python scrape_with_social.py --all --fb-posts 5 --tweets 5

# Analyse
python show_audience.py --platform all --days 30 > reports/audience_$(Get-Date -Format 'yyyy-MM-dd').txt

# Médias inactifs
python show_audience.py --platform all --inactive 7 > reports/inactive_$(Get-Date -Format 'yyyy-MM-dd').txt
```

## 📊 Exemples de rapports

### Rapport hebdomadaire

```powershell
python show_audience.py --platform all --days 7 > rapport_hebdo.txt
```

### Rapport mensuel

```powershell
python show_audience.py --platform all --days 30 > rapport_mensuel.txt
```

### Alerte inactivité

```powershell
python show_audience.py --platform all --inactive 3 > alerte_inactifs.txt
```

## 🎯 Prochaines étapes

- [ ] Export des rapports en PDF/Excel
- [ ] Graphiques de tendances
- [ ] Alertes automatiques par email
- [ ] Dashboard web interactif
- [ ] Comparaison historique
- [ ] Prédiction de tendances

## ✅ Résumé

Le Module 3 permet maintenant de :
- ✅ Analyser l'audience **séparément par plateforme**
- ✅ Mesurer le **volume de publications**
- ✅ Calculer la **fréquence de publication**
- ✅ Suivre l'**engagement** (likes, partages, commentaires, etc.)
- ✅ Identifier les **médias inactifs**
- ✅ Générer un **classement par influence**
- ✅ Comparer les **performances multi-plateformes**

**Le système d'analyse d'audience est opérationnel ! 📊🚀**
