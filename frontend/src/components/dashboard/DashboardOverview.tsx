import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { TrendingUp, AlertTriangle, Users, FileText } from 'lucide-react';

export default function DashboardOverview() {
     // Données simulées
  const kpiData = [
    { label: "Articles collectés", value: "12,847", change: "+15%", icon: FileText, color: "text-primary" },
    { label: "Médias surveillés", value: "8", change: "100%", icon: Users, color: "text-accent" },
    { label: "Contenus sensibles", value: "23", change: "-5%", icon: AlertTriangle, color: "text-destructive" },
    { label: "Engagement total", value: "45.2K", change: "+22%", icon: TrendingUp, color: "text-success" },
  ];

  const weeklyData = [
    { jour: "Lun", articles: 1840, engagement: 6200 },
    { jour: "Mar", articles: 1950, engagement: 6800 },
    { jour: "Mer", articles: 2100, engagement: 7200 },
    { jour: "Jeu", articles: 1890, engagement: 6500 },
    { jour: "Ven", articles: 2150, engagement: 7500 },
    { jour: "Sam", articles: 1650, engagement: 5800 },
    { jour: "Dim", articles: 1267, engagement: 4900 },
  ];

  const themeData = [
    { name: "Politique", value: 3245, color: "hsl(var(--chart-1))" },
    { name: "Sécurité", value: 2890, color: "hsl(var(--chart-2))" },
    { name: "Économie", value: 2340, color: "hsl(var(--chart-3))" },
    { name: "Santé", value: 1890, color: "hsl(var(--chart-4))" },
    { name: "Culture", value: 1450, color: "hsl(var(--chart-5))" },
    { name: "Sport", value: 1032, color: "hsl(210 20% 65%)" },
  ];

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
              <p className={`text-xs ${kpi.change.startsWith('+') ? 'text-success' : 'text-destructive'}`}>
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
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="jour" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: "hsl(var(--card))", 
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)"
                  }} 
                />
                <Bar dataKey="articles" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Engagement */}
        <Card>
          <CardHeader>
            <CardTitle>Engagement des lecteurs</CardTitle>
            <CardDescription>Évolution de l'engagement hebdomadaire</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="jour" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: "hsl(var(--card))", 
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)"
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
          <CardDescription>Distribution des contenus par catégorie (30 derniers jours)</CardDescription>
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
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
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
                    borderRadius: "var(--radius)"
                  }} 
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-3">
              {themeData.map((theme, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: theme.color }} />
                    <span className="text-sm font-medium">{theme.name}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">{theme.value.toLocaleString()} articles</span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
