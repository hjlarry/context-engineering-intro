name: "Mermaid Converter Plugin for Dify Platform"
description: |

## Purpose
Complete implementation of a Dify plugin that converts Mermaid diagram code to image files (PNG/JPG/PDF) using the mermaid.ink API service.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Build a functional Dify plugin that accepts Mermaid diagram code as input and returns converted images in various formats (PNG, JPG, PDF, SVG) using the mermaid.ink API service.

## Why
- **Business value**: Enables users to generate visual diagrams programmatically within Dify workflows
- **Integration**: Seamlessly works with existing Dify agent and workflow systems
- **Problems solved**: Eliminates manual diagram creation and provides automated visualization for AI agents

## What
A Dify tool plugin that:
- Accepts Mermaid diagram code as string input
- Supports multiple output formats (PNG, JPG, PDF, SVG)
- Includes configurable parameters for image customization
- Returns image files as blob messages
- Handles errors gracefully with informative messages

### Success Criteria
- [ ] Plugin successfully converts valid Mermaid code to images
- [ ] Supports PNG, JPG, PDF, and SVG output formats
- [ ] Handles invalid Mermaid code with clear error messages
- [ ] Includes proper logging for debugging
- [ ] Follows Dify plugin architecture patterns
- [ ] Plugin can be loaded and executed in Dify environment

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: https://docs.dify.ai/plugin-dev-zh/0211-getting-started-by-prompt
  why: Core Dify plugin development patterns and tool implementation
  
- url: https://docs.dify.ai/plugin-dev-zh/9242-reverse-invocation-model
  why: LLM invocation patterns if needed for advanced features
  
- url: https://mermaid.ink/
  why: API endpoint structure and parameter documentation
  
- url: https://github.com/jihchi/mermaid.ink
  why: Implementation examples and base64 encoding patterns
  
- file: examples/your_plugin/tools/your_plugin.py
  why: Tool implementation pattern to follow exactly
  
- file: examples/your_plugin/tools/your_plugin.yaml
  why: Tool configuration structure and parameter definitions
  
- file: examples/your_plugin/provider/your_plugin.py
  why: Provider validation pattern (no API key needed for mermaid.ink)
  
- file: examples/your_plugin/provider/your_plugin.yaml
  why: Provider configuration pattern
  
- file: examples/your_plugin/manifest.yaml
  why: Main plugin configuration structure
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash
examples/your_plugin/
├── _assets/             # Icons and visual resources
├── provider/            # Provider definitions and validation
│   ├── your_plugin.py   # Credential validation logic
│   └── your_plugin.yaml # Provider configuration
├── tools/               # Tool implementations
│   ├── your_plugin.py   # Tool functionality implementation
│   └── your_plugin.yaml # Tool parameters and description
├── main.py              # Entry file
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation
├── PRIVACY.md           # PRIVACY
└── requirements.txt     # Dependency list
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
examples/your_plugin/
├── _assets/             # Icons and visual resources (NO CHANGES)
├── provider/            # Provider definitions and validation
│   ├── mermaid_converter.py   # No credentials needed - empty validation
│   └── mermaid_converter.yaml # Provider config - no API keys required
├── tools/               # Tool implementations
│   ├── mermaid_converter.py   # Main converter tool implementation
│   └── mermaid_converter.yaml # Tool parameters: mermaid_code, output_format, etc.
├── main.py              # Entry file (NO CHANGES)
├── manifest.yaml        # Updated plugin name and description
├── README.md            # Updated documentation
├── PRIVACY.md           # PRIVACY (NO CHANGES)
└── requirements.txt     # Add requests library
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: mermaid.ink requires base64 encoding of diagram code
# Example: base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')

# CRITICAL: Dify Tool class requires Generator[ToolInvokeMessage] return type
# Must yield messages, not return them

# CRITICAL: Use self.create_blob_message() for image files
# Set proper mime_type: image/png, image/jpeg, application/pdf, image/svg+xml

# CRITICAL: Always use logging with proper handler
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

# CRITICAL: HTTP timeouts are important for external API calls
# Default timeout should be 30 seconds

