/**
 * Custom hooks for classification queries using TanStack Query
 */

import { useQuery } from '@tanstack/react-query';
import { classificationService, Category } from '@/services/classification.service';

/**
 * Hook to fetch classifications by category
 */
export const useClassificationsByCategory = (categorie: Category, limit = 100) => {
  return useQuery({
    queryKey: ['classifications', 'category', categorie, limit],
    queryFn: async () => {
      const response = await classificationService.getByCategory(categorie, limit);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch classification statistics
 */
export const useClassificationStats = (days = 30) => {
  return useQuery({
    queryKey: ['classifications', 'stats', days],
    queryFn: async () => {
      const response = await classificationService.getStats(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};
