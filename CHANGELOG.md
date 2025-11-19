# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2025-01-20

### Changed
- Updated README with PyPI installation instructions as recommended option
- Added PyPI version and downloads badges
- Added quick install section for better user experience
- Reorganized installation options (PyPI first, source second)

## [0.2.1] - 2025-01-19

### Fixed
- Fixed PyPI deployment workflow to use correct secret name (PYPI_API_TOKEN_AGENT)

## [0.2.0] - 2025-01-19

### Added
- Project ready for open source release
- Comprehensive documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- MIT License
- Professional README with badges and examples
- Automated PyPI publishing with GitHub Actions
- CI/CD workflows for testing and deployment

### Added
- **Dynamic project naming**: Projects are now generated in directories named after the project (snake_case)
- **Comprehensive constants architecture**: Separated global and module-specific constants
- **Scalable database architecture**: Abstract base class with SQLite and PostgreSQL implementations
- **Singleton pattern** for database connections
- **Enhanced main.py**: Added startup events and root endpoint with API information
- **Pagination constants**: DEFAULT_SKIP, DEFAULT_LIMIT, MAX_LIMIT
- **API documentation constants**: Comprehensive descriptions for all fields

### Changed
- Improved database connection management with proper pooling
- Enhanced code structure with better separation of concerns
- Updated templates to be fully dynamic based on project name

### Fixed
- Connection pool configuration for PostgreSQL
- Project structure naming consistency

## [0.1.0] - 2025-01-XX

### Added
- **Interactive CLI** with user-friendly prompts (like create-react-app)
- Support for PostgreSQL and SQLite databases
- Optional Docker and docker-compose configuration
- CI/CD support (GitHub Actions or GitLab CI)
- **Clean architecture** implementation:
  - Repository pattern for data access
  - Service layer for business logic
  - Router layer for API endpoints
  - Dependency injection with FastAPI
- **Complete project structure**:
  - FastAPI application with example endpoints
  - SQLAlchemy models and migrations setup
  - Pydantic schemas for validation
  - Pytest configuration with example tests
  - Makefile for common tasks
- **LangChain/LangGraph integration** for intelligent code generation
- Configuration summary and confirmation before generation
- Smart defaults for quick setup

### Technical Details
- Built with Python 3.11+
- Uses OpenAI GPT-4 for code generation
- LangGraph for agent workflow management
- Pydantic for configuration validation

## [0.0.1] - 2024-XX-XX

### Added
- Initial proof of concept
- Basic FastAPI boilerplate generation
- Simple CLI interface
- Minimal project structure

---

## Version History Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## Upgrade Guide

### From 0.1.0 to 0.2.0

No breaking changes. New features are additive.

**New features available:**
- Project directories are now named after your project
- Enhanced database architecture with better pooling
- More comprehensive constants for API documentation

**Action required:**
- None - fully backward compatible

## Future Releases

### Planned for 0.3.0
- PyPI package distribution
- MySQL database support
- Authentication templates (JWT, OAuth2)
- More CI/CD options

### Planned for 0.4.0
- GraphQL support
- WebSocket examples
- Celery task queue integration
- Admin panel generation

### Planned for 1.0.0
- Stable API
- Complete test coverage
- Full documentation
- Production battle-tested

---

For more details on each release, see the [GitHub Releases](https://github.com/martialo12/fastapi-boilerplate-agent/releases) page.
