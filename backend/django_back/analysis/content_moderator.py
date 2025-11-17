"""
Module de détection de contenus sensibles avec Ollama
Détecte : incitation à la haine, fake news, discours toxique
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ContentModerator:
    """
    Analyseur de contenus sensibles utilisant Ollama
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "mistral:latest"):
        """
        Initialise le modérateur de contenu
        
        Args:
            ollama_url: URL de l'API Ollama
            model: Modèle Ollama à utiliser
        """
        self.ollama_url = ollama_url
        self.model = model
        self.api_endpoint = f"{ollama_url}/api/generate"
    
    def check_ollama_status(self) -> bool:
        """
        Vérifie si Ollama est disponible
        
        Returns:
            True si Ollama est disponible, False sinon
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _call_ollama(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Appelle l'API Ollama
        
        Args:
            prompt: Le prompt à envoyer
            max_tokens: Nombre maximum de tokens
            
        Returns:
            Réponse du modèle
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Faible température pour plus de cohérence
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"❌ Erreur Ollama: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"❌ Erreur lors de l'appel à Ollama: {e}")
            return ""
    
    def analyze_toxicity(self, text: str) -> Dict:
        """
        Analyse la toxicité d'un contenu
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dict avec score de toxicité et détails
        """
        prompt = f"""Tu es un modérateur de contenu pour un régulateur des médias au Burkina Faso.

IMPORTANT: Distingue entre:
- RAPPORTER/INFORMER sur des faits (même graves) = LÉGITIME, score faible
- PROMOUVOIR/INCITER à la haine ou violence = PROBLÉMATIQUE, score élevé

Texte à analyser: "{text}"

Évalue UNIQUEMENT si l'auteur INCITE ou PROMEUT (note de 0 à 10):
1. Incitation à la haine (contre un groupe ethnique, religieux, etc.)
2. Appel à la violence ou discours agressif
3. Insultes ou langage offensant direct
4. Discrimination active

Un article qui RAPPORTE des faits (même violents) sans les promouvoir doit avoir un score FAIBLE.

Réponds UNIQUEMENT au format JSON suivant:
{{
    "est_toxique": true/false,
    "score_toxicite": 0-10,
    "contexte": "informatif/promotionnel"
}}"""

        response = self._call_ollama(prompt)
        
        try:
            # Extraire le JSON de la réponse
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                return self._default_toxicity_result()
        except json.JSONDecodeError:
            print(f"⚠️ Impossible de parser la réponse JSON: {response}")
            return self._default_toxicity_result()
    
    def analyze_misinformation(self, text: str) -> Dict:
        """
        Analyse si le contenu contient de la désinformation
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dict avec score de désinformation et détails
        """
        prompt = f"""Tu es un modérateur de contenu pour un régulateur des médias au Burkina Faso.

IMPORTANT: Distingue entre:
- Article journalistique factuel avec sources = LÉGITIME, score faible
- Affirmations fausses présentées comme vraies = PROBLÉMATIQUE, score élevé

Texte à analyser: "{text}"

Évalue UNIQUEMENT si le contenu PROPAGE de fausses informations (note de 0 à 10):
1. Affirmations manifestement fausses ou non vérifiables
2. Manipulation évidente de faits
3. Théories du complot sans fondement
4. Propagande mensongère

Un article qui cite des sources officielles ou rapporte des faits vérifiables doit avoir un score FAIBLE.

Réponds UNIQUEMENT au format JSON suivant:
{{
    "est_desinformation": true/false,
    "score_desinformation": 0-10,
    "sources_citees": true/false
}}"""

        response = self._call_ollama(prompt)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                return self._default_misinformation_result()
        except json.JSONDecodeError:
            print(f"⚠️ Impossible de parser la réponse JSON: {response}")
            return self._default_misinformation_result()
    
    def analyze_sensitivity(self, text: str) -> Dict:
        """
        Analyse la sensibilité globale du contenu
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dict avec niveau de sensibilité et catégories
        """
        prompt = f"""Tu es un modérateur de contenu pour un régulateur des médias au Burkina Faso.

IMPORTANT: 
- Un article qui INFORME sur des sujets sensibles de manière FACTUELLE = sensibilité FAIBLE/MOYENNE
- Un article qui EXPLOITE ou SENSATIONNALISE de manière irresponsable = sensibilité ÉLEVÉE/CRITIQUE

Texte à analyser: "{text}"

Évalue si le contenu aborde des sujets sensibles de manière IRRESPONSABLE:
1. Violence ou conflit armé (traitement sensationnaliste)
2. Terrorisme (glorification ou détails excessifs)
3. Politique controversée (partialité extrême)
4. Religion sensible (propos offensants)
5. Santé publique (panique inutile)

