import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {

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

export default function ThematicAnalysis() {
  const themes = [
    {
      name: "Politique",
      icon: Newspaper,
      articles: 3245,
      percentage: 25.3,
      color: "hsl(var(--chart-1))",
      trend: "+12%",
    },
    {
      name: "Sécurité",
      icon: Shield,
      articles: 2890,
      percentage: 22.5,
      color: "hsl(var(--chart-2))",
      trend: "+8%",
    },
    {
      name: "Économie",
      icon: DollarSign,
      articles: 2340,
      percentage: 18.2,
      color: "hsl(var(--chart-3))",
      trend: "+5%",
    },
    {
      name: "Santé",
      icon: Heart,
      articles: 1890,
      percentage: 14.7,
      color: "hsl(var(--chart-4))",
      trend: "+3%",
    },
    {
      name: "Culture",
      icon: Palette,
      articles: 1450,
      percentage: 11.3,
      color: "hsl(var(--chart-5))",
      trend: "+15%",
    },
    {
      name: "Sport",
      icon: Trophy,
      articles: 1032,
      percentage: 8.0,
      color: "hsl(210 20% 65%)",
      trend: "-2%",
    },
  ];

  const weeklyThemes = [
    {
      semaine: "S1",
      Politique: 620,
      Sécurité: 580,
      Économie: 450,
      Santé: 360,
      Culture: 280,
      Sport: 210,
    },
    {
      semaine: "S2",
      Politique: 650,
      Sécurité: 590,
      Économie: 460,
      Santé: 380,
      Culture: 290,
      Sport: 205,
    },
    {
      semaine: "S3",
      Politique: 680,
      Sécurité: 610,
      Économie: 480,
      Santé: 390,
      Culture: 310,
      Sport: 215,
    },
    {
      semaine: "S4",
      Politique: 720,
      Sécurité: 640,
      Économie: 500,
      Santé: 400,
      Culture: 320,
      Sport: 220,
    },
    {
      semaine: "S5",
      Politique: 575,
      Sécurité: 470,
      Économie: 450,
      Santé: 360,
      Culture: 250,
      Sport: 182,
    },
  ];

  const topSubthemes = [
    { theme: "Politique", subtheme: "Élections locales", count: 245 },
    {
      theme: "Politique",
      subtheme: "Réformes institutionnelles",
      count: 198,
    },
    {
      theme: "Sécurité",
      subtheme: "Opérations antiterroristes",
      count: 312,
    },
    { theme: "Sécurité", subtheme: "Sécurité routière", count: 156 },
    { theme: "Économie", subtheme: "Agriculture", count: 289 },
    { theme: "Économie", subtheme: "Secteur minier", count: 234 },
    { theme: "Santé", subtheme: "Campagne de vaccination", count: 178 },
    { theme: "Santé", subtheme: "Infrastructures sanitaires", count: 145 },
  ];
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

      {/* Sous-thèmes populaires */}
      <Card>
        <CardHeader>
          <CardTitle>Sous-thèmes les plus traités</CardTitle>
          <CardDescription>
            Sujets spécifiques par grande catégorie (30 derniers jours)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {themes.slice(0, 4).map((theme, themeIndex) => (
              <div key={themeIndex}>
                <div className="flex items-center gap-2 mb-2">
                  <theme.icon
                    className="h-4 w-4"
                    style={{ color: theme.color }}
                  />
                  <span className="font-semibold text-sm">{theme.name}</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 ml-6">
                  {topSubthemes
                    .filter((item) => item.theme === theme.name)
                    .map((sub, subIndex) => (
                      <div
                        key={subIndex}
                        className="flex items-center justify-between p-2 rounded border bg-card"
                      >
                        <span className="text-sm">{sub.subtheme}</span>
                        <Badge variant="secondary">{sub.count}</Badge>
                      </div>
                    ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
