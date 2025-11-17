import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Play,
  Globe,
  Rss,
  Facebook,
  Twitter,
  Clock,
  CheckCircle2,
  XCircle,
  Loader2,
} from "lucide-react";
import { toast } from "@/hooks/use-toast";
import {
  useScrapeAll,
  useScrapingSchedule,
  useUpdateScrapingSchedule,
  useToggleScrapingSchedule,
  useScrapingHistory,
} from "@/hooks/useScraping";

const ScrapingControl = () => {
  const scrapeAllMutation = useScrapeAll();
  const { data: schedule } = useScrapingSchedule();
  const updateScheduleMutation = useUpdateScrapingSchedule();
  const toggleScheduleMutation = useToggleScrapingSchedule();

  // Récupération de l'historique avec polling automatique toutes les 5 secondes
  const { data: history } = useScrapingHistory({ limit: 10 });

  const handleLaunchScraping = () => {
    // Empêcher les doubles clics
    if (scrapeAllMutation.isPending) {
      return;
    }

    scrapeAllMutation.mutate(
      { days: 7 },
      {
        onSuccess: (result) => {
          toast({
            title: "Scraping terminé",
            description: `${
              result?.total_articles || 0
            } articles collectés avec succès.`,
          });
        },
      }
    );
  };

  const handleAutomationToggle = (enabled: boolean) => {
    toggleScheduleMutation.mutate(enabled);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "running":
        return (
          <Badge variant="outline" className="gap-1">
            <Loader2 className="h-3 w-3 animate-spin" />
            En cours
          </Badge>
        );
      case "completed":
        return (
          <Badge
            variant="outline"
            className="gap-1 border-success text-success"
          >
            <CheckCircle2 className="h-3 w-3" />
            Terminé
          </Badge>
        );
      case "failed":
        return (
          <Badge variant="destructive" className="gap-1">
            <XCircle className="h-3 w-3" />
            Échoué
          </Badge>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Lancement manuel */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Play className="h-5 w-5" />
            Lancer la collecte des données
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1  gap-4">
            <Button
              variant="outline"
              className="h-24 flex flex-col gap-2"
              onClick={handleLaunchScraping}
              disabled={scrapeAllMutation.isPending}
            >
              {scrapeAllMutation.isPending ? (
                <>
                  <Loader2 className="h-16 w-16 animate-spin" />
                  <span>Collecte en cours...</span>
                </>
              ) : (
                <>
                  <Play className="h-16 w-16" />
                  <span>Lancer la collecte des données</span>
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Automatisation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Automatisation du scraping
          </CardTitle>
          <CardDescription>
            Configurez l'exécution automatique périodique des scraping
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label htmlFor="automation-switch" className="text-base">
                Activer l'automatisation
              </Label>
              <p className="text-sm text-muted-foreground">
                Le scraping sera exécuté automatiquement selon la fréquence
                choisie
              </p>
            </div>
            <Switch
              id="automation-switch"
              checked={schedule?.enabled || false}
              onCheckedChange={handleAutomationToggle}
            />
          </div>

          {schedule?.enabled && (
            <div className="space-y-2 pt-2 border-t">
              <Label htmlFor="frequency">Fréquence d'exécution</Label>
              <Select
                value={schedule.frequency}
                onValueChange={(value) =>
                  updateScheduleMutation.mutate({
                    ...schedule,
                    frequency: value as "hourly" | "daily" | "weekly",
                  })
                }
              >
                <SelectTrigger id="frequency">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="hourly">Toutes les heures</SelectItem>
                  <SelectItem value="daily">Tous les jours</SelectItem>
                  <SelectItem value="weekly">Toutes les semaines</SelectItem>
                </SelectContent>
              </Select>
              {schedule.next_run && (
                <p className="text-sm text-muted-foreground">
                  Prochaine exécution :{" "}
                  {new Date(schedule.next_run).toLocaleString("fr-FR")}
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
      {/* Historique */}
      <Card>
        <CardHeader>
          <CardTitle>Historique des scraping</CardTitle>
          <CardDescription>
            Résultats des derniers scraping exécutés
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date de lancement</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Articles collectés</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {/* Afficher l'historique de l'API */}
              {history?.tasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell className="text-muted-foreground">
                    {new Date(task.started_at).toLocaleString("fr-FR")}
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={task.type === "manual" ? "outline" : "secondary"}
                    >
                      {task.type === "manual" ? "Manuel" : "Automatique"}
                    </Badge>
                  </TableCell>
                  <TableCell>{getStatusBadge(task.status)}</TableCell>
                  <TableCell className="text-right font-medium">
                    {task.status === "running" ? "-" : task.total_articles}
                  </TableCell>
                </TableRow>
              ))}
              {!history?.tasks.length && (
                <TableRow>
                  <TableCell
                    colSpan={4}
                    className="text-center text-muted-foreground"
                  >
                    Aucun historique de scraping disponible
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default ScrapingControl;
