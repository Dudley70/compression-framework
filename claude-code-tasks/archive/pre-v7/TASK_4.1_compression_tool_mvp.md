# Claude Code Task: Compression Tool MVP (Task 4.1)

**Task ID**: TASK-4.1-COMPRESSION-TOOL-MVP  
**Priority**: HIGH (Critical Path)  
**Estimated Time**: 6-10 hours  
**Approach**: TDD with checkpoint system  
**Dependencies**: Tasks 1.1, 1.2, 2.1, 2.2, 2.3 (all complete)

---

## Project Context

This is part of a compression research project that has developed a unified theory for AI context optimization. All compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints:

- **σ (Structure)**: Structural density (0=prose → 1=data)
- **γ (Granularity)**: Semantic detail level (0=keywords → 1=full detail)  
- **κ (Scaffolding)**: Contextual explanation (0=none → 1=full context)

**Current Phase**: Tool Development - building automation to apply validated compression methods safely.

**Previous Validation**: All critical safety mechanisms validated with 70/70 tests passing:
- Compression scoring (6 metrics)
- Token drift detection
- Round-trip idempotency
- Content analysis (section-level)
- Multi-layered safety checks (4 layers)

**This Task's Role**: Build MVP Python CLI tool that safely compresses markdown documents using validated components.

---

## Objective

Create production-ready compression automation tool that:
1. Analyzes document compression state and recommends techniques
2. Applies LSC compression methods with safety validation
3. Provides multi-metric validation reporting
4. Integrates all validated safety components
5. Enables empirical testing of framework predictions

**Core Problem**: Manual compression is time-intensive and error-prone. Need automation that maintains safety while providing measurable benefits.

**Solution**: Python CLI tool integrating compression scoring, safety validation, and technique application with comprehensive reporting.

---

## Architecture Overview

### Tool Components
```
compress.py (main CLI)
├── Document Analysis (TASK-1.1)
│   ├── Compression state detection
│   ├── Section-level analysis
│   └── Technique recommendations
├── Safety Validation (TASK-2.3)
│   ├── Pre-check (already compressed)
│   ├── Entity preservation (80%)
│   ├── Minimal benefit (15% reduction)
│   └── Semantic similarity (75%)
├── Compression Application
│   ├── LSC technique implementation
│   ├── Section-aware processing
│   └── Preserve document structure
├── Validation & Reporting (TASK-2.1, TASK-1.2)
│   ├── Compression score (6 metrics)
│   ├── Token drift detection
│   └── Round-trip verification
└── Output Generation
    ├── Compressed document
    ├── Validation report
    └── Recommendation summary
```

### Integration Requirements
- **analyze_compression_state.py**: Document analysis and recommendations
- **safety_checks.py**: Multi-layered safety validation
- **compression_score.py**: 6-metric scoring algorithm
- **detect_token_drift.py**: Token growth detection
- **mock_compressor.py**: Round-trip test patterns (reference)

---

## LSC Compression Techniques

The tool implements 5 core LSC techniques validated in the framework:

### 1. Lists & Tables (σ↑)
**Target**: Verbose prose descriptions
**Method**: Convert to structured lists or tables
**Safety**: Preserve all information, verify entity completeness
**Example**:
```
Before: "The system supports three authentication methods. First, there's 
OAuth2 which provides secure delegation. Second, API keys offer simple 
programmatic access. Third, JWT tokens enable stateless authentication."

After:
**Auth Methods**:
- OAuth2: Secure delegation
- API Keys: Programmatic access  
- JWT: Stateless auth
```

### 2. Hierarchical Structure (σ↑)
**Target**: Flat or poorly organized content
**Method**: Add headers, nested lists, clear hierarchy
**Safety**: Maintain logical relationships, preserve meaning
**Example**:
```
Before: "The API has several endpoints. GET /users returns user list. 
POST /users creates user. GET /users/:id returns single user..."

After:
## User Endpoints
### Retrieval
- `GET /users` - List all
- `GET /users/:id` - Get one
### Modification  
- `POST /users` - Create
- `PUT /users/:id` - Update
```

### 3. Remove Redundancy (γ↓)
**Target**: Repetitive explanations, examples
**Method**: State once, eliminate duplicates
**Safety**: Keep one clear instance, verify no unique info lost
**Example**:
```
Before: "OAuth2 is secure. OAuth2 prevents token theft. OAuth2 uses 
delegation. The OAuth2 standard provides secure authentication through 
delegation and prevents token theft..."

After: "OAuth2: Secure authentication via delegation, prevents token theft"
```

