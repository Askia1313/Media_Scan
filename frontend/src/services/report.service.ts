/**
 * Service pour la génération de rapports
 */

import { apiClient } from './api.client';
import { API_ENDPOINTS } from './api.config';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import * as XLSX from 'xlsx';

// Déclaration pour jspdf-autotable
declare module 'jspdf' {
  interface jsPDF {
    autoTable: (options: any) => jsPDF;
    lastAutoTable: { finalY: number };
  }
}

export type ReportPeriod = 'daily' | 'weekly';

interface ReportData {
  period: ReportPeriod;
  startDate: string;
  endDate: string;
  stats: any;
  ranking: any[];
  categoryStats: any[];
  articles: any[];
  weeklyStats: any[];
  medias: any[];
  audienceWeb: any[];
  audienceFacebook: any[];
  audienceTwitter: any[];
}

export const reportService = {
  /**
   * Récupérer les données pour le rapport
   */
  async getReportData(period: ReportPeriod): Promise<ReportData> {
    const days = period === 'daily' ? 1 : 7;
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    // Récupérer toutes les données en parallèle
    const [
      statsRes, 
      rankingRes, 
      categoryRes, 
      articlesRes,
      weeklyStatsRes,
      mediasRes,
      audienceWebRes,
      audienceFbRes,
      audienceTwitterRes
    ] = await Promise.all([
      apiClient.get(API_ENDPOINTS.STATS, { days }),
      apiClient.get(API_ENDPOINTS.RANKING, { days }),
      apiClient.get(API_ENDPOINTS.CLASSIFICATIONS_STATS, { days }),
      apiClient.get(API_ENDPOINTS.ARTICLES, { days, limit: 200 }),
      apiClient.get(API_ENDPOINTS.CLASSIFICATIONS_WEEKLY, { weeks: period === 'daily' ? 1 : 2 }),
      apiClient.get(API_ENDPOINTS.MEDIAS, { actif: true }),
      apiClient.get(API_ENDPOINTS.AUDIENCE_WEB, { days }),
      apiClient.get(API_ENDPOINTS.AUDIENCE_FACEBOOK, { days }),
      apiClient.get(API_ENDPOINTS.AUDIENCE_TWITTER, { days }),
    ]);

    return {
      period,
      startDate: startDate.toISOString(),
      endDate: endDate.toISOString(),
      stats: statsRes.data || {},
      ranking: (rankingRes.data as any[]) || [],
      categoryStats: (categoryRes.data as any[]) || [],
      articles: (articlesRes.data as any[]) || [],
      weeklyStats: (weeklyStatsRes.data as any[]) || [],
      medias: (mediasRes.data as any[]) || [],
      audienceWeb: (audienceWebRes.data as any[]) || [],
      audienceFacebook: (audienceFbRes.data as any[]) || [],
      audienceTwitter: (audienceTwitterRes.data as any[]) || [],
    };
  },

  /**
   * Générer un rapport PDF
   */
  async generatePDF(period: ReportPeriod): Promise<void> {
    const data = await this.getReportData(period);
    const doc = new jsPDF();

    // En-tête
    doc.setFontSize(20);
    doc.text('CSC Média Monitor', 105, 20, { align: 'center' });
    
    doc.setFontSize(14);
    const periodText = period === 'daily' ? 'Rapport Journalier' : 'Rapport Hebdomadaire';
    doc.text(periodText, 105, 30, { align: 'center' });
    
    doc.setFontSize(10);
    const dateText = `Du ${new Date(data.startDate).toLocaleDateString('fr-FR')} au ${new Date(data.endDate).toLocaleDateString('fr-FR')}`;
    doc.text(dateText, 105, 38, { align: 'center' });

    let yPos = 50;

    // Résumé exécutif
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('📋 RÉSUMÉ EXÉCUTIF', 14, yPos);
    yPos += 10;

    doc.setFont(undefined, 'normal');
    doc.setFontSize(10);
    
    // Calculer les métriques clés
    const totalEngagement = data.ranking.reduce((sum: number, m: any) => sum + (m.engagement_total || 0), 0);
    const avgEngagement = data.ranking.length > 0 ? Math.round(totalEngagement / data.ranking.length) : 0;
    const topMedia = data.ranking[0];
    const totalFbPosts = data.ranking.reduce((sum: number, m: any) => sum + (m.total_posts_facebook || 0), 0);
    
    doc.text(`📊 Médias actifs surveillés: ${data.stats.total_medias || 0}`, 20, yPos);
    yPos += 6;
    doc.text(`📰 Articles collectés: ${data.stats.total_articles || 0}`, 20, yPos);
    yPos += 6;
    doc.text(`📱 Posts Facebook: ${totalFbPosts}`, 20, yPos);
    yPos += 6;
    doc.text(`💬 Engagement total: ${totalEngagement.toLocaleString('fr-FR')}`, 20, yPos);
    yPos += 6;
    doc.text(`📈 Engagement moyen par média: ${avgEngagement.toLocaleString('fr-FR')}`, 20, yPos);
    yPos += 6;
    doc.text(`🏆 Média le plus performant: ${topMedia?.nom || 'N/A'}`, 20, yPos);
    yPos += 6;
    doc.text(`🎯 Catégories identifiées: ${data.stats.total_categories || 0}`, 20, yPos);
    yPos += 12;

    // Classement détaillé des médias
    if (data.ranking && data.ranking.length > 0) {
      doc.setFontSize(12);
      doc.setFont(undefined, 'bold');
      doc.text('🏆 CLASSEMENT DES MÉDIAS PAR PERFORMANCE', 14, yPos);
      yPos += 8;

      const rankingData = data.ranking.map((media: any, index: number) => [
        `${index + 1}`,
        media.nom || 'N/A',
        media.total_articles || 0,
        media.total_posts_facebook || 0,
        (media.total_likes || 0).toLocaleString('fr-FR'),
        (media.total_comments || 0).toLocaleString('fr-FR'),
        (media.total_shares || 0).toLocaleString('fr-FR'),
        (media.engagement_total || 0).toLocaleString('fr-FR'),
      ]);

      (doc as any).autoTable({
        startY: yPos,
        head: [['#', 'Média', 'Articles', 'Posts FB', 'Likes', 'Comm.', 'Partages', 'Engagement']],
        body: rankingData,
        theme: 'striped',
        headStyles: { fillColor: [59, 130, 246], fontSize: 9 },
        bodyStyles: { fontSize: 8 },
        margin: { left: 14, right: 14 },
        columnStyles: {
          0: { cellWidth: 10 },
          1: { cellWidth: 40 },
          2: { cellWidth: 20 },
          3: { cellWidth: 20 },
          4: { cellWidth: 20 },
          5: { cellWidth: 20 },
          6: { cellWidth: 20 },
          7: { cellWidth: 25 },
        },
      });

      yPos = (doc as any).lastAutoTable.finalY + 12;
    }

    // Nouvelle page pour l'analyse thématique
    doc.addPage();
    yPos = 20;
    
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('📑 ANALYSE THÉMATIQUE', 14, yPos);
    yPos += 10;

    // Répartition par catégorie
    if (data.categoryStats && data.categoryStats.length > 0) {
      doc.setFontSize(11);
      doc.text('Distribution des catégories', 14, yPos);
      yPos += 8;

      const totalCat = data.categoryStats.reduce((sum: number, c: any) => sum + (c.total || 0), 0);
      const categoryData = data.categoryStats.map((cat: any) => {
        const percentage = totalCat > 0 ? ((cat.total || 0) / totalCat * 100).toFixed(1) : '0.0';
        return [
          cat.categorie || 'N/A',
          cat.total || 0,
          `${percentage}%`,
          `${((cat.confiance_moyenne || 0) * 100).toFixed(1)}%`,
        ];
      });

      (doc as any).autoTable({
        startY: yPos,
        head: [['Catégorie', 'Nombre', '% du total', 'Confiance']],
        body: categoryData,
        theme: 'striped',
        headStyles: { fillColor: [59, 130, 246] },
        margin: { left: 14, right: 14 },
      });

      yPos = (doc as any).lastAutoTable.finalY + 15;
      
      // Insights thématiques
      doc.setFontSize(10);
      doc.setFont(undefined, 'bold');
      doc.text('💡 Insights:', 14, yPos);
      yPos += 6;
      doc.setFont(undefined, 'normal');
      
      const topCategory = data.categoryStats[0];
      if (topCategory) {
        doc.text(`• Catégorie dominante: ${topCategory.categorie} (${topCategory.total} articles)`, 20, yPos);
        yPos += 6;
      }
      
      const highConfidence = data.categoryStats.filter((c: any) => (c.confiance_moyenne || 0) > 0.8).length;
      doc.text(`• ${highConfidence} catégories avec confiance > 80%`, 20, yPos);
      yPos += 12;
    }

    // Nouvelle page pour l'analyse d'audience
    doc.addPage();
    yPos = 20;
    
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('👥 ANALYSE D\'AUDIENCE', 14, yPos);
    yPos += 10;

    // Audience Web
    if (data.audienceWeb && data.audienceWeb.length > 0) {
      doc.setFontSize(11);
      doc.text('Performance Web', 14, yPos);
      yPos += 8;

      const webData = data.audienceWeb.slice(0, 5).map((media: any) => [
        media.nom || 'N/A',
        (media.total_articles || 0).toLocaleString('fr-FR'),
        (media.total_vues || 0).toLocaleString('fr-FR'),
        (media.total_commentaires || 0).toLocaleString('fr-FR'),
      ]);

      (doc as any).autoTable({
        startY: yPos,
        head: [['Média', 'Articles', 'Vues', 'Commentaires']],
        body: webData,
        theme: 'striped',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 14, right: 14 },
      });

      yPos = (doc as any).lastAutoTable.finalY + 12;
    }

    // Audience Facebook
    if (data.audienceFacebook && data.audienceFacebook.length > 0) {
      doc.setFontSize(11);
      doc.text('Performance Facebook', 14, yPos);
      yPos += 8;

      const fbData = data.audienceFacebook.slice(0, 5).map((media: any) => [
        media.nom || 'N/A',
        (media.total_posts || 0).toLocaleString('fr-FR'),
        (media.total_likes || 0).toLocaleString('fr-FR'),
        (media.engagement_moyen || 0).toLocaleString('fr-FR'),
      ]);

      (doc as any).autoTable({
        startY: yPos,
        head: [['Média', 'Posts', 'Likes', 'Eng. Moyen']],
        body: fbData,
        theme: 'striped',
        headStyles: { fillColor: [59, 89, 152] },
        margin: { left: 14, right: 14 },
      });

      yPos = (doc as any).lastAutoTable.finalY + 12;
    }

    // Recommandations stratégiques
    doc.addPage();
    yPos = 20;
    
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('💡 RECOMMANDATIONS STRATÉGIQUES', 14, yPos);
    yPos += 12;

    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    
    // Analyser les tendances
    const lowPerformers = data.ranking.filter((m: any) => (m.engagement_total || 0) < avgEngagement).length;
    const highPerformers = data.ranking.filter((m: any) => (m.engagement_total || 0) > avgEngagement * 1.5).length;
    
    doc.setFont(undefined, 'bold');
    doc.text('📊 Analyse de performance:', 14, yPos);
    yPos += 7;
    doc.setFont(undefined, 'normal');
    doc.text(`• ${highPerformers} médias dépassent 150% de l'engagement moyen`, 20, yPos);
    yPos += 6;
    doc.text(`• ${lowPerformers} médias sont en dessous de la moyenne`, 20, yPos);
    yPos += 10;

    doc.setFont(undefined, 'bold');
    doc.text('🎯 Actions recommandées:', 14, yPos);
    yPos += 7;
    doc.setFont(undefined, 'normal');
    
    if (topMedia) {
      doc.text(`• Analyser les stratégies de ${topMedia.nom} (leader du classement)`, 20, yPos);
      yPos += 6;
    }
    
    if (lowPerformers > 0) {
      doc.text(`• Renforcer le suivi des ${lowPerformers} médias sous-performants`, 20, yPos);
      yPos += 6;
    }
    
    const topCat = data.categoryStats[0];
    if (topCat) {
      doc.text(`• Capitaliser sur la catégorie "${topCat.categorie}" (${topCat.total} articles)`, 20, yPos);
      yPos += 6;
    }
    
    doc.text(`• Diversifier la couverture thématique (${data.stats.total_categories} catégories actuelles)`, 20, yPos);
    yPos += 6;
    doc.text('• Augmenter la fréquence de collecte pour les médias à fort engagement', 20, yPos);
    yPos += 10;

    doc.setFont(undefined, 'bold');
    doc.text('⚠️ Points de vigilance:', 14, yPos);
    yPos += 7;
    doc.setFont(undefined, 'normal');
    doc.text('• Surveiller les variations d\'engagement sur les réseaux sociaux', 20, yPos);
    yPos += 6;
    doc.text('• Vérifier la qualité des classifications automatiques', 20, yPos);
    yPos += 6;
    doc.text('• Identifier les contenus sensibles nécessitant une modération', 20, yPos);

    // Nouvelle page pour les articles récents
    if (data.articles && data.articles.length > 0) {
      doc.addPage();
      yPos = 20;

      doc.setFontSize(14);
      doc.setFont(undefined, 'bold');
      doc.text('📰 ARTICLES RÉCENTS', 14, yPos);
      yPos += 8;

      const articlesData = data.articles.slice(0, 20).map((article: any) => [
        new Date(article.date_publication).toLocaleDateString('fr-FR'),
        article.titre?.substring(0, 70) + (article.titre?.length > 70 ? '...' : '') || 'N/A',
        (article.vues || 0).toLocaleString('fr-FR'),
      ]);

      (doc as any).autoTable({
        startY: yPos,
        head: [['Date', 'Titre', 'Vues']],
        body: articlesData,
        theme: 'striped',
        headStyles: { fillColor: [59, 130, 246], fontSize: 9 },
        bodyStyles: { fontSize: 8 },
        margin: { left: 14, right: 14 },
        columnStyles: {
          0: { cellWidth: 25 },
          1: { cellWidth: 140 },
          2: { cellWidth: 20 },
        },
      });
    }

    // Pied de page
    const pageCount = (doc as any).internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFontSize(8);
      doc.setTextColor(150);
      doc.text(
        `Page ${i} sur ${pageCount} - Généré le ${new Date().toLocaleDateString('fr-FR')} à ${new Date().toLocaleTimeString('fr-FR')}`,
        105,
        290,
        { align: 'center' }
      );
    }

    // Télécharger
    const filename = `rapport_${period}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
  },

  /**
   * Générer un rapport Excel
   */
  async generateExcel(period: ReportPeriod): Promise<void> {
    const data = await this.getReportData(period);
    const workbook = XLSX.utils.book_new();

    // Calculer les métriques pour le résumé
    const totalEngagement = data.ranking.reduce((sum: number, m: any) => sum + (m.engagement_total || 0), 0);
    const avgEngagement = data.ranking.length > 0 ? Math.round(totalEngagement / data.ranking.length) : 0;
    const topMedia = data.ranking[0];
    const totalFbPosts = data.ranking.reduce((sum: number, m: any) => sum + (m.total_posts_facebook || 0), 0);
    
    // Feuille 1: Résumé Exécutif
    const statsData = [
      ['CSC MÉDIA MONITOR'],
      [period === 'daily' ? 'RAPPORT JOURNALIER' : 'RAPPORT HEBDOMADAIRE'],
      [`Du ${new Date(data.startDate).toLocaleDateString('fr-FR')} au ${new Date(data.endDate).toLocaleDateString('fr-FR')}`],
      [],
      ['RÉSUMÉ EXÉCUTIF'],
      [],
      ['Indicateur', 'Valeur'],
      ['Médias actifs surveillés', data.stats.total_medias || 0],
      ['Articles collectés', data.stats.total_articles || 0],
      ['Posts Facebook', totalFbPosts],
      ['Engagement total', totalEngagement],
      ['Engagement moyen par média', avgEngagement],
      ['Média le plus performant', topMedia?.nom || 'N/A'],
      ['Catégories identifiées', data.stats.total_categories || 0],
      [],
      ['MÉTRIQUES CLÉS'],
      [],
      ['Total Likes', data.ranking.reduce((sum: number, m: any) => sum + (m.total_likes || 0), 0)],
      ['Total Commentaires', data.ranking.reduce((sum: number, m: any) => sum + (m.total_comments || 0), 0)],
      ['Total Partages', data.ranking.reduce((sum: number, m: any) => sum + (m.total_shares || 0), 0)],
    ];
    const statsSheet = XLSX.utils.aoa_to_sheet(statsData);
    XLSX.utils.book_append_sheet(workbook, statsSheet, 'Résumé');

    // Feuille 2: Classement des médias
    if (data.ranking && data.ranking.length > 0) {
      const rankingData = [
        ['Classement des Médias'],
        [],
        ['Rang', 'Média', 'Articles', 'Posts Facebook', 'Likes', 'Commentaires', 'Partages', 'Engagement Total'],
        ...data.ranking.map((media: any, index: number) => [
          index + 1,
          media.nom || 'N/A',
          media.total_articles || 0,
          media.total_posts_facebook || 0,
          media.total_likes || 0,
          media.total_comments || 0,
          media.total_shares || 0,
          media.engagement_total || 0,
        ]),
      ];
      const rankingSheet = XLSX.utils.aoa_to_sheet(rankingData);
      XLSX.utils.book_append_sheet(workbook, rankingSheet, 'Classement');
    }

    // Feuille 3: Catégories
    if (data.categoryStats && data.categoryStats.length > 0) {
      const categoryData = [
        ['Répartition par Catégorie'],
        [],
        ['Catégorie', 'Nombre d\'articles', 'Confiance moyenne (%)'],
        ...data.categoryStats.map((cat: any) => [
          cat.categorie || 'N/A',
          cat.total || 0,
          ((cat.confiance_moyenne || 0) * 100).toFixed(1),
        ]),
      ];
      const categorySheet = XLSX.utils.aoa_to_sheet(categoryData);
      XLSX.utils.book_append_sheet(workbook, categorySheet, 'Catégories');
    }

    // Feuille 4: Audience Web
    if (data.audienceWeb && data.audienceWeb.length > 0) {
      const webData = [
        ['Performance Web'],
        [],
        ['Média', 'Articles', 'Vues', 'Commentaires', 'Vues/Article'],
        ...data.audienceWeb.map((media: any) => [
          media.nom || 'N/A',
          media.total_articles || 0,
          media.total_vues || 0,
          media.total_commentaires || 0,
          media.total_articles > 0 ? Math.round((media.total_vues || 0) / media.total_articles) : 0,
        ]),
      ];
      const webSheet = XLSX.utils.aoa_to_sheet(webData);
      XLSX.utils.book_append_sheet(workbook, webSheet, 'Audience Web');
    }

    // Feuille 5: Audience Facebook
    if (data.audienceFacebook && data.audienceFacebook.length > 0) {
      const fbData = [
        ['Performance Facebook'],
        [],
        ['Média', 'Posts', 'Likes', 'Commentaires', 'Partages', 'Engagement Total', 'Engagement Moyen'],
        ...data.audienceFacebook.map((media: any) => [
          media.nom || 'N/A',
          media.total_posts || 0,
          media.total_likes || 0,
          media.total_commentaires || 0,
          media.total_partages || 0,
          media.engagement_total || 0,
          media.engagement_moyen || 0,
        ]),
      ];
      const fbSheet = XLSX.utils.aoa_to_sheet(fbData);
      XLSX.utils.book_append_sheet(workbook, fbSheet, 'Audience Facebook');
    }

    // Feuille 6: Articles récents
    if (data.articles && data.articles.length > 0) {
      const articlesData = [
        ['Articles Récents'],
        [],
        ['Date', 'Titre', 'Auteur', 'URL', 'Vues', 'Commentaires'],
        ...data.articles.map((article: any) => [
          new Date(article.date_publication).toLocaleDateString('fr-FR'),
          article.titre || 'N/A',
          article.auteur || 'N/A',
          article.url || 'N/A',
          article.vues || 0,
          article.commentaires || 0,
        ]),
      ];
      const articlesSheet = XLSX.utils.aoa_to_sheet(articlesData);
      XLSX.utils.book_append_sheet(workbook, articlesSheet, 'Articles');
    }

    // Feuille 7: Recommandations
    const lowPerformers = data.ranking.filter((m: any) => (m.engagement_total || 0) < avgEngagement).length;
    const highPerformers = data.ranking.filter((m: any) => (m.engagement_total || 0) > avgEngagement * 1.5).length;
    const topCat = data.categoryStats[0];
    
    const recommendationsData = [
      ['RECOMMANDATIONS STRATÉGIQUES'],
      [],
      ['Type', 'Recommandation'],
      ['Performance', `${highPerformers} médias dépassent 150% de l'engagement moyen`],
      ['Performance', `${lowPerformers} médias sont en dessous de la moyenne`],
      [],
      ['ACTIONS RECOMMANDÉES'],
      [],
      ['Priorité', 'Action'],
      ['Haute', topMedia ? `Analyser les stratégies de ${topMedia.nom} (leader du classement)` : 'N/A'],
      ['Haute', lowPerformers > 0 ? `Renforcer le suivi des ${lowPerformers} médias sous-performants` : 'N/A'],
      ['Moyenne', topCat ? `Capitaliser sur la catégorie "${topCat.categorie}" (${topCat.total} articles)` : 'N/A'],
      ['Moyenne', `Diversifier la couverture thématique (${data.stats.total_categories} catégories actuelles)`],
      ['Moyenne', 'Augmenter la fréquence de collecte pour les médias à fort engagement'],
      [],
      ['POINTS DE VIGILANCE'],
      [],
      ['Domaine', 'Point à surveiller'],
      ['Engagement', 'Surveiller les variations d\'engagement sur les réseaux sociaux'],
      ['Qualité', 'Vérifier la qualité des classifications automatiques'],
      ['Modération', 'Identifier les contenus sensibles nécessitant une modération'],
    ];
    const recommendationsSheet = XLSX.utils.aoa_to_sheet(recommendationsData);
    XLSX.utils.book_append_sheet(workbook, recommendationsSheet, 'Recommandations');

    // Télécharger
    const filename = `rapport_${period}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(workbook, filename);
  },
};
