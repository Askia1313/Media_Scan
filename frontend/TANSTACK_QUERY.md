# TanStack Query Integration

This project uses **TanStack Query v5** (formerly React Query) for efficient server state management.

## Overview

TanStack Query provides:

- **Automatic caching** with configurable stale times
- **Background refetching** to keep data fresh
- **Request deduplication** to avoid redundant API calls
- **Loading and error states** out of the box
- **Optimistic updates** for mutations
- **DevTools** for debugging queries

## Configuration

The QueryClient is configured in `src/App.tsx` with these defaults:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2, // Retry failed requests twice
      staleTime: 5 * 60 * 1000, // Data is fresh for 5 minutes
      gcTime: 10 * 60 * 1000, // Cache persists for 10 minutes
      refetchOnWindowFocus: false, // Don't refetch on window focus
      refetchOnReconnect: true, // Refetch when reconnecting
    },
    mutations: {
      retry: 1, // Retry failed mutations once
    },
  },
});
```

## Custom Hooks

All API calls are wrapped in custom hooks located in `src/hooks/`:

### Articles (`useArticles.ts`)

- `useArticles(params?)` - Fetch all articles with optional filters
- `useArticlesByMedia(mediaId, limit)` - Fetch articles by media
- `useRecentArticles(days, limit)` - Fetch recent articles

### Audience (`useAudience.ts`)

- `useWebAudience(days)` - Web audience data
- `useFacebookAudience(days)` - Facebook audience data
- `useTwitterAudience(days)` - Twitter audience data
- `useGlobalAudience(days)` - Global audience across all platforms
- `useInactiveMedia(daysThreshold)` - Inactive media detection

### Classifications (`useClassifications.ts`)

- `useClassificationsByCategory(category, limit)` - Classifications by category
- `useClassificationStats(days)` - Classification statistics

### Media (`useMedia.ts`)

- `useMedia()` - Fetch all media
- `useMediaById(id)` - Fetch single media by ID

### Ranking (`useRanking.ts`)

- `useRanking(days)` - Media ranking by influence

### Scraping (`useScraping.ts`) - Mutations

- `useTriggerScraping()` - Trigger scraping operation
- `useScrapeMedia()` - Scrape specific media
- `useScrapeAll()` - Scrape all media

### Stats (`useStats.ts`)

- `useStats(days)` - Global statistics
- `useHealthCheck()` - API health check

## Usage Examples

### Basic Query

```typescript
import { useStats } from "@/hooks/useStats";

function Dashboard() {
  const { data, isLoading, error } = useStats(30);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>Total Articles: {data?.total_articles}</div>;
}
```

### Query with Data Transformation

```typescript
import { useMemo } from "react";
import { useRecentArticles } from "@/hooks/useArticles";

function ArticleChart() {
  const { data: articles, isLoading } = useRecentArticles(7, 1000);

  const chartData = useMemo(() => {
    if (!articles) return [];
    // Transform articles into chart format
    return articles.map((article) => ({
      date: article.date_publication,
      views: article.vues,
    }));
  }, [articles]);

  return <Chart data={chartData} />;
}
```

### Mutation with Optimistic Updates

```typescript
import { useScrapeMedia } from "@/hooks/useScraping";

function ScrapeButton({ url }: { url: string }) {
  const { mutate, isPending } = useScrapeMedia();

  const handleScrape = () => {
    mutate({ url, options: { days: 7 } });
  };

  return (
    <button onClick={handleScrape} disabled={isPending}>
      {isPending ? "Scraping..." : "Start Scrape"}
    </button>
  );
}
```

### Parallel Queries

```typescript
import { useStats } from "@/hooks/useStats";
import { useMedia } from "@/hooks/useMedia";
import { useRanking } from "@/hooks/useRanking";

function Overview() {
  const stats = useStats(30);
  const media = useMedia();
  const ranking = useRanking(30);

  const isLoading = stats.isLoading || media.isLoading || ranking.isLoading;

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <Stats data={stats.data} />
      <MediaList data={media.data} />
      <Rankings data={ranking.data} />
    </div>
  );
}
```

## Query Keys

Query keys are structured for easy invalidation:

```typescript
// Articles
["articles"][("articles", params)][("articles", "media", mediaId, limit)][ // All articles // Filtered articles // Articles by media
  ("articles", "recent", days, limit)
][ // Recent articles
  // Audience
  ("audience", "web", days)
][("audience", "facebook", days)][("audience", "twitter", days)][
  ("audience", "global", days)
][("audience", "inactive", daysThreshold)][
  // Classifications
  ("classifications", "category", category, limit)
][("classifications", "stats", days)][
  // Media
  "media"
][("media", id)][ // All media // Single media
  // Ranking
  ("ranking", days)
][
  // Stats
  ("stats", days)
]["health"];
```

## Cache Invalidation

Mutations automatically invalidate related queries:

```typescript
// After scraping, these queries are invalidated:
queryClient.invalidateQueries({ queryKey: ["articles"] });
queryClient.invalidateQueries({ queryKey: ["stats"] });
queryClient.invalidateQueries({ queryKey: ["classifications"] });
```

## DevTools

React Query DevTools are available in development mode. Click the floating icon in the bottom-right corner to:

- View all active queries
- Inspect query data and state
- Manually refetch or invalidate queries
- Monitor network requests

## Best Practices

1. **Use custom hooks** instead of calling services directly
2. **Leverage useMemo** for expensive data transformations
3. **Set appropriate staleTime** based on data volatility
4. **Use enabled option** to conditionally run queries
5. **Invalidate queries** after mutations to refresh data
6. **Handle loading and error states** in components
7. **Keep query keys consistent** for proper cache management

## Migration from useState/useEffect

Before (manual state management):

```typescript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const loadData = async () => {
    setLoading(true);
    const response = await service.getData();
    setData(response.data);
    setLoading(false);
  };
  loadData();
}, []);
```

After (TanStack Query):

```typescript
const { data, isLoading } = useCustomHook();
```

## Resources

- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [React Query v5 Migration Guide](https://tanstack.com/query/latest/docs/react/guides/migrating-to-v5)
- [Query Keys Guide](https://tanstack.com/query/latest/docs/react/guides/query-keys)
