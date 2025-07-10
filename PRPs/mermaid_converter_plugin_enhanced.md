name: "Enhanced Mermaid Converter Plugin for Dify Platform"
description: |

## Purpose
Complete implementation of a production-ready Dify plugin that converts Mermaid diagram code to image files (PNG/JPG/PDF/SVG) using the mermaid.ink API service with comprehensive error handling, retry logic, and advanced customization options.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Build a production-ready Dify plugin that accepts Mermaid diagram code as input and returns converted images in various formats using the mermaid.ink API with robust error handling, retry mechanisms, and comprehensive customization options.

## Why
- **Business value**: Enables users to generate visual diagrams programmatically within Dify workflows
- **Integration**: Seamlessly works with existing Dify agent and workflow systems  
- **Problems solved**: Eliminates manual diagram creation and provides automated visualization for AI agents
- **Production ready**: Includes proper error handling, logging, and resilience features

## What
A comprehensive Dify tool plugin that:
- Accepts Mermaid diagram code as string input
- Supports multiple output formats (PNG, JPG, PDF, SVG) with format-specific optimizations
- Includes configurable parameters for theme, background, size, and PDF options
- Returns image files as blob messages with proper mime types
- Handles errors gracefully with informative messages and retry logic
- Implements rate limiting and timeout handling for API stability
- Provides comprehensive logging for debugging and monitoring

### Success Criteria
- [ ] Plugin successfully converts valid Mermaid code to images in all formats
- [ ] Supports PNG, JPG, PDF, and SVG output formats with format-specific features
- [ ] Handles invalid Mermaid code with clear error messages
- [ ] Implements retry logic for transient API failures
- [ ] Includes proper logging for debugging and monitoring
- [ ] Follows exact Dify plugin architecture patterns from examples
- [ ] Plugin can be loaded and executed in Dify environment
- [ ] All validation gates pass without errors

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: https://docs.dify.ai/en/plugins/quick-start/develop-plugins/tool-plugin
  why: Official tool plugin development guide with complete patterns
  
- url: https://docs.dify.ai/en/plugins/schema-definition/tool
  why: Tool schema definition and parameter configuration syntax
  
- url: https://docs.dify.ai/en/plugins/best-practice/how-to-print-strings-to-logs-for-debugging
  why: Proper logging patterns and debugging approaches
  
- url: https://github.com/langgenius/dify-plugins
  why: Official plugin examples and implementation patterns
  
- url: https://github.com/langgenius/dify-official-plugins
  why: Production plugin examples with advanced patterns
  
- url: https://mermaid.ink/
  why: API endpoint structure and parameter documentation
  
- url: https://github.com/jihchi/mermaid.ink
  why: Implementation examples and base64 encoding patterns
  
- file: examples/your_plugin/tools/your_plugin.py
  why: Exact tool implementation pattern to follow
  
- file: examples/your_plugin/tools/your_plugin.yaml
  why: Tool configuration structure and parameter definitions
  
- file: examples/your_plugin/provider/your_plugin.py
  why: Provider validation pattern (simplified for mermaid.ink)
  
- file: examples/your_plugin/provider/your_plugin.yaml
  why: Provider configuration pattern
  
- file: examples/your_plugin/manifest.yaml
  why: Main plugin configuration structure
  
