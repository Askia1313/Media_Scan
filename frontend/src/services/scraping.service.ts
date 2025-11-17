/**
 * Service pour le scraping
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { ScrapingRequest, ScrapingResponse, ScrapingSchedule, ScrapingScheduleResponse } from './types';

export const scrapingService = {
  /**
   * Déclencher un scraping
   */
  async trigger(request: ScrapingRequest): Promise<ApiResponse<ScrapingResponse>> {
    return apiClient.post<ScrapingResponse>(
      API_ENDPOINTS.SCRAPING_TRIGGER,
      request
    );
  },

  /**
   * Scraper un média spécifique
   */
  async scrapeMedia(
    url: string,
    options?: {
      days?: number;
      fbPosts?: number;
      tweets?: number;
      skipFacebook?: boolean;
      skipTwitter?: boolean;
    }
  ): Promise<ApiResponse<ScrapingResponse>> {
    return this.trigger({
      url,
      all: false,
      days: options?.days,
      fb_posts: options?.fbPosts,
      tweets: options?.tweets,
      skip_facebook: options?.skipFacebook,
      skip_twitter: options?.skipTwitter,
    });
  },

  /**
   * Scraper tous les médias
   */
  async scrapeAll(options?: {
    days?: number;
    fbPosts?: number;
    tweets?: number;
  }): Promise<ApiResponse<ScrapingResponse>> {
    return this.trigger({
      all: true,
      days: options?.days,
      fb_posts: options?.fbPosts,
      tweets: options?.tweets,
    });
  },

  /**
   * Récupérer la configuration de l'automatisation
   */
  async getSchedule(): Promise<ApiResponse<ScrapingSchedule>> {
    return apiClient.get<ScrapingSchedule>(API_ENDPOINTS.SCRAPING_SCHEDULE);
  },

  /**
   * Créer ou mettre à jour l'automatisation du scraping
   */
  async updateSchedule(schedule: ScrapingSchedule): Promise<ApiResponse<ScrapingScheduleResponse>> {
    return apiClient.post<ScrapingScheduleResponse>(
      API_ENDPOINTS.SCRAPING_SCHEDULE,
      schedule
    );
  },

  /**
   * Activer/Désactiver l'automatisation
   */
  async toggleSchedule(enabled: boolean): Promise<ApiResponse<ScrapingScheduleResponse>> {
    return apiClient.post<ScrapingScheduleResponse>(
      API_ENDPOINTS.SCRAPING_SCHEDULE,
      { enabled }
    );
  },

  /**
   * Supprimer l'automatisation
   */
  async deleteSchedule(): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(API_ENDPOINTS.SCRAPING_SCHEDULE);
  },
};
