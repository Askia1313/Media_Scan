# 📱 Media Scanner - Frontend

Interface web moderne pour la surveillance et l'analyse des médias burkinabè. Application React/TypeScript avec TailwindCSS et shadcn/ui, offrant une expérience utilisateur fluide pour visualiser les données collectées par le backend.

## 🏗️ Architecture

```
frontend/
├── public/                    # Fichiers statiques
│   ├── favicon.ico
│   ├── placeholder.svg
│   └── robots.txt
│
├── src/
│   ├── components/           # Composants React
│   │   ├── dashboard/        # Composants du tableau de bord
│   │   │   ├── DashboardOverview.tsx      # Vue d'ensemble avec graphiques
│   │   │   ├── MediaRanking.tsx           # Classement des médias
│   │   │   ├── ThematicAnalysis.tsx       # Analyse thématique
│   │   │   ├── SensitiveContent.tsx       # Contenu sensible/modération
│   │   │   ├── ScheduleControl.tsx        # Contrôle du scraping automatique
│   │   │   ├── ScrapingControl.tsx        # Déclenchement manuel du scraping
│   │   │   ├── MediaManagement.tsx        # Gestion des médias
│   │   │   └── ReportDialog.tsx           # Génération de rapports
│   │   │
│   │   └── ui/               # Composants UI shadcn/ui (40+ composants)
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── dialog.tsx
│   │       ├── table.tsx
│   │       └── ... (autres composants)
│   │
│   ├── hooks/                # Custom React Hooks
│   │   ├── useMedia.ts       # Gestion des médias
│   │   ├── useArticles.ts    # Récupération des articles
│   │   ├── useClassifications.ts  # Classifications thématiques
│   │   ├── useAudience.ts    # Données d'audience
│   │   ├── useRanking.ts     # Classement des médias
│   │   ├── useScraping.ts    # Contrôle du scraping
│   │   ├── useStats.ts       # Statistiques globales
│   │   └── use-toast.ts      # Notifications toast
│   │
│   ├── services/             # Services API
│   │   ├── api.client.ts     # Client HTTP générique
│   │   ├── api.config.ts     # Configuration API
│   │   ├── types.ts          # Types TypeScript
│   │   ├── media.service.ts  # Service médias
│   │   ├── article.service.ts     # Service articles
│   │   ├── classification.service.ts  # Service classifications
│   │   ├── social.service.ts      # Service réseaux sociaux
│   │   ├── audience.service.ts    # Service audience
│   │   ├── ranking.service.ts     # Service classement
│   │   ├── scraping.service.ts    # Service scraping
│   │   ├── stats.service.ts       # Service statistiques
│   │   ├── report.service.ts      # Service génération de rapports
│   │   └── index.ts          # Point d'entrée des services
│   │
│   ├── pages/                # Pages de l'application
│   │   ├── Index.tsx         # Page principale (dashboard)
│   │   └── NotFound.tsx      # Page 404
│   │
│   ├── lib/                  # Utilitaires
│   │   └── utils.ts          # Fonctions utilitaires
│   │
│   ├── App.tsx               # Composant racine
│   ├── main.tsx              # Point d'entrée
│   └── index.css             # Styles globaux
│
├── .env                      # Variables d'environnement
├── package.json              # Dépendances npm
├── vite.config.ts            # Configuration Vite
├── tsconfig.json             # Configuration TypeScript
├── tailwind.config.ts        # Configuration TailwindCSS
└── postcss.config.js         # Configuration PostCSS
```

## 🛠️ Stack Technique

### Core

- **React 18.3.1** - Bibliothèque UI
- **TypeScript 5.8.3** - Typage statique
- **Vite 5.4.19** - Build tool ultra-rapide
- **React Router DOM 6.30.1** - Routing

### State Management & Data Fetching

- **TanStack Query 5.83.0** - Gestion du state serveur
  - Cache intelligent
  - Invalidation automatique
  - Retry automatique
  - Optimistic updates
