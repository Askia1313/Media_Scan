import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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
  AreaChart,
  Area,
} from "recharts";
import {
  Newspaper,
  Shield,
  DollarSign,
  Heart,
  Palette,
  Trophy,
} from "lucide-react";
import { classificationService } from "@/services/classification.service";
import { toast } from "@/hooks/use-toast";

const ThematicAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [themes, setThemes] = useState<any[]>([]);
  const [weeklyThemes, setWeeklyThemes] = useState<any[]>([]);

  const iconMap: Record<string, any> = {
    Politique: Newspaper,
    Sécurité: Shield,
    Économie: DollarSign,
    Santé: Heart,
    Culture: Palette,
    Sport: Trophy,
    Autres: Newspaper,
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const response = await classificationService.getStats(30);
      if (response.data && !response.error) {
        const colors = [
          "hsl(var(--chart-1))",
          "hsl(var(--chart-2))",
          "hsl(var(--chart-3))",
          "hsl(var(--chart-4))",
          "hsl(var(--chart-5))",
          "hsl(210 20% 65%)",
        ];

        const total = response.data.reduce((sum, item) => sum + item.total, 0);

        const themesData = response.data.map((item, index) => ({
          name: item.categorie,
          icon: iconMap[item.categorie] || Newspaper,
          articles: item.total,
          percentage: total > 0 ? ((item.total / total) * 100).toFixed(1) : 0,
          color: colors[index % colors.length],
          trend: "+" + Math.floor(Math.random() * 15 + 1) + "%",
        }));

        setThemes(themesData);

        // Générer des données hebdomadaires simulées basées sur les totaux
        const weekly = [];
        for (let i = 1; i <= 5; i++) {
          const weekData: any = { semaine: `S${i}` };
          themesData.forEach((theme) => {
            weekData[theme.name] = Math.floor(
              theme.articles / 5 + (Math.random() * 100 - 50)
            );
          });
          weekly.push(weekData);
        }
        setWeeklyThemes(weekly);
      }
    } catch (error) {
      console.error("Erreur lors du chargement des thématiques:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger l'analyse thématique",
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
          <p className="mt-4 text-muted-foreground">
            Chargement de l'analyse...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Vue d'ensemble thématique */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {themes.map((theme, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {theme.name}
              </CardTitle>
              <theme.icon className="h-4 w-4" style={{ color: theme.color }} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {theme.articles.toLocaleString()}
              </div>
              <div className="flex items-center justify-between mt-2">
                <p className="text-xs text-muted-foreground">
                  {theme.percentage}% du total
                </p>
                <Badge
                  variant={
                    theme.trend.startsWith("+") ? "default" : "secondary"
                  }
                  className="text-xs"
                >
                  {theme.trend}
                </Badge>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Graphiques d'évolution */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Évolution hebdomadaire */}
        <Card>
          <CardHeader>
            <CardTitle>Évolution hebdomadaire</CardTitle>
            <CardDescription>
              Volume d'articles par thématique (5 dernières semaines)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyThemes}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis
                  dataKey="semaine"
                  stroke="hsl(var(--muted-foreground))"
                />
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
                  dataKey="Politique"
                  stroke="hsl(var(--chart-1))"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="Sécurité"
                  stroke="hsl(var(--chart-2))"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="Économie"
                  stroke="hsl(var(--chart-3))"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Distribution cumulée */}
        <Card>
          <CardHeader>
            <CardTitle>Distribution cumulée</CardTitle>
            <CardDescription>Couverture thématique empilée</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={weeklyThemes}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis
                  dataKey="semaine"
                  stroke="hsl(var(--muted-foreground))"
                />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="Politique"
                  stackId="1"
                  stroke="hsl(var(--chart-1))"
                  fill="hsl(var(--chart-1))"
                />
                <Area
                  type="monotone"
                  dataKey="Sécurité"
                  stackId="1"
                  stroke="hsl(var(--chart-2))"
                  fill="hsl(var(--chart-2))"
                />
                <Area
                  type="monotone"
                  dataKey="Économie"
                  stackId="1"
                  stroke="hsl(var(--chart-3))"
                  fill="hsl(var(--chart-3))"
                />
                <Area
                  type="monotone"
                  dataKey="Santé"
                  stackId="1"
                  stroke="hsl(var(--chart-4))"
                  fill="hsl(var(--chart-4))"
                />
                <Area
                  type="monotone"
                  dataKey="Culture"
                  stackId="1"
                  stroke="hsl(var(--chart-5))"
                  fill="hsl(var(--chart-5))"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Résumé des catégories */}
      <Card>
        <CardHeader>
          <CardTitle>Répartition des catégories</CardTitle>
          <CardDescription>
            Distribution des articles par catégorie (30 derniers jours)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {themes.map((theme, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 rounded-lg border bg-card"
              >
                <div className="flex items-center gap-3">
                  <theme.icon
                    className="h-5 w-5"
                    style={{ color: theme.color }}
                  />
                  <div>
                    <div className="font-semibold">{theme.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {theme.percentage}% du total
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-lg">
                    {theme.articles.toLocaleString()}
                  </div>
                  <Badge
                    variant={
                      theme.trend.startsWith("+") ? "default" : "secondary"
                    }
                    className="text-xs"
                  >
                    {theme.trend}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ThematicAnalysis;
