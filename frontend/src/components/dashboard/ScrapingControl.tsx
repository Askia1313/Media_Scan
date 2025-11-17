import { useState } from "react";
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

interface ScrapingTask {
  id: string;
  type: "html" | "rss" | "twitter" | "facebook";
  status: "running" | "completed" | "failed";
  startedAt: string;
  itemsCollected: number;
}

const ScrapingControl = () => {
  const [tasks, setTasks] = useState<ScrapingTask[]>([
    {
      id: "1",
      type: "html",
      status: "completed",
      startedAt: "2024-03-15 10:30",
      itemsCollected: 45,
    },
    {
      id: "2",
      type: "rss",
      status: "completed",
      startedAt: "2024-03-15 14:20",
      itemsCollected: 32,
    },
  ]);

  const [automation, setAutomation] = useState({
    enabled: false,
    frequency: "daily",
  });

  const handleLaunchScraping = (
    type: "html" | "rss" | "twitter" | "facebook"
  ) => {
    const newTask: ScrapingTask = {
      id: Date.now().toString(),
      type,
      status: "running",
      startedAt: new Date().toLocaleString("fr-FR"),
      itemsCollected: 0,
    };

    setTasks([newTask, ...tasks]);

    toast({
      title: "Scraping lancé",
      description: `Le scraping ${getTypeLabel(type)} a été lancé avec succès.`,
    });

    // Simulation: compléter après 3 secondes
    setTimeout(() => {
      setTasks((prev) =>
        prev.map((task) =>
          task.id === newTask.id
            ? {
                ...task,
                status: "completed",
                itemsCollected: Math.floor(Math.random() * 50) + 10,
              }
            : task
        )
      );

      toast({
        title: "Scraping terminé",
        description: `Le scraping ${getTypeLabel(type)} est terminé.`,
      });
    }, 3000);
  };

  const handleAutomationToggle = (enabled: boolean) => {
    setAutomation({ ...automation, enabled });

    toast({
      title: enabled ? "Automatisation activée" : "Automatisation désactivée",
      description: enabled
        ? `Le scraping sera exécuté automatiquement toutes les ${getFrequencyLabel(
            automation.frequency
          )}.`
        : "Le scraping automatique a été désactivé.",
    });
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "html":
        return "HTML";
      case "rss":
        return "RSS";
      case "twitter":
        return "Twitter";
      case "facebook":
        return "Facebook";
      default:
        return type;
    }
  };

  const getFrequencyLabel = (frequency: string) => {
    switch (frequency) {
      case "hourly":
        return "heures";
      case "daily":
        return "jours";
      case "weekly":
        return "semaines";
      default:
        return frequency;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "html":
        return <Globe className="h-4 w-4" />;
      case "rss":
        return <Rss className="h-4 w-4" />;
      case "twitter":
        return <Twitter className="h-4 w-4" />;
      case "facebook":
        return <Facebook className="h-4 w-4" />;
      default:
        return null;
    }
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
            Lancer un scraping manuel
          </CardTitle>
          <CardDescription>
            Choisissez le type de scraping à exécuter immédiatement
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Button
              variant="outline"
              className="h-24 flex flex-col gap-2"
              onClick={() => handleLaunchScraping("html")}
            >
              <Globe className="h-8 w-8" />
              <span>Scraping HTML</span>
            </Button>

            <Button
              variant="outline"
              className="h-24 flex flex-col gap-2"
              onClick={() => handleLaunchScraping("rss")}
            >
              <Rss className="h-8 w-8" />
              <span>Scraping RSS</span>
            </Button>

            <Button
              variant="outline"
              className="h-24 flex flex-col gap-2"
              onClick={() => handleLaunchScraping("twitter")}
            >
              <Twitter className="h-8 w-8" />
              <span>Scraping Twitter</span>
            </Button>

            <Button
              variant="outline"
              className="h-24 flex flex-col gap-2"
              onClick={() => handleLaunchScraping("facebook")}
            >
              <Facebook className="h-8 w-8" />
              <span>Scraping Facebook</span>
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
              checked={automation.enabled}
              onCheckedChange={handleAutomationToggle}
            />
          </div>

          {automation.enabled && (
            <div className="space-y-2 pt-2 border-t">
              <Label htmlFor="frequency">Fréquence d'exécution</Label>
              <Select
                value={automation.frequency}
                onValueChange={(value) =>
                  setAutomation({ ...automation, frequency: value })
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
              <p className="text-sm text-muted-foreground">
                Prochaine exécution :{" "}
                {new Date(Date.now() + 3600000).toLocaleString("fr-FR")}
              </p>
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
                <TableHead>Type</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead>Date de lancement</TableHead>
                <TableHead className="text-right">Articles collectés</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      {getTypeIcon(task.type)}
                      <span className="font-medium">
                        {getTypeLabel(task.type)}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>{getStatusBadge(task.status)}</TableCell>
                  <TableCell className="text-muted-foreground">
                    {task.startedAt}
                  </TableCell>
                  <TableCell className="text-right font-medium">
                    {task.status === "running" ? "-" : task.itemsCollected}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default ScrapingControl;