- file: examples/your_plugin/requirements.txt
  why: Dependency management (requests already included in dify_plugin)
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash
examples/your_plugin/
├── _assets/             # Icons and visual resources
│   └── icon.svg         # Plugin icon (NO CHANGES)
├── provider/            # Provider definitions and validation
│   ├── your_plugin.py   # Credential validation logic
│   └── your_plugin.yaml # Provider configuration
├── tools/               # Tool implementations
│   ├── your_plugin.py   # Tool functionality implementation
│   └── your_plugin.yaml # Tool parameters and description
├── main.py              # Entry file (NO CHANGES)
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation
├── PRIVACY.md           # PRIVACY (NO CHANGES)
└── requirements.txt     # Dependency list
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
examples/your_plugin/
├── _assets/             # Icons and visual resources (NO CHANGES)
│   └── icon.svg         # Plugin icon
├── provider/            # Provider definitions and validation
│   ├── mermaid_converter.py   # Empty validation - no credentials needed
│   └── mermaid_converter.yaml # Provider config - no API keys required
├── tools/               # Tool implementations
│   ├── mermaid_converter.py   # Main converter tool with retry logic and error handling
│   └── mermaid_converter.yaml # Tool parameters: mermaid_code, output_format, theme, etc.
├── main.py              # Entry file (NO CHANGES)
├── manifest.yaml        # Updated plugin name, description, and metadata
├── README.md            # Updated documentation with usage examples
├── PRIVACY.md           # PRIVACY (NO CHANGES)
└── requirements.txt     # Dependencies (requests already included)
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: mermaid.ink requires URL-safe base64 encoding of diagram code
# Use: base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
# NOT: base64.b64encode() - this will cause URL encoding issues

# CRITICAL: Dify Tool class requires Generator[ToolInvokeMessage] return type
# Must yield messages, not return them
# Pattern: yield self.create_blob_message(blob=data, meta={"mime_type": "image/png"})

# CRITICAL: Use self.create_blob_message() for image files with proper metadata
# Set exact mime_type: image/png, image/jpeg, application/pdf, image/svg+xml
# Set file_name: f"mermaid_diagram.{format}" for proper downloads

# CRITICAL: Always use logging with proper handler from dify_plugin
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)

# CRITICAL: HTTP timeouts and retries are essential for external API calls
# mermaid.ink can be slow for complex diagrams (30+ seconds)
# Implement exponential backoff: time.sleep((2 ** attempt) * random.uniform(0.5, 1.5))

# CRITICAL: requests library is already included in dify_plugin>=0.2.0
# Comment in requirements.txt shows: "dify_plugin contains Flask,Werkzeug,dpkt,gevent,httpx,pydantic_settings,pydantic,pyyaml,requests,socksio,tiktoken,yarl,packaging"
# No need to add requests separately

# GOTCHA: mermaid.ink returns different content-types and requires different URLs
# /img/ endpoint: supports ?type=png/jpeg/webp, returns image/jpeg by default
# /svg/ endpoint: returns image/svg+xml, no type parameter needed  
# /pdf/ endpoint: returns application/pdf, supports ?landscape&paper=a3&fit

# GOTCHA: Invalid Mermaid code returns HTTP 400 with error message in response body
# Large diagrams return HTTP 413 (Request Entity Too Large)
# Rate limiting returns HTTP 429 (Too Many Requests)
# Always check response.status_code AND response.text for error details

# GOTCHA: URL length limits for GET requests (~6-8KB)
# Base64 encoding increases size by ~33%
# Check encoded length before making request: len(encoded) < 6000

# GOTCHA: Dify plugin YAML parameter validation is strict
# type: must be exact match (string, number, boolean, select, secret-input)
# form: must be "llm" or "form" - case sensitive
# required: must be boolean true/false, not string

# GOTCHA: Plugin manifest.yaml requires exact matching
# author field must match between manifest.yaml and provider/*.yaml
# name field becomes plugin identifier - use snake_case

# CRITICAL: Generator must yield, never return
# Bad: return self.create_text_message("done")
# Good: yield self.create_text_message("done")
```

## Implementation Blueprint

### Data models and structure

Parameter validation and type definitions:
```python
# Tool parameters (from tool YAML)
class MermaidConverterParams:
    mermaid_code: str          # required - The Mermaid diagram syntax
    output_format: str         # optional - png/jpg/jpeg/svg/pdf, default 'png'
    theme: str                 # optional - default/dark/neutral/forest, default 'default'
    background_color: str      # optional - hex color or named color with !, default transparent
    width: int                 # optional - image width in pixels
    height: int                # optional - image height in pixels 
    scale: int                 # optional - scale factor 1-3, requires width/height
    # PDF-specific options
    paper_size: str           # optional - a3/a4/a5/letter, default 'a4'
    landscape: bool           # optional - PDF landscape orientation, default False
    fit_to_content: bool      # optional - PDF size fits diagram, default True

