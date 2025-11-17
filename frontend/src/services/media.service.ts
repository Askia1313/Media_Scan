/**
 * Service pour la gestion des médias
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Media } from './types';

export interface CreateMediaDto {
  nom: string;
  url: string;
  type_site?: string;
  facebook_page?: string;
  twitter_account?: string;
  actif?: boolean;
}

export interface UpdateMediaDto {
  nom?: string;
  url?: string;
  type_site?: string;
  facebook_page?: string;
  twitter_account?: string;
  actif?: boolean;
}

export const mediaService = {
  /**
   * Récupérer tous les médias
   */
  async getAll(): Promise<ApiResponse<Media[]>> {
    return apiClient.get<Media[]>(API_ENDPOINTS.MEDIAS);
  },

  /**
   * Récupérer un média par son ID
   */
  async getById(id: number): Promise<ApiResponse<Media>> {
    return apiClient.get<Media>(API_ENDPOINTS.MEDIA_DETAIL(id));
  },

  /**
   * Créer un nouveau média
   */
  async create(data: CreateMediaDto): Promise<ApiResponse<Media>> {
    return apiClient.post<Media>(API_ENDPOINTS.MEDIAS, data);
  },

  /**
   * Mettre à jour un média
   */
  async update(id: number, data: UpdateMediaDto): Promise<ApiResponse<Media>> {
    return apiClient.put<Media>(API_ENDPOINTS.MEDIA_DETAIL(id), data);
  },

  /**
   * Supprimer un média
   */
  async delete(id: number): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(API_ENDPOINTS.MEDIA_DETAIL(id));
  },
};
