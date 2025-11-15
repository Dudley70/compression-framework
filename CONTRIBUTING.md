# Contributing to Compression Framework

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/compression-framework.git
   cd compression-framework
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   pytest tests/test_compress.py -v
   ```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the existing code style:
- Use docstrings for functions
- Add type hints where helpful
- Keep functions focused and small
- Comment complex logic

### 3. Write Tests

All new features need tests:
```python
def test_your_feature():
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_output
```

### 4. Run Tests

```bash
# Run all tests
pytest tests/test_compress.py -v

# Run with coverage
pytest tests/test_compress.py --cov=compress_v7_hybrid

# Run specific test
pytest tests/test_compress.py::TestExtractSacredContent::test_single_prompt_extraction -v
```

### 5. Commit

Use clear commit messages:
```bash
git commit -m "feat: add batch processing support"
git commit -m "fix: handle edge case in prompt extraction"
git commit -m "docs: update README with new examples"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `perf:` Performance improvements

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to any related issues
- Test results showing all tests pass

---

## Areas for Contribution

### High Priority

1. **Size Tuning** (Issue #1)
   - Output is 27% larger than target
   - Need to tune V7 abbreviation rules
   - Test on multiple document types

2. **Structure Validation** (Issue #2)
   - Fix false positives in structure checks
   - Update regex patterns for score detection
   - Add more robust validation logic

3. **Model Name Validation** (Issue #3)
   - Validate model names against known models
   - Provide clear error messages for invalid models
   - Auto-suggest closest valid model

### Medium Priority

4. **Batch Processing** (Issue #4)
   - Process multiple documents in one run
   - Parallel processing support
   - Progress reporting

5. **Better Progress Reporting** (Issue #5)
   - Show compression ratio per step
   - ETA for long documents
   - Better verbose output

6. **Configuration Files** (Issue #6)
   - Save/load compression settings
   - Per-project configuration
   - Validation rules customization

### Low Priority

7. **Output Formats** (Issue #7)
   - JSON output option
   - HTML output with styling
   - Summary reports

8. **Documentation** (Issue #8)
   - More examples
   - Tutorial videos
   - API documentation

---

## Code Style

### Python Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

### Example

```python
def extract_sacred_content(document: str) -> dict:
    """
    Extract test prompts, code blocks, formulas from document.
    
    Args:
        document: Original markdown content
        
    Returns:
        Dictionary with sacred_items, modified_document, and counts
    """
    sacred_items = []
    # Implementation...
    return {
        "sacred_items": sacred_items,
        "modified_document": modified_doc,
        "count": counts
    }
```

---

## Testing Guidelines

### Test Structure

```python
class TestFeatureName:
    """Tests for feature_name functionality."""
    
    def test_basic_case(self):
        """Should handle basic input correctly."""
        # Test implementation
        
    def test_edge_case(self):
        """Should handle edge cases gracefully."""
        # Test implementation
        
    def test_error_case(self):
        """Should raise appropriate errors."""
        with pytest.raises(ValueError):
            # Test implementation
```

### Test Coverage

- Aim for >90% code coverage
- Test all public functions
- Test error handling
- Test edge cases

---

## Documentation Guidelines

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining purpose,
    behavior, and any important notes.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is negative
        
    Example:
        >>> function_name("test", 5)
        True
    """
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Installation instructions if dependencies change

---

## Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest tests/test_compress.py -v
   ```

2. **Update documentation**
   - README.md if user-facing changes
   - Docstrings for new functions
   - CHANGELOG.md with your changes

3. **Create PR with**:
   - Clear title: "feat: add batch processing"
   - Description of what changed and why
   - Link to related issues
   - Screenshots/examples if applicable

4. **Respond to review feedback**
   - Address all comments
   - Push updates to your branch
   - Mark conversations as resolved

---

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🎉