# Response types
mime_types = {
    "png": "image/png",
    "jpg": "image/jpeg", 
    "jpeg": "image/jpeg",
    "svg": "image/svg+xml",
    "pdf": "application/pdf"
}
```

### list of tasks to be completed to fullfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY examples/your_plugin/manifest.yaml:
  - CHANGE name from "your_plugin" to "mermaid_converter"
  - UPDATE label and description for mermaid diagram conversion
  - KEEP all permission settings as-is (tool, model, endpoint, app, storage enabled)
  - UPDATE plugins.tools reference to provider/mermaid_converter.yaml
  - CHANGE author to match your identity
  - VALIDATE YAML syntax after changes

Task 2:
CREATE examples/your_plugin/provider/mermaid_converter.py:
  - COPY exact pattern from: provider/your_plugin.py
  - CHANGE class name to MermaidConverterProvider  
  - IMPLEMENT empty _validate_credentials method (no API key needed)
  - ADD proper imports: typing.Any, ToolProvider, ToolProviderCredentialValidationError
  - KEEP exact method signature and exception handling pattern

Task 3:
CREATE examples/your_plugin/provider/mermaid_converter.yaml:
  - COPY exact pattern from: provider/your_plugin.yaml
  - CHANGE identity.name to "mermaid_converter"
  - CHANGE identity.author to match manifest.yaml
  - UPDATE label and description for mermaid conversion
  - REMOVE entire credentials_for_provider section (no API keys needed)
  - UPDATE tools reference to tools/mermaid_converter.yaml
  - SET extra.python.source to provider/mermaid_converter.py

Task 4:
CREATE examples/your_plugin/tools/mermaid_converter.yaml:
  - COPY exact pattern from: tools/your_plugin.yaml
  - CHANGE identity.name to "mermaid_converter"  
  - UPDATE labels and descriptions for mermaid conversion
  - DEFINE comprehensive parameters section with all mermaid options
  - SET proper parameter types, requirements, and validation
  - REFERENCE tools/mermaid_converter.py in extra.python.source

Task 5:
CREATE examples/your_plugin/tools/mermaid_converter.py:
  - COPY exact class structure from: tools/your_plugin.py
  - CHANGE class name to MermaidConverterTool
  - IMPLEMENT complete _invoke method with mermaid.ink API integration
  - ADD comprehensive error handling with retry logic
  - IMPLEMENT support for all output formats and customization options
  - ADD proper logging with dify_plugin logger
  - INCLUDE input validation and sanitization

Task 6:
UPDATE examples/your_plugin/README.md:
  - CHANGE title and description to mermaid converter
  - DOCUMENT all supported parameters and their effects
  - PROVIDE usage examples for different output formats
  - EXPLAIN supported Mermaid diagram types
  - ADD troubleshooting section for common issues

Task 7:
VALIDATE plugin structure and configuration:
  - CHECK all YAML files validate without syntax errors
  - VERIFY Python files import without ImportError
  - TEST basic plugin loading and parameter validation
  - CONFIRM all references and file paths are correct
```

### Per task pseudocode as needed added to each task

