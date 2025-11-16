import { useMemo } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
import { Badge } from "@/components/ui/badge";
import { Plus, Trash2, Globe, Facebook, Twitter } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { toast } from "@/hooks/use-toast";
import { useMedia } from "@/hooks/useMedia";

const mediaSchema = z.object({
  name: z
    .string()
    .min(2, "Le nom doit contenir au moins 2 caractères")
    .max(100),
  type: z.enum(["web", "facebook", "twitter"], {
    required_error: "Veuillez sélectionner un type",
  }),
  url: z.string().min(1, "Ce champ est requis").max(500),
});

type MediaFormData = z.infer<typeof mediaSchema>;

interface Media {
  id: string;
  name: string;
  type: "web" | "facebook" | "twitter";
  url: string;
  addedAt: string;
}

const MediaManagement = () => {
  // Use TanStack Query hook
  const { data: mediaData, isLoading: loading } = useMedia();

  // Transform media data
  const medias = useMemo(() => {
    if (!mediaData) return [];

    return mediaData.map((media) => {
      let type: "web" | "facebook" | "twitter" = "web";
      let url = media.url;

      if (media.facebook_page) {
        type = "facebook";
        url = media.facebook_page;
      } else if (media.twitter_account) {
        type = "twitter";
        url = media.twitter_account;
      }

      return {
        id: media.id.toString(),
        name: media.nom,
        type,
        url,
        addedAt: new Date(media.created_at).toISOString().split("T")[0],
      };
    });
  }, [mediaData]);

  const form = useForm<MediaFormData>({
    resolver: zodResolver(mediaSchema),
    defaultValues: {
      name: "",
      type: "web",
      url: "",
    },
  });

  const onSubmit = (data: MediaFormData) => {
    // TODO: Implement mutation hook for adding media
    // For now, this is client-side only and won't persist
    toast({
      title: "Média ajouté (local)",
      description: `${data.name} - Cette fonctionnalité nécessite une mutation API.`,
    });
    form.reset();
  };

  const handleDelete = (id: string) => {
    // TODO: Implement mutation hook for deleting media
    // For now, this is client-side only and won't persist
    const media = medias.find((m) => m.id === id);
    toast({
      title: "Suppression (local)",
      description: `${media?.name} - Cette fonctionnalité nécessite une mutation API.`,
      variant: "destructive",
    });
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "web":
        return <Globe className="h-4 w-4" />;
      case "facebook":
        return <Facebook className="h-4 w-4" />;
      case "twitter":
        return <Twitter className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "web":
        return "Site Web";
      case "facebook":
        return "Facebook";
      case "twitter":
        return "Twitter";
      default:
        return type;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Chargement des médias...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Formulaire d'ajout */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="h-5 w-5" />
            Ajouter un média à surveiller
          </CardTitle>
          <CardDescription>
            Ajoutez des pages web, des comptes Facebook ou Twitter à surveiller
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nom du média</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: Lefaso.net" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="type"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Type</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner le type" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="web">
                            <div className="flex items-center gap-2">
                              <Globe className="h-4 w-4" />
                              Site Web
                            </div>
                          </SelectItem>
                          <SelectItem value="facebook">
                            <div className="flex items-center gap-2">
                              <Facebook className="h-4 w-4" />
                              Facebook
                            </div>
                          </SelectItem>
                          <SelectItem value="twitter">
                            <div className="flex items-center gap-2">
                              <Twitter className="h-4 w-4" />
                              Twitter
                            </div>
                          </SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="url"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>URL / Nom d'utilisateur</FormLabel>
                      <FormControl>
                        <Input
                          placeholder={
                            form.watch("type") === "web"
                              ? "https://exemple.com"
                              : form.watch("type") === "twitter"
                              ? "@username"
                              : "username"
                          }
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button type="submit" className="w-full md:w-auto">
                <Plus className="h-4 w-4 mr-2" />
                Ajouter le média
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>

      {/* Liste des médias */}
      <Card>
        <CardHeader>
          <CardTitle>Médias surveillés ({medias.length})</CardTitle>
          <CardDescription>
            Liste des médias actuellement sous surveillance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nom</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>URL / Utilisateur</TableHead>
                <TableHead>Date d'ajout</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {medias.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center text-muted-foreground py-8"
                  >
                    Aucun média ajouté. Utilisez le formulaire ci-dessus pour en
                    ajouter.
                  </TableCell>
                </TableRow>
              ) : (
                medias.map((media) => (
                  <TableRow key={media.id}>
                    <TableCell className="font-medium">{media.name}</TableCell>
                    <TableCell>
                      <Badge variant="outline" className="gap-1">
                        {getIcon(media.type)}
                        {getTypeLabel(media.type)}
                      </Badge>
                    </TableCell>
                    <TableCell className="font-mono text-sm text-muted-foreground">
                      {media.url}
                    </TableCell>
                    <TableCell>
                      {new Date(media.addedAt).toLocaleDateString("fr-FR")}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(media.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default MediaManagement;
