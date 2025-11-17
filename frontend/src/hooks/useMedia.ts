/**
 * Custom hooks for media queries using TanStack Query
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { mediaService, CreateMediaDto, UpdateMediaDto } from '@/services/media.service';

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

/**
 * Hook to create a new media
 */
export const useCreateMedia = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateMediaDto) => {
      const response = await mediaService.create(data);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch media list
      queryClient.invalidateQueries({ queryKey: ['media'] });
    },
  });
};

/**
 * Hook to update a media
 */
export const useUpdateMedia = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: UpdateMediaDto }) => {
      const response = await mediaService.update(id, data);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: (_, variables) => {
      // Invalidate media list and specific media
      queryClient.invalidateQueries({ queryKey: ['media'] });
      queryClient.invalidateQueries({ queryKey: ['media', variables.id] });
    },
  });
};

/**
 * Hook to delete a media
 */
export const useDeleteMedia = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const response = await mediaService.delete(id);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch media list
      queryClient.invalidateQueries({ queryKey: ['media'] });
    },
  });
};