- **TanStack Query DevTools 5.90.2** - Outils de développement

### UI Framework

- **TailwindCSS 3.4.17** - Framework CSS utility-first
- **shadcn/ui** - Collection de composants réutilisables
  - 40+ composants Radix UI
  - Accessible (ARIA)
  - Personnalisable
  - Dark mode ready

### Composants UI (Radix UI)

- **@radix-ui/react-dialog** - Modales
- **@radix-ui/react-dropdown-menu** - Menus déroulants
- **@radix-ui/react-tabs** - Onglets
- **@radix-ui/react-select** - Sélecteurs
- **@radix-ui/react-toast** - Notifications
- **@radix-ui/react-switch** - Interrupteurs
- **@radix-ui/react-progress** - Barres de progression
- Et 30+ autres composants...

### Visualisation de données

- **Recharts 2.15.4** - Graphiques React
  - Bar charts
  - Line charts
  - Pie charts
  - Area charts
  - Responsive

### Formulaires

- **React Hook Form 7.61.1** - Gestion de formulaires performante
- **Zod 3.25.76** - Validation de schémas
- **@hookform/resolvers 3.10.0** - Intégration Zod + RHF

### Utilitaires

- **date-fns 3.6.0** - Manipulation de dates
- **clsx 2.1.1** - Gestion conditionnelle de classes CSS
- **tailwind-merge 2.6.0** - Fusion de classes Tailwind
- **lucide-react 0.462.0** - Icônes (1000+)

### Génération de rapports

- **jsPDF 3.0.3** - Génération de PDF
- **jspdf-autotable 5.0.2** - Tables pour PDF
- **xlsx 0.18.5** - Génération de fichiers Excel

### Notifications

- **sonner 1.7.4** - Toast notifications élégantes

## 🎨 Fonctionnalités

### 1. 🎯 Scraping Control

**Composant :** [ScrapingControl.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/ScrapingControl.tsx:0:0-0:0)

- Déclenchement manuel du scraping
- Configuration des paramètres :
  - Scraper tous les médias ou un média spécifique
  - Nombre de jours à récupérer
  - Nombre de posts Facebook
  - Nombre de tweets
  - Options pour ignorer Facebook/Twitter
- Feedback en temps réel
- Affichage des résultats

### 2. 📊 Dashboard Overview

**Composant :** [DashboardOverview.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/DashboardOverview.tsx:0:0-0:0)

**KPIs affichés :**

- Nombre total de médias
- Total de publications (articles + posts + tweets)
- Nombre de catégories thématiques
- Média le plus engageant

**Graphiques :**

- **Pie Chart** : Distribution des articles par thématique
- **Bar Chart** : Publications par jour de la semaine
- **Line Chart** : Évolution des publications sur 7 jours
- **Table** : Derniers articles publiés

### 3. 🏆 Media Ranking

**Composant :** [MediaRanking.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/MediaRanking.tsx:0:0-0:0)

Classement des médias par :

- Engagement total (Facebook + Twitter)
- Nombre d'articles
- Nombre de posts Facebook
- Nombre de tweets
- Engagement moyen

**Fonctionnalités :**

- Tri par colonne
- Filtrage par période (7, 14, 30 jours)
- Badges de statut
- Métriques détaillées par plateforme

### 4. 📈 Thematic Analysis

**Composant :** [ThematicAnalysis.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/ThematicAnalysis.tsx:0:0-0:0)

**Catégories :**

- Politique
- Économie
- Sécurité
- Santé
- Culture
- Sport
- Autres

**Visualisations :**

- Distribution globale par catégorie
- Évolution hebdomadaire
- Score de confiance moyen
- Tendances

### 5. ⚠️ Sensitive Content

**Composant :** [SensitiveContent.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/SensitiveContent.tsx:0:0-0:0)

**Modération de contenu :**