### 4. Technical Shorthand (κ↓)
**Target**: Overly explained technical concepts
**Method**: Use standard abbreviations, assume domain knowledge
**Safety**: Only compress well-known terms, preserve critical details
**Example**:
```
Before: "HyperText Transfer Protocol Secure (HTTPS) provides encrypted 
communication over the network using Transport Layer Security (TLS)..."

After: "HTTPS: Encrypted communication via TLS"
```

### 5. Information Density (σ↑ γ↑)
**Target**: Low-density prose
**Method**: Pack more meaning per token
**Safety**: Verify comprehension preserved, check entity retention
**Example**:
```
Before: "When you are making a request to the API endpoint, you need to 
make sure that you include the authentication header in your request..."

After: "API requests require authentication header"
```

---

## TDD Approach

### Phase 1: Test Infrastructure (Checkpoint 1)

**Goal**: Create comprehensive test suite before implementation

**Test Categories**:
1. **Document Analysis Tests**
   - Detect compression state (uncompressed, partially compressed, fully compressed)
   - Identify applicable techniques per section
   - Generate appropriate recommendations
   - Handle edge cases (empty, malformed, mixed state)

2. **Compression Application Tests**
   - Apply each LSC technique correctly
   - Preserve document structure (headers, code blocks, links)
   - Handle section boundaries appropriately
   - Maintain markdown syntax validity

3. **Safety Integration Tests**
   - Pre-check detects already compressed content
   - Entity preservation blocks dangerous loss
   - Minimal benefit rejects insufficient compression
   - Semantic similarity catches meaning drift

4. **Validation & Reporting Tests**
   - Compression score calculated correctly (6 metrics)
   - Token drift detected accurately
   - Round-trip verification passes
   - Reports generated with all required metrics

5. **End-to-End Tests**
   - Full compression workflow completes
   - Multiple sections handled independently
   - Error cases handled gracefully
   - Output files written correctly

**Deliverable**: Complete test suite (tests/test_compress_tool.py) with 30+ tests

**Validation Criteria**:
- All test cases defined with expected inputs/outputs
- Test fixtures created for real-world scenarios
- Tests initially fail (TDD red phase)
- Clear assertions for each safety mechanism

**Checkpoint 1 Complete When**:
- [ ] Test file exists with 30+ test cases
- [ ] Test fixtures created (5+ example documents)
- [ ] All tests initially fail (expected for TDD)
- [ ] Checkpoint report documents test coverage
- [ ] pytest runs successfully (all tests skip/fail appropriately)

---

### Phase 2: Core Implementation (Checkpoint 2)

**Goal**: Implement compression tool to pass all tests

**Components to Build**:

#### 1. CLI Interface (compress.py)
```python
# Command structure:
# python compress.py analyze <input_file>     # Analysis only, no compression
# python compress.py compress <input_file>    # Full compression with safety
# python compress.py validate <original> <compressed>  # Validation only

# Flags:
# --dry-run              # Show what would be compressed
# --force               # Skip safety checks (dangerous, log warning)
# --output <file>       # Custom output path
# --report <file>       # Save validation report
# --verbose            # Detailed progress logging
```

#### 2. Document Analyzer Integration
```python
from analyze_compression_state import CompressionStateAnalyzer

class CompressionTool:
    def __init__(self):
        self.analyzer = CompressionStateAnalyzer()
        self.safety = SafetyValidator()
    
    def analyze_document(self, file_path: str) -> AnalysisResult:
        """Analyze document and recommend techniques"""
        # Uses TASK-1.1 analyzer
        # Returns section-level recommendations
        # Identifies compression opportunities
```

#### 3. LSC Technique Implementations
```python
class LSCTechniques:
    def apply_lists_tables(self, text: str) -> str:
        """Convert prose to structured lists/tables"""
        # Pattern detection for list-suitable content
        # Preserve information while restructuring
        # Maintain markdown formatting
    
    def apply_hierarchical_structure(self, text: str) -> str:
        """Add/improve document hierarchy"""
        # Analyze existing structure
        # Add appropriate headers
        # Create nested organization
    
    def remove_redundancy(self, text: str) -> str:
        """Eliminate duplicate information"""
        # Detect semantic duplicates
        # Preserve unique information
        # Maintain clarity
    
    def apply_technical_shorthand(self, text: str) -> str:
        """Use standard abbreviations"""
        # Known term dictionary
        # Context-appropriate compression
        # Preserve critical details
    
    def increase_information_density(self, text: str) -> str:
        """Pack more meaning per token"""
        # Remove filler words
        # Condense phrasing
        # Maintain comprehension
```

