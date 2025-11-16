

# 🛡️ Module de Modération de Contenu avec Ollama

## 🎯 Objectif

Détecter automatiquement les contenus sensibles dans les articles, posts Facebook et tweets :
- **Incitation à la haine** : Discours contre des groupes ethniques, religieux, etc.
- **Fake news / Désinformation** : Affirmations non vérifiées, manipulation de faits
- **Discours toxique** : Violence, insultes, discrimination
- **Contenus sensibles** : Terrorisme, conflits armés, politique controversée

## ✅ Fonctionnalités

### 1. Analyse de toxicité
- Incitation à la haine (0-10)
- Violence et agressivité (0-10)
- Insultes et langage offensant (0-10)
- Discrimination (0-10)

### 2. Détection de désinformation
- Affirmations non vérifiées (0-10)
- Manipulation de faits (0-10)
- Théories du complot (0-10)
- Propagande (0-10)
- Identification d'éléments suspects

### 3. Analyse de sensibilité
- Violence ou conflit armé
- Terrorisme
- Politique controversée
- Religion sensible
- Santé publique

### 4. Score de risque global
- Calcul pondéré : 40% toxicité + 40% désinformation + 20% sensibilité
- Niveaux : MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE
- Signalement automatique si score ≥ 6/10

## 🚀 Installation

### 1. Installer Ollama

**Windows** :
```powershell
# Télécharger depuis https://ollama.ai
# Ou avec winget
winget install Ollama.Ollama
```

**Linux/Mac** :
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Télécharger le modèle

```powershell
ollama pull llama3.2
```

### 3. Lancer Ollama

```powershell
ollama serve
```

Le serveur démarre sur `http://localhost:11434`

## 📊 Utilisation

### Analyser tous les contenus

```powershell
python moderate_content.py --type all --limit 10
```

### Analyser uniquement les articles

```powershell
python moderate_content.py --type articles --limit 20
```

### Analyser les posts Facebook

```powershell
python moderate_content.py --type facebook --limit 15
```

### Analyser les tweets

```powershell
python moderate_content.py --type twitter --limit 15
```

### Analyser un média spécifique

```powershell
python moderate_content.py --type all --media-id 1 --limit 10
```

### Afficher les contenus signalés

```powershell
python moderate_content.py --show-flagged
```

### Afficher les statistiques

```powershell
python moderate_content.py --stats
```

### Tester la connexion à Ollama

```powershell
python moderate_content.py --test
```

## 📈 Exemples de résultats

### Analyse d'un article

```
🔍 Analyse de l'article 123: Tensions politiques au Burkina Faso...
   🚨 SIGNALÉ - 🟠 ÉLEVÉ (Score: 7.2)
      ⚠️ Toxique: Contient des propos discriminatoires
      ⚠️ Sensible: Aborde un conflit politique sensible
```

### Analyse d'un post Facebook

```
🔍 Analyse du post 456: Message controversé...
   ✅ OK - 🟡 MOYEN (Score: 3.5)
```

### Contenus signalés

```
🚨 Contenus signalés
================================================================================

🔴 CRITIQUE - ARTICLE #789
   Score de risque: 8.5/10
   Signalements: Toxique, Désinformation
   Analysé le: 2025-11-16 10:30:00

🟠 ÉLEVÉ - TWEET #456
   Score de risque: 6.8/10
   Signalements: Toxique, Sensible
   Analysé le: 2025-11-16 10:25:00
```

### Statistiques

```
📊 Statistiques de modération
================================================================================
Total analysé: 50
Total signalé: 8
Contenus toxiques: 5
Désinformation: 3
Contenus sensibles: 12
Score de risque moyen: 3.2/10

Taux de signalement: 16.0%
```

## 🔧 Intégration dans le workflow

### Après le scraping

```powershell
# 1. Scraper les contenus
python scrape_with_social.py --all

# 2. Analyser les contenus
python moderate_content.py --type all --limit 50

# 3. Voir les contenus signalés
python moderate_content.py --show-flagged
```

### Automatisation quotidienne

Créez un script PowerShell :

```powershell
# daily_moderation.ps1
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back
env\Scripts\activate

# Scraping
python scrape_with_social.py --all --fb-posts 5 --tweets 5

# Modération
python moderate_content.py --type all --limit 100

# Rapport des contenus signalés
python moderate_content.py --show-flagged > reports/flagged_$(Get-Date -Format 'yyyy-MM-dd').txt

# Statistiques
python moderate_content.py --stats > reports/moderation_stats_$(Get-Date -Format 'yyyy-MM-dd').txt
```

## 📊 Structure de la base de données

