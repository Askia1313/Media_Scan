/**
 * Service pour la modération de contenu
 */

import { apiClient } from './api.client';

export interface ModerationStats {
  total_analyzed: number;
  total_flagged: number;
  total_toxic: number;
  total_misinformation: number;
  total_sensitive: number;
  avg_risk_score: number;
}

export interface FlaggedContent {
  id: number;
  content_type: string;
  content_id: number;
  risk_score: number;
  risk_level: string;
  is_toxic: boolean;
  is_misinformation: boolean;
  is_sensitive: boolean;
  analyzed_at: string;
  toxicity_details?: any;
  misinformation_details?: any;
  sensitivity_details?: any;
  primary_issue?: string;
}

export interface ContentModeration {
  content_type: string;
  content_id: number;
  risk_score: number;
  risk_level: string;
  should_flag: boolean;
  toxicity: {
    est_toxique: boolean;
    score_toxicite: number;
    raison: string;
    contexte?: string;
  };
  misinformation: {
    est_desinformation: boolean;
    score_desinformation: number;
    raison: string;
    sources_citees?: boolean;
  };
  sensitivity: {
    est_sensible: boolean;
    score_sensibilite: number;
    raison: string;
    traitement?: string;
  };
  analyzed_at: string;
}

class ModerationService {
  /**
   * Récupère les statistiques de modération
   */
  async getStats() {
    return apiClient.get<ModerationStats>('/api/moderation/stats/');
  }

  /**
   * Récupère les contenus signalés
   */
  async getFlaggedContents(
    contentType?: string,
    limit: number = 50
  ) {
    const params = new URLSearchParams();
    if (contentType) params.append('content_type', contentType);
    params.append('limit', limit.toString());

    return apiClient.get<FlaggedContent[]>(`/api/moderation/flagged/?${params.toString()}`);
  }

  /**
   * Récupère les détails de modération d'un contenu
   */
  async getContentModeration(
    contentType: string,
    contentId: number
  ) {
    return apiClient.get<ContentModeration>(
      `/api/moderation/content/?type=${contentType}&id=${contentId}`
    );
  }
}

export const moderationService = new ModerationService();