#### 4. Safety Validation Integration
```python
from safety_checks import SafetyValidator

def compress_with_safety(self, original: str, compressed: str) -> ValidationResult:
    """Apply compression with safety checks"""
    # Run SafetyValidator from TASK-2.3
    # Check all 4 layers
    # Return detailed validation results
    # Block unsafe compressions
```

#### 5. Multi-Metric Validation
```python
from compression_score import calculate_compression_score
from detect_token_drift import detect_token_drift

def validate_compression(self, original: str, compressed: str) -> ValidationReport:
    """Generate comprehensive validation report"""
    # Compression score (6 metrics)
    # Token drift detection
    # Safety validation results
    # Round-trip verification status
    # Recommendation summary
```

#### 6. Report Generation
```python
class ValidationReport:
    """Structured validation output"""
    
    def __init__(self, original, compressed, safety_result, score, drift):
        self.original_tokens = count_tokens(original)
        self.compressed_tokens = count_tokens(compressed)
        self.compression_ratio = compressed_tokens / original_tokens
        self.safety_passed = safety_result.passed
        self.safety_warnings = safety_result.warnings
        self.compression_score = score
        self.token_drift = drift
    
    def to_markdown(self) -> str:
        """Generate markdown report"""
        # Summary section
        # Detailed metrics
        # Safety analysis
        # Recommendations
    
    def to_json(self) -> dict:
        """Generate JSON for automation"""
```

**Implementation Requirements**:
- Preserve markdown structure (headers, code blocks, links, lists)
- Handle section boundaries correctly
- Maintain document metadata
- Process multi-section documents independently
- Generate detailed progress logging

**Deliverable**: Working compress.py tool with all components

**Validation Criteria**:
- All 30+ tests passing
- Safety integration working correctly
- Reports generated accurately
- CLI interface functional
- Error handling comprehensive

**Checkpoint 2 Complete When**:
- [ ] compress.py implemented (400+ lines)
- [ ] All test cases passing
- [ ] Safety checks integrated
- [ ] Reports generated correctly
- [ ] Checkpoint report shows test results
- [ ] pytest shows 100% pass rate

---

### Phase 3: Real-World Validation (Checkpoint 3)

**Goal**: Test tool on actual project documentation

**Test Documents** (use from project):
1. PROJECT.md - Strategic documentation (moderate compression)
2. docs/research/lsc/LSC_CONTEXT_EFFICIENCY.md - Technical reference (high structure)
3. docs/analysis/information-preservation-framework.md - Analytical document
4. SESSION.md - Session notes (conversational, may have compression opportunities)
5. validation_report_task_2.3.md - Technical report (already well-structured)

**Validation Process**:
1. Run analysis on each document
2. Apply compression with safety checks
3. Generate validation reports
4. Verify safety mechanisms work correctly
5. Measure actual compression ratios
6. Compare predictions to results

**Success Criteria**:
- Tool runs without errors on all documents
- Safety checks correctly refuse inappropriate compression
- Compression ratios match predictions (±5%)
- No information loss detected
- Reports provide actionable insights
- Performance acceptable (<30 seconds per document)

**Expected Outcomes**:
- Some documents compressed (meeting safety criteria)
- Some documents refused (already compressed or insufficient benefit)
- Some documents warned (edge cases requiring review)
- Comprehensive validation data collected

**Deliverable**: Real-world validation report

**Validation Criteria**:
- Tested on 5+ real documents
- All safety mechanisms verified
- Compression ratios documented
- Performance metrics collected
- Edge cases handled appropriately

**Checkpoint 3 Complete When**:
- [ ] 5+ documents tested
- [ ] All safety mechanisms validated
- [ ] No false negatives detected
- [ ] Validation report generated
- [ ] Checkpoint report documents results
- [ ] Tool ready for broader use

---

## Detailed Test Cases

### Test Suite Structure

