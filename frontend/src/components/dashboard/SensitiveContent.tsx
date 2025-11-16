import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Ban, Flame, Eye } from "lucide-react";
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

export default function SensitiveContent() {
  const alertTypes = [
    {
      type: "Discours de haine",
      count: 8,
      severity: "high",
      color: "hsl(var(--destructive))",
      icon: Flame,
    },
    {
      type: "Désinformation",
      count: 12,
      severity: "high",
      color: "hsl(var(--warning))",
      icon: Ban,
    },
    {
      type: "Contenu toxique",
      count: 3,
      severity: "medium",
      color: "hsl(var(--accent))",
      icon: AlertTriangle,
    },
  ];

  const weeklyAlerts = [
    { semaine: "S1", haine: 2, desinformation: 3, toxicite: 1 },
    { semaine: "S2", haine: 3, desinformation: 4, toxicite: 2 },
    { semaine: "S3", haine: 1, desinformation: 2, toxicite: 0 },
    { semaine: "S4", haine: 1, desinformation: 2, toxicite: 0 },
    { semaine: "S5", haine: 1, desinformation: 1, toxicite: 0 },
  ];

  const recentAlerts = [
    {
      id: 1,
      media: "Lefaso.net",
      type: "Désinformation",
      title: "Information non vérifiée sur les subventions agricoles",
      date: "Il y a 2 heures",
      severity: "high",
      status: "En cours d'examen",
      url: "#",
    },
    {
      id: 2,
      media: "FasoPresse",
      type: "Discours de haine",
      title: "Commentaire incitant à la violence communautaire",
      date: "Il y a 5 heures",
      severity: "high",
      status: "Signalé au média",
      url: "#",
    },
    {
      id: 3,
      media: "Burkina 24",
      type: "Désinformation",
      title: "Chiffres erronés sur la situation sécuritaire",
      date: "Hier",
      severity: "medium",
      status: "En cours d'examen",
      url: "#",
    },
    {
      id: 4,
      media: "L'Observateur",
      type: "Contenu toxique",
      title: "Propos discriminatoires dans un article d'opinion",
      date: "Hier",
      severity: "medium",
      status: "Résolu",
      url: "#",
    },
    {
      id: 5,
      media: "Sidwaya",
      type: "Désinformation",
      title: "Fausse attribution de citation à un ministre",
      date: "Il y a 2 jours",
      severity: "high",
      status: "Signalé au média",
      url: "#",
    },
  ];

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
}
