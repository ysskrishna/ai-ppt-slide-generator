# Contributing to AI PPT Generator

Thank you for your interest in contributing to AI PPT Generator! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and considerate of others
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Be open to different viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment details (OS, Python version, Docker version, etc.)
- Any relevant error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and examples
- Any potential implementation ideas (optional)

### Pull Requests

1. **Fork the repository** and clone it locally
2. **Create a branch** for your changes:
   ```sh
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests if applicable

4. **Test your changes**:
   ```sh
   # Using Docker Compose
   docker-compose up --build
   
   # Or locally
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

5. **Commit your changes**:
   ```sh
   git commit -m "Add: description of your changes"
   ```
   Use clear, descriptive commit messages. Prefix with:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

6. **Push to your fork**:
   ```sh
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**:
   - Provide a clear title and description
   - Reference any related issues
   - Describe what changes you made and why
   - Include screenshots or examples if applicable

## Development Setup

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Git

### Setting Up the Development Environment

1. **Clone the repository**:
   ```sh
   git clone https://github.com/ysskrishna/ai-ppt-slide-generator.git
   cd ai-ppt-slide-generator
   ```

2. **Set up environment variables**:
   Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=postgresql://service_user:service_password@db:5432/presentation_db
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run with Docker Compose** (recommended):
   ```sh
   docker-compose up --build
   ```

4. **Or run locally**:
   ```sh
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

## Code Style Guidelines

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

## Project Structure

```
ai-ppt-slide-generator/
├── backend/
│   ├── core/          # Core configuration and utilities
│   ├── models/        # Database models and schemas
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic and services
│   └── main.py        # FastAPI application entry point
├── docker-compose.yml # Docker Compose configuration
└── README.md          # Project documentation
```

## Testing

When adding new features or fixing bugs:
- Test the API endpoints using the provided examples
- Verify that generated PPTX files are valid
- Test with different slide layouts and configurations
- Ensure database operations work correctly

## Questions?

If you have questions or need help, feel free to:
- Open an issue with the `question` label
- Check existing issues and discussions

Thank you for contributing to AI PPT Generator! 🎉

