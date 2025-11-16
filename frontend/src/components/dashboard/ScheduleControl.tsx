import { useMemo } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  Calendar,
  Activity,
} from "lucide-react";
import { useGlobalAudience } from "@/hooks/useAudience";

const ScheduleControl = () => {
  // Use TanStack Query hook
  const { data: audienceData, isLoading: loading } = useGlobalAudience(90);

  // Transform data to compliance metrics
  const mediaCompliance = useMemo(() => {
    if (!audienceData) return [];

    return audienceData.map((media) => {
      const totalPubs = media.total_publications;
      const requiredDays = 90;
      const activeDays = media.web?.jours_avec_publication || 0;
      const publicationsPerWeek = Math.round((totalPubs / 90) * 7);
      const expectedPublications = 40;

      // Calculer le score de conformité
      const dayCompliance = (activeDays / requiredDays) * 100;
      const pubCompliance = Math.min(
        100,
        (publicationsPerWeek / expectedPublications) * 100
      );
      const complianceScore = Math.round((dayCompliance + pubCompliance) / 2);

      // Déterminer le statut
      let status = "compliant";
      if (complianceScore < 70) {
        status = "alert";
      } else if (complianceScore < 90) {
        status = "warning";
      }

      // Formater la dernière publication
      const daysSince = media.web?.jours_depuis_derniere_pub || 0;
      let lastPub = "Jamais";
      if (daysSince === 0) {
        lastPub = "Aujourd'hui";
      } else if (daysSince === 1) {
        lastPub = "Il y a 1 jour";
      } else if (daysSince < 7) {
        lastPub = `Il y a ${daysSince} jours`;
      } else {
        lastPub = `Il y a ${Math.floor(daysSince / 7)} semaines`;
      }

      return {
        name: media.nom,
        status,
        activeDays,
        requiredDays,
        lastPublication: lastPub,
        publicationsPerWeek,
        expectedPublications,
        compliance: complianceScore,
      };
    });
  }, [audienceData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">
            Chargement du contrôle...
          </p>
        </div>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "compliant":
        return (
          <Badge variant="outline" className="border-success text-success">
            <CheckCircle2 className="h-3 w-3 mr-1" />
            Conforme
          </Badge>
        );
      case "warning":
        return (
          <Badge variant="outline" className="border-warning text-warning">
            <AlertCircle className="h-3 w-3 mr-1" />
            Attention
          </Badge>
        );
      case "alert":
        return (
          <Badge
            variant="outline"
            className="border-destructive text-destructive"
          >
            <XCircle className="h-3 w-3 mr-1" />
            Non conforme
          </Badge>
        );
      default:
        return null;
    }
  };

  const getComplianceColor = (compliance: number) => {
    if (compliance >= 90) return "text-success";
    if (compliance >= 70) return "text-warning";
    return "text-destructive";
  };

  const complianceSummary = {
    compliant: mediaCompliance.filter((m) => m.status === "compliant").length,
    warning: mediaCompliance.filter((m) => m.status === "warning").length,
    alert: mediaCompliance.filter((m) => m.status === "alert").length,
  };

  return (
    <div className="space-y-6">
      {/* Résumé de conformité */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-l-4 border-l-success">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conformes</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {complianceSummary.compliant}
            </div>
            <p className="text-xs text-muted-foreground">
              médias respectant les obligations
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-warning">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">À surveiller</CardTitle>
            <AlertCircle className="h-4 w-4 text-warning" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {complianceSummary.warning}
            </div>
            <p className="text-xs text-muted-foreground">
              médias nécessitant une attention
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-destructive">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Non conformes</CardTitle>
            <XCircle className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{complianceSummary.alert}</div>
            <p className="text-xs text-muted-foreground">
              médias en situation d'alerte
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tableau détaillé de conformité */}
      <Card>
        <CardHeader>
          <CardTitle>Contrôle des grilles de programmes</CardTitle>
          <CardDescription>
            Respect des obligations réglementaires par média
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {mediaCompliance.map((media, index) => (
              <div
                key={index}
                className="p-4 rounded-lg border bg-card space-y-3"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <h4 className="font-semibold">{media.name}</h4>
                    {getStatusBadge(media.status)}
                  </div>
                  <div
                    className={`text-2xl font-bold ${getComplianceColor(
                      media.compliance
                    )}`}
                  >
                    {media.compliance}%
                  </div>
                </div>

                <Progress value={media.compliance} className="h-2" />

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 text-sm">
                  <div>
                    <div className="flex items-center gap-1 text-muted-foreground mb-1">
                      <Calendar className="h-3 w-3" />
                      <span>Activité</span>
                    </div>
                    <div className="font-semibold">
                      {media.activeDays}/{media.requiredDays} jours
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center gap-1 text-muted-foreground mb-1">
                      <Activity className="h-3 w-3" />
                      <span>Publications/sem.</span>
                    </div>
                    <div className="font-semibold">
                      {media.publicationsPerWeek}/{media.expectedPublications}
                    </div>
                  </div>

                  <div>
                    <div className="text-muted-foreground mb-1">
                      Dernière publication
                    </div>
                    <div className="font-semibold">{media.lastPublication}</div>
                  </div>

                  <div>
                    <div className="text-muted-foreground mb-1">Statut</div>
                    <div className="font-semibold">
                      {media.status === "compliant" && "Régulier"}
                      {media.status === "warning" && "Irrégularités"}
                      {media.status === "alert" && "Risque cessation"}
                    </div>
                  </div>
                </div>

                {media.status !== "compliant" && (
                  <div className="pt-2 border-t">
                    <p className="text-sm text-muted-foreground">
                      {media.status === "warning" &&
                        "⚠️ Activité en baisse. Vérifier la régularité des publications."}
                      {media.status === "alert" &&
                        "🚨 Inactivité prolongée détectée. Risque de cessation imminente."}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Alertes d'inactivité */}
      <Card>
        <CardHeader>
          <CardTitle>Alertes d'inactivité</CardTitle>
          <CardDescription>
            Médias nécessitant une intervention du CSC
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {mediaCompliance
              .filter((m) => m.status === "alert")
              .map((media, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 rounded-lg border border-destructive/50 bg-destructive/5"
                >
                  <XCircle className="h-5 w-5 text-destructive mt-0.5" />
                  <div className="flex-1">
                    <h5 className="font-semibold text-sm">{media.name}</h5>
                    <p className="text-sm text-muted-foreground mt-1">
                      Seulement {media.activeDays} jours d'activité sur 90
                      requis. Dernière publication : {media.lastPublication}.
                    </p>
                    <p className="text-sm font-medium text-destructive mt-2">
                      Action recommandée : Notification officielle au média
                    </p>
                  </div>
                </div>
              ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ScheduleControl;
