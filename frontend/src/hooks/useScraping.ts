/**
 * Custom hooks for scraping mutations using TanStack Query
 */

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { scrapingService } from '@/services/scraping.service';
import { ScrapingRequest } from '@/services/types';
import { toast } from '@/hooks/use-toast';

/**
 * Hook to trigger scraping
 */
export const useTriggerScraping = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (request: ScrapingRequest) => {
      const response = await scrapingService.trigger(request);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      // Invalidate relevant queries after successful scraping
      queryClient.invalidateQueries({ queryKey: ['articles'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['classifications'] });
      
      toast({
        title: 'Succès',
        description: 'Le scraping a été lancé avec succès',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Erreur',
        description: error.message || 'Échec du lancement du scraping',
        variant: 'destructive',
      });
    },
  });
};

/**
 * Hook to scrape a specific media
 */
export const useScrapeMedia = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      url,
      options,
    }: {
      url: string;
      options?: {
        days?: number;
        fbPosts?: number;
        tweets?: number;
        skipFacebook?: boolean;
        skipTwitter?: boolean;
      };
    }) => {
      const response = await scrapingService.scrapeMedia(url, options);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      
      toast({
        title: 'Succès',
        description: 'Le scraping du média a été lancé',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Erreur',
        description: error.message || 'Échec du scraping du média',
        variant: 'destructive',
      });
    },
  });
};

/**
 * Hook to scrape all media
 */
export const useScrapeAll = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (options?: {
      days?: number;
      fbPosts?: number;
      tweets?: number;
    }) => {
      const response = await scrapingService.scrapeAll(options);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['classifications'] });
      
      toast({
        title: 'Succès',
        description: 'Le scraping de tous les médias a été lancé',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Erreur',
        description: error.message || 'Échec du scraping global',
        variant: 'destructive',
      });
    },
  });
};
