import { useMemo, useState } from "react";
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
import { Plus, Trash2, Globe, Facebook, Twitter, Edit, X } from "lucide-react";
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
import {
  useMedia,
  useCreateMedia,
  useDeleteMedia,
  useUpdateMedia,
} from "@/hooks/useMedia";

const mediaSchema = z.object({
  name: z
    .string()
    .min(2, "Le nom doit contenir au moins 2 caractères")
    .max(100),
  url: z.string().url("URL invalide").min(1, "L'URL du site web est requise"),
  type_site: z.string().optional(),
  facebook_page: z.string().optional(),
  twitter_account: z.string().optional(),
});

type MediaFormData = z.infer<typeof mediaSchema>;

interface Media {
  id: string;
  name: string;
  url: string;
  type_site?: string;
  facebook_page?: string;
  twitter_account?: string;
  actif: boolean;
  addedAt: string;
}

const MediaManagement = () => {
  // Use TanStack Query hooks
  const { data: mediaData, isLoading: loading } = useMedia();
  const createMediaMutation = useCreateMedia();
  const updateMediaMutation = useUpdateMedia();
  const deleteMediaMutation = useDeleteMedia();

  // État pour le mode édition
  const [editingMediaId, setEditingMediaId] = useState<number | null>(null);

  // Transform media data
  const medias = useMemo(() => {
    if (!mediaData) return [];

    return mediaData.map((media) => ({
      id: media.id.toString(),
      name: media.nom,
      url: media.url,
      type_site: media.type_site,
      facebook_page: media.facebook_page,
      twitter_account: media.twitter_account,
      actif: media.actif,
      addedAt: new Date(media.created_at).toISOString().split("T")[0],
    }));
  }, [mediaData]);

  const form = useForm<MediaFormData>({
    resolver: zodResolver(mediaSchema),
    defaultValues: {
      name: "",
      url: "",
      type_site: "unknown",
      facebook_page: "",
      twitter_account: "",
    },
  });

  const onSubmit = async (data: MediaFormData) => {
    try {
      if (editingMediaId) {
        // Mode édition
        await updateMediaMutation.mutateAsync({
          id: editingMediaId,
          data: {
            nom: data.name,
            url: data.url,
            type_site: data.type_site || "unknown",
            facebook_page: data.facebook_page || undefined,
            twitter_account: data.twitter_account || undefined,
          },
        });

        toast({
          title: "✅ Média modifié",
          description: `${data.name} a été modifié avec succès.`,
        });

        setEditingMediaId(null);
        form.reset({
          name: "",
          url: "",
          type_site: "unknown",
          facebook_page: "",
          twitter_account: "",
        });
      } else {
        // Mode création
        await createMediaMutation.mutateAsync({
          nom: data.name,
          url: data.url,
          type_site: data.type_site || "unknown",
          facebook_page: data.facebook_page || undefined,
          twitter_account: data.twitter_account || undefined,
          actif: true,
        });

        toast({
          title: "✅ Média ajouté",
          description: `${data.name} a été ajouté avec succès.`,
        });

        form.reset({
          name: "",
          url: "",
          type_site: "unknown",
          facebook_page: "",
          twitter_account: "",
        });
      }
    } catch (error) {
      toast({
        title: "❌ Erreur",
        description:
          error instanceof Error
            ? error.message
            : "Impossible de sauvegarder le média",
        variant: "destructive",
      });
    }
  };

  const handleEdit = (media: Media) => {
    // Charger les données dans le formulaire
    form.reset({
      name: media.name,
      url: media.url,
      type_site: media.type_site || "unknown",
      facebook_page: media.facebook_page || "",
      twitter_account: media.twitter_account || "",
    });

    setEditingMediaId(parseInt(media.id));

    // Scroll vers le formulaire
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelEdit = () => {
    setEditingMediaId(null);
    form.reset();
  };

  const handleDelete = async (id: string) => {
    const media = medias.find((m) => m.id === id);

    if (
      !confirm(
        `Êtes-vous sûr de vouloir supprimer "${media?.name}" ?\n\nCela supprimera également tous les articles, posts Facebook et tweets associés.`
      )
    ) {
      return;
    }

    try {
      await deleteMediaMutation.mutateAsync(parseInt(id));

      // Si on était en train d'éditer ce média, annuler l'édition
      if (editingMediaId === parseInt(id)) {
        handleCancelEdit();
      }

      toast({
        title: "✅ Média supprimé",
        description: `${media?.name} a été supprimé avec succès.`,
      });
    } catch (error) {
      toast({
        title: "❌ Erreur",
        description:
          error instanceof Error
            ? error.message
            : "Impossible de supprimer le média",
        variant: "destructive",
      });
    }
  };

  const getPlatformBadges = (media: Media) => {
    const badges = [];

    if (media.url) {
      badges.push(
        <Badge key="web" variant="outline" className="gap-1">
          <Globe className="h-3 w-3" />
          Web
        </Badge>
      );
    }

    if (media.facebook_page) {
      badges.push(
        <Badge key="facebook" variant="outline" className="gap-1">
          <Facebook className="h-3 w-3" />
          Facebook
        </Badge>
      );
    }

    if (media.twitter_account) {
      badges.push(
        <Badge key="twitter" variant="outline" className="gap-1">
          <Twitter className="h-3 w-3" />
          Twitter
        </Badge>
      );
    }

    return badges;
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
            {editingMediaId ? (
              <>
                <Edit className="h-5 w-5" />
                Modifier le média
              </>
            ) : (
              <>
                <Plus className="h-5 w-5" />
                Ajouter un média à surveiller
              </>
            )}
          </CardTitle>
          <CardDescription>
            {editingMediaId ? (
              <span className="flex items-center gap-2">
                Mode édition activé - Modifiez les informations ci-dessous
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCancelEdit}
                  className="h-6 px-2"
                >
                  <X className="h-3 w-3 mr-1" />
                  Annuler
                </Button>
              </span>
            ) : (
              "Ajoutez des pages web, des comptes Facebook ou Twitter à surveiller"
            )}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nom du média *</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: Lefaso.net" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="url"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>URL du site web *</FormLabel>
                      <FormControl>
                        <Input placeholder="https://exemple.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="type_site"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Type de site</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="wordpress">WordPress</SelectItem>
                          <SelectItem value="html">HTML</SelectItem>
                          <SelectItem value="rss">RSS</SelectItem>
                          <SelectItem value="unknown">Inconnu</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="facebook_page"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        <Facebook className="h-4 w-4 inline mr-1" />
                        Page Facebook
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="nom_page" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="twitter_account"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        <Twitter className="h-4 w-4 inline mr-1" />
                        Compte Twitter
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="username (sans @)" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="flex gap-2">
                <Button
                  type="submit"
                  className="flex-1 md:flex-initial"
                  disabled={
                    createMediaMutation.isPending ||
                    updateMediaMutation.isPending
                  }
                >
                  {editingMediaId ? (
                    <>
                      <Edit className="h-4 w-4 mr-2" />
                      {updateMediaMutation.isPending
                        ? "Modification en cours..."
                        : "Modifier le média"}
                    </>
                  ) : (
                    <>
                      <Plus className="h-4 w-4 mr-2" />
                      {createMediaMutation.isPending
                        ? "Ajout en cours..."
                        : "Ajouter le média"}
                    </>
                  )}
                </Button>

                {editingMediaId && (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleCancelEdit}
                  >
                    <X className="h-4 w-4 mr-2" />
                    Annuler
                  </Button>
                )}
              </div>
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
                <TableHead>Plateformes</TableHead>
                <TableHead>URL</TableHead>
                <TableHead>Facebook</TableHead>
                <TableHead>Twitter</TableHead>
                <TableHead>Statut</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {medias.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={7}
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
                      <div className="flex gap-1 flex-wrap">
                        {getPlatformBadges(media)}
                      </div>
                    </TableCell>
                    <TableCell className="font-mono text-xs text-muted-foreground max-w-[200px] truncate">
                      {media.url}
                    </TableCell>
                    <TableCell className="font-mono text-xs text-muted-foreground">
                      {media.facebook_page || (
                        <span className="text-gray-400">-</span>
                      )}
                    </TableCell>
                    <TableCell className="font-mono text-xs text-muted-foreground">
                      {media.twitter_account ? (
                        `@${media.twitter_account}`
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <Badge variant={media.actif ? "default" : "secondary"}>
                        {media.actif ? "Actif" : "Inactif"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex gap-1 justify-end">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEdit(media)}
                          title="Modifier"
                        >
                          <Edit className="h-4 w-4 text-blue-600" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(media.id)}
                          disabled={deleteMediaMutation.isPending}
                          title="Supprimer"
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </div>
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
