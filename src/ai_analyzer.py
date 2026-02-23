"""
AI-powered content analyzer using OpenAI.
"""
from typing import Optional, Any
from openai import OpenAI

from .config import settings
from .logging_config import get_logger

logger = get_logger(__name__)


class AIAnalyzer:
    """AI-powered analyzer for web scraping data."""

    # Constants for API configuration
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 2000
    TRUNCATION_MULTIPLIER = 5

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the AI analyzer.

        Args:
            api_key: OpenAI API key
            model: Model to use (e.g., 'gpt-4', 'gpt-3.5-turbo')
        """
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model

        if not self.api_key:
            logger.warning("OpenAI API key not configured. AI features will be unavailable.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def _call_openai(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Make a call to OpenAI API.

        Args:
            prompt: The user prompt
            system_message: Optional system message

        Returns:
            Response text from the model
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.DEFAULT_TEMPERATURE,
                max_tokens=self.DEFAULT_MAX_TOKENS
            )

            content = response.choices[0].message.content
            return content.strip() if content else ""

        except Exception as e:
            logger.error("Error calling OpenAI API: %s", e)
            raise

    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize a text using AI.

        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words

        Returns:
            Summary text
        """
        if len(text.split()) <= max_length:
            return text

        prompt = f"Please summarize the following text in approximately {max_length} words:\n\n{text}"
        system_message = "You are a helpful assistant that creates concise and accurate summaries."

        try:
            summary = self._call_openai(prompt, system_message)
            logger.info("Text summarized successfully")
            return summary
        except Exception as e:
            logger.error("Error summarizing text: %s", e)
            return text[:max_length * self.TRUNCATION_MULTIPLIER]  # Fallback to truncation

    def extract_entities(self, text: str) -> dict[str, Any]:
        """
        Extract named entities from text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with entity types and their values
        """
        prompt = f"""Extract and categorize the following entities from the text:
        - People (names of persons)
        - Organizations (companies, institutions)
        - Locations (cities, countries)
        - Dates (any date references)
        - Products (product names)

        Text: {text}

        Return the results as a JSON-like structure with entity types as keys and lists of entities as values."""

        system_message = "You are an expert in named entity recognition. Extract entities accurately."

        try:
            result = self._call_openai(prompt, system_message)
            logger.info("Entities extracted successfully")
            # In production, you'd want to parse this more robustly
            return {"raw_entities": result}
        except Exception as e:
            logger.error("Error extracting entities: %s", e)
            return {}

    def classify_content(self, text: str, categories: list[str]) -> dict[str, Any]:
        """
        Classify content into predefined categories.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Classification results
        """
        categories_str = ", ".join(categories)
        prompt = (
            f"Classify the following text into one of these categories: {categories_str}\n\n"
            f"Text: {text}\n\n"
            "Provide the most appropriate category and a confidence score (0-1)."
        )

        system_message = "You are an expert content classifier. Provide accurate classifications."

        try:
            result = self._call_openai(prompt, system_message)
            logger.info("Content classified successfully")
            return {"classification": result}
        except Exception as e:
            logger.error("Error classifying content: %s", e)
            return {}

    def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """
        Analyze sentiment of text.

        Args:
            text: Text to analyze

        Returns:
            Sentiment analysis results
        """
        prompt = (
            "Analyze the sentiment of the following text.\n"
            "Provide:\n"
            "1. Overall sentiment (positive/negative/neutral)\n"
            "2. Confidence score (0-1)\n"
            "3. Key phrases that indicate the sentiment\n\n"
            f"Text: {text}"
        )

        system_message = (
            "You are an expert in sentiment analysis. Provide detailed and accurate analysis."
        )

        try:
            result = self._call_openai(prompt, system_message)
            logger.info("Sentiment analyzed successfully")
            return {"sentiment": result}
        except Exception as e:
            logger.error("Error analyzing sentiment: %s", e)
            return {}

    def extract_keywords(self, text: str, num_keywords: int = 10) -> list[str]:
        """
        Extract key terms and phrases from text.

        Args:
            text: Text to analyze
            num_keywords: Number of keywords to extract

        Returns:
            List of keywords
        """
        prompt = (
            f"Extract the {num_keywords} most important keywords or key phrases "
            "from the following text.\n"
            "Return them as a comma-separated list.\n\n"
            f"Text: {text}"
        )

        system_message = "You are an expert in keyword extraction. Identify the most relevant terms."

        try:
            result = self._call_openai(prompt, system_message)
            keywords = [k.strip() for k in result.split(',')]
            logger.info("Extracted %d keywords", len(keywords))
            return keywords[:num_keywords]
        except Exception as e:
            logger.error("Error extracting keywords: %s", e)
            return []

    def analyze(self, data: dict[str, Any], analysis_type: str = "full") -> dict[str, Any]:
        """
        Perform comprehensive analysis on scraped data.

        Args:
            data: Scraped data dictionary
            analysis_type: Type of analysis ('full', 'summary', 'sentiment', 'entities')

        Returns:
            Analysis results

        Raises:
            ValueError: If analysis_type is invalid
        """
        # Validate analysis type
        valid_types = ['full', 'summary', 'sentiment', 'entities']
        if analysis_type not in valid_types:
            raise ValueError(
                f"Invalid analysis_type. Must be one of: {', '.join(valid_types)}"
            )

        if not data or 'text' not in data:
            logger.warning("No text content to analyze")
            return {}

        text = data['text']
        results = {
            'url': data.get('url', ''),
            'title': data.get('title', '')
        }

        try:
            if analysis_type in ['full', 'summary']:
                results['summary'] = self.summarize_text(text)

            if analysis_type in ['full', 'sentiment']:
                results['sentiment'] = self.analyze_sentiment(text)

            if analysis_type in ['full', 'entities']:
                results['entities'] = self.extract_entities(text)

            if analysis_type == 'full':
                results['keywords'] = self.extract_keywords(text)

            logger.info("Analysis completed: %s", analysis_type)
            return results

        except Exception as e:
            logger.error("Error during analysis: %s", e)
            return results
