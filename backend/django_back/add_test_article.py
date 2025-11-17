#!/usr/bin/env python3
"""
Script pour ajouter des articles de test (normaux et problématiques)
"""

from database.db_manager import DatabaseManager
from database.models import Article
from datetime import datetime

def main():
    db = DatabaseManager()
    
    # Récupérer un média existant
    medias = db.get_all_medias()
    if not medias:
        print("❌ Aucun média trouvé")
        return
    
    media_id = medias[0].id
    print(f"📰 Ajout d'articles de test pour le média: {medias[0].nom}")
    
    # Article 1: Normal - Reportage factuel
    article1 = Article(
        media_id=media_id,
        titre="Opération antiterroriste dans le Sahel : 15 terroristes neutralisés",
        contenu="""Le ministère de la Défense a annoncé ce mardi qu'une opération militaire menée dans la région du Sahel a permis de neutraliser 15 éléments terroristes. 
        
Selon le communiqué officiel, l'opération s'est déroulée dans la nuit du lundi à mardi dans la province du Soum. Les Forces de Défense et de Sécurité (FDS) ont également saisi des armes et du matériel logistique.

Le gouvernement burkinabè poursuit ses efforts de sécurisation du territoire national face aux groupes armés terroristes qui sévissent dans plusieurs régions du pays.

Cette opération s'inscrit dans le cadre de la stratégie nationale de lutte contre le terrorisme adoptée par les autorités de la Transition.""",
        url="https://test.com/article-normal-1",
        date_publication=datetime.now().isoformat(),
        source_type="test"
    )
    
    # Article 2: Problématique - Incitation à la haine
    article2 = Article(
        media_id=media_id,
        titre="Il faut éliminer tous ces traîtres et collaborateurs !",
        contenu="""Ces gens-là sont des ennemis du peuple ! Ils méritent tous d'être punis sévèrement. 
        
Nous devons nous débarrasser de tous ces vendus qui collaborent avec l'ennemi. Ils ne méritent aucune pitié. Ce sont des rats qu'il faut exterminer.

Le peuple doit se lever et faire justice lui-même. Nous savons qui ils sont, où ils habitent. Il est temps d'agir et de les faire payer pour leur trahison.

Tous ceux qui ne sont pas avec nous sont contre nous. Il n'y a pas de place pour les modérés ou les neutres. Vous êtes soit avec le peuple, soit vous êtes un traître qui mérite le même sort.""",
        url="https://test.com/article-problematique-1",
        date_publication=datetime.now().isoformat(),
        source_type="test"
    )
    
    # Article 3: Problématique - Désinformation
    article3 = Article(
        media_id=media_id,
        titre="RÉVÉLATION CHOC : Le vaccin contre le COVID contient des puces de contrôle mental",
        contenu="""Des sources anonymes révèlent que le vaccin contre le COVID-19 contient en réalité des nano-puces développées par des organisations secrètes pour contrôler la population.
        
Ces puces permettraient de surveiller tous vos déplacements et même de lire vos pensées. C'est un complot mondial orchestré par les grandes puissances pour asservir l'humanité.

Les médias officiels vous mentent ! Ne croyez pas ce que disent les médecins et les scientifiques, ils sont tous achetés. La vérité est que ce vaccin est une arme biologique déguisée.

Partagez cette information avant qu'elle ne soit censurée ! Le gouvernement essaie de cacher la vérité mais nous, nous savons.""",
        url="https://test.com/article-problematique-2",
        date_publication=datetime.now().isoformat(),
        source_type="test"
    )
    
    # Article 4: Normal - Article politique équilibré
    article4 = Article(
        media_id=media_id,
        titre="Dialogue politique : Les partis politiques appellent à des réformes",
        contenu="""Les représentants de plusieurs partis politiques ont participé ce mercredi à une rencontre sur les réformes institutionnelles.
        
Selon les participants, les discussions ont porté sur la révision du code électoral, la réforme de la justice et le renforcement de la démocratie. Les échanges se sont déroulés dans un climat apaisé.

Le parti au pouvoir et l'opposition ont exprimé des points de vue divergents sur certains aspects, mais tous s'accordent sur la nécessité de poursuivre le dialogue.

Une prochaine rencontre est prévue dans deux semaines pour approfondir les discussions sur les propositions formulées.""",
        url="https://test.com/article-normal-2",
        date_publication=datetime.now().isoformat(),
        source_type="test"
    )
    
    # Ajouter les articles
    articles = [article1, article2, article3, article4]
    added = 0
    
    for article in articles:
        if not db.article_exists(article.url):
            article_id = db.add_article(article)
            if article_id:
                added += 1
                print(f"✅ Article ajouté (ID: {article_id}): {article.titre[:60]}...")
        else:
            print(f"⏭️ Article existe déjà: {article.titre[:60]}...")
    
    print(f"\n📊 {added} nouveaux articles ajoutés")
    print("\n🔍 Articles de test:")
    print("  1. Article NORMAL (terrorisme factuel)")
    print("  2. Article PROBLÉMATIQUE (incitation à la haine)")
    print("  3. Article PROBLÉMATIQUE (désinformation)")
    print("  4. Article NORMAL (politique équilibré)")

if __name__ == "__main__":
    main()