- Détection de toxicité
- Détection de désinformation
- Contenu sensible
- Niveaux de risque : MINIMAL, FAIBLE, MOYEN, ÉLEVÉ, CRITIQUE

**Affichage :**

- Liste des contenus signalés
- Filtres par type et niveau de risque
- Détails de l'analyse
- Actions de modération

### 6. ⏰ Schedule Control

**Composant :** [ScheduleControl.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/ScheduleControl.tsx:0:0-0:0)

**Configuration du scraping automatique :**

- Activation/désactivation
- Fréquence : horaire, quotidienne, hebdomadaire
- Paramètres de scraping
- Historique des tâches
- Prochaine exécution planifiée

### 7. 🎛️ Media Management

**Composant :** [MediaManagement.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/MediaManagement.tsx:0:0-0:0)

**Gestion CRUD des médias :**

- Liste de tous les médias
- Ajout de nouveaux médias
- Modification des médias existants
- Suppression de médias
- Configuration des comptes sociaux

**Formulaire :**

- Nom du média
- URL du site
- Type de site (WordPress, HTML, RSS)
- Page Facebook
- Compte Twitter
- Statut actif/inactif

### 8. 📄 Report Generation

**Composant :** [ReportDialog.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/ReportDialog.tsx:0:0-0:0)

**Génération de rapports :**

- Format PDF
- Format Excel
- Période personnalisable
- Sélection des données à inclure
- Téléchargement direct

## 🔌 Services API

### Architecture des services

Tous les services utilisent le pattern suivant :

1. **Client HTTP générique** (`api.client.ts`)
2. **Configuration centralisée** (`api.config.ts`)
3. **Types TypeScript stricts** ([types.ts](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/services/types.ts:0:0-0:0))
4. **Services spécialisés** par domaine

### api.client.ts

Client HTTP avec :

- Timeout configurable (30s)
- Gestion d'erreurs
- Abort controller
- Types génériques

```typescript
class ApiClient {
  async get<T>(endpoint: string, params?: Record<string, any>)
  async post<T>(endpoint: string, data?: any)
  async put<T>(endpoint: string, data?: any)
  async delete<T>(endpoint: string)
}
```

### Services disponibles

#### 1. mediaService

```typescript
mediaService.getAll()           // Liste des médias
mediaService.getById(id)        // Média par ID
mediaService.create(data)       // Créer un média
mediaService.update(id, data)   // Modifier un média
mediaService.delete(id)         // Supprimer un média
```

#### 2. articleService

```typescript
articleService.getAll(params)   // Articles avec filtres
articleService.getRecent(days, limit)  // Articles récents
```

#### 3. classificationService

```typescript
classificationService.getStats(days)    // Stats par catégorie
classificationService.getWeekly(weeks)  // Stats hebdomadaires
```

#### 4. socialService

```typescript
socialService.getFacebookPosts(mediaId, limit)
socialService.getTwitterTweets(mediaId, limit)
```

#### 5. audienceService

```typescript
audienceService.getWeb(days)       // Audience web
audienceService.getFacebook(days)  // Audience Facebook
audienceService.getTwitter(days)   // Audience Twitter
audienceService.getGlobal(days)    // Audience globale
audienceService.getInactive(threshold)  // Médias inactifs
```

#### 6. rankingService

```typescript
rankingService.getRanking(days)  // Classement des médias
```

#### 7. scrapingService

```typescript
scrapingService.trigger(request)       // Déclencher scraping
scrapingService.getSchedule()          // Config automatique
scrapingService.updateSchedule(data)   // Modifier config
scrapingService.getHistory()           // Historique
```

#### 8. statsService

```typescript
statsService.getOverview(days)  // Statistiques globales
```

## 🎣 Custom Hooks

### TanStack Query Hooks

Tous les hooks utilisent TanStack Query pour :

- Cache automatique
- Invalidation intelligente
- Retry sur erreur
- Loading states
- Error handling

#### useMedia

