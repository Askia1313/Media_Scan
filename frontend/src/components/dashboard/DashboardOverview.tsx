import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { TrendingUp, FileText, Users, AlertTriangle } from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { statsService } from "@/services/stats.service";
import { classificationService } from "@/services/classification.service";
import { articleService } from "@/services/article.service";
import { toast } from "@/hooks/use-toast";

const DashboardOverview = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);
  const [themeData, setThemeData] = useState<any[]>([]);
  const [weeklyData, setWeeklyData] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // Charger les statistiques globales
      const statsResponse = await statsService.get(30);
      if (statsResponse.data && !statsResponse.error) {
        setStats(statsResponse.data);
      }

      // Charger les statistiques de classification
      const classifResponse = await classificationService.getStats(30);
      if (classifResponse.data && !classifResponse.error) {
        const colors = [
          "hsl(var(--chart-1))",
          "hsl(var(--chart-2))",
          "hsl(var(--chart-3))",
          "hsl(var(--chart-4))",
          "hsl(var(--chart-5))",
          "hsl(210 20% 65%)",
        ];

        const themes = classifResponse.data.map((item, index) => ({
          name: item.categorie,
          value: item.total,
          color: colors[index % colors.length],
        }));
        setThemeData(themes);
      }

      // Charger les articles récents pour le graphique hebdomadaire
      const articlesResponse = await articleService.getRecent(7, 1000);
      if (articlesResponse.data && !articlesResponse.error) {
        // Grouper par jour de la semaine
        const dayNames = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"];
        const grouped = articlesResponse.data.reduce((acc: any, article) => {
          const date = new Date(article.date_publication);
          const dayIndex = date.getDay();
          const dayName = dayNames[dayIndex];

          if (!acc[dayName]) {
            acc[dayName] = { jour: dayName, articles: 0, engagement: 0 };
          }
          acc[dayName].articles++;
          acc[dayName].engagement +=
            (article.vues || 0) + (article.commentaires || 0);
          return acc;
        }, {});

        const weekly = dayNames.map(
          (day) => grouped[day] || { jour: day, articles: 0, engagement: 0 }
        );
        setWeeklyData(weekly);
      }
    } catch (error) {
      console.error("Erreur lors du chargement des données:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger les données du tableau de bord",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const kpiData = [
    {
      label: "Articles collectés",
      value: stats?.total_articles?.toLocaleString() || "0",
      change: "+15%",
      icon: FileText,
      color: "text-primary",
    },
    {
      label: "Médias surveillés",
      value: stats?.total_medias?.toString() || "0",
      change: "100%",
      icon: Users,
      color: "text-accent",
    },
    {
      label: "Catégories",
      value: stats?.total_categories?.toString() || "0",
      change: "-",
      icon: AlertTriangle,
      color: "text-destructive",
    },
    {
      label: "Top média",
      value: stats?.top_media?.nom || "N/A",
      change: "+22%",
      icon: TrendingUp,
      color: "text-success",
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">
            Chargement des données...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* KPIs */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {kpiData.map((kpi, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{kpi.label}</CardTitle>
              <kpi.icon className={`h-4 w-4 ${kpi.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{kpi.value}</div>
              <p
                className={`text-xs ${
                  kpi.change.startsWith("+")
                    ? "text-success"
                    : "text-destructive"
                }`}
              >
                {kpi.change} vs. semaine dernière
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Graphiques principaux */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Volume d'articles */}
        <Card>
          <CardHeader>
            <CardTitle>Volume de publication</CardTitle>
            <CardDescription>Articles collectés cette semaine</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={weeklyData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis dataKey="jour" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                  }}
                />
                <Bar
                  dataKey="articles"
                  fill="hsl(var(--primary))"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Engagement */}
        <Card>
          <CardHeader>
            <CardTitle>Engagement des lecteurs</CardTitle>
            <CardDescription>
              Évolution de l'engagement hebdomadaire
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis dataKey="jour" stroke="hsl(var(--muted-foreground))" />
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
                  dataKey="engagement"
                  stroke="hsl(var(--accent))"
                  strokeWidth={2}
                  dot={{ fill: "hsl(var(--accent))" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Distribution thématique */}
      <Card>
        <CardHeader>
          <CardTitle>Répartition thématique</CardTitle>
          <CardDescription>
            Distribution des contenus par catégorie (30 derniers jours)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6 items-center">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={themeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {themeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-3">
              {themeData.map((theme, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: theme.color }}
                    />
                    <span className="text-sm font-medium">{theme.name}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {theme.value.toLocaleString()} articles
                  </span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardOverview;