# GOTCHA: mermaid.ink returns different content-types based on endpoint
# /img/ returns image/jpeg by default
# /svg/ returns image/svg+xml
# /pdf/ returns application/pdf

# GOTCHA: Invalid Mermaid code returns HTTP 400 with error message
# Always check response.status_code before processing
```

## Implementation Blueprint

### Data models and structure

No complex data models needed - simple parameter validation:
```python
# Input validation
mermaid_code: str (required) - The Mermaid diagram code
output_format: str (optional) - png/jpg/pdf/svg, default 'png'
theme: str (optional) - default/dark/neutral/forest, default 'default'
background_color: str (optional) - hex color for background
width: int (optional) - image width
height: int (optional) - image height
```

### list of tasks to be completed to fullfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY examples/your_plugin/manifest.yaml:
  - CHANGE name from "your_plugin" to "mermaid_converter"
  - UPDATE label and description for mermaid conversion
  - KEEP all permission settings as-is
  - UPDATE tools reference to provider/mermaid_converter.yaml

Task 2:
MODIFY examples/your_plugin/requirements.txt:
  - ADD "requests>=2.31.0" for HTTP requests
  - KEEP existing dependencies if any

Task 3:
CREATE examples/your_plugin/provider/mermaid_converter.py:
  - COPY pattern from: provider/your_plugin.py
  - CHANGE class name to MermaidConverterProvider
  - EMPTY _validate_credentials method (no API key needed)

Task 4:
CREATE examples/your_plugin/provider/mermaid_converter.yaml:
  - COPY pattern from: provider/your_plugin.yaml
  - CHANGE identity name to "mermaid_converter"
  - REMOVE credentials_for_provider section (no API keys)
  - UPDATE tools reference to tools/mermaid_converter.yaml

Task 5:
CREATE examples/your_plugin/tools/mermaid_converter.py:
  - COPY pattern from: tools/your_plugin.py
  - CHANGE class name to MermaidConverterTool
  - IMPLEMENT _invoke method with mermaid.ink API calls
  - ADD proper error handling and logging
  - SUPPORT multiple output formats

Task 6:
CREATE examples/your_plugin/tools/mermaid_converter.yaml:
  - COPY pattern from: tools/your_plugin.yaml
  - DEFINE parameters for mermaid_code, output_format, theme, etc.
  - SET proper descriptions and validation rules
  - REFERENCE tools/mermaid_converter.py

Task 7:
UPDATE examples/your_plugin/README.md:
  - DOCUMENT the mermaid converter functionality
  - PROVIDE usage examples with different formats
  - EXPLAIN supported parameters and options
```

### Per task pseudocode as needed added to each task

```python
# Task 5 - Main tool implementation pseudocode
class MermaidConverterTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # PATTERN: Always validate input first
        mermaid_code = tool_parameters.get("mermaid_code", "").strip()
        if not mermaid_code:
            yield self.create_text_message("Error: Mermaid code is required")
            return
            
        output_format = tool_parameters.get("output_format", "png").lower()
        theme = tool_parameters.get("theme", "default")
        
        # CRITICAL: Base64 encode the mermaid code
        import base64
        encoded_diagram = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
        
        # PATTERN: Build URL based on format
        if output_format == "svg":
            url = f"https://mermaid.ink/svg/{encoded_diagram}"
        elif output_format == "pdf":
            url = f"https://mermaid.ink/pdf/{encoded_diagram}"
        else:  # png, jpg, jpeg
            url = f"https://mermaid.ink/img/{encoded_diagram}"
            url += f"?type={output_format}&theme={theme}"
        
        # CRITICAL: HTTP request with timeout
        try:
            import requests
            logger.info(f"Converting mermaid diagram to {output_format}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                error_msg = f"Conversion failed: HTTP {response.status_code}"
                logger.error(error_msg)
                yield self.create_text_message(error_msg)
                return
                
            # PATTERN: Determine mime type
            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg", 
                "jpeg": "image/jpeg",
                "svg": "image/svg+xml",
                "pdf": "application/pdf"
            }
            
            mime_type = mime_types.get(output_format, "image/png")
            filename = f"mermaid_diagram.{output_format}"
            
            # CRITICAL: Return as blob message
            yield self.create_blob_message(
                blob=response.content,
                meta={"mime_type": mime_type, "file_name": filename}
            )
            
            logger.info(f"Successfully converted diagram to {output_format}")
            
        except requests.Timeout:
            error_msg = "Conversion timeout - mermaid.ink took too long to respond"
            logger.error(error_msg)
            yield self.create_text_message(error_msg)
        except Exception as e:
            error_msg = f"Conversion error: {str(e)}"
            logger.error(error_msg)
            yield self.create_text_message(error_msg)
```