```typescript
const { data, isLoading, error } = useMedia()
const { data } = useMediaById(id)
const { mutate } = useCreateMedia()
const { mutate } = useUpdateMedia()
const { mutate } = useDeleteMedia()
```

#### useArticles

```typescript
const { data } = useRecentArticles(days, limit)
const { data } = useArticlesByMedia(mediaId, limit)
```

#### useClassifications

```typescript
const { data } = useClassificationStats(days)
const { data } = useWeeklyCategoryStats(weeks)
```

#### useAudience

```typescript
const { data } = useAudienceWeb(days)
const { data } = useAudienceFacebook(days)
const { data } = useAudienceTwitter(days)
const { data } = useAudienceGlobal(days)
```

#### useRanking

```typescript
const { data } = useRanking(days)
```

#### useScraping

```typescript
const { mutate, isPending } = useTriggerScraping()
const { data } = useScrapingSchedule()
const { mutate } = useUpdateSchedule()
const { data } = useScrapingHistory()
```

#### useStats

```typescript
const { data } = useStats(days)
```

## 🚀 Installation

### Prérequis

- Node.js 18+
- npm ou yarn

### Installation des dépendances

```bash
cd frontend
npm install
```

### Configuration

Créer un fichier [.env](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/backend/django_back/.env:0:0-0:0) à la racine du frontend :

```env
VITE_API_URL=http://localhost:8000
```

### Lancement en développement

```bash
npm run dev
```

L'application démarre sur `http://localhost:8080/`

### Build pour production

```bash
npm run build
```

Les fichiers optimisés sont générés dans `dist/`

### Preview du build

```bash
npm run preview
```

## 🎨 Personnalisation

### Thème

Le thème est configurable via CSS variables dans `src/index.css` :

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --secondary: 210 40% 96.1%;
  /* ... autres variables */
}
```

### Dark Mode

Le dark mode est supporté via `next-themes` :

```typescript
import { ThemeProvider } from "next-themes"

<ThemeProvider attribute="class" defaultTheme="system">
  {children}
