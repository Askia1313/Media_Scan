import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { FileDown, FileText, Loader2 } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import {
  reportSimpleService as reportService,
  ReportPeriod,
} from "@/services/report-simple.service";

interface ReportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  format: "pdf" | "excel";
}

const ReportDialog = ({ open, onOpenChange, format }: ReportDialogProps) => {
  const [period, setPeriod] = useState<ReportPeriod>("daily");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);

    try {
      if (format === "pdf") {
        await reportService.generatePDF(period);
      } else {
        await reportService.generateExcel(period);
      }

      toast({
        title: "Rapport généré",
        description: `Le rapport ${
          period === "daily" ? "journalier" : "hebdomadaire"
        } a été téléchargé au format ${format.toUpperCase()}.`,
      });

      onOpenChange(false);
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Impossible de générer le rapport. Veuillez réessayer.",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {format === "pdf" ? (
              <FileText className="h-5 w-5" />
            ) : (
              <FileDown className="h-5 w-5" />
            )}
            Générer un rapport {format.toUpperCase()}
          </DialogTitle>
          <DialogDescription>
            Sélectionnez la période du rapport à générer
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <RadioGroup
            value={period}
            onValueChange={(value) => setPeriod(value as ReportPeriod)}
          >
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="daily" id="daily" />
              <Label htmlFor="daily" className="cursor-pointer">
                <div className="font-medium">Rapport Journalier</div>
                <div className="text-sm text-muted-foreground">
                  Données des dernières 24 heures
                </div>
              </Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="weekly" id="weekly" />
              <Label htmlFor="weekly" className="cursor-pointer">
                <div className="font-medium">Rapport Hebdomadaire</div>
                <div className="text-sm text-muted-foreground">
                  Données des 7 derniers jours
                </div>
              </Label>
            </div>
          </RadioGroup>

          <div className="rounded-lg bg-muted p-4 text-sm">
            <p className="font-medium mb-2">Le rapport inclura :</p>
            <ul className="list-disc list-inside space-y-1 text-muted-foreground">
              <li>Nombre total de médias (conformes/non conformes)</li>
              <li>Nombre de scrapings lancés</li>
              <li>Articles collectés et articles problématiques</li>
              <li>Taux de conformité des médias et articles</li>
              <li>Top 5 médias les plus actifs</li>
              <li>Classement complet par engagement</li>
              <li>Proportion détaillée de chaque catégorie</li>
              <li>Liste des articles récents</li>
            </ul>
            <p className="text-xs text-muted-foreground mt-2">
              📊 Basé sur les données réellement collectées dans la période
              sélectionnée
            </p>
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isGenerating}
          >
            Annuler
          </Button>
          <Button onClick={handleGenerate} disabled={isGenerating}>
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Génération...
              </>
            ) : (
              <>
                {format === "pdf" ? (
                  <FileText className="mr-2 h-4 w-4" />
                ) : (
                  <FileDown className="mr-2 h-4 w-4" />
                )}
                Générer
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ReportDialog;
