"""
AI-powered content analyzer using OpenAI.
"""
import logging
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI

from .config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI-powered analyzer for web scraping data."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the AI analyzer.
        
        Args:
            api_key: OpenAI API key (uses settings if not provided)
            model: Model to use (uses settings if not provided)
        """
        self.api_key = api_key or settings.openai.api_key
        self.model = model or settings.openai.model
        
        if self.api_key and self.api_key != "your-api-key-here":
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No valid OpenAI API key provided. AI features will be disabled.")
    
    def _call_openai(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Make a call to OpenAI API.
        
        Args:
            prompt: User prompt
            system_message: System message (optional)
            
        Returns:
            API response text
            
        Raises:
            ValueError: If client is not initialized
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please provide a valid API key.")
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using AI.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        # For very short text, return as-is
        if len(text) < max_length:
            return text
        
        # Truncate if text is very long
        max_context = max_length * 5
        if len(text) > max_context:
            text = text[:max_context] + "..."
        
        prompt = f"Summarize the following text in approximately {max_length} characters:\n\n{text}"
        return self._call_openai(prompt)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of entity types and their values
        """
        prompt = f"""Extract named entities from the following text and categorize them.
Return the results as a JSON object with categories like 'people', 'organizations', 'locations', 'dates', etc.

Text: {text}

Return only valid JSON."""
        
        response = self._call_openai(prompt)
        
        # TODO: Add proper JSON parsing with error handling for production
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse entity extraction response")
            return {}
    
    def classify_content(self, text: str, categories: List[str]) -> Dict[str, Any]:
        """
        Classify text into predefined categories.
        
        Args:
            text: Text to classify
            categories: List of possible categories
            
        Returns:
            Dictionary with classification results
        """
        categories_str = ", ".join(categories)
        prompt = f"""Classify the following text into one of these categories: {categories_str}
Return the category and a confidence score (0-1).

Text: {text}

Return as JSON with 'category' and 'confidence' fields."""
        
        response = self._call_openai(prompt)
        
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"category": categories[0], "confidence": 0.0}
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment analysis
        """
        prompt = f"""Analyze the sentiment of the following text.
Return as JSON with 'sentiment' (positive/negative/neutral), 'score' (0-1), and 'reasoning'.

Text: {text}"""
        
        response = self._call_openai(prompt)
        
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"sentiment": "neutral", "score": 0.5, "reasoning": "Failed to parse"}
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract key topics/keywords from text.
        
        Args:
            text: Text to analyze
            num_keywords: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        prompt = f"""Extract the {num_keywords} most important keywords or topics from this text.
Return as a JSON array of strings.

Text: {text}"""
        
        response = self._call_openai(prompt)
        
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return []
    
    def analyze(self, scraped_data: Dict[str, Any], analysis_type: str = "full") -> Dict[str, Any]:
        """
        Perform comprehensive analysis on scraped data.
        
        Args:
            scraped_data: Dictionary with scraped content
            analysis_type: Type of analysis ('full', 'summary', 'entities', 'sentiment')
            
        Returns:
            Dictionary with analysis results
        """
        if not self.client:
            return {"error": "AI features not available"}
        
        text = scraped_data.get('text', '')
        if not text:
            return {"error": "No text content to analyze"}
        
        results = {
            'url': scraped_data.get('url', ''),
            'original_title': scraped_data.get('title', '')
        }
        
        try:
            if analysis_type in ['full', 'summary']:
                results['summary'] = self.summarize_text(text)
            
            if analysis_type in ['full', 'entities']:
                results['entities'] = self.extract_entities(text[:1000])  # Limit for cost
            
            if analysis_type in ['full', 'sentiment']:
                results['sentiment'] = self.analyze_sentiment(text[:500])
            
            if analysis_type == 'full':
                results['keywords'] = self.extract_keywords(text[:1000])
        
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            results['error'] = str(e)
        
        return results