```python
# tests/test_compress_tool.py

import pytest
from compress import CompressionTool, LSCTechniques, ValidationReport

class TestDocumentAnalysis:
    """Test document analysis and recommendations"""
    
    def test_detect_uncompressed_document(self):
        """Identify verbose prose needing compression"""
        tool = CompressionTool()
        result = tool.analyze_document("tests/fixtures/verbose_prose.md")
        assert result.compression_score < 0.4
        assert "lists_tables" in result.recommended_techniques
    
    def test_detect_already_compressed(self):
        """Recognize highly structured documents"""
        tool = CompressionTool()
        result = tool.analyze_document("tests/fixtures/already_compressed.md")
        assert result.compression_score >= 0.8
        assert result.recommended_techniques == []
    
    def test_section_level_analysis(self):
        """Analyze each section independently"""
        tool = CompressionTool()
        result = tool.analyze_document("tests/fixtures/mixed_state.md")
        assert len(result.sections) > 1
        assert any(s.needs_compression for s in result.sections)
        assert any(not s.needs_compression for s in result.sections)
    
    def test_technique_recommendations(self):
        """Recommend appropriate LSC techniques"""
        tool = CompressionTool()
        result = tool.analyze_document("tests/fixtures/flat_list.md")
        assert "hierarchical_structure" in result.recommended_techniques
        assert "lists_tables" in result.recommended_techniques

class TestLSCTechniques:
    """Test individual compression technique application"""
    
    def test_lists_tables_conversion(self):
        """Convert prose to structured lists"""
        lsc = LSCTechniques()
        original = "The API supports three methods: GET for retrieval, POST for creation, DELETE for removal."
        result = lsc.apply_lists_tables(original)
        assert "- GET:" in result or "GET:" in result
        assert "retrieval" in result.lower()
        assert len(result) < len(original)
    
    def test_hierarchical_structure_addition(self):
        """Add headers to flat content"""
        lsc = LSCTechniques()
        original = "First topic content here. Second topic content here."
        result = lsc.apply_hierarchical_structure(original)
        assert result.count("#") >= 2  # Headers added
    
    def test_redundancy_removal(self):
        """Eliminate duplicate information"""
        lsc = LSCTechniques()
        original = "OAuth2 is secure. OAuth2 prevents theft. OAuth2 is secure authentication."
        result = lsc.remove_redundancy(original)
        assert result.count("OAuth2") < original.count("OAuth2")
        assert "secure" in result.lower()
        assert "prevents theft" in result.lower() or "theft" in result.lower()
    
    def test_technical_shorthand(self):
        """Use standard abbreviations"""
        lsc = LSCTechniques()
        original = "HyperText Transfer Protocol Secure (HTTPS) with Transport Layer Security (TLS)"
        result = lsc.apply_technical_shorthand(original)
        assert "HTTPS" in result
        assert "TLS" in result
        assert len(result) < len(original)
    
    def test_information_density(self):
        """Increase meaning per token"""
        lsc = LSCTechniques()
        original = "When you are making a request, you need to include the header."
        result = lsc.increase_information_density(original)
        assert "request" in result.lower()
        assert "header" in result.lower()
        assert len(result) < len(original)
    
    def test_preserve_code_blocks(self):
        """Never compress code blocks"""
        lsc = LSCTechniques()
        original = "Example code:\n```python\nprint('hello')\n```\nThis code prints hello."
        result = lsc.apply_lists_tables(original)
        assert "```python" in result
        assert "print('hello')" in result
    
    def test_preserve_links(self):
        """Maintain markdown links"""
        lsc = LSCTechniques()
        original = "See [documentation](https://example.com) for more details about the system."
        result = lsc.increase_information_density(original)
        assert "[documentation](https://example.com)" in result

class TestSafetyIntegration:
    """Test safety validation integration"""
    
    def test_precheck_blocks_compressed(self):
        """Pre-check refuses already compressed"""
        tool = CompressionTool()
        original = open("tests/fixtures/already_compressed.md").read()
        compressed = "Even more compressed version"
        result = tool.compress_with_safety(original, compressed)
        assert not result.passed
        assert "pre-check" in result.failure_reason.lower()
    
    def test_entity_preservation_blocks_loss(self):
        """Entity check refuses dangerous loss"""
        tool = CompressionTool()
        original = "The API uses OAuth2, JWT, and HTTPS with TLS encryption. Configure via .env file."
        compressed = "The system uses security."
        result = tool.compress_with_safety(original, compressed)
        assert not result.passed
        assert "entity" in result.failure_reason.lower()
    
    def test_minimal_benefit_blocks_insufficient(self):
        """Minimal benefit check refuses small gains"""
        tool = CompressionTool()
        original = "A" * 1000  # 1000 tokens
        compressed = "A" * 900  # Only 10% reduction
        result = tool.compress_with_safety(original, compressed)
        assert not result.passed
        assert "minimal benefit" in result.failure_reason.lower()
    
    def test_semantic_similarity_blocks_drift(self):
        """Semantic check catches meaning changes"""
        tool = CompressionTool()
        original = "Authentication is required for all API endpoints."
        compressed = "Authentication is optional for API endpoints."
        result = tool.compress_with_safety(original, compressed)
        assert not result.passed
        assert "semantic" in result.failure_reason.lower()
    
    def test_safe_compression_passes(self):
        """Valid compression passes all checks"""
        tool = CompressionTool()
        original = "When making requests to the API, you need to include authentication headers in every request."
        compressed = "API requests require authentication headers."
        result = tool.compress_with_safety(original, compressed)
        assert result.passed
        assert len(result.warnings) == 0

class TestValidationReporting:
    """Test validation and report generation"""
    
    def test_compression_score_calculated(self):
        """Compression score uses 6-metric algorithm"""
        tool = CompressionTool()
        original = "verbose prose text"
        compressed = "concise text"
        report = tool.validate_compression(original, compressed)
        assert report.compression_score is not None
        assert 0 <= report.compression_score <= 1
    
    def test_token_drift_detected(self):
        """Token drift detection identifies growth"""
        tool = CompressionTool()
        original = "A" * 100
        # Simulate drift by expanding  
        compressed = "A" * 150
        report = tool.validate_compression(original, compressed)
        assert report.token_drift.growth_detected
    
    def test_report_markdown_generation(self):
        """Markdown report contains all metrics"""
        tool = CompressionTool()
        original = "test content here"
        compressed = "test content"
        report = tool.validate_compression(original, compressed)
        markdown = report.to_markdown()
        assert "Token Count" in markdown
        assert "Compression Ratio" in markdown
        assert "Safety Validation" in markdown
        assert "Compression Score" in markdown
    
    def test_report_json_generation(self):
        """JSON report has structured data"""
        tool = CompressionTool()
        original = "test content here"
        compressed = "test content"
        report = tool.validate_compression(original, compressed)
        json_data = report.to_json()
        assert "original_tokens" in json_data
        assert "compressed_tokens" in json_data
        assert "safety_passed" in json_data
        assert "compression_score" in json_data

class TestCLIInterface:
    """Test command-line interface"""
    
    def test_analyze_command(self, tmp_path):
        """Analyze command shows recommendations"""
        test_file = tmp_path / "test.md"
        test_file.write_text("verbose content here that needs compression")
        result = run_cli(f"analyze {test_file}")
        assert result.returncode == 0
        assert "Recommended Techniques" in result.stdout
    
    def test_compress_command(self, tmp_path):
        """Compress command creates output"""
        test_file = tmp_path / "test.md"
        test_file.write_text("verbose content here")
        output_file = tmp_path / "test_compressed.md"
        result = run_cli(f"compress {test_file} --output {output_file}")
        assert result.returncode == 0
        assert output_file.exists()
    
    def test_dry_run_flag(self, tmp_path):
        """Dry run shows changes without applying"""
        test_file = tmp_path / "test.md"
        test_file.write_text("verbose content")
        result = run_cli(f"compress {test_file} --dry-run")
        assert result.returncode == 0
        assert "Would compress" in result.stdout
        # Original file unchanged
        assert test_file.read_text() == "verbose content"
    
    def test_report_generation(self, tmp_path):
        """Report flag saves validation report"""
        test_file = tmp_path / "test.md"
        test_file.write_text("content")
        report_file = tmp_path / "report.md"
        result = run_cli(f"compress {test_file} --report {report_file}")
        assert report_file.exists()
        report_content = report_file.read_text()
        assert "Compression Score" in report_content

class TestEndToEnd:
    """Test complete workflows"""
    
    def test_full_compression_workflow(self, tmp_path):
        """Complete analysis → compress → validate flow"""
        # Create test document
        test_doc = tmp_path / "document.md"
        test_doc.write_text("This is a very verbose document with lots of prose...")
        
        # Analyze
        tool = CompressionTool()
        analysis = tool.analyze_document(str(test_doc))
        assert len(analysis.recommended_techniques) > 0
        
        # Compress
        compressed = tool.compress_file(str(test_doc))
        assert len(compressed) < len(test_doc.read_text())
        
        # Validate
        report = tool.validate_compression(test_doc.read_text(), compressed)
        assert report.safety_passed
        
        # Save
        output = tmp_path / "compressed.md"
        output.write_text(compressed)
        assert output.exists()
    
    def test_multi_section_document(self, tmp_path):
        """Handle documents with multiple sections"""
        content = """# Section 1
Verbose prose here that needs compression.

# Section 2  
Already compressed: API endpoints, configs, structured content.

# Section 3
More verbose content requiring compression."""
        
        test_doc = tmp_path / "multi.md"
        test_doc.write_text(content)
        
        tool = CompressionTool()
        analysis = tool.analyze_document(str(test_doc))
        
        # Should identify mixed compression state
        assert len(analysis.sections) == 3
        compressed_sections = [s for s in analysis.sections if not s.needs_compression]
        needs_compression = [s for s in analysis.sections if s.needs_compression]
        assert len(compressed_sections) >= 1
        assert len(needs_compression) >= 1
    
    def test_error_handling_malformed(self, tmp_path):
        """Handle malformed documents gracefully"""
        test_doc = tmp_path / "malformed.md"
        test_doc.write_text("```python\nunclosed code block")
        
        tool = CompressionTool()
        # Should not crash, should return error
        try:
            result = tool.compress_file(str(test_doc))
            # If it succeeds, should preserve structure
            assert "```python" in result
        except Exception as e:
            # If it fails, should be graceful
            assert "malformed" in str(e).lower() or "parse" in str(e).lower()
```

---

## Test Fixtures

Create test fixtures in `tests/fixtures/` for real-world scenarios:

### 1. verbose_prose.md
```markdown
# API Documentation

When you want to make a request to our API, you need to first obtain an API key. The API key can be obtained by going to the developer portal and creating a new application. Once you have created the application, you will be able to see your API key in the application settings.

After you have obtained your API key, you need to include it in the Authorization header of your HTTP requests. The format for the authorization header is "Bearer" followed by a space and then your API key.

The API supports three different types of requests. The first type is GET requests, which are used for retrieving data. The second type is POST requests, which are used for creating new resources. The third type is DELETE requests, which are used for deleting existing resources.
```

### 2. already_compressed.md
```markdown
# API Quick Reference

## Authentication
**Required**: Bearer token in `Authorization` header
**Obtain**: Developer portal → Create app → Copy key

## Endpoints
### Data Operations
- `GET /api/resource` - Retrieve list
- `POST /api/resource` - Create new  
- `DELETE /api/resource/:id` - Remove

### Headers
```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

## Rate Limits
- 1000 req/hour (authenticated)
- 100 req/hour (anonymous)
```

### 3. mixed_state.md
```markdown
# Project Overview

This document contains a mix of verbose and compressed content to test section-level analysis.

## Introduction

When working with our compression framework, it's important to understand that there are many different approaches you can take. Some sections of your documentation might already be well-structured and concise, while other sections might contain verbose prose that would benefit from compression techniques.

## Technical Stack
- Python 3.9+
- spaCy (NER)
- sentence-transformers (embeddings)
- tiktoken (tokenization)
- pytest (testing)

## Implementation Details

The implementation follows a multi-layered approach where we first analyze the document to understand its current compression state. Then we identify which sections would benefit from compression. After that, we apply appropriate compression techniques while ensuring that safety checks are performed. Finally, we validate the results and generate a comprehensive report.

## Dependencies
**Core**:
- markdown-it-py: Parse/generate markdown
- spacy: en_core_web_sm model  
- sentence-transformers: all-MiniLM-L6-v2

**Dev**:
- pytest: Testing framework
- black: Code formatting
```

### 4. entity_heavy.md  
```markdown
# Technology Stack Documentation

The application uses React for the frontend framework, with Redux for state management and React Router for navigation. The backend is built with Node.js using the Express.js framework. For the database, we use PostgreSQL with the Sequelize ORM. Authentication is handled through OAuth2 using the passport.js library with JWT tokens. The application is deployed on AWS using EC2 instances behind an ELB load balancer, with RDS for the database and S3 for static assets. Monitoring is done through CloudWatch and Datadog.

Configuration is managed through environment variables defined in .env files. The .env.production file contains the production database URL, AWS credentials including AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, and API keys for third-party services. Development uses .env.development with local database settings.
```

### 5. semantic_test.md
```markdown
# Security Requirements

All API endpoints must validate authentication tokens before processing requests. Rate limiting is required to prevent abuse. Input validation must sanitize all user-provided data. HTTPS is mandatory for all communications. Password storage must use bcrypt with minimum 10 salt rounds.
```

---

## Success Criteria

### Must Pass (Critical)
- [ ] All 30+ tests passing (100% success rate)
- [ ] Safety integration working (blocks unsafe compression)
- [ ] LSC techniques implemented correctly (all 5)
- [ ] CLI interface functional (analyze, compress, validate commands)
- [ ] Reports generated accurately (markdown + JSON)
- [ ] Real-world validation successful (5+ documents)
- [ ] No information loss detected in any test
- [ ] Performance acceptable (<30s per document)

### Should Pass (Important)
- [ ] Section-level analysis working
- [ ] Multi-section documents handled correctly
- [ ] Error handling comprehensive
- [ ] Progress logging informative
- [ ] Dry-run mode accurate
- [ ] Output formatting consistent

### Nice to Have (Optional)
- [ ] Batch processing support
- [ ] Configuration file support
- [ ] Plugin architecture for custom techniques
- [ ] Web UI preview (future enhancement)

---

## Deliverables

