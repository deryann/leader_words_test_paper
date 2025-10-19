# Word Test Paper Generator - AI Coding Agent Instructions

## Project Overview

A bilingual English word test paper generator that creates randomized vocabulary tests with two question types: **explain** (definition → word) and **statement** (fill-in-the-blank). Generates paired DOCX files (test + answer sheet) from JSON configurations. Supports CLI, GUI (tkinter), and Web (FastAPI) interfaces.

## Architecture (SOLID Principles)

This codebase was refactored from a monolithic `run.py` to follow SOLID principles. Key architectural pattern:

```
application.py (orchestrator)
    ↓ depends on interfaces (not implementations)
├── services.py (ConfigLoader, DocumentGenerator, FileManager, DataShuffler)
├── gui_manager.py (GUIManager, IconManager)
└── models.py (TestData, TestItem, TestPaperConfig, GeneratedFiles)
```

**Critical**: All components use **dependency injection** through `interfaces.py`. When extending functionality:
1. Define interface in `interfaces.py` (inherits `ABC`)
2. Implement in `services.py` or new module
3. Inject via `TestPaperApplication.__init__()`

See `REFACTORING_SUMMARY.md` for full SOLID implementation details.

## Configuration System

### Version-based Config Folders
- Active config version controlled by `CFG_VERSION` in `variables.py` (currently `"cfg-202509"`)
- Config folders: `cfg-202407/`, `cfg-202502/`, `cfg-202509/`
- **To switch versions**: Edit `CFG_VERSION` in `variables.py` - this changes the source for ALL interfaces (CLI, GUI, Web)

### JSON Schema
All config files follow this structure (see `from-text-to-cfg-spec.md`):
```json
{
  "explain": [["definition text", "target_word"], ...],
  "statement": [["Sentence with target_word.", "target_word"], ...]
}
```

**Critical validation**: In `statement` items, the `target_word` MUST appear verbatim in the sentence (case-sensitive, preserves tense/plurality). Generator replaces it with `__________________`.

## Running the Application

### Package Management: Use `uv` (not pip)
```powershell
# Install dependencies
uv sync --no-install-project

# Run CLI
uv run python run.py -i 2A-p01.json

# Run GUI
uv run python run.py --gui

# Run Web Server
uv run uvicorn app:app --reload
```

See `UV_USAGE.md` for complete `uv` workflows. Fallback to pip only if `uv sync` fails.

## Key Workflows

### Adding New Config Files
1. Place `.json` file in current `CFG_VERSION` folder (e.g., `cfg-202509/`)
2. Follow schema validation from `models.py` → `TestData.validate()`
3. Use `from-text-to-cfg-spec.md` as guide when converting raw text data

### Document Generation Pipeline
```
ConfigLoader.load_config() → TestData
    ↓
DataShuffler.shuffle_data() → shuffled TestData (seeded with current timestamp)
    ↓
DocumentGenerator.generate_test_paper() → GeneratedFiles
    ↓
Output: {basename}_test.docx, {basename}_test-{N}-ans.docx
```

**Filename collision handling**: Auto-increments counter (`-{N}`) if file exists. See `services.py:DocumentGenerator._generate_test_paper()` lines 132-161.

## Code Patterns

### Error Handling
- All custom exceptions inherit from `TestPaperGeneratorError` (see `exceptions.py`)
- Use specific exception types: `ConfigurationError`, `ValidationError`, `DocumentGenerationError`
- Validation happens at load time in `ConfigLoader.load_config()`, not during generation

### Document Formatting
Default settings in `TestPaperConfig` (`models.py`):
- Font: Comic Sans MS, 12pt
- Margins: 1cm (converted to inches: `1/2.54`)
- Headings: `["1st", "2nd"]` for explain/statement sections

When modifying formatting, edit `services.py:DocumentGenerator._apply_document_formatting()`.

### GUI Icon Management
Icons loaded from `icons/` folder:
- Requires PNG → ICO conversion via PIL/Pillow
- Handles Windows taskbar icon with `ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID()`
- See `gui_manager.py:IconManager` for implementation

## Web Interface (`app.py`)

FastAPI endpoints:
- `GET /` → Serves `static/index.html`
- `GET /api/configs` → Lists files from current `CFG_FOLDER`
- `GET /api/generate?config={filename}&format={docx|pdf}` → Generates files
- `GET /download/{filename}` → Downloads from `output/`

**PDF conversion**: Uses `pandoc` subprocess. Must be installed separately (https://pandoc.org/installing.html).

## Testing Conventions

No formal test suite yet, but validation occurs at:
1. `TestData.validate()` - Ensures word appears in statement text
2. `ConfigLoader.load_config()` - JSON schema validation
3. `DocumentGenerator` - File existence checks before saving

When adding tests, target `interfaces.py` abstractions for easy mocking.

## Dependencies

Core (see `pyproject.toml`):
- `python-docx` - DOCX generation (test/answer sheets)
- `fastapi` + `uvicorn` - Web interface
- `pillow` - Icon format conversion (optional)
- External: `pandoc` - PDF conversion (not Python package)

## Common Pitfalls

1. **Don't hardcode config paths** - Always use `CFG_FOLDER` from `variables.py`
2. **Word matching is case-sensitive** - `"Spanish"` in JSON won't match `"spanish"` in statement
3. **Shuffling uses timestamp seed** - Tests generated at same second will be identical
4. **File extensions auto-added** - Pass `"2A-p01"` not `"2A-p01.json"` to `ConfigLoader`
5. **Windows-specific printing** - Uses `os.startfile(filepath, "print")` in `application.py`

## Future Extensions

To add new output formats (PDF, HTML):
1. Create new interface in `interfaces.py` (e.g., `PDFGeneratorInterface`)
2. Implement in new service class
3. Inject into `TestPaperApplication` alongside `DocumentGenerator`
4. Both generators can consume the same shuffled `TestData`


## **Documentation Language:**

- All specifications, plans, and user-facing documentation MUST-be written in Traditional Chinese (zh-TW)
- Code comments and technical documentation MAY use English for technical clarity
- Commit messages and internal development notes MAY use English