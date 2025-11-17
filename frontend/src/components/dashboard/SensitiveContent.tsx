import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { AlertTriangle, Ban, Flame, Eye, ExternalLink, X } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { moderationService } from "@/services/moderation.service";
import { articleService } from "@/services/article.service";
import { mediaService } from "@/services/media.service";
import { toast } from "@/hooks/use-toast";

const SensitiveContent = () => {
  const [loading, setLoading] = useState(true);
  const [alertTypes, setAlertTypes] = useState<any[]>([]);
  const [weeklyAlerts, setWeeklyAlerts] = useState<any[]>([]);
  const [recentAlerts, setRecentAlerts] = useState<any[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<any>(null);
  const [articleDetails, setArticleDetails] = useState<any>(null);
  const [moderationDetails, setModerationDetails] = useState<any>(null);
  const [mediaDetails, setMediaDetails] = useState<any>(null);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // Charger les contenus signalés depuis l'API de modération
      const flaggedResponse = await moderationService.getFlaggedContents(
        undefined,
        50
      );

      if (flaggedResponse.data && !flaggedResponse.error) {
        const flaggedContents = flaggedResponse.data;

        // Transformer les données pour l'affichage
        const alerts = flaggedContents.map((content) => {
          const date = new Date(content.analyzed_at);
          const now = new Date();
          const diffHours = Math.floor(
            (now.getTime() - date.getTime()) / (1000 * 60 * 60)
          );

          let dateStr = "";
          if (diffHours < 1) {
            dateStr = "À l'instant";
          } else if (diffHours < 24) {
            dateStr = `Il y a ${diffHours}h`;
          } else if (diffHours < 48) {
            dateStr = "Hier";
          } else {
            dateStr = `Il y a ${Math.floor(diffHours / 24)}j`;
          }

          // Utiliser le type principal déterminé par l'IA
          let type = "Contenu sensible";
          if (content.primary_issue) {
            switch (content.primary_issue) {
              case "toxicity":
                type = "Discours de haine";
                break;
              case "misinformation":
                type = "Désinformation";
                break;
              case "sensitivity":
                type = "Contenu sensible";
                break;
            }
          }

          // Déterminer la sévérité basée sur le score
          let severity = "medium";
          if (content.risk_score >= 8) {
            severity = "high";
          } else if (content.risk_score < 5) {
            severity = "low";
          }

          return {
            id: content.id,
            content_id: content.content_id,
            content_type: content.content_type,
            media:
              content.content_type === "article"
                ? "Article"
                : content.content_type === "facebook_post"
                ? "Facebook"
                : "Twitter",
            type,
            title: `${content.content_type} #${content.content_id}`,
            date: dateStr,
            severity,
            status: "En cours d'examen",
            risk_score: content.risk_score,
            risk_level: content.risk_level,
          };
        });

        setRecentAlerts(alerts.slice(0, 10));

        // Compter les alertes par type
        const typeCounts = {
          "Discours de haine": 0,
          Désinformation: 0,
          "Contenu toxique": 0,
        };

        alerts.forEach((alert) => {
          if (typeCounts[alert.type as keyof typeof typeCounts] !== undefined) {
            typeCounts[alert.type as keyof typeof typeCounts]++;
          }
        });

        const alertTypesData = [
          {
            type: "Discours de haine",
            count: typeCounts["Discours de haine"],
            severity: "high",
            color: "hsl(var(--destructive))",
            icon: Flame,
          },
          {
            type: "Désinformation",
            count: typeCounts["Désinformation"],
            severity: "high",
            color: "hsl(var(--warning))",
            icon: Ban,
          },
          {
            type: "Contenu toxique",
            count: typeCounts["Contenu toxique"],
            severity: "medium",
            color: "hsl(var(--accent))",
            icon: AlertTriangle,
          },
        ];

        setAlertTypes(alertTypesData);

        // Données hebdomadaires simplifiées (à améliorer avec de vraies données temporelles)
        const weekly = [
          {
            semaine: "Cette semaine",
            haine: typeCounts["Discours de haine"],
            desinformation: typeCounts["Désinformation"],
            toxicite: typeCounts["Contenu toxique"],
          },
        ];
        setWeeklyAlerts(weekly);
      }
    } catch (error) {
      console.error("Erreur lors du chargement des alertes:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les contenus sensibles",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleViewAlert = async (alert: any) => {
    setSelectedAlert(alert);
    setDetailsLoading(true);

    try {
      // Charger les détails de l'article si c'est un article
      if (alert.content_type === "article") {
        const articleResponse = await articleService.getRecent(30, 1000);
        if (articleResponse.data) {
          const article = articleResponse.data.find(
            (a) => a.id === alert.content_id
          );
          setArticleDetails(article);

          // Charger les détails du média
          if (article?.media_id) {
            const mediaResponse = await mediaService.getById(article.media_id);
            if (mediaResponse.data) {
              setMediaDetails(mediaResponse.data);
            }
          }
        }
      }

      // Charger les détails de modération
      const moderationResponse = await moderationService.getContentModeration(
        alert.content_type,
        alert.content_id
      );
      if (moderationResponse.data) {
        setModerationDetails(moderationResponse.data);
      }
    } catch (error) {
      console.error("Erreur lors du chargement des détails:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les détails",
        variant: "destructive",
      });
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleCloseModal = () => {
    setSelectedAlert(null);
    setArticleDetails(null);
    setModerationDetails(null);
    setMediaDetails(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Analyse des contenus...</p>
        </div>
      </div>
    );
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "high":
        return <Badge variant="destructive">Élevé</Badge>;
      case "medium":
        return (
          <Badge variant="default" className="bg-accent">
            Moyen
          </Badge>
        );
      default:
        return <Badge variant="secondary">Faible</Badge>;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "En cours d'examen":
        return (
          <Badge variant="outline" className="border-warning text-warning">
            En cours
          </Badge>
        );
      case "Signalé au média":
        return (
          <Badge
            variant="outline"
            className="border-destructive text-destructive"
          >
            Signalé
          </Badge>
        );
      case "Résolu":
        return (
          <Badge variant="outline" className="border-success text-success">
            Résolu
          </Badge>
        );
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Vue d'ensemble des alertes */}
      <div className="grid gap-4 md:grid-cols-3">
        {alertTypes.map((alert, index) => (
          <Card
            key={index}
            className="border-l-4"
            style={{ borderLeftColor: alert.color }}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {alert.type}
              </CardTitle>
              <alert.icon className="h-4 w-4" style={{ color: alert.color }} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{alert.count}</div>
              <div className="flex items-center gap-2 mt-2">
                {getSeverityBadge(alert.severity)}
                <p className="text-xs text-muted-foreground">cette semaine</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Évolution temporelle */}
      <Card>
        <CardHeader>
          <CardTitle>Évolution des contenus sensibles</CardTitle>
          <CardDescription>
            Nombre d'alertes détectées par semaine
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weeklyAlerts}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(var(--border))"
              />
              <XAxis dataKey="semaine" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
              />
              <Line
                type="monotone"
                dataKey="haine"
                stroke="hsl(var(--destructive))"
                strokeWidth={2}
                name="Discours de haine"
              />
              <Line
                type="monotone"
                dataKey="desinformation"
                stroke="hsl(var(--warning))"
                strokeWidth={2}
                name="Désinformation"
              />
              <Line
                type="monotone"
                dataKey="toxicite"
                stroke="hsl(var(--accent))"
                strokeWidth={2}
                name="Toxicité"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Liste des alertes récentes */}
      <Card>
        <CardHeader>
          <CardTitle>Alertes récentes</CardTitle>
          <CardDescription>
            Contenus sensibles détectés nécessitant une attention
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentAlerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-start gap-4 p-4 rounded-lg border bg-card hover:bg-accent/5 transition-colors"
              >
                <div className="mt-1">
                  <AlertTriangle className="h-5 w-5 text-warning" />
                </div>
                <div className="flex-1 min-w-0 space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h4 className="font-medium text-sm">{alert.title}</h4>
                      <p className="text-xs text-muted-foreground mt-1">
                        {alert.media} • {alert.date}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="shrink-0"
                      onClick={() => handleViewAlert(alert)}
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      Voir
                    </Button>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant="outline">{alert.type}</Badge>
                    {getSeverityBadge(alert.severity)}
                    {getStatusBadge(alert.status)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Statistiques globales */}
      <Card>
        <CardHeader>
          <CardTitle>Statistiques de modération</CardTitle>
          <CardDescription>
            Vue d'ensemble de l'analyse de contenu
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Total analysé</p>
              <p className="text-2xl font-bold">{recentAlerts.length}</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                Taux de signalement
              </p>
              <p className="text-2xl font-bold">
                {recentAlerts.length > 0 ? "100%" : "0%"}
              </p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Score moyen</p>
              <p className="text-2xl font-bold">
                {recentAlerts.length > 0
                  ? (
                      recentAlerts.reduce(
                        (sum, a) => sum + (a.risk_score || 0),
                        0
                      ) / recentAlerts.length
                    ).toFixed(1)
                  : "0.0"}
                /10
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Modal de détails */}
      <Dialog open={!!selectedAlert} onOpenChange={handleCloseModal}>
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Détails du contenu signalé</DialogTitle>
            <DialogDescription>
              Analyse de modération et contenu complet
            </DialogDescription>
          </DialogHeader>

          {detailsLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Informations générales */}
              {selectedAlert && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{selectedAlert.type}</Badge>
                    {getSeverityBadge(selectedAlert.severity)}
                    <Badge variant="outline" className="ml-auto">
                      {selectedAlert.risk_level}
                    </Badge>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Score de risque:{" "}
                    <span className="font-bold text-destructive">
                      {selectedAlert.risk_score}/10
                    </span>
                  </div>
                </div>
              )}

              {/* Contenu de l'article */}
              {articleDetails && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Article</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-base mb-2">
                        {articleDetails.titre}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        {mediaDetails && (
                          <>
                            <span className="font-medium text-foreground">
                              {mediaDetails.nom}
                            </span>
                            <span>•</span>
                          </>
                        )}
                        <span>
                          Publié le{" "}
                          {new Date(
                            articleDetails.date_publication
                          ).toLocaleDateString("fr-FR")}
                        </span>
                      </div>
                    </div>
                    <div className="prose prose-sm max-w-none">
                      <p className="text-sm whitespace-pre-wrap">
                        {articleDetails.contenu || articleDetails.extrait}
                      </p>
                    </div>
                    {articleDetails.url && (
                      <Button variant="outline" size="sm" asChild>
                        <a
                          href={articleDetails.url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <ExternalLink className="h-4 w-4 mr-2" />
                          Voir l'article original
                        </a>
                      </Button>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Analyse de modération */}
              {moderationDetails && (
                <div className="space-y-4">
                  {/* Toxicité */}
                  {moderationDetails.toxicity?.est_toxique && (
                    <Card className="border-destructive">
                      <CardHeader>
                        <CardTitle className="text-base flex items-center gap-2">
                          <Flame className="h-4 w-4 text-destructive" />
                          Discours de haine détecté
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <span className="font-medium">
                            Score de toxicité:{" "}
                          </span>
                          <span className="text-destructive font-bold">
                            {moderationDetails.toxicity.score_toxicite}/10
                          </span>
                        </div>
                        {moderationDetails.toxicity.contexte && (
                          <div className="text-sm">
                            <Badge
                              variant={
                                moderationDetails.toxicity.contexte ===
                                "informatif"
                                  ? "outline"
                                  : "destructive"
                              }
                            >
                              {moderationDetails.toxicity.contexte ===
                              "informatif"
                                ? "Contexte informatif"
                                : "Contexte promotionnel"}
                            </Badge>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  )}

                  {/* Désinformation */}
                  {moderationDetails.misinformation?.est_desinformation && (
                    <Card className="border-warning">
                      <CardHeader>
                        <CardTitle className="text-base flex items-center gap-2">
                          <Ban className="h-4 w-4 text-warning" />
                          Désinformation détectée
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <span className="font-medium">
                            Score de désinformation:{" "}
                          </span>
                          <span className="text-warning font-bold">
                            {
                              moderationDetails.misinformation
                                .score_desinformation
                            }
                            /10
                          </span>
                        </div>
                        {moderationDetails.misinformation.sources_citees !==
                          undefined && (
                          <div className="text-sm">
                            <Badge
                              variant={
                                moderationDetails.misinformation.sources_citees
                                  ? "outline"
                                  : "destructive"
                              }
                            >
                              {moderationDetails.misinformation.sources_citees
                                ? "✓ Sources citées"
                                : "✗ Aucune source"}
                            </Badge>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  )}

                  {/* Sensibilité */}
                  {moderationDetails.sensitivity?.est_sensible && (
                    <Card className="border-accent">
                      <CardHeader>
                        <CardTitle className="text-base flex items-center gap-2">
                          <AlertTriangle className="h-4 w-4 text-accent" />
                          Contenu sensible
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <span className="font-medium">
                            Score de sensibilité:{" "}
                          </span>
                          <span className="text-accent font-bold">
                            {moderationDetails.sensitivity.score_sensibilite}/10
                          </span>
                        </div>
                        {moderationDetails.sensitivity.traitement && (
                          <div className="text-sm">
                            <Badge
                              variant={
                                moderationDetails.sensitivity.traitement ===
                                "factuel"
                                  ? "outline"
                                  : "destructive"
                              }
                            >
                              {moderationDetails.sensitivity.traitement ===
                              "factuel"
                                ? "Traitement factuel"
                                : "Traitement sensationnaliste"}
                            </Badge>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  )}
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default SensitiveContent;
