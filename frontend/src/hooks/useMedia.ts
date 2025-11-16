/**
 * Custom hooks for media queries using TanStack Query
 */

import { useQuery } from '@tanstack/react-query';
import { mediaService } from '@/services/media.service';

/**
 * Hook to fetch all media
 */
export const useMedia = () => {
  return useQuery({
    queryKey: ['media'],
    queryFn: async () => {
      const response = await mediaService.getAll();
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes (media data changes less frequently)
  });
};

/**
 * Hook to fetch a single media by ID
 */
export const useMediaById = (id: number) => {
  return useQuery({
    queryKey: ['media', id],
    queryFn: async () => {
      const response = await mediaService.getById(id);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    enabled: !!id, // Only run if id is provided
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};
