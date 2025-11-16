/**
 * Custom hooks for audience queries using TanStack Query
 */

import { useQuery } from '@tanstack/react-query';
import { audienceService } from '@/services/audience.service';

/**
 * Hook to fetch web audience data
 */
export const useWebAudience = (days = 30) => {
  return useQuery({
    queryKey: ['audience', 'web', days],
    queryFn: async () => {
      const response = await audienceService.getWeb(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch Facebook audience data
 */
export const useFacebookAudience = (days = 30) => {
  return useQuery({
    queryKey: ['audience', 'facebook', days],
    queryFn: async () => {
      const response = await audienceService.getFacebook(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch Twitter audience data
 */
export const useTwitterAudience = (days = 30) => {
  return useQuery({
    queryKey: ['audience', 'twitter', days],
    queryFn: async () => {
      const response = await audienceService.getTwitter(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch global audience data (all platforms)
 */
export const useGlobalAudience = (days = 30) => {
  return useQuery({
    queryKey: ['audience', 'global', days],
    queryFn: async () => {
      const response = await audienceService.getGlobal(days);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch inactive media
 */
export const useInactiveMedia = (daysThreshold = 7) => {
  return useQuery({
    queryKey: ['audience', 'inactive', daysThreshold],
    queryFn: async () => {
      const response = await audienceService.getInactive(daysThreshold);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};
