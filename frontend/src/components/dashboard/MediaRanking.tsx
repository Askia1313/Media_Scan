import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Trophy, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";


export default function MediaRanking() {
const mediaRanking = [
    { 
      rank: 1, 
      name: "Lefaso.net", 
      score: 92, 
      articles: 3240, 
      engagement: 15200, 
      reach: 45000, 
      trend: "up",
      change: "+5"
    },
    { 
      rank: 2, 
      name: "FasoPresse", 
      score: 87, 
      articles: 2890, 
      engagement: 13800, 
      reach: 38000, 
      trend: "up",
      change: "+3"
    },
    { 
      rank: 3, 
      name: "Sidwaya", 
      score: 84, 
      articles: 2650, 
      engagement: 12100, 
      reach: 35000, 
      trend: "stable",
      change: "0"
    },
    { 
      rank: 4, 
      name: "L'Observateur Paalga", 
      score: 79, 
      articles: 2340, 
      engagement: 10500, 
      reach: 28000, 
      trend: "down",
      change: "-2"
    },
    { 
      rank: 5, 
      name: "Burkina 24", 
      score: 76, 
      articles: 2180, 
      engagement: 9800, 
      reach: 26000, 
      trend: "up",
      change: "+1"
    },
    { 
      rank: 6, 
      name: "Le Pays", 
      score: 72, 
      articles: 1950, 
      engagement: 8900, 
      reach: 22000, 
      trend: "stable",
      change: "0"
    },
    { 
      rank: 7, 
      name: "AIB", 
      score: 68, 
      articles: 1780, 
      engagement: 8200, 
      reach: 19000, 
      trend: "up",
      change: "+2"
    },
    { 
      rank: 8, 
      name: "Mutations", 
      score: 64, 
      articles: 1620, 
      engagement: 7400, 
      reach: 16000, 
      trend: "down",
      change: "-1"
    },
  ];

  const topMediaComparison = [
    { critere: "Volume", Lefaso: 90, FasoPresse: 82, Sidwaya: 75 },
    { critere: "Engagement", Lefaso: 88, FasoPresse: 85, Sidwaya: 78 },
    { critere: "Portée", Lefaso: 95, FasoPresse: 80, Sidwaya: 82 },
    { critere: "Régularité", Lefaso: 92, FasoPresse: 88, Sidwaya: 90 },
    { critere: "Diversité", Lefaso: 85, FasoPresse: 90, Sidwaya: 88 },
  ];

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="h-4 w-4 text-success" />;
      case "down":
        return <TrendingDown className="h-4 w-4 text-destructive" />;
      default:
        return <Minus className="h-4 w-4 text-muted-foreground" />;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return "text-success";
    if (score >= 70) return "text-accent";
    return "text-warning";
  };


  return (
     <div className="space-y-6">
      {/* Top 3 Podium */}
      <div className="grid gap-4 md:grid-cols-3">
        {mediaRanking.slice(0, 3).map((media, index) => (
          <Card key={media.rank} className={index === 0 ? "border-primary shadow-lg" : ""}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {index === 0 && <Trophy className="h-5 w-5 text-accent" />}
                  <Badge variant={index === 0 ? "default" : "secondary"}>
                    #{media.rank}
                  </Badge>
                </div>
                <div className="flex items-center gap-1">
                  {getTrendIcon(media.trend)}
                  <span className="text-xs text-muted-foreground">{media.change}</span>
                </div>
              </div>
              <CardTitle className="text-lg">{media.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Score d'influence</span>
                  <span className={`font-bold ${getScoreColor(media.score)}`}>{media.score}/100</span>
                </div>
                <Progress value={media.score} className="h-2" />
              </div>
              <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t">
                <div>
                  <div className="text-xs text-muted-foreground">Articles</div>
                  <div className="text-sm font-semibold">{media.articles.toLocaleString()}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Engagement</div>
                  <div className="text-sm font-semibold">{(media.engagement / 1000).toFixed(1)}K</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Portée</div>
                  <div className="text-sm font-semibold">{(media.reach / 1000).toFixed(0)}K</div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Classement complet et comparaison */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Tableau de classement */}
        <Card>
          <CardHeader>
            <CardTitle>Classement complet</CardTitle>
            <CardDescription>Tous les médias surveillés classés par score d'influence</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {mediaRanking.map((media) => (
                <div key={media.rank} className="flex items-center gap-3 p-3 rounded-lg border bg-card hover:bg-accent/5 transition-colors">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-muted font-bold text-sm">
                    {media.rank}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium truncate">{media.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {media.articles.toLocaleString()} articles • {(media.engagement / 1000).toFixed(1)}K engagement
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {getTrendIcon(media.trend)}
                    <span className={`text-lg font-bold ${getScoreColor(media.score)}`}>
                      {media.score}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Comparaison radar */}
        <Card>
          <CardHeader>
            <CardTitle>Comparaison Top 3</CardTitle>
            <CardDescription>Analyse multi-critères des trois premiers médias</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={topMediaComparison}>
                <PolarGrid stroke="hsl(var(--border))" />
                <PolarAngleAxis dataKey="critere" stroke="hsl(var(--muted-foreground))" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="hsl(var(--muted-foreground))" />
                <Radar name="Lefaso.net" dataKey="Lefaso" stroke="hsl(var(--chart-1))" fill="hsl(var(--chart-1))" fillOpacity={0.3} />
                <Radar name="FasoPresse" dataKey="FasoPresse" stroke="hsl(var(--chart-2))" fill="hsl(var(--chart-2))" fillOpacity={0.3} />
                <Radar name="Sidwaya" dataKey="Sidwaya" stroke="hsl(var(--chart-3))" fill="hsl(var(--chart-3))" fillOpacity={0.3} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: "hsl(var(--card))", 
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)"
                  }} 
                />
              </RadarChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-chart-1" />
                <span>Lefaso.net</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-chart-2" />
                <span>FasoPresse</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-chart-3" />
                <span>Sidwaya</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
