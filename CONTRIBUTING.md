# Contributing to FastAPI Boilerplate Generator

First off, thank you for considering contributing to FastAPI Boilerplate Generator! 🎉

It's people like you that make this tool a great resource for the FastAPI community.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, CLI outputs)
- **Describe the behavior you observed** and what you expected
- **Include screenshots** if relevant
- **Specify your environment** (OS, Python version, etc.)

### Suggesting Enhancements ✨

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List examples** of how it would be used
- **Include mockups or examples** if applicable

### Pull Requests 🔧

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you're adding functionality
4. **Update documentation** if needed
5. **Ensure tests pass**: `pytest`
6. **Format your code**: `black src tests`
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- OpenAI API key (for testing)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/martialo12/fastapi-boilerplate-agent.git
cd fastapi-boilerplate-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run tests
pytest

# Run the CLI
python -m fastapi_boilerplate_agent.cli
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting: `black src tests`
- Use [Flake8](https://flake8.pycqa.org/) for linting: `flake8 src tests`
- Maximum line length: 100 characters
- Use type hints where appropriate

### Code Organization

```
src/fastapi_boilerplate_agent/
├── __init__.py
├── cli.py              # CLI interface
├── config.py           # Configuration models
├── graph.py            # LangGraph workflow
└── tools.py            # Code generation templates
```

### Naming Conventions

- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings:

```python
def generate_project(config: Dict) -> Dict[str, str]:
    """Generate a FastAPI project from configuration.
    
    Args:
        config: Project configuration dictionary
        
    Returns:
        Dictionary mapping file paths to file contents
        
    Raises:
        ValueError: If configuration is invalid
    """
```

### Testing

- Write tests for new functionality
- Maintain or improve code coverage
- Use pytest fixtures for common setup
- Name test files: `test_*.py`
- Name test functions: `test_*`

```python
def test_generate_project_with_postgres():
    """Test project generation with PostgreSQL."""
    config = {"project_name": "test_api", "db": "postgres"}
    result = generate_project(config)
    assert "app/main.py" in result
```

## Commit Message Guidelines

Use clear and meaningful commit messages:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(cli): add option to skip Docker configuration

Added a new prompt option that allows users to skip Docker
configuration entirely. This is useful for users who don't
use Docker in their workflow.

Closes #42
```

```
fix(database): correct PostgreSQL connection pooling

Fixed an issue where connection pool was not properly
configured for PostgreSQL databases, causing connection
leaks under high load.

Fixes #128
```

## Project Structure

Understanding the project structure helps you contribute effectively:

```
fastapi-boilerplate-agent/
├── src/
│   └── fastapi_boilerplate_agent/
│       ├── __init__.py
│       ├── cli.py          # Interactive CLI
│       ├── config.py       # Pydantic models
│       ├── graph.py        # LangGraph agent
│       └── tools.py        # Templates & generation
├── tests/
│   ├── __init__.py
│   └── test_*.py           # Test files
├── examples/              # Example generated projects
├── .github/
│   ├── workflows/         # CI/CD workflows
│   └── ISSUE_TEMPLATE/    # Issue templates
├── pyproject.toml         # Package configuration
├── README.md              # Main documentation
├── CONTRIBUTING.md        # This file
├── LICENSE                # MIT License
└── CHANGELOG.md           # Version history
```

## Adding New Features

### Adding Database Support

1. Add template in `tools.py` (e.g., `DATABASE_MYSQL_PY`)
2. Update CLI prompt in `cli.py`
3. Add condition in generation logic
4. Update documentation
5. Add tests

### Adding New Templates

1. Define template string in `tools.py`
2. Add generation logic in `generate_fastapi_boilerplate_func()`
3. Add tests for the new template
4. Update README with examples

### Improving LLM Prompts

1. Modify prompts in `graph.py`
2. Test with various inputs
3. Document prompt improvements
4. Consider edge cases

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src/fastapi_boilerplate_agent

# Run with verbose output
pytest -v
```

### Writing Tests

- Test happy paths and edge cases
- Use descriptive test names
- Keep tests focused and isolated
- Mock external dependencies (OpenAI API)

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange
    config = {"project_name": "test"}
    
    # Act
    result = function_to_test(config)
    
    # Assert
    assert expected_result in result
```

## Documentation

### Updating Documentation

- Keep README.md up to date
- Add docstrings to new code
- Update examples if needed
- Document breaking changes in CHANGELOG.md

### Writing Good Documentation

- Be clear and concise
- Include code examples
- Explain *why*, not just *what*
- Use proper formatting (Markdown)

## Release Process

(For maintainers)

1. Update `CHANGELOG.md`
2. Bump version in `pyproject.toml`
3. Create GitHub release
4. Tag with version number
5. Publish to PyPI (when ready)

## Getting Help

- **Discord**: [Join our server](#) (coming soon)
- **GitHub Discussions**: Ask questions and discuss ideas
- **GitHub Issues**: Report bugs and request features

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! Open an issue with the "question" label or reach out in GitHub Discussions.

---

**Thank you for contributing! 🙏**

Every contribution, no matter how small, makes a difference!
