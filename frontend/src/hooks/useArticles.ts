/**
 * Custom hooks for article queries using TanStack Query
 */

import { useQuery } from '@tanstack/react-query';
import { articleService, ArticleParams } from '@/services/article.service';

/**
 * Hook to fetch all articles with optional filters
 */
export const useArticles = (params?: ArticleParams) => {
  return useQuery({
    queryKey: ['articles', params],
    queryFn: async () => {
      const response = await articleService.getAll(params);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
};

/**
 * Hook to fetch articles by media
 */
export const useArticlesByMedia = (mediaId: number, limit = 100) => {
  return useQuery({
    queryKey: ['articles', 'media', mediaId, limit],
    queryFn: async () => {
      const response = await articleService.getByMedia(mediaId, limit);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    enabled: !!mediaId, // Only run if mediaId is provided
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
};

/**
 * Hook to fetch recent articles
 */
export const useRecentArticles = (days = 7, limit = 100) => {
  return useQuery({
    queryKey: ['articles', 'recent', days, limit],
    queryFn: async () => {
      const response = await articleService.getRecent(days, limit);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 3 * 60 * 1000, // 3 minutes
  });
};
