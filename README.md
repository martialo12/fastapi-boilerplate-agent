# 🚀 FastAPI Boilerplate Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An **AI-powered CLI tool** that generates production-ready FastAPI projects with **clean architecture**, interactive prompts, and customizable configurations. Built with LangChain and LangGraph.

## ✨ Features

### 🎯 Interactive CLI
- **User-friendly prompts** like `create-react-app`
- **Smart defaults** for quick setup
- **Configuration preview** before generation
- **No command-line flags** to remember

### 🏗️ Clean Architecture
- **Repository pattern** for data access
- **Service layer** for business logic
- **Dependency injection** with FastAPI
- **Domain-driven structure** (one module per project)

### 🗄️ Database Support
- **PostgreSQL** with advanced connection pooling
- **SQLite** for development/testing
- **Abstract base class** for easy extension
- **Singleton pattern** for connection management

### 🐳 DevOps Ready
- **Docker** support with multi-stage builds
- **docker-compose** with database services
- **GitHub Actions** or **GitLab CI** pipelines
- **Makefile** for common tasks

### 📝 Well Documented
- **Comprehensive constants** for API documentation
- **Pydantic models** for validation
- **Example tests** with pytest
- **README** for each generated project

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **OpenAI API Key** (for LLM-powered generation)

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/martialo12/fastapi-boilerplate-agent.git
cd fastapi-boilerplate-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Option 2: Install with pip (future)

```bash
# Coming soon
pip install fastapi-boilerplate-generator
```

## 🚀 Quick Start

### 1. Run the interactive CLI

```bash
python -m fastapi_boilerplate_agent.cli
```

### 2. Answer the prompts

The CLI will guide you through the configuration:
- **Project name**: Choose your project name (e.g., `MyAwesomeAPI`)
- **Database**: PostgreSQL or SQLite
- **Docker**: Include Docker support?
- **CI/CD**: GitHub Actions, GitLab CI, or none

### 3. Review and confirm

Check the configuration summary and confirm generation.

### 4. Start developing!

```bash
cd my_awesome_api  # Your project directory
make install       # Install dependencies
make run          # Start the server
```

Your API is now running at `http://localhost:8000` 🎉

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Interactive CLI

The CLI will guide you through the project setup with interactive prompts:

```
🚀 FastAPI Boilerplate Generator
==================================================

Project name [my_fastapi_app]: ticket_system

Database options:
  1. PostgreSQL (recommended for production)
  2. SQLite (good for development)
Choose database [1/2]: 1

Include Docker support? [Y/n]: y

CI/CD options:
  1. GitHub Actions
  2. GitLab CI
  3. None
Choose CI/CD [1/2/3]: 1

==================================================
📝 Configuration Summary:
  • Project: ticket_system
  • Database: PostgreSQL
  • Docker: Yes
  • CI/CD: GitHub Actions
==================================================

Generate project with these settings? [Y/n]: y

⏳ Generating project...
✅ Successfully generated project in: /path/to/ticket_system

📖 Next steps:
  1. cd ticket_system
  2. make install
  3. make run

💡 See README.md for more details!
```

**Note:** The project is generated in a directory named after your project (in snake_case format):
- `MyAwesomeAPI` → `my_awesome_api/`
- `BrainROI` → `brain_roi/`
- `InvestWithMe` → `invest_with_me/`

## 📁 Generated Project Structure

