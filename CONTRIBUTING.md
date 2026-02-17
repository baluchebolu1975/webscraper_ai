# Contributing to WebScraper AI

Thank you for your interest in contributing to WebScraper AI!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/webscraper_ai.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest tests/`
4. Format code: `black src/ tests/`
5. Check linting: `flake8 src/ tests/`
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a pull request

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 100)
- Add docstrings to all functions and classes
- Write tests for new features

## Testing

- Write unit tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

## Reporting Issues

- Use the GitHub issue tracker
- Provide detailed description
- Include steps to reproduce
- Add relevant code snippets or error messages

## Questions?

Feel free to open an issue for any questions or discussions.
