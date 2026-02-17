"""
Tests for the AI analyzer module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ai_analyzer import AIAnalyzer


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    mock_client = Mock()
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    
    mock_message.content = "This is a test response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def analyzer_with_mock(mock_openai_client):
    """Create an AIAnalyzer with mocked OpenAI client."""
    analyzer = AIAnalyzer(api_key="test_key")
    analyzer.client = mock_openai_client
    return analyzer


def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = AIAnalyzer(api_key="test_key", model="gpt-4")
    assert analyzer.api_key == "test_key"
    assert analyzer.model == "gpt-4"


def test_analyzer_without_api_key():
    """Test analyzer initialization without API key."""
    with patch('src.ai_analyzer.settings') as mock_settings:
        mock_settings.openai_api_key = ""
        analyzer = AIAnalyzer()
        assert analyzer.client is None


def test_call_openai(analyzer_with_mock, mock_openai_client):
    """Test OpenAI API call."""
    result = analyzer_with_mock._call_openai("Test prompt")
    assert result == "This is a test response"
    mock_openai_client.chat.completions.create.assert_called_once()


def test_call_openai_with_system_message(analyzer_with_mock, mock_openai_client):
    """Test OpenAI API call with system message."""
    result = analyzer_with_mock._call_openai(
        "Test prompt",
        system_message="You are a helpful assistant"
    )
    assert result == "This is a test response"
    
    call_args = mock_openai_client.chat.completions.create.call_args
    messages = call_args.kwargs['messages']
    assert len(messages) == 2
    assert messages[0]['role'] == 'system'
    assert messages[1]['role'] == 'user'


def test_summarize_text(analyzer_with_mock):
    """Test text summarization."""
    long_text = " ".join(["word"] * 300)  # Create long text
    summary = analyzer_with_mock.summarize_text(long_text, max_length=50)
    assert isinstance(summary, str)


def test_summarize_short_text(analyzer_with_mock):
    """Test summarization of already short text."""
    short_text = "This is a short text"
    summary = analyzer_with_mock.summarize_text(short_text, max_length=100)
    assert summary == short_text  # Should return original text


def test_extract_entities(analyzer_with_mock):
    """Test entity extraction."""
    text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
    entities = analyzer_with_mock.extract_entities(text)
    assert isinstance(entities, dict)
    assert 'raw_entities' in entities


def test_classify_content(analyzer_with_mock):
    """Test content classification."""
    text = "This is a technology article about AI."
    categories = ["Technology", "Sports", "Politics"]
    classification = analyzer_with_mock.classify_content(text, categories)
    assert isinstance(classification, dict)
    assert 'classification' in classification


def test_analyze_sentiment(analyzer_with_mock):
    """Test sentiment analysis."""
    text = "This is a wonderful product! I love it!"
    sentiment = analyzer_with_mock.analyze_sentiment(text)
    assert isinstance(sentiment, dict)
    assert 'sentiment' in sentiment


def test_extract_keywords(analyzer_with_mock, mock_openai_client):
    """Test keyword extraction."""
    # Mock response with comma-separated keywords
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    mock_message.content = "keyword1, keyword2, keyword3"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_openai_client.chat.completions.create.return_value = mock_response
    
    text = "This is a text about machine learning and artificial intelligence."
    keywords = analyzer_with_mock.extract_keywords(text, num_keywords=5)
    assert isinstance(keywords, list)
    assert len(keywords) <= 5


def test_analyze_full(analyzer_with_mock):
    """Test full analysis."""
    data = {
        'url': 'https://example.com',
        'title': 'Test Page',
        'text': 'This is a test text for analysis.'
    }
    results = analyzer_with_mock.analyze(data, analysis_type='full')
    
    assert 'url' in results
    assert 'title' in results
    assert isinstance(results, dict)


def test_analyze_summary_only(analyzer_with_mock):
    """Test summary-only analysis."""
    data = {
        'url': 'https://example.com',
        'title': 'Test Page',
        'text': 'This is a test text for analysis.'
    }
    results = analyzer_with_mock.analyze(data, analysis_type='summary')
    
    assert 'summary' in results
    assert 'sentiment' not in results


def test_analyze_empty_data(analyzer_with_mock):
    """Test analysis with empty data."""
    data = {}
    results = analyzer_with_mock.analyze(data)
    assert results == {}


def test_analyze_without_client():
    """Test analysis without initialized client."""
    analyzer = AIAnalyzer(api_key="")
    analyzer.client = None
    
    data = {
        'text': 'Test text'
    }
    
    with pytest.raises(ValueError):
        analyzer._call_openai("test prompt")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
