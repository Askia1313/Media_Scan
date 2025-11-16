/**
 * Custom hooks for stats queries using TanStack Query
 */

import { useQuery } from "@tanstack/react-query";
import { statsService } from "@/services/stats.service";

/**
 * Hook to fetch global statistics
 */
export const useStats = (days = 30) => {
  return useQuery({
    queryKey: ["stats", days],
    queryFn: async () => {
      const response = await statsService.get(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
  });
};

/**
 * Hook to check API health
 */
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await statsService.health();
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 1 * 60 * 1000, // 1 minute
    refetchInterval: 2 * 60 * 1000, // Refetch every 2 minutes
  });
};