### Integration Points
```yaml
NO DATABASE CHANGES NEEDED

NO CONFIG CHANGES NEEDED - Using external API

EXTERNAL DEPENDENCIES:
  - add to: requirements.txt
  - pattern: "requests>=2.31.0"
  
PLUGIN STRUCTURE:
  - modify: manifest.yaml (plugin metadata)
  - create: provider/mermaid_converter.* (provider config)  
  - create: tools/mermaid_converter.* (tool implementation)
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# No Python linting tools specified in codebase
# Verify files can be imported without syntax errors
python -c "import examples.your_plugin.tools.mermaid_converter"
python -c "import examples.your_plugin.provider.mermaid_converter"

# Expected: No ImportError or SyntaxError
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns
```python
# CREATE test_mermaid_converter.py with these test cases:
def test_valid_mermaid_conversion():
    """Test successful mermaid conversion"""
    tool = MermaidConverterTool()
    params = {"mermaid_code": "graph TD\nA-->B"}
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert messages[0].type == "blob"

def test_empty_mermaid_code():
    """Test empty input validation"""
    tool = MermaidConverterTool()
    params = {"mermaid_code": ""}
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert "required" in messages[0].message.lower()

def test_different_output_formats():
    """Test PNG, SVG, PDF format support"""
    tool = MermaidConverterTool()
    formats = ["png", "svg", "pdf"]
    
    for fmt in formats:
        params = {"mermaid_code": "graph TD\nA-->B", "output_format": fmt}
        messages = list(tool._invoke(params))
        assert len(messages) == 1
        assert messages[0].type == "blob"
```

```bash
# Run manual validation since no test framework specified:
# Test with simple diagram:
# mermaid_code: "graph TD\nA[Start] --> B[End]"
# Expected: PNG image file returned as blob
```

### Level 3: Integration Test
```bash
# Test plugin loading in Dify environment
# Verify manifest.yaml is valid
python -c "import yaml; yaml.safe_load(open('examples/your_plugin/manifest.yaml'))"

# Test tool parameter validation
python -c "import yaml; yaml.safe_load(open('examples/your_plugin/tools/mermaid_converter.yaml'))"

# Manual API test
curl "https://mermaid.ink/img/Z3JhcGggVEQKQVtTdGFydF0gLS0+IEJbRW5kXQ"
# Expected: Image data returned
```

## Final validation Checklist
- [ ] All Python files import without errors
- [ ] manifest.yaml validates as proper YAML
- [ ] Tool YAML files validate as proper YAML  
- [ ] Manual test with simple mermaid diagram succeeds
- [ ] All output formats (PNG, SVG, PDF) work correctly
- [ ] Error cases handled gracefully (empty input, invalid diagrams)
- [ ] Logging works correctly for debugging
- [ ] Requirements.txt includes requests dependency

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode the mermaid.ink URL - use constants
- ❌ Don't skip base64 encoding - API requires it
- ❌ Don't ignore HTTP status codes - check for 400/500 errors  
- ❌ Don't use sync requests without timeout - API may be slow
- ❌ Don't return strings for images - use create_blob_message()
- ❌ Don't forget proper mime types for different formats
- ❌ Don't skip logging - essential for debugging external API calls

## Confidence Score: 9/10

High confidence for one-pass implementation because:
✅ Clear external API with simple base64 encoding
✅ Well-defined plugin structure to follow
✅ Straightforward HTTP request implementation  
✅ Comprehensive error handling patterns provided
✅ All necessary context and gotchas documented
✅ Validation steps are executable and clear

Minor risk: External API dependency could introduce edge cases, but error handling patterns should cover these scenarios.