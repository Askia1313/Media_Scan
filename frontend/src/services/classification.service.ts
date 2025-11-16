/**
 * Service pour la gestion des classifications
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Classification, ClassificationStats, WeeklyCategoryStats } from './types';

export type Category = 
  | 'Politique'
  | 'Économie'
  | 'Sécurité'
  | 'Santé'
  | 'Culture'
  | 'Sport'
  | 'Autres';

export interface ClassificationParams {
  categorie: Category;
  limit?: number;
}

export const classificationService = {
  /**
   * Récupérer les classifications par catégorie
   */
  async getByCategory(
    categorie: Category,
    limit = 100
  ): Promise<ApiResponse<Classification[]>> {
    return apiClient.get<Classification[]>(API_ENDPOINTS.CLASSIFICATIONS, {
      categorie,
      limit,
    });
  },

  /**
   * Récupérer les statistiques par catégorie
   */
  async getStats(days = 30): Promise<ApiResponse<ClassificationStats[]>> {
    return apiClient.get<ClassificationStats[]>(
      API_ENDPOINTS.CLASSIFICATIONS_STATS,
      { days }
    );
  },

  /**
   * Récupérer les statistiques hebdomadaires par catégorie
   */
  async getWeeklyStats(weeks = 5): Promise<ApiResponse<WeeklyCategoryStats[]>> {
    return apiClient.get<WeeklyCategoryStats[]>(
      API_ENDPOINTS.CLASSIFICATIONS_WEEKLY,
      { weeks }
    );
  },
};
