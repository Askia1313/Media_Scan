"""
Script de test pour la modération de contenu
"""

from analysis.content_moderator import ContentModerator


def test_toxicity():
    """Test de détection de toxicité"""
    print("\n🧪 Test de détection de toxicité")
    print("=" * 80)
    
    moderator = ContentModerator()
    
    # Test 1: Contenu neutre
    text1 = "Le président a annoncé de nouvelles mesures économiques pour soutenir les entreprises."
    result1 = moderator.analyze_toxicity(text1)
    print(f"\n📝 Texte neutre:")
    print(f"   Toxique: {result1['est_toxique']}")
    print(f"   Score: {result1['score_toxicite']}/10")
    
    # Test 2: Contenu potentiellement toxique
    text2 = "Ces gens sont tous des menteurs et des voleurs qui détruisent notre pays!"
    result2 = moderator.analyze_toxicity(text2)
    print(f"\n📝 Texte potentiellement toxique:")
    print(f"   Toxique: {result2['est_toxique']}")
    print(f"   Score: {result2['score_toxicite']}/10")
    print(f"   Raison: {result2['raison']}")


def test_misinformation():
    """Test de détection de désinformation"""
    print("\n🧪 Test de détection de désinformation")
    print("=" * 80)
    
    moderator = ContentModerator()
    
    # Test 1: Information factuelle
    text1 = "Selon les données officielles, l'inflation a augmenté de 2% ce trimestre."
    result1 = moderator.analyze_misinformation(text1)
    print(f"\n📝 Information factuelle:")
    print(f"   Désinformation: {result1['est_desinformation']}")
    print(f"   Score: {result1['score_desinformation']}/10")
    
    # Test 2: Affirmation non vérifiée
    text2 = "Des sources secrètes révèlent que le gouvernement cache la vérité sur l'épidémie!"
    result2 = moderator.analyze_misinformation(text2)
    print(f"\n📝 Affirmation non vérifiée:")
    print(f"   Désinformation: {result2['est_desinformation']}")
    print(f"   Score: {result2['score_desinformation']}/10")
    print(f"   Raison: {result2['raison']}")


def test_sensitivity():
    """Test de détection de sensibilité"""
    print("\n🧪 Test de détection de sensibilité")
    print("=" * 80)
    
    moderator = ContentModerator()
    
    # Test 1: Contenu non sensible
    text1 = "Le festival culturel aura lieu ce weekend avec de nombreux artistes locaux."
    result1 = moderator.analyze_sensitivity(text1)
    print(f"\n📝 Contenu non sensible:")
    print(f"   Sensible: {result1['est_sensible']}")
    print(f"   Niveau: {result1['niveau_sensibilite']}")
    print(f"   Score: {result1['score_sensibilite']}/10")
    
    # Test 2: Contenu sensible
    text2 = "Nouvelle attaque terroriste dans le nord du pays, plusieurs victimes signalées."
    result2 = moderator.analyze_sensitivity(text2)
    print(f"\n📝 Contenu sensible:")
    print(f"   Sensible: {result2['est_sensible']}")
    print(f"   Niveau: {result2['niveau_sensibilite']}")
    print(f"   Score: {result2['score_sensibilite']}/10")
    print(f"   Catégories: {result2['categories_sensibles']}")


def test_full_analysis():
    """Test d'analyse complète"""
    print("\n🧪 Test d'analyse complète")
    print("=" * 80)
    
    moderator = ContentModerator()
    
    # Texte d'exemple
    text = """
    Le gouvernement a annoncé de nouvelles mesures de sécurité suite aux récents 
    événements dans la région du Sahel. Ces mesures visent à renforcer la protection 
    des populations civiles face aux menaces terroristes.
    """
    
    result = moderator.analyze_content(text, 'article')
    
    print(f"\n📝 Texte analysé:")
    print(f"   Type: {result['content_type']}")
    print(f"   Longueur: {result['text_length']} caractères")
    print(f"\n📊 Résultats:")
    print(f"   Score de risque: {result['risk_score']}/10")
    print(f"   Niveau de risque: {result['risk_level']}")
    print(f"   À signaler: {result['should_flag']}")
    print(f"\n🔍 Détails:")
    print(f"   Toxique: {result['toxicity']['est_toxique']} (Score: {result['toxicity']['score_toxicite']})")
    print(f"   Désinformation: {result['misinformation']['est_desinformation']} (Score: {result['misinformation']['score_desinformation']})")
    print(f"   Sensible: {result['sensitivity']['est_sensible']} (Score: {result['sensitivity']['score_sensibilite']})")


def main():
    """Fonction principale"""
    print("\n🛡️ Tests de modération de contenu avec Ollama")
    print("=" * 80)
    
    # Tester la connexion
    moderator = ContentModerator()
    if not moderator.test_connection():
        print("\n❌ Impossible de se connecter à Ollama")
        print("💡 Lancez Ollama avec: ollama serve")
        print("💡 Téléchargez le modèle avec: ollama pull llama3.2")
        return
    
    # Lancer les tests
    try:
        test_toxicity()
        test_misinformation()
        test_sensitivity()
        test_full_analysis()
        
        print("\n✅ Tous les tests sont terminés")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")


if __name__ == "__main__":
    main()
