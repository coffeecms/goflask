# Contributing to GoFlask

Thank you for your interest in contributing to GoFlask! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Performance Considerations](#performance-considerations)

## Code of Conduct

This project adheres to a code of conduct based on respect, inclusivity, and collaboration. By participating, you agree to uphold these values:

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive community environment
- Report any unacceptable behavior to the maintainers

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Go 1.21 or higher (for core development)
- Git for version control
- Basic understanding of Flask and Go

### Fork and Clone

1. Fork the GoFlask repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/goflask.git
   cd goflask
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/goflask/goflask.git
   ```

## Development Setup

### Python Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

### Go Environment

1. Ensure Go is installed and configured
2. Install Go dependencies:
   ```bash
   cd go-backend
   go mod download
   ```

3. Build the Go shared library:
   ```bash
   go build -buildmode=c-shared -o goflask.dll goflask_c_api.go
   ```

### Verification

Run the test suite to verify your setup:
```bash
python -m pytest tests/
```

## Making Changes

### Branching Strategy

1. Create a feature branch from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes in logical commits
3. Keep commits small and focused
4. Write clear commit messages

### Types of Contributions

#### Bug Fixes
- Fix identified issues
- Add regression tests
- Update documentation if needed

#### New Features
- Discuss major features in issues first
- Maintain Flask compatibility
- Consider performance implications
- Add comprehensive tests
- Update documentation

#### Performance Improvements
- Benchmark before and after changes
- Provide performance metrics
- Ensure no regression in functionality

#### Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify language

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core.py

# Run with coverage
python -m pytest --cov=goflask tests/

# Run performance tests
python -m pytest tests/performance/
```

### Writing Tests

1. Follow existing test patterns
2. Use descriptive test names
3. Include both positive and negative test cases
4. Test edge cases and error conditions
5. Add performance benchmarks for new features

### Test Structure
```python
def test_feature_description():
    """Test that feature works as expected"""
    # Arrange
    app = GoFlask(__name__)
    
    # Act
    result = app.some_method()
    
    # Assert
    assert result == expected_value
```

## Submitting Changes

### Pull Request Process

1. Ensure all tests pass
2. Update documentation as needed
3. Add yourself to CONTRIBUTORS.md
4. Submit a pull request with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes made
   - Testing performed

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing performed

## Documentation
- [ ] Documentation updated
- [ ] Examples added/updated
- [ ] Changelog updated

## Performance Impact
- [ ] No performance impact
- [ ] Performance improvement (include benchmarks)
- [ ] Potential performance regression (justified)
```

## Code Style

### Python Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for public functions
- Use meaningful variable names
- Keep line length under 88 characters

```python
def create_response(data: Dict[str, Any], status_code: int = 200) -> GoFlaskResponse:
    """
    Create a GoFlask response object.
    
    Args:
        data: Response data to serialize
        status_code: HTTP status code
        
    Returns:
        GoFlaskResponse object
    """
    return GoFlaskResponse(data, status_code)
```

### Go Code Style

- Follow Go standard formatting (use `gofmt`)
- Use meaningful function and variable names
- Add comments for exported functions
- Handle errors appropriately
- Follow Go best practices

```go
// CreateApp creates a new GoFlask application instance
func CreateApp(name string) *App {
    app := fiber.New(fiber.Config{
        ErrorHandler: defaultErrorHandler,
    })
    return &App{
        fiber: app,
        name:  name,
    }
}
```

### Formatting Tools

- Python: Use `black` and `isort` for formatting
- Go: Use `gofmt` and `goimports`
- Run formatters before committing:

```bash
# Python formatting
black goflask/
isort goflask/

# Go formatting
gofmt -w go-backend/
goimports -w go-backend/
```

## Documentation

### Documentation Standards

1. Write clear, concise documentation
2. Include code examples
3. Update README.md for significant changes
4. Add docstrings to new functions
5. Update API documentation

### Example Documentation

```python
def enable_cors(self, origins: List[str] = None, methods: List[str] = None) -> None:
    """
    Enable CORS middleware for cross-origin requests.
    
    This method configures Cross-Origin Resource Sharing (CORS) to allow
    web applications running at different domains to access this API.
    
    Args:
        origins: List of allowed origins. Defaults to ['*'] (all origins).
        methods: List of allowed HTTP methods. Defaults to all standard methods.
        
    Example:
        >>> app = GoFlask(__name__)
        >>> app.enable_cors(origins=['https://myapp.com'], methods=['GET', 'POST'])
        
    Note:
        For production use, specify explicit origins instead of using '*'.
    """
```

## Performance Considerations

### Performance Guidelines

1. Measure performance impact of changes
2. Use benchmarks for performance-critical code
3. Consider memory usage implications
4. Optimize for common use cases
5. Document performance characteristics

### Benchmarking

```python
import time
from goflask import GoFlask

def benchmark_request_handling():
    """Benchmark request handling performance"""
    app = GoFlask(__name__)
    
    @app.route('/test')
    def test_endpoint():
        return {'message': 'test'}
    
    start_time = time.time()
    # Simulate requests
    for _ in range(1000):
        # Measure request handling
        pass
    end_time = time.time()
    
    print(f"Handled 1000 requests in {end_time - start_time:.2f} seconds")
```

### Performance Targets

- Maintain 5x performance advantage over Flask
- Keep memory usage within 30% of Flask baseline
- Response times under 10ms for simple endpoints
- Support 1000+ concurrent connections

## Release Process

### Versioning

GoFlask follows Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Update documentation
5. Create release notes
6. Tag release in Git
7. Publish to PyPI

## Getting Help

### Resources

- Documentation: [docs](docs/)
- Examples: [examples](examples/)
- Issues: GitHub Issues
- Discussions: GitHub Discussions

### Contact

- Create an issue for bugs or feature requests
- Use discussions for questions and ideas
- Follow the project for updates

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Annual contributor highlights

Thank you for contributing to GoFlask! Your efforts help make high-performance web development accessible to the Python community.
