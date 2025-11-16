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
import { AlertTriangle, Ban, Flame, Eye, ExternalLink } from "lucide-react";
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
import { articleService } from "@/services/article.service";
import { toast } from "@/hooks/use-toast";

const SensitiveContent = () => {
  const [loading, setLoading] = useState(true);
  const [alertTypes, setAlertTypes] = useState<any[]>([]);
  const [weeklyAlerts, setWeeklyAlerts] = useState<any[]>([]);
  const [recentAlerts, setRecentAlerts] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // Charger les articles récents
      const response = await articleService.getRecent(30, 500);
      if (response.data && !response.error) {
        // Simuler la détection de contenu sensible
        // Dans un vrai système, cela viendrait d'un service d'analyse IA
        const sensitiveKeywords = {
          haine: ["violence", "haine", "discrimination", "attaque"],
          desinformation: ["faux", "mensonge", "rumeur", "non vérifié"],
          toxicite: ["toxique", "offensant", "inapproprié"],
        };

        const alerts: any[] = [];
        const weeklyData: any = {};

        response.data.forEach((article) => {
          const content = (article.titre + " " + article.contenu).toLowerCase();
          let alertType = null;

          // Détecter le type d'alerte (simulation simple)
          if (sensitiveKeywords.haine.some((kw) => content.includes(kw))) {
            alertType = "Discours de haine";
          } else if (
            sensitiveKeywords.desinformation.some((kw) => content.includes(kw))
          ) {
            alertType = "Désinformation";
          } else if (
            sensitiveKeywords.toxicite.some((kw) => content.includes(kw))
          ) {
            alertType = "Contenu toxique";
          }

          if (alertType && alerts.length < 10) {
            const date = new Date(article.date_publication);
            const now = new Date();
            const diffHours = Math.floor(
              (now.getTime() - date.getTime()) / (1000 * 60 * 60)
            );

            let dateStr = "";
            if (diffHours < 24) {
              dateStr = `Il y a ${diffHours} heures`;
            } else if (diffHours < 48) {
              dateStr = "Hier";
            } else {
              dateStr = `Il y a ${Math.floor(diffHours / 24)} jours`;
            }

            alerts.push({
              id: article.id,
              media: "Média", // On pourrait faire un join avec les médias
              type: alertType,
              title: article.titre,
              date: dateStr,
              severity: Math.random() > 0.5 ? "high" : "medium",
              status: ["En cours d'examen", "Signalé au média", "Résolu"][
                Math.floor(Math.random() * 3)
              ],
              url: article.url,
            });
          }
        });

        setRecentAlerts(alerts);

        // Compter les alertes par type
        const typeCounts = {
          "Discours de haine": { count: 0, icon: Flame },
          Désinformation: { count: 0, icon: Ban },
          "Contenu toxique": { count: 0, icon: AlertTriangle },
        };

        alerts.forEach((alert) => {
          if (typeCounts[alert.type as keyof typeof typeCounts]) {
            typeCounts[alert.type as keyof typeof typeCounts].count++;
          }
        });

        const alertTypesData = [
          {
            type: "Discours de haine",
            count: typeCounts["Discours de haine"].count,
            severity: "high",
            color: "hsl(var(--destructive))",
            icon: Flame,
          },
          {
            type: "Désinformation",
            count: typeCounts["Désinformation"].count,
            severity: "high",
            color: "hsl(var(--warning))",
            icon: Ban,
          },
          {
            type: "Contenu toxique",
            count: typeCounts["Contenu toxique"].count,
            severity: "medium",
            color: "hsl(var(--accent))",
            icon: AlertTriangle,
          },
        ];

        setAlertTypes(alertTypesData);

        // Générer des données hebdomadaires simulées
        const weekly = [
          {
            semaine: "S1",
            haine: Math.floor(Math.random() * 5),
            desinformation: Math.floor(Math.random() * 5),
            toxicite: Math.floor(Math.random() * 3),
          },
          {
            semaine: "S2",
            haine: Math.floor(Math.random() * 5),
            desinformation: Math.floor(Math.random() * 5),
            toxicite: Math.floor(Math.random() * 3),
          },
          {
            semaine: "S3",
            haine: Math.floor(Math.random() * 5),
            desinformation: Math.floor(Math.random() * 5),
            toxicite: Math.floor(Math.random() * 3),
          },
          {
            semaine: "S4",
            haine: Math.floor(Math.random() * 5),
            desinformation: Math.floor(Math.random() * 5),
            toxicite: Math.floor(Math.random() * 3),
          },
          {
            semaine: "S5",
            haine: typeCounts["Discours de haine"].count,
            desinformation: typeCounts["Désinformation"].count,
            toxicite: typeCounts["Contenu toxique"].count,
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
                    <Button variant="ghost" size="sm" className="shrink-0">
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

      {/* Statistiques par média */}
      <Card>
        <CardHeader>
          <CardTitle>Répartition par média</CardTitle>
          <CardDescription>
            Nombre de contenus sensibles détectés par source
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart
              data={[
                { media: "Lefaso", count: 4 },
                { media: "FasoPresse", count: 6 },
                { media: "Burkina 24", count: 3 },
                { media: "Sidwaya", count: 5 },
                { media: "L'Obs.", count: 2 },
                { media: "AIB", count: 2 },
                { media: "Le Pays", count: 1 },
              ]}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(var(--border))"
              />
              <XAxis dataKey="media" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
              />
              <Bar
                dataKey="count"
                fill="hsl(var(--destructive))"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default SensitiveContent;
