import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import {
  BarChart3,
  FileDown,
  TrendingUp,
  AlertTriangle,
  Radio,
  FileText,
  Settings,
  Play,
} from "lucide-react";
import DashboardOverview from "@/components/dashboard/DashboardOverview";
import MediaRanking from "@/components/dashboard/MediaRanking";
import ThematicAnalysis from "@/components/dashboard/ThematicAnalysis";
import SensitiveContent from "@/components/dashboard/SensitiveContent";
import ScheduleControl from "@/components/dashboard/ScheduleControl";
import MediaManagement from "@/components/dashboard/MediaManagement";
import { toast } from "@/hooks/use-toast";
import ScrapingControl from "@/components/dashboard/ScrapingControl";
import ReportDialog from "@/components/dashboard/ReportDialog";

/*import { testApi } from "@/services/test-api";

testApi();*/

const Index = () => {
  const [activeTab, setActiveTab] = useState("scraping");
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [reportFormat, setReportFormat] = useState<"pdf" | "excel">("pdf");

  const handleExport = (format: "pdf" | "excel") => {
    setReportFormat(format);
    setReportDialogOpen(true);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-primary flex items-center justify-center">
                <Radio className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  CSC Média Monitor
                </h1>
                <p className="text-sm text-muted-foreground">
                  Plateforme de surveillance des médias
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleExport("excel")}
              >
                <FileDown className="h-4 w-4 mr-2" />
                Excel
              </Button>
              <Button
                variant="default"
                size="sm"
                onClick={() => handleExport("pdf")}
              >
                <FileText className="h-4 w-4 mr-2" />
                PDF
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="space-y-6"
        >
          <TabsList className="grid w-full grid-cols-7 lg:w-auto lg:inline-grid">
            <TabsTrigger value="scraping" className="gap-2">
              <Play className="h-4 w-4" />
              <span className="hidden sm:inline">Scraping</span>
            </TabsTrigger>
            <TabsTrigger value="overview" className="gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Vue d'ensemble</span>
            </TabsTrigger>
            <TabsTrigger value="ranking" className="gap-2">
              <TrendingUp className="h-4 w-4" />
              <span className="hidden sm:inline">Classement</span>
            </TabsTrigger>
            <TabsTrigger value="themes" className="gap-2">
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Thématiques</span>
            </TabsTrigger>
            <TabsTrigger value="alerts" className="gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span className="hidden sm:inline">Alertes</span>
            </TabsTrigger>
            <TabsTrigger value="schedule" className="gap-2">
              <Radio className="h-4 w-4" />
              <span className="hidden sm:inline">Contrôle</span>
            </TabsTrigger>
            <TabsTrigger value="media" className="gap-2">
              <Settings className="h-4 w-4" />
              <span className="hidden sm:inline">Médias</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="scraping" className="space-y-6">
            <ScrapingControl />
          </TabsContent>

          <TabsContent value="overview" className="space-y-6">
            <DashboardOverview />
          </TabsContent>

          <TabsContent value="ranking" className="space-y-6">
            <MediaRanking />
          </TabsContent>

          <TabsContent value="themes" className="space-y-6">
            <ThematicAnalysis />
          </TabsContent>

          <TabsContent value="alerts" className="space-y-6">
            <SensitiveContent />
          </TabsContent>

          <TabsContent value="schedule" className="space-y-6">
            <ScheduleControl />
          </TabsContent>

          <TabsContent value="media" className="space-y-6">
            <MediaManagement />
          </TabsContent>
        </Tabs>
      </main>

      {/* Dialogue de génération de rapports */}
      <ReportDialog
        open={reportDialogOpen}
        onOpenChange={setReportDialogOpen}
        format={reportFormat}
      />
    </div>
  );
};

export default Index;