```
my_awesome_api/                    # Your project directory
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── constants.py           # Global constants
│   │   └── database.py            # Database connection (SQLite/PostgreSQL)
│   └── my_awesome_api/            # Domain module (named after your project)
│       ├── __init__.py
│       ├── constants.py           # Module-specific constants
│       ├── dependencies.py        # FastAPI dependencies
│       ├── exceptions.py          # Custom exceptions
│       ├── models.py              # SQLAlchemy models
│       ├── repositories.py        # Data access layer
│       ├── router.py              # API endpoints
│       ├── schemas.py             # Pydantic schemas
│       └── services.py            # Business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── test_api.py                # API endpoint tests
│   └── test_services.py           # Service layer tests
├── .github/workflows/
│   └── ci.yml                     # GitHub Actions (if selected)
├── Dockerfile                     # Docker configuration (if selected)
├── docker-compose.yml             # Docker Compose (if selected)
├── Makefile                       # Common tasks
├── pyproject.toml                 # Project metadata
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

## 🛠️ Technologies Used

### Generator
- **[LangChain](https://python.langchain.com/)** - LLM orchestration framework
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Agent workflow management
- **[OpenAI GPT-4](https://openai.com/)** - AI-powered code generation
- **[Python 3.11+](https://www.python.org/)** - Programming language

### Generated Projects
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation
- **[Pytest](https://docs.pytest.org/)** - Testing framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[Docker](https://www.docker.com/)** - Containerization (optional)

## 💡 Examples

### Example 1: Simple API with SQLite

```bash
$ python -m fastapi_boilerplate_agent.cli

Project name: TodoAPI
Database: 2 (SQLite)
Docker: n
CI/CD: 3 (None)

✅ Successfully generated project in: /path/to/todo_api

$ cd todo_api
$ make install
$ make run
# API running at http://localhost:8000
```

### Example 2: Production-Ready API

```bash
$ python -m fastapi_boilerplate_agent.cli

Project name: EcommerceAPI
Database: 1 (PostgreSQL)
Docker: y
CI/CD: 1 (GitHub Actions)

✅ Successfully generated project in: /path/to/ecommerce_api

$ cd ecommerce_api
$ docker-compose up -d  # Start PostgreSQL
$ make install
$ make test            # Run tests
$ make run             # Start API
```

## 🎯 Use Cases

- **🚀 Rapid Prototyping**: Start a new FastAPI project in seconds
- **📚 Learning**: Study clean architecture patterns
- **💼 Enterprise**: Generate production-ready boilerplate
- **🔬 Experimentation**: Try different tech stacks quickly
- **📦 Microservices**: Quickly scaffold multiple services

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/martialo12/fastapi-boilerplate-agent.git
cd fastapi-boilerplate-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies (including dev)
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests

# Lint
flake8 src tests
```

### Ways to Contribute

- 🐛 Report bugs
- ✨ Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the project

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** community for the amazing framework
- **LangChain** team for the LLM orchestration tools
- All **contributors** who help improve this project

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/martialo12/fastapi-boilerplate-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/martialo12/fastapi-boilerplate-agent/discussions)
- **Email**: martialo218@gmail.com

## 🗺️ Roadmap

- [ ] PyPI package distribution
- [ ] Support for more databases (MySQL, MongoDB)
- [ ] Authentication templates (JWT, OAuth2)
- [ ] GraphQL support
- [ ] WebSocket examples
- [ ] Celery task queue integration
- [ ] Admin panel generation
- [ ] API versioning templates
- [ ] Multi-tenancy support
- [ ] Kubernetes deployment configs

## ❓ FAQ

**Q: Do I need an OpenAI API key?**  
A: Yes, the generator uses GPT-4 to intelligently create your project structure.

**Q: Can I customize the generated code?**  
A: Absolutely! The generated code is yours to modify as needed.

**Q: Is the generated code production-ready?**  
A: Yes, it follows best practices, but you should review and adjust for your specific needs.

**Q: What Python version is required?**  
A: Python 3.11 or higher for the generator. Generated projects use Python 3.11+.

**Q: Can I add more features to the generated project?**  
A: Yes! The generated structure is designed to be easily extended.

**Q: Is this free to use?**  
A: Yes, the generator is MIT licensed. You only pay for OpenAI API usage.

---

**Made with ❤️ by the FastAPI community**

⭐ Star us on GitHub if you find this project useful!
