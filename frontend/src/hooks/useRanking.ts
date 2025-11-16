/**
 * Custom hooks for ranking queries using TanStack Query
 */

import { useQuery } from '@tanstack/react-query';
import { rankingService } from '@/services/ranking.service';

/**
 * Hook to fetch media ranking by influence
 */
export const useRanking = (days = 30) => {
  return useQuery({
    queryKey: ['ranking', days],
    queryFn: async () => {
      const response = await rankingService.get(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};