```python
# Task 5 - Complete tool implementation with production features
import base64
import time
import random
import logging
from collections.abc import Generator
from typing import Any, Optional

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.config.logger_format import plugin_logger_handler

# Setup logging using Dify pattern
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)

class MermaidConverterTool(Tool):
    """Converts Mermaid diagram code to images using mermaid.ink API."""
    
    # Constants for configuration
    MERMAID_INK_BASE_URL = "https://mermaid.ink"
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    MAX_ENCODED_SIZE = 6000  # URL length limit
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Main tool invocation method following exact Dify pattern.
        
        Args:
            tool_parameters: Dict containing user-provided parameters
            
        Yields:
            ToolInvokeMessage: Results or error messages
        """
        try:
            # PATTERN: Always validate input first (from Dify best practices)
            mermaid_code = tool_parameters.get("mermaid_code", "").strip()
            if not mermaid_code:
                yield self.create_text_message("Error: Mermaid code is required and cannot be empty")
                return
            
            # Extract and validate parameters with defaults
            output_format = tool_parameters.get("output_format", "png").lower()
            theme = tool_parameters.get("theme", "default")
            background_color = tool_parameters.get("background_color", "")
            width = tool_parameters.get("width")
            height = tool_parameters.get("height") 
            scale = tool_parameters.get("scale")
            paper_size = tool_parameters.get("paper_size", "a4")
            landscape = tool_parameters.get("landscape", False)
            fit_to_content = tool_parameters.get("fit_to_content", True)
            
            # Validate output format
            valid_formats = ["png", "jpg", "jpeg", "svg", "pdf"]
            if output_format not in valid_formats:
                yield self.create_text_message(f"Error: Invalid output format '{output_format}'. Supported: {valid_formats}")
                return
            
            logger.info(f"Converting Mermaid diagram to {output_format} format")
            
            # CRITICAL: Use URL-safe base64 encoding (not regular base64)
            try:
                encoded_diagram = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
            except Exception as e:
                yield self.create_text_message(f"Error: Failed to encode diagram: {str(e)}")
                return
            
            # Check encoded size to prevent URL length issues
            if len(encoded_diagram) > self.MAX_ENCODED_SIZE:
                yield self.create_text_message("Error: Diagram too large for API (>6KB encoded). Try simplifying the diagram.")
                return
            
            # PATTERN: Build URL based on format (from mermaid.ink documentation)
            url = self._build_api_url(encoded_diagram, output_format, theme, background_color, 
                                    width, height, scale, paper_size, landscape, fit_to_content)
            
            logger.info(f"Making request to mermaid.ink API: {url[:100]}...")
            
            # CRITICAL: HTTP request with retry logic and timeout
            image_data, mime_type = self._make_request_with_retry(url, output_format)
            
            # Generate appropriate filename
            filename = f"mermaid_diagram.{output_format}"
            
            # CRITICAL: Return as blob message with proper metadata
            yield self.create_blob_message(
                blob=image_data,
                meta={
                    "mime_type": mime_type, 
                    "file_name": filename
                }
            )
            
            logger.info(f"Successfully converted diagram to {output_format} ({len(image_data)} bytes)")
            
        except Exception as e:
            error_msg = f"Unexpected error during conversion: {str(e)}"
            logger.error(error_msg)
            yield self.create_text_message(error_msg)
    
    def _build_api_url(self, encoded_diagram: str, output_format: str, theme: str, 
                      background_color: str, width: Optional[int], height: Optional[int],
                      scale: Optional[int], paper_size: str, landscape: bool, 
                      fit_to_content: bool) -> str:
        """Build the complete API URL with parameters."""
        
        # PATTERN: Determine endpoint based on format
        if output_format == "svg":
            url = f"{self.MERMAID_INK_BASE_URL}/svg/{encoded_diagram}"
        elif output_format == "pdf":
            url = f"{self.MERMAID_INK_BASE_URL}/pdf/{encoded_diagram}"
        else:  # png, jpg, jpeg
            url = f"{self.MERMAID_INK_BASE_URL}/img/{encoded_diagram}"
        
        # Build query parameters
        params = []
        
        # Format-specific parameters
        if output_format in ["png", "jpg", "jpeg"]:
            params.append(f"type={output_format}")
            if theme and theme != "default":
                params.append(f"theme={theme}")
        
        # Common parameters
        if background_color:
            # Handle named colors with ! prefix
            if background_color.startswith("!"):
                params.append(f"bgColor={background_color}")
            else:
                # Assume hex color, remove # if present
                color = background_color.lstrip("#")
                params.append(f"bgColor={color}")
        
        if width:
            params.append(f"width={width}")
        if height:
            params.append(f"height={height}")
        if scale and width and height:
            params.append(f"scale={scale}")
        
        # PDF-specific parameters
        if output_format == "pdf":
            if paper_size != "a4":
                params.append(f"paper={paper_size}")
            if landscape:
                params.append("landscape")
            if fit_to_content:
                params.append("fit")
        
        # Add parameters to URL
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    def _make_request_with_retry(self, url: str, output_format: str) -> tuple[bytes, str]:
        """Make HTTP request with exponential backoff retry logic."""
        
        # Determine expected content type
        mime_types = {
            "png": "image/png",
            "jpg": "image/jpeg", 
            "jpeg": "image/jpeg",
            "svg": "image/svg+xml",
            "pdf": "application/pdf"
        }
        expected_mime_type = mime_types[output_format]
        
        last_exception = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, timeout=self.DEFAULT_TIMEOUT)
                
                if response.status_code == 200:
                    return response.content, expected_mime_type
                
                elif response.status_code == 400:
                    raise ValueError(f"Invalid Mermaid syntax or parameters: {response.text}")
                
                elif response.status_code == 413:
                    raise ValueError("Diagram too large for mermaid.ink API")
                
                elif response.status_code == 429:
                    # Rate limited - longer wait
                    if attempt < self.MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * 2 + random.uniform(1, 3)
                        logger.warning(f"Rate limited, waiting {wait_time:.1f}s before retry {attempt + 1}")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ValueError("Rate limit exceeded - try again later")
                
                elif 500 <= response.status_code < 600:
                    # Server error - retry with exponential backoff
                    if attempt < self.MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * random.uniform(0.5, 1.5)
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time:.1f}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ValueError(f"Server error {response.status_code}: {response.text}")
                
                else:
                    raise ValueError(f"HTTP {response.status_code}: {response.text}")
                
            except requests.Timeout as e:
                last_exception = e
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = (2 ** attempt) * random.uniform(0.5, 1.5)
                    logger.warning(f"Request timeout, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                    continue
                
            except requests.ConnectionError as e:
                last_exception = e
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = (2 ** attempt) * random.uniform(0.5, 1.5) 
                    logger.warning(f"Connection error, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                    continue
        
        # All retries failed
        if last_exception:
            raise ValueError(f"Request failed after {self.MAX_RETRIES} retries: {str(last_exception)}")
        else:
            raise ValueError(f"Request failed after {self.MAX_RETRIES} retries")
```

### Integration Points
```yaml
NO DATABASE CHANGES NEEDED

NO CONFIG CHANGES NEEDED - Using external API

EXTERNAL DEPENDENCIES:
  - requests library: Already included in dify_plugin>=0.2.0
  - No additional dependencies required
  
PLUGIN STRUCTURE:
  - modify: manifest.yaml (plugin metadata and tool references)
  - create: provider/mermaid_converter.py (provider validation class)
  - create: provider/mermaid_converter.yaml (provider configuration)
  - create: tools/mermaid_converter.py (main tool implementation)
  - create: tools/mermaid_converter.yaml (tool parameter definitions)
  - update: README.md (documentation and usage examples)
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Validate Python syntax and imports
python -c "
import sys; sys.path.append('examples/your_plugin')
try:
    from tools.mermaid_converter import MermaidConverterTool
    from provider.mermaid_converter import MermaidConverterProvider
    print('✓ All Python imports successful')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
except SyntaxError as e:
    print(f'✗ Syntax error: {e}')
    exit(1)
"

# Validate YAML syntax
python -c "
import yaml
files = [
    'examples/your_plugin/manifest.yaml',
    'examples/your_plugin/provider/mermaid_converter.yaml', 
    'examples/your_plugin/tools/mermaid_converter.yaml'
]
for file in files:
    try:
        with open(file) as f:
            yaml.safe_load(f)
        print(f'✓ {file} valid YAML')
    except yaml.YAMLError as e:
        print(f'✗ {file} YAML error: {e}')
        exit(1)
"

# Expected: All validations pass with ✓ messages
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns
```python
# CREATE test_mermaid_converter.py with comprehensive test cases:

def test_valid_mermaid_conversion_png():
    """Test successful PNG conversion with simple diagram."""
    tool = MermaidConverterTool()
    params = {
        "mermaid_code": "graph TD\n    A[Start] --> B[End]",
        "output_format": "png"
    }
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert hasattr(messages[0], 'blob')
    assert messages[0].meta['mime_type'] == 'image/png'
    assert messages[0].meta['file_name'] == 'mermaid_diagram.png'

def test_svg_format_conversion():
    """Test SVG format conversion."""
    tool = MermaidConverterTool()
    params = {
        "mermaid_code": "graph LR\n    A --> B --> C",
        "output_format": "svg"
    }
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert messages[0].meta['mime_type'] == 'image/svg+xml'

def test_pdf_format_with_options():
    """Test PDF format with landscape and paper size."""
    tool = MermaidConverterTool()
    params = {
        "mermaid_code": "graph TD\n    A --> B",
        "output_format": "pdf",
        "paper_size": "a3",
        "landscape": True
    }
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert messages[0].meta['mime_type'] == 'application/pdf'

def test_empty_mermaid_code_validation():
    """Test empty input validation."""
    tool = MermaidConverterTool()
    params = {"mermaid_code": ""}
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert "required" in messages[0].message.lower()

def test_invalid_output_format():
    """Test invalid format handling."""
    tool = MermaidConverterTool()
    params = {
        "mermaid_code": "graph TD\n    A --> B",
        "output_format": "invalid"
    }
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert "invalid output format" in messages[0].message.lower()

def test_theme_and_background_options():
    """Test theme and background customization."""
    tool = MermaidConverterTool()
    params = {
        "mermaid_code": "graph TD\n    A --> B",
        "output_format": "png",
        "theme": "dark",
        "background_color": "!white"
    }
    
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert messages[0].meta['mime_type'] == 'image/png'

def test_provider_validation():
    """Test provider credential validation (should be empty)."""
    provider = MermaidConverterProvider()
    # Should not raise any exceptions since no credentials needed
    try:
        provider._validate_credentials({})
    except Exception as e:
        assert False, f"Provider validation failed: {e}"
```

```bash
# Run manual validation with real API calls:
python -c "
from examples.your_plugin.tools.mermaid_converter import MermaidConverterTool
tool = MermaidConverterTool()
params = {
    'mermaid_code': 'graph TD\n    A[Start] --> B[Process] --> C[End]',
    'output_format': 'png'
}
messages = list(tool._invoke(params))
print(f'Result: {len(messages)} message(s)')
if messages and hasattr(messages[0], 'blob'):
    print(f'Success: Generated {len(messages[0].blob)} bytes of {messages[0].meta[\"mime_type\"]}')
else:
    print(f'Error: {messages[0].message if messages else \"No messages\"}')
"

# Expected: Success message with byte count and mime type
```

### Level 3: Integration Test
```bash
# Test plugin loading and configuration validation
python -c "
import yaml
import json

# Validate manifest structure
with open('examples/your_plugin/manifest.yaml') as f:
    manifest = yaml.safe_load(f)
    
required_fields = ['version', 'type', 'author', 'name', 'label', 'description', 'plugins']
for field in required_fields:
    assert field in manifest, f'Missing required field: {field}'
    
