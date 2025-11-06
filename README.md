# Compression Framework

**Version**: 1.0  
**Status**: Production Ready  
**Last Updated**: 2025-11-07

---

## What This Repository Contains

This is the **development repository** for the Compression Framework - a comprehensive system for optimizing LLM context windows through systematic documentation compression.

### For External Projects

**Want to use the framework in your project?**

👉 **Start here: [docs/README.md](docs/README.md)** - Framework overview and quick start

👉 **External adoption: [docs/EXTERNAL_PROJECT_GUIDE.md](docs/EXTERNAL_PROJECT_GUIDE.md)** - Complete adoption guide

**What you'll find:**
- Unified (σ,γ,κ) compression theory
- Decision framework for when/how to compress
- 8 ready-to-use templates
- Compression techniques catalog
- Empirical validation evidence
- Integration patterns and examples

---

### For Framework Development

**Working on the framework itself?**

👉 **Start here: [PROJECT.md](PROJECT.md)** - Strategic context and decisions

👉 **Current status: [SESSION.md](SESSION.md)** - Latest session state

**What you'll find:**
- Framework development history
- Tool implementation (compress.py)
- Test suite and validation
- Empirical research data
- Task specifications

---

## Repository Structure

```
Compression/
├── docs/                         # 📦 FRAMEWORK (for external projects)
│   ├── README.md                 # Framework overview
│   ├── EXTERNAL_PROJECT_GUIDE.md # Adoption guide
│   ├── THEORY.md                 # Unified (σ,γ,κ) model
│   ├── VALIDATION.md             # Empirical evidence
│   ├── reference/                # Decision framework & techniques
│   ├── guides/                   # Integration guide
│   ├── templates/                # 8 ready-to-use templates
│   ├── skills/                   # Claude Skill specification
│   └── research/                 # Research foundations
│
├── compress.py                   # 🔧 Production compression tool
├── scripts/                      # Development utilities
├── tests/                        # Test suite (145/145 passing)
│
├── PROJECT.md                    # 📋 Development: Strategic context
├── SESSION.md                    # 📋 Development: Current state
│
└── [Development artifacts]       # Validation reports, checkpoints, etc.
```

---

## Quick Links

### Using the Framework
- [Framework Overview](docs/README.md) - Start here for external projects
- [External Project Adoption Guide](docs/EXTERNAL_PROJECT_GUIDE.md) - Complete adoption pathway
- [Theory](docs/THEORY.md) - Unified compression model
- [Decision Framework](docs/reference/DECISION_FRAMEWORK.md) - When/how to compress
- [Techniques Catalog](docs/reference/TECHNIQUES.md) - All compression methods
- [Templates](docs/templates/) - Ready-to-use document templates

### Framework Development
- [PROJECT.md](PROJECT.md) - Strategic context
- [SESSION.md](SESSION.md) - Current session state
- [Validation Evidence](docs/VALIDATION.md) - Empirical results
- [Tool Documentation](compress.py) - Production tool

---

## Framework Highlights

**Unified Theory**: All compression techniques optimize three parameters (σ,γ,κ) subject to comprehension constraints.

**Empirical Validation**:
- ✅ 96.7% convergence (techniques self-stabilize)
- ✅ 70-85% token reduction (documentation)
- ✅ 95-99.5% reduction (conversations)
- ✅ Validated across 4 projects
- ✅ Quantified ROI (6:1 to 64:1 by team size)

**Production Ready**:
- Compression tool (862 lines, validated)
- 8 templates (high/medium compression)
- Claude Skill specification
- Complete integration guide
- 145/145 tests passing (100%)

---

## Original Methods

Both source methods developed by Dudley:

**LSC (LLM-Shorthand Context)**:
- Proactive documentation compression
- 70-85% token reduction
- Originally from Claude_Templates project

**CCM (Context Compression Method)**:
- Retrospective conversational compression  
- 99.5% reduction
- Originally from LettaSetup project

**This Framework**: Unifies both methods under (σ,γ,κ) theory with multi-dimensional decision framework and practical adoption resources.

---

## Getting Started

### As External Project
1. Read [docs/README.md](docs/README.md) (5 minutes)
2. Follow [docs/EXTERNAL_PROJECT_GUIDE.md](docs/EXTERNAL_PROJECT_GUIDE.md) (30 minutes)
3. Adapt templates to your project (2-4 hours)
4. Start using compressed documentation

### As Framework Developer
1. Read [PROJECT.md](PROJECT.md) - Strategic context
2. Read [SESSION.md](SESSION.md) - Current state
3. Check git log for recent work
4. See SESSION.md for next steps

---

## License & Attribution

All methods (LSC, CCM, Unified Framework) are original work by Dudley.

Framework is production-ready and available for adoption in other projects.

---

## Contact & Related Projects

**Project Location**: `/Users/dudley/Projects/Compression`

**Related Projects**:
- Claude_Templates: LSC origin
- LettaSetup: CCM origin  
- CC_Projects: Framework validation case study

---

**Framework ready for external adoption. Start with [docs/README.md](docs/README.md) or [docs/EXTERNAL_PROJECT_GUIDE.md](docs/EXTERNAL_PROJECT_GUIDE.md).**