</ThemeProvider>
```

### Composants UI

Les composants shadcn/ui sont personnalisables :

```bash
# Ajouter un nouveau composant
npx shadcn-ui@latest add [component-name]
```

## 📱 Responsive Design

L'application est entièrement responsive :

- **Mobile** : < 640px
- **Tablet** : 640px - 1024px
- **Desktop** : > 1024px

Breakpoints TailwindCSS :

- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px
- `2xl:` 1536px

## 🔧 Configuration Vite

```typescript
export default defineConfig({
  server: {
    host: "::",
    port: 8080,
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

**Fonctionnalités :**

- Hot Module Replacement (HMR)
- Fast Refresh
- Alias `@/` pour imports absolus
- Build optimisé avec code splitting

## 📦 Structure des composants

### Composants Dashboard

Chaque composant dashboard suit ce pattern :

```typescript
const Component = () => {
  // 1. Hooks TanStack Query
  const { data, isLoading } = useData()
  
  // 2. State local
  const [filter, setFilter] = useState()
  
  // 3. Computed values (useMemo)
  const processedData = useMemo(() => {
    // Transformation des données
  }, [data])
  
  // 4. Handlers
  const handleAction = () => {
    // Logique métier
  }
  
  // 5. Render
  return (
    <Card>
      {/* UI */}
    </Card>
  )
}
```

### Composants UI (shadcn/ui)

Tous les composants UI sont :

- **Accessibles** : Support ARIA complet
- **Personnalisables** : Via props et CSS
- **Composables** : Peuvent être combinés
- **Type-safe** : TypeScript strict

## 🧪 Tests

### Tests API

Un service de test est disponible :

```typescript
import { testApi } from '@/services/test-api'

// Tester tous les endpoints
testApi()
```

### React Query DevTools

Les DevTools sont activés en développement :

```typescript
<ReactQueryDevtools initialIsOpen={false} />
```

**Fonctionnalités :**

- Inspection du cache
- Visualisation des queries
- Mutations tracking
- Performance monitoring

## 🔐 Sécurité

### Variables d'environnement

Utiliser `VITE_` prefix pour exposer les variables :

```env
VITE_API_URL=http://localhost:8000
```

Accès dans le code :

```typescript
import.meta.env.VITE_API_URL
```

### CORS

Le backend doit autoriser l'origine du frontend :

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
```

## 📊 Performance

### Optimisations implémentées

1. **Code Splitting** : Chargement lazy des routes
2. **Tree Shaking** : Élimination du code mort
3. **Cache TanStack Query** :
   - `staleTime`: 5 minutes
   - `gcTime`: 10 minutes
4. **Memoization** : `useMemo` pour calculs coûteux
5. **Debouncing** : Sur les inputs de recherche
6. **Virtual Scrolling** : Pour grandes listes (si nécessaire)

### Métriques

- **First Contentful Paint** : < 1.5s
- **Time to Interactive** : < 3s
- **Bundle size** : ~500KB (gzipped)

## 🐛 Débogage

### Console Logs

Les services API loggent automatiquement :

- Requêtes envoyées
- Réponses reçues
- Erreurs

### React DevTools

Installer l'extension Chrome/Firefox :

- Inspection des composants
- Props et state
- Hooks debugging

### Network Tab

Vérifier les appels API dans l'onglet Network du navigateur.

## 🚢 Déploiement

### Build de production

```bash
npm run build
```

### Serveur statique

Les fichiers dans `dist/` peuvent être servis par :

- **Nginx**
- **Apache**
- **Vercel**
- **Netlify**
- **GitHub Pages**

### Configuration Nginx

```nginx
server {
    listen 80;
    server_name media-scanner.example.com;
    root /var/www/media-scanner/dist;
  
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Variables d'environnement production

```env
VITE_API_URL=https://api.media-scanner.example.com
```

## 📝 Conventions de code

### Naming

- **Composants** : PascalCase ([MediaRanking.tsx](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/components/dashboard/MediaRanking.tsx:0:0-0:0))
- **Hooks** : camelCase avec prefix `use` ([useMedia.ts](cci:7://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/hooks/useMedia.ts:0:0-0:0))
- **Services** : camelCase avec suffix `Service` (`mediaService`)
- **Types** : PascalCase ([Media](cci:2://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/services/types.ts:5:0-15:1), [Article](cci:2://file:///c:/Users/DarkSide/Desktop/Media_Scanne/frontend/src/services/types.ts:18:0-35:1))

### Imports

Ordre des imports :

1. React & libraries
2. Components
3. Hooks
4. Services & types
5. Styles

```typescript
import { useState } from "react"
import { Card } from "@/components/ui/card"
import { useMedia } from "@/hooks/useMedia"
import { mediaService } from "@/services"
import "./styles.css"
```

### TypeScript

- Typage strict activé
- Pas de `any` (sauf exceptions justifiées)
- Interfaces pour les props
- Types pour les données API

## 🔄 Workflow de développement

1. **Créer une branche** : `git checkout -b feature/nouvelle-fonctionnalite`
2. **Développer** : Coder + tester
3. **Commit** : Messages descriptifs
4. **Push** : `git push origin feature/nouvelle-fonctionnalite`
5. **Pull Request** : Review + merge

## 📚 Ressources

### Documentation

- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [TanStack Query](https://tanstack.com/query/latest)
- [TailwindCSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Radix UI](https://www.radix-ui.com/)
- [Recharts](https://recharts.org/)
- [Vite](https://vitejs.dev/)

### Composants

Tous les composants shadcn/ui sont documentés sur [ui.shadcn.com](https://ui.shadcn.com/)

## 🤝 Contribution

Pour contribuer :

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📄 License

Ce projet est développé dans le cadre du Media Scanner pour l'analyse des médias burkinabè.

---

**Développé avec ❤️ pour l'analyse des médias burkinabè**