Un reportage factuel et équilibré sur ces sujets doit avoir un score FAIBLE.

Réponds UNIQUEMENT au format JSON suivant:
{{
    "est_sensible": true/false,
    "score_sensibilite": 0-10,
    "traitement": "factuel/sensationnaliste"
}}"""

        response = self._call_ollama(prompt)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                return self._default_sensitivity_result()
        except json.JSONDecodeError:
            print(f"⚠️ Impossible de parser la réponse JSON: {response}")
            return self._default_sensitivity_result()
    
    def analyze_content(self, text: str, content_type: str = "article") -> Dict:
        """
        Analyse complète d'un contenu en un seul appel IA
        
        Args:
            text: Texte à analyser
            content_type: Type de contenu (article, facebook_post, tweet)
            
        Returns:
            Dict avec toutes les analyses
        """
        if not text or len(text.strip()) < 10:
            return self._default_analysis_result()
        
        print(f"🔍 Analyse du contenu ({content_type})...")
        
        # Limiter la taille du texte pour l'analyse
        text_sample = text[:2000] if len(text) > 2000 else text
        
        # Analyse unifiée avec décision de l'IA sur le type principal
        prompt = f"""Tu es un modérateur de contenu pour un régulateur des médias au Burkina Faso.

Analyse ce texte et détermine s'il contient du contenu problématique.

IMPORTANT: Distingue entre:
- RAPPORTER/INFORMER sur des faits = LÉGITIME, scores faibles
- PROMOUVOIR/INCITER = PROBLÉMATIQUE, scores élevés

Texte: "{text_sample}"

Évalue ces 3 aspects (scores 0-10):
1. Toxicité: Incitation à la haine, violence, insultes, discrimination
2. Désinformation: Fausses informations, manipulation, théories du complot
3. Sensibilité: Traitement irresponsable de sujets sensibles

Puis DÉCIDE quel est le problème PRINCIPAL (si aucun, mets "none"):
- "toxicity" si c'est principalement du discours de haine/violence
- "misinformation" si c'est principalement de la désinformation
- "sensitivity" si c'est principalement un traitement sensationnaliste
- "none" si le contenu est acceptable

Réponds UNIQUEMENT au format JSON:
{{
    "toxicity_score": 0-10,
    "misinformation_score": 0-10,
    "sensitivity_score": 0-10,
    "primary_issue": "toxicity/misinformation/sensitivity/none",
    "contexte": "informatif/promotionnel",
    "sources_citees": true/false,
    "traitement": "factuel/sensationnaliste"
}}"""

        response = self._call_ollama(prompt, max_tokens=200)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                
                # Construire les détails
                toxicity = {
                    'est_toxique': result.get('toxicity_score', 0) >= 6,
                    'score_toxicite': result.get('toxicity_score', 0),
                    'contexte': result.get('contexte', 'informatif')
                }
                
                misinformation = {
                    'est_desinformation': result.get('misinformation_score', 0) >= 6,
                    'score_desinformation': result.get('misinformation_score', 0),
                    'sources_citees': result.get('sources_citees', False)
                }
                
                sensitivity = {
                    'est_sensible': result.get('sensitivity_score', 0) >= 6,
                    'score_sensibilite': result.get('sensitivity_score', 0),
                    'traitement': result.get('traitement', 'factuel')
                }
                
                # Calcul du score de risque
                risk_score = (
                    result.get('toxicity_score', 0) * 0.4 +
                    result.get('misinformation_score', 0) * 0.4 +
                    result.get('sensitivity_score', 0) * 0.2
                )
                
                risk_level = self._determine_risk_level(risk_score)
                
                should_flag = (
                    risk_score >= 7.0 or
                    result.get('toxicity_score', 0) >= 8.0 or
                    result.get('misinformation_score', 0) >= 8.0
                )
                
                return {
                    'content_type': content_type,
                    'analyzed_at': datetime.now().isoformat(),
                    'toxicity': toxicity,
                    'misinformation': misinformation,
                    'sensitivity': sensitivity,
                    'risk_score': round(risk_score, 2),
                    'risk_level': risk_level,
                    'should_flag': should_flag,
                    'primary_issue': result.get('primary_issue', 'none'),
                    'text_length': len(text)
                }
            else:
                return self._default_analysis_result()
        except Exception as e:
            print(f"⚠️ Erreur parsing: {e}")
            return self._default_analysis_result()
    
    def _calculate_risk_score(self, toxicity: Dict, misinformation: Dict, sensitivity: Dict) -> float:
        """
        Calcule le score de risque global
        
        Args:
            toxicity: Résultat de l'analyse de toxicité
            misinformation: Résultat de l'analyse de désinformation
            sensitivity: Résultat de l'analyse de sensibilité
            
        Returns:
            Score de risque (0-10)
        """
        # Pondération: toxicité 40%, désinformation 40%, sensibilité 20%
        toxicity_score = toxicity.get('score_toxicite', 0)
        misinfo_score = misinformation.get('score_desinformation', 0)
        sensitivity_score = sensitivity.get('score_sensibilite', 0)
        
        risk_score = (
            toxicity_score * 0.4 +
            misinfo_score * 0.4 +
            sensitivity_score * 0.2
        )
        
        return risk_score
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """
        Détermine le niveau de risque
        
        Args:
            risk_score: Score de risque (0-10)
            
        Returns:
            Niveau de risque
        """
        if risk_score >= 8:
            return "🔴 CRITIQUE"
        elif risk_score >= 6:
            return "🟠 ÉLEVÉ"
        elif risk_score >= 4:
            return "🟡 MOYEN"
        elif risk_score >= 2:
            return "🟢 FAIBLE"
        else:
            return "✅ MINIMAL"
    
    def _determine_primary_issue(self, toxicity: Dict, misinformation: Dict, sensitivity: Dict) -> str:
        """
        Détermine le type principal de problème détecté
        
        Args:
            toxicity: Résultat de l'analyse de toxicité
            misinformation: Résultat de l'analyse de désinformation
            sensitivity: Résultat de l'analyse de sensibilité
            
        Returns:
            Type principal: 'toxicity', 'misinformation', 'sensitivity', ou 'none'
        """
        tox_score = toxicity.get('score_toxicite', 0)
        mis_score = misinformation.get('score_desinformation', 0)
        sens_score = sensitivity.get('score_sensibilite', 0)
        
        # Si aucun score significatif
        if max(tox_score, mis_score, sens_score) < 3:
            return 'none'
        
        # Retourner le type avec le score le plus élevé
        max_score = max(tox_score, mis_score, sens_score)
        
        if max_score == tox_score:
            return 'toxicity'
        elif max_score == mis_score:
            return 'misinformation'
        else:
            return 'sensitivity'
    
    def _default_toxicity_result(self) -> Dict:
        """Résultat par défaut pour l'analyse de toxicité"""
        return {
            'est_toxique': False,
            'score_toxicite': 0,
            'incitation_haine': 0,
            'violence': 0,
            'insultes': 0,
            'discrimination': 0,
            'raison': 'Analyse non disponible'
        }
    
    def _default_misinformation_result(self) -> Dict:
        """Résultat par défaut pour l'analyse de désinformation"""
        return {
            'est_desinformation': False,
            'score_desinformation': 0,
            'affirmations_non_verifiees': 0,
            'manipulation_faits': 0,
            'theorie_complot': 0,
            'propagande': 0,
            'raison': 'Analyse non disponible',
            'elements_suspects': []
        }
    
    def _default_sensitivity_result(self) -> Dict:
        """Résultat par défaut pour l'analyse de sensibilité"""
        return {
            'est_sensible': False,
            'niveau_sensibilite': 'faible',
            'score_sensibilite': 0,
            'categories_sensibles': [],
            'raison': 'Analyse non disponible'
        }
    
    def _default_analysis_result(self) -> Dict:
        """Résultat par défaut pour une analyse complète"""
        return {
            'content_type': 'unknown',
            'analyzed_at': datetime.now().isoformat(),
            'toxicity': self._default_toxicity_result(),
            'misinformation': self._default_misinformation_result(),
            'sensitivity': self._default_sensitivity_result(),
            'risk_score': 0,
            'risk_level': '✅ MINIMAL',
            'should_flag': False,
            'text_length': 0
        }
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à Ollama
        
        Returns:
            True si la connexion fonctionne
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Connexion à Ollama réussie")
                print(f"📦 Modèles disponibles: {[m['name'] for m in models]}")
                return True
            else:
                print(f"❌ Erreur de connexion à Ollama: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Impossible de se connecter à Ollama: {e}")
            print(f"💡 Assurez-vous qu'Ollama est lancé: ollama serve")
            return False


# Fonction utilitaire pour analyser rapidement un texte
def analyze_text(text: str, content_type: str = "article") -> Dict:
    """
    Fonction utilitaire pour analyser un texte
    
    Args:
        text: Texte à analyser
        content_type: Type de contenu
        
    Returns:
        Résultat de l'analyse
    """
    moderator = ContentModerator()
    return moderator.analyze_content(text, content_type)