### Code Files
1. **compress.py** (400-600 lines)
   - CLI interface
   - Document analyzer integration
   - LSC technique implementations
   - Safety validation integration
   - Report generation

2. **tests/test_compress_tool.py** (600-800 lines)
   - 30+ comprehensive test cases
   - Unit tests for each component
   - Integration tests for workflows
   - End-to-end scenarios

3. **tests/fixtures/** (5+ files)
   - verbose_prose.md
   - already_compressed.md
   - mixed_state.md
   - entity_heavy.md
   - semantic_test.md

### Documentation
4. **checkpoints/checkpoint_1_tool_tests.md**
   - TDD Phase 1 completion
   - Test coverage summary
   - Fixture descriptions

5. **checkpoints/checkpoint_2_tool_impl.md**
   - Implementation completion
   - Test results summary
   - Component descriptions

6. **checkpoints/checkpoint_3_tool_validated.md**
   - Real-world validation results
   - Performance metrics
   - Safety verification

7. **validation_report_task_4.1.md**
   - Final validation report
   - Tool capabilities summary
   - Deployment readiness assessment
   - Next steps recommendations

### Integration Artifacts
8. **README_compress_tool.md**
   - Usage instructions
   - Example commands
   - Configuration options
   - Troubleshooting guide

---

## Technical Requirements

### Python Version
- Python 3.9 or higher
- Virtual environment recommended

### Dependencies (requirements.txt)
```
# Core compression
markdown-it-py>=3.0.0
spacy>=3.7.0
sentence-transformers>=2.2.0
tiktoken>=0.5.0
scikit-learn>=1.3.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# CLI
click>=8.1.0
rich>=13.0.0  # Optional: Better CLI formatting

# Existing validated components (local imports)
# - analyze_compression_state.py (TASK-1.1)
# - safety_checks.py (TASK-2.3)
# - compression_score.py (TASK-2.1)
# - detect_token_drift.py (TASK-1.2)
```

### spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Performance Requirements
- Document analysis: <5 seconds
- Compression application: <15 seconds
- Validation reporting: <10 seconds
- Total per document: <30 seconds
- Memory usage: <1GB per process

### Error Handling
- Graceful handling of malformed markdown
- Clear error messages for safety failures
- File I/O error handling
- Logging for debugging
- Recovery from component failures

---

## Implementation Notes

### Integration with Existing Components

**From TASK-1.1 (Content Analyzer)**:
```python
from analyze_compression_state import CompressionStateAnalyzer

analyzer = CompressionStateAnalyzer()
result = analyzer.analyze_document(file_path)
# Returns: compression_score, sections, recommended_techniques
```

**From TASK-2.3 (Safety Checks)**:
```python
from safety_checks import SafetyValidator

validator = SafetyValidator()
result = validator.validate_compression(original, compressed)
# Returns: passed, warnings, failure_reasons
```

**From TASK-2.1 (Compression Score)**:
```python
from compression_score import calculate_compression_score

score = calculate_compression_score(text)
# Returns: float 0.0-1.0 (higher = more compressed)
```

**From TASK-1.2 (Token Drift)**:
```python
from detect_token_drift import detect_token_drift

drift = detect_token_drift(original, compressed)
# Returns: DriftResult with growth_detected, metrics
```

### LSC Implementation Strategy

Each LSC technique should:
1. **Pattern Detection**: Identify sections that would benefit
2. **Safe Transformation**: Apply technique while preserving meaning
3. **Structure Preservation**: Maintain markdown validity
4. **Validation**: Verify no information loss

**Example Pattern**:
```python
def apply_lists_tables(self, text: str) -> str:
    """Convert prose to structured lists"""
    # 1. Detect prose patterns that describe lists
    # 2. Extract items and their descriptions
    # 3. Format as markdown list
    # 4. Preserve any non-list content
    # 5. Return transformed text
```

### Markdown Preservation Rules

**Never Modify**:
- Code blocks (```...```)
- Inline code (`...`)
- URLs and links ([text](url))
- Images (![alt](url))
- HTML comments (<!-- ... -->)
- Front matter (---)

**Preserve Structure**:
- Header hierarchy (# ## ###)
- List nesting and ordering
- Table formatting
- Blockquotes (>)
- Horizontal rules (---)

### Section Boundary Detection

Documents should be processed at section level:
- Split on headers (# ## ### etc.)
- Analyze each section independently
- Apply techniques per-section
- Rejoin maintaining structure
- Preserve section relationships

### Safety Decision Logic

```python
def should_compress(analysis, safety_result):
    """Determine if compression should proceed"""
    
    # Pre-check failure: immediate refuse
    if not safety_result.pre_check_passed:
        return False, "Already compressed"
    
    # Count safety failures
    failures = sum([
        not safety_result.entity_preservation_passed,
        not safety_result.minimal_benefit_passed,
        not safety_result.semantic_similarity_passed
    ])
    
    if failures == 0:
        return True, "All safety checks passed"
    elif failures == 1:
        return "warn", f"Warning: {safety_result.warning_reason}"
    else:
        return False, f"Multiple safety failures: {safety_result.failure_reasons}"
```

---

## Testing Strategy

### Unit Test Coverage
- Each LSC technique independently
- Safety check integration points
- Report generation functions
- CLI command parsing
- File I/O operations

### Integration Test Coverage
- Full compression workflow
- Multi-section document handling
- Safety validation integration
- Report generation end-to-end

### Real-World Test Coverage
- Project documentation (PROJECT.md, SESSION.md)
- Technical references (LSC framework, validation reports)
- Mixed compression states
- Edge cases (empty, malformed, already compressed)

### Test Execution
```bash
# Run all tests
pytest tests/test_compress_tool.py -v

# Run with coverage
pytest tests/test_compress_tool.py --cov=compress --cov-report=html

# Run specific test class
pytest tests/test_compress_tool.py::TestSafetyIntegration -v

# Run with detailed output
pytest tests/test_compress_tool.py -vv --tb=short
```

---

## Validation Checklist

### Checkpoint 1: Tests Written ✓
- [ ] Test file created with 30+ test cases
- [ ] Test fixtures created (5+ documents)
- [ ] All tests initially fail (TDD red phase)
- [ ] Test coverage documented in checkpoint report
- [ ] pytest runs without errors (tests skip/fail appropriately)

### Checkpoint 2: Implementation Complete ✓
- [ ] compress.py implemented (400+ lines)
- [ ] All test cases passing (100% success)
- [ ] LSC techniques working correctly
- [ ] Safety integration verified
- [ ] Reports generated accurately
- [ ] CLI commands functional
- [ ] Checkpoint report shows test results

### Checkpoint 3: Real-World Validated ✓
- [ ] Tested on 5+ project documents
- [ ] Safety mechanisms verified in practice
- [ ] Performance meets requirements (<30s/doc)
- [ ] No false negatives detected
- [ ] Compression ratios measured
- [ ] Edge cases handled appropriately
- [ ] Final validation report complete

---

## Expected Outcomes

### Tool Capabilities
- **Analysis**: Identify compression opportunities per section
- **Application**: Apply LSC techniques safely with validation
- **Safety**: Block dangerous compression, warn on edge cases
- **Reporting**: Generate comprehensive validation reports
- **CLI**: User-friendly command-line interface

### Empirical Data Collection
- Compression ratios for different document types
- Safety check effectiveness (false positive/negative rates)
- Performance metrics per document
- Technique applicability patterns
- Framework prediction validation

### Production Readiness
- Comprehensive test coverage (30+ tests)
- Safety validation integrated (4-layer system)
- Error handling complete
- Performance acceptable
- Documentation thorough
- Ready for CC_Projects application

---

## Next Phase Preview

**After Task 4.1 Completes**, the tool will be ready for:

1. **Claude Code Skill Wrapper** (Task 4.2)
   - Progressive disclosure interface
   - Session context integration
   - Interactive compression workflow

2. **Empirical Validation** (Task 5.x)
   - Apply to CC_Projects documentation
   - Measure framework predictions vs actuals
   - Collect compression effectiveness data

3. **White Paper Development** (Task 6.x)
   - Mathematical formalization with evidence
   - Empirical results section
   - Publication-quality documentation

**This task creates the foundation for all subsequent work by providing a safe, validated, production-ready compression automation tool.**

---

## Common Pitfalls to Avoid

1. **Over-compression**: Don't sacrifice clarity for compression ratio
2. **Ignoring Safety**: Never bypass safety checks without explicit user override
3. **Breaking Markdown**: Preserve code blocks, links, images
4. **Information Loss**: Verify entity preservation always
5. **Poor Error Messages**: Provide actionable feedback on failures
6. **Performance Issues**: Cache model loading, optimize token counting
7. **Inconsistent Output**: Maintain consistent formatting patterns
8. **Incomplete Testing**: Test edge cases, malformed input, error paths

---

**Task Status**: READY FOR EXECUTION
**Confidence Level**: HIGH (comprehensive specification, proven patterns)
**Risk Level**: LOW (all safety mechanisms validated, TDD approach)

**🎯 GO/NO-GO**: ✅ GO - Specification complete, dependencies validated, success criteria clear