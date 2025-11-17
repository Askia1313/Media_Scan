/**
 * Custom hooks for scraping mutations using TanStack Query
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { scrapingService } from '@/services/scraping.service';
import { ScrapingRequest, ScrapingSchedule } from '@/services/types';
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
      // Invalidate relevant queries after successful scraping
      queryClient.invalidateQueries({ queryKey: ['articles'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      queryClient.invalidateQueries({ queryKey: ['classifications'] });
    },
  });
};

/**
 * Hook to get scraping schedule
 */
export const useScrapingSchedule = () => {
  return useQuery({
    queryKey: ['scraping-schedule'],
    queryFn: async () => {
      const response = await scrapingService.getSchedule();
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
  });
};

/**
 * Hook to update scraping schedule
 */
export const useUpdateScrapingSchedule = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (schedule: ScrapingSchedule) => {
      const response = await scrapingService.updateSchedule(schedule);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scraping-schedule'] });
      toast({
        title: 'Succès',
        description: 'L\'automatisation a été mise à jour',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Erreur',
        description: error.message || 'Échec de la mise à jour de l\'automatisation',
        variant: 'destructive',
      });
    },
  });
};

/**
 * Hook to toggle scraping schedule
 */
export const useToggleScrapingSchedule = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (enabled: boolean) => {
      const response = await scrapingService.toggleSchedule(enabled);
      if (response.error) {
        throw new Error(response.error);
      }
      return response.data;
    },
    onSuccess: (data, enabled) => {
      queryClient.invalidateQueries({ queryKey: ['scraping-schedule'] });
      toast({
        title: enabled ? 'Automatisation activée' : 'Automatisation désactivée',
        description: enabled
          ? 'Le scraping sera exécuté automatiquement selon la fréquence configurée'
          : 'Le scraping automatique a été désactivé',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Erreur',
        description: error.message || 'Échec du changement d\'état de l\'automatisation',
        variant: 'destructive',
      });
    },
  });
};
