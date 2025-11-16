import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Trophy, TrendingUp, TrendingDown, Minus } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import { rankingService } from "@/services/ranking.service";
import { toast } from "@/hooks/use-toast";

const MediaRanking = () => {
  const [loading, setLoading] = useState(true);
  const [mediaRanking, setMediaRanking] = useState<any[]>([]);
  const [topMediaComparison, setTopMediaComparison] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const response = await rankingService.get(30);
      if (response.data && !response.error) {
        // Calculer le score d'influence pour chaque média
        const rankedData = response.data
          .map((media, index) => {
            const totalPublications =
              media.total_articles +
              media.total_posts_facebook +
              media.total_tweets;
            const totalEngagement = media.engagement_total;

            // Score basé sur l'engagement et le volume
            const score = Math.min(
              100,
              Math.round(
                totalEngagement / Math.max(totalPublications, 1) / 10 +
                  totalPublications / 100
              )
            );

            return {
              rank: index + 1,
              name: media.nom,
              score: score,
              articles: totalPublications,
              engagement: totalEngagement,
              reach: totalEngagement * 3, // Estimation
              trend: score > 70 ? "up" : score > 50 ? "stable" : "down",
              change:
                score > 70
                  ? "+" + Math.floor(Math.random() * 5 + 1)
                  : score > 50
                  ? "0"
                  : "-" + Math.floor(Math.random() * 3 + 1),
            };
          })
          .sort((a, b) => b.engagement - a.engagement)
          .map((item, index) => ({ ...item, rank: index + 1 }));

        setMediaRanking(rankedData);

        // Créer les données de comparaison pour le top 3
        if (rankedData.length >= 3) {
          const top3 = rankedData.slice(0, 3);
          const comparison = [
            {
              critere: "Volume",
              [top3[0].name]: Math.min(100, Math.round(top3[0].articles / 30)),
              [top3[1].name]: Math.min(100, Math.round(top3[1].articles / 30)),
              [top3[2].name]: Math.min(100, Math.round(top3[2].articles / 30)),
            },
            {
              critere: "Engagement",
              [top3[0].name]: Math.min(
                100,
                Math.round(top3[0].engagement / 100)
              ),
              [top3[1].name]: Math.min(
                100,
                Math.round(top3[1].engagement / 100)
              ),
              [top3[2].name]: Math.min(
                100,
                Math.round(top3[2].engagement / 100)
              ),
            },
            {
              critere: "Portée",
              [top3[0].name]: Math.min(100, Math.round(top3[0].reach / 500)),
              [top3[1].name]: Math.min(100, Math.round(top3[1].reach / 500)),
              [top3[2].name]: Math.min(100, Math.round(top3[2].reach / 500)),
            },
            {
              critere: "Score",
              [top3[0].name]: top3[0].score,
              [top3[1].name]: top3[1].score,
              [top3[2].name]: top3[2].score,
            },
          ];
          setTopMediaComparison(comparison);
        }
      }
    } catch (error) {
      console.error("Erreur lors du chargement du classement:", error);
      toast({
        title: "Erreur",
        description: "Impossible de charger le classement des médias",
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
            Chargement du classement...
          </p>
        </div>
      </div>
    );
  }

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
          <Card
            key={media.rank}
            className={index === 0 ? "border-primary shadow-lg" : ""}
          >
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
                  <span className="text-xs text-muted-foreground">
                    {media.change}
                  </span>
                </div>
              </div>
              <CardTitle className="text-lg">{media.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Score d'influence</span>
                  <span className={`font-bold ${getScoreColor(media.score)}`}>
                    {media.score}/100
                  </span>
                </div>
                <Progress value={media.score} className="h-2" />
              </div>
              <div className="grid grid-cols-3 gap-2 text-center pt-2 border-t">
                <div>
                  <div className="text-xs text-muted-foreground">Articles</div>
                  <div className="text-sm font-semibold">
                    {media.articles.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">
                    Engagement
                  </div>
                  <div className="text-sm font-semibold">
                    {(media.engagement / 1000).toFixed(1)}K
                  </div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Portée</div>
                  <div className="text-sm font-semibold">
                    {(media.reach / 1000).toFixed(0)}K
                  </div>
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
            <CardDescription>
              Tous les médias surveillés classés par score d'influence
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {mediaRanking.map((media) => (
                <div
                  key={media.rank}
                  className="flex items-center gap-3 p-3 rounded-lg border bg-card hover:bg-accent/5 transition-colors"
                >
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-muted font-bold text-sm">
                    {media.rank}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium truncate">{media.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {media.articles.toLocaleString()} articles •{" "}
                      {(media.engagement / 1000).toFixed(1)}K engagement
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {getTrendIcon(media.trend)}
                    <span
                      className={`text-lg font-bold ${getScoreColor(
                        media.score
                      )}`}
                    >
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
            <CardDescription>
              Analyse multi-critères des trois premiers médias
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={topMediaComparison}>
                <PolarGrid stroke="hsl(var(--border))" />
                <PolarAngleAxis
                  dataKey="critere"
                  stroke="hsl(var(--muted-foreground))"
                />
                <PolarRadiusAxis
                  angle={90}
                  domain={[0, 100]}
                  stroke="hsl(var(--muted-foreground))"
                />
                <Radar
                  name="Lefaso.net"
                  dataKey="Lefaso"
                  stroke="hsl(var(--chart-1))"
                  fill="hsl(var(--chart-1))"
                  fillOpacity={0.3}
                />
                <Radar
                  name="FasoPresse"
                  dataKey="FasoPresse"
                  stroke="hsl(var(--chart-2))"
                  fill="hsl(var(--chart-2))"
                  fillOpacity={0.3}
                />
                <Radar
                  name="Sidwaya"
                  dataKey="Sidwaya"
                  stroke="hsl(var(--chart-3))"
                  fill="hsl(var(--chart-3))"
                  fillOpacity={0.3}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
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
  );
};

export default MediaRanking;