### Table `content_moderation`

```sql
CREATE TABLE content_moderation (
    id INTEGER PRIMARY KEY,
    content_type TEXT,  -- 'article', 'facebook_post', 'tweet'
    content_id INTEGER,
    
    -- Scores globaux
    risk_score REAL,
    risk_level TEXT,
    should_flag BOOLEAN,
    
    -- Toxicité
    is_toxic BOOLEAN,
    toxicity_score REAL,
    hate_speech_score REAL,
    violence_score REAL,
    insults_score REAL,
    discrimination_score REAL,
    
    -- Désinformation
    is_misinformation BOOLEAN,
    misinformation_score REAL,
    unverified_claims_score REAL,
    fact_manipulation_score REAL,
    conspiracy_score REAL,
    propaganda_score REAL,
    suspicious_elements TEXT,
    
    -- Sensibilité
    is_sensitive BOOLEAN,
    sensitivity_level TEXT,
    sensitivity_score REAL,
    sensitive_categories TEXT,
    
    analyzed_at TIMESTAMP,
    model_used TEXT
);
```

## 🎨 Niveaux de risque

| Score | Niveau | Icône | Action |
|-------|--------|-------|--------|
| 0-2 | MINIMAL | ✅ | Aucune action |
| 2-4 | FAIBLE | 🟢 | Surveillance |
| 4-6 | MOYEN | 🟡 | Attention |
| 6-8 | ÉLEVÉ | 🟠 | Signalement |
| 8-10 | CRITIQUE | 🔴 | Alerte immédiate |

## 🔍 Critères de détection

### Toxicité
- Langage haineux contre des groupes
- Appels à la violence
- Insultes et attaques personnelles
- Discrimination ethnique/religieuse

### Désinformation
- Affirmations sans sources
- Manipulation de statistiques
- Théories du complot
- Propagande politique

### Sensibilité
- Conflits armés et terrorisme
- Crises politiques
- Questions religieuses sensibles
- Épidémies et santé publique

## 💡 Bonnes pratiques

### 1. Analyser régulièrement
```powershell
# Tous les jours
python moderate_content.py --type all --limit 50
```

### 2. Surveiller les contenus signalés
```powershell
# Vérifier les alertes
python moderate_content.py --show-flagged
```

### 3. Ajuster les seuils
Le score de risque peut être ajusté dans `content_moderator.py` :
```python
def _calculate_risk_score(self, toxicity, misinformation, sensitivity):
    # Modifier les pondérations selon vos besoins
    risk_score = (
        toxicity_score * 0.4 +  # 40% toxicité
        misinfo_score * 0.4 +   # 40% désinformation
        sensitivity_score * 0.2  # 20% sensibilité
    )
    return risk_score
```

### 4. Utiliser différents modèles
```python
# Dans content_moderator.py
moderator = ContentModerator(model="llama3.2")  # Par défaut
moderator = ContentModerator(model="mistral")   # Alternative
```

## 🚨 Limitations

1. **Dépend d'Ollama** : Le serveur Ollama doit être lancé
2. **Temps d'analyse** : ~5-10 secondes par contenu
3. **Précision** : Le modèle peut avoir des faux positifs/négatifs
4. **Langue** : Optimisé pour le français
5. **Contexte** : L'analyse est basée sur le texte uniquement

## 🔧 Dépannage

### Erreur : "Impossible de se connecter à Ollama"

```powershell
# Vérifier qu'Ollama est lancé
ollama serve

# Vérifier que le modèle est installé
ollama list

# Télécharger le modèle si nécessaire
ollama pull llama3.2
```

### Analyse trop lente

```powershell
# Réduire le nombre de contenus
python moderate_content.py --type articles --limit 5

# Utiliser un modèle plus rapide
# Modifier model="llama3.2" en model="phi" dans content_moderator.py
```

### Faux positifs

- Ajuster les seuils dans `_determine_risk_level()`
- Modifier les pondérations dans `_calculate_risk_score()`
- Utiliser un modèle différent

## 📚 Ressources

- **Ollama** : https://ollama.ai
- **Modèles disponibles** : https://ollama.ai/library
- **Documentation Ollama** : https://github.com/ollama/ollama

## ✅ Résumé

Le module de modération permet de :
- ✅ Détecter automatiquement les contenus toxiques
- ✅ Identifier la désinformation et les fake news
- ✅ Repérer les contenus sensibles
- ✅ Calculer un score de risque global
- ✅ Signaler les contenus problématiques
- ✅ Générer des statistiques de modération

**La modération de contenu est opérationnelle ! 🛡️🚀**