assert manifest['type'] == 'plugin'
assert manifest['name'] == 'mermaid_converter'
print('✓ Manifest validation passed')

# Validate provider configuration
with open('examples/your_plugin/provider/mermaid_converter.yaml') as f:
    provider = yaml.safe_load(f)
    
assert provider['identity']['name'] == 'mermaid_converter'
assert 'credentials_for_provider' not in provider  # No API keys
print('✓ Provider configuration valid')

# Validate tool configuration  
with open('examples/your_plugin/tools/mermaid_converter.yaml') as f:
    tool = yaml.safe_load(f)
    
assert tool['identity']['name'] == 'mermaid_converter'
assert 'parameters' in tool
required_params = ['mermaid_code']
for param in tool['parameters']:
    if param['name'] in required_params:
        assert param['required'] == True
print('✓ Tool configuration valid')
"

# Test actual API connectivity
curl -s "https://mermaid.ink/img/Z3JhcGggVEQKICAgIEFbU3RhcnRdIC0tPiBCW0VuZF0%3D" > /tmp/test_mermaid.jpg
if [ -s /tmp/test_mermaid.jpg ]; then
    echo "✓ mermaid.ink API connectivity confirmed"
    rm /tmp/test_mermaid.jpg
else
    echo "✗ mermaid.ink API not accessible"
fi

# Expected: All validations pass with ✓ messages
```

## Final validation Checklist
- [ ] All Python files import without ImportError or SyntaxError
- [ ] All YAML files validate as proper YAML syntax
- [ ] manifest.yaml contains correct plugin metadata and tool references
- [ ] Provider configuration matches identity requirements
- [ ] Tool configuration defines all required parameters correctly
- [ ] Manual test with simple mermaid diagram succeeds for PNG format
- [ ] Manual test with SVG format succeeds
- [ ] Manual test with PDF format succeeds
- [ ] Error cases handled gracefully (empty input, invalid format, large diagrams)
- [ ] Logging works correctly and appears in output
- [ ] mermaid.ink API connectivity confirmed
- [ ] All file references and paths are correct
- [ ] Plugin follows exact Dify architecture patterns

---

## Anti-Patterns to Avoid
- ❌ Don't use base64.b64encode() - use base64.urlsafe_b64encode() for URL safety
- ❌ Don't skip retry logic - mermaid.ink API can be unreliable
- ❌ Don't ignore HTTP status codes - check for 400/413/429/500 errors specifically
- ❌ Don't use requests without timeout - API can hang indefinitely  
- ❌ Don't return strings for images - use create_blob_message() with proper metadata
- ❌ Don't forget proper mime types - browsers need them for file handling
- ❌ Don't skip logging - essential for debugging external API calls
- ❌ Don't hardcode URLs or constants - use class constants for maintainability
- ❌ Don't ignore diagram size limits - check encoded length before API calls
- ❌ Don't use regular sleep() for retries - implement exponential backoff with jitter
- ❌ Don't skip parameter validation - validate all inputs before processing
- ❌ Don't ignore YAML syntax requirements - Dify plugin loading is strict

## Confidence Score: 10/10

Maximum confidence for one-pass implementation because:
✅ Complete external API implementation with comprehensive error handling  
✅ Exact Dify plugin patterns extracted from actual example files
✅ Production-ready retry logic with exponential backoff and jitter
✅ Comprehensive parameter validation and error scenarios covered
✅ All critical gotchas documented with specific solutions
✅ Executable validation steps that will catch any issues
✅ Complete implementation pseudocode with exact imports and patterns
✅ Real-world error handling for API timeouts, rate limits, and failures
✅ Format-specific URL building and parameter handling
✅ Proper logging integration using Dify's logging system

This PRP provides complete context for implementing a production-ready Mermaid converter plugin that will work reliably in the Dify environment.