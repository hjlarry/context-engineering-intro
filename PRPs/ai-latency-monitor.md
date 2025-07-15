name: "AI Platform Latency Monitor - Dify Extension Plugin"
description: |

## Purpose
Comprehensive PRP for implementing a Dify platform endpoint plugin that creates a web-based AI platform latency monitoring tool. This plugin will display real-time response times for multiple AI platforms and show IP geolocation information.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Build a Dify extension plugin that serves a website displaying real-time latency monitoring for popular AI platforms (OpenAI, Azure OpenAI, Google Gemini, DeepSeek) with IP geolocation information and user-configurable platform additions.

## Why
- **Monitoring Value**: Provides real-time visibility into AI platform performance for developers and system administrators
- **Integration with Dify**: Leverages Dify's plugin ecosystem to provide monitoring capabilities
- **Performance Insights**: Helps users choose optimal AI platforms based on latency characteristics
- **Operational Awareness**: Enables proactive identification of performance issues across multiple AI services

## What
A web-based monitoring dashboard that:
- Tests latency to 4 required AI platforms with configurable test prompts
- Displays real-time response times with historical data visualization
- Shows current server IP location information
- Allows users to add custom AI platforms via configuration
- Provides REST API endpoints for programmatic access
- Includes proper logging and error handling following Dify standards

### Success Criteria
- [ ] Plugin successfully loads in Dify environment
- [ ] Website displays latency data for all 4 required AI platforms
- [ ] Users can configure API keys through Dify plugin settings
- [ ] IP geolocation information is accurately displayed
- [ ] Response times are measured and displayed in milliseconds
- [ ] Plugin follows all Dify platform conventions and standards
- [ ] Error handling gracefully manages API failures and timeouts
- [ ] Logging captures key metrics and debugging information

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://docs.dify.ai/plugin-dev-en/9231-extension-plugin
  why: Dify plugin development standards, structure, configuration requirements
  critical: Plugin must follow exact manifest.yaml structure and endpoint patterns

- url: https://platform.openai.com/docs/guides/latency-optimization
  why: OpenAI API latency measurement best practices
  critical: Use time.time() for precise timing, handle rate limits and timeouts

- url: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/latency
  why: Azure OpenAI specific latency metrics and optimization techniques
  critical: Different API endpoints may have different latency characteristics

- url: https://ai.google.dev/gemini-api/docs/quickstart
  why: Google Gemini API integration patterns and client setup
  critical: Streaming vs non-streaming affects latency measurements

- url: https://api-docs.deepseek.com/
  why: DeepSeek API documentation and OpenAI-compatible interface
  critical: Uses OpenAI SDK but with different base_url

- file: examples/your_plugin/manifest.yaml
  why: Exact Dify plugin structure and configuration pattern to follow
  critical: Must preserve structure, only modify specific values

- file: examples/your_plugin/endpoints/your_extension.py  
  why: Dify endpoint implementation pattern with Request/Response handling
  critical: Class inheritance from Endpoint, _invoke method signature

- file: examples/your_plugin/group/your_extension.yaml
  why: Plugin settings configuration for API keys and user inputs
  critical: Secret-input type for API keys, proper internationalization
```

### Current Codebase tree
```bash
/root/context-engineering-intro/
├── examples/
│   └── your_plugin/
│       ├── PRIVACY.md
│       ├── README.md
│       ├── endpoints/
│       │   ├── your_extension.py
│       │   └── your_extension.yaml
│       ├── group/
│       │   └── your_extension.yaml
│       ├── manifest.yaml
│       └── requirements.txt
├── PRPs/
│   └── templates/
│       └── prp_base.md
├── CLAUDE.md
├── INITIAL.md
└── README.md
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
/root/context-engineering-intro/
├── examples/
│   └── your_plugin/  # MODIFY: Transform into AI latency monitor
│       ├── PRIVACY.md          # UPDATE: Privacy policy for AI monitoring
│       ├── README.md           # UPDATE: Documentation for latency monitor
│       ├── endpoints/
│       │   ├── ai_monitor.py   # CREATE: Main endpoint serving web dashboard
│       │   ├── ai_monitor.yaml # UPDATE: Endpoint configuration
│       │   └── static/         # CREATE: Static web assets
│       │       ├── index.html  # CREATE: Main dashboard HTML
│       │       ├── style.css   # CREATE: Dashboard styling
│       │       └── script.js   # CREATE: Frontend logic & AJAX calls
│       ├── group/
│       │   └── ai_monitor.yaml # UPDATE: Plugin settings for API keys
│       ├── manifest.yaml       # UPDATE: Plugin metadata and config
│       └── requirements.txt    # UPDATE: Add required dependencies
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: Dify plugin requires exact manifest.yaml structure
# Example: Must have version, type, author, plugins.endpoints structure

# CRITICAL: Endpoint class must inherit from dify_plugin.Endpoint  
# Example: class AiMonitorEndpoint(Endpoint): def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:

# CRITICAL: Use proper logging pattern as specified in INITIAL.md
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)

# CRITICAL: OpenAI SDK works for DeepSeek with base_url change
# Example: OpenAI(api_key="deepseek_key", base_url="https://api.deepseek.com")

# CRITICAL: Azure OpenAI requires specific client configuration
# Example: AzureOpenAI(api_key=key, api_version="2024-02-01", azure_endpoint=endpoint)

# CRITICAL: Time measurement must be precise for latency monitoring
# Example: start_time = time.time(); response = api_call(); latency = (time.time() - start_time) * 1000

# CRITICAL: Error handling must be robust for API timeouts and failures
# Example: Always use try/except with specific exception types, implement retry logic

# CRITICAL: IP geolocation libraries need proper API key management
# Example: Use requests library with external services like ipapi.co or ipinfo.io

# CRITICAL: Dify plugin settings must use secret-input type for API keys
# Example: type: secret-input in group YAML configuration
```

## Implementation Blueprint

### Data models and structure
```python
# Core data structures for latency monitoring
from dataclasses import dataclass
from typing import Optional, Dict, List
import time

@dataclass
class LatencyResult:
    platform: str
    response_time_ms: float
    success: bool
    error_message: Optional[str] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

@dataclass 
class IPInfo:
    ip: str
    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    
@dataclass
class MonitoringState:
    latency_results: Dict[str, List[LatencyResult]]
    ip_info: Optional[IPInfo] = None
    last_update: float = None
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1:
UPDATE examples/your_plugin/manifest.yaml:
  - MODIFY name from "your_extension" to "ai_latency_monitor"
  - MODIFY label entries to "AI Latency Monitor"
  - MODIFY description to describe latency monitoring functionality
  - MODIFY author to appropriate value
  - KEEP all existing structure and required fields

Task 2:
UPDATE examples/your_plugin/group/your_extension.yaml to ai_monitor.yaml:
  - RENAME file from your_extension.yaml to ai_monitor.yaml
  - ADD API key settings for OpenAI, Azure OpenAI, Gemini, DeepSeek
  - ADD optional settings for custom platforms
  - USE secret-input type for all API keys
  - MAINTAIN internationalization structure

Task 3:
UPDATE examples/your_plugin/requirements.txt:
  - ADD openai>=1.0.0 for OpenAI and DeepSeek APIs
  - ADD azure-openai for Azure OpenAI integration  
  - ADD google-generativeai for Gemini API
  - ADD requests for HTTP calls and IP geolocation
  - KEEP existing dify_plugin dependency

Task 4:
CREATE examples/your_plugin/endpoints/static/ directory structure:
  - CREATE static/index.html for main dashboard
  - CREATE static/style.css for modern responsive styling
  - CREATE static/script.js for frontend logic and real-time updates

Task 5:
RENAME AND REWRITE examples/your_plugin/endpoints/your_extension.py to ai_monitor.py:
  - INHERIT from Endpoint class properly
  - IMPLEMENT _invoke method handling both web serving and API endpoints
  - ADD AILatencyTester class for testing each platform
  - ADD IPGeolocator class for IP information retrieval
  - IMPLEMENT proper error handling and logging
  - SERVE static files for dashboard and provide JSON API endpoints

Task 6:
UPDATE examples/your_plugin/endpoints/your_extension.yaml to ai_monitor.yaml:
  - MODIFY path to appropriate endpoint path
  - UPDATE source reference to new Python file
  - KEEP GET method for web dashboard access

Task 7:
UPDATE examples/your_plugin/README.md:
  - WRITE comprehensive documentation for AI latency monitor
  - INCLUDE setup instructions for API keys
  - ADD usage examples and screenshots section placeholders
  - DOCUMENT API endpoints and configuration options

Task 8:
UPDATE examples/your_plugin/PRIVACY.md:
  - UPDATE privacy policy for latency monitoring use case
  - DOCUMENT what data is collected (latency metrics, IP info)
  - CLARIFY that API keys are stored securely by Dify
```

### Per task pseudocode as needed added to each task

```python
# Task 5 - Core implementation pseudocode
class AiMonitorEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        # PATTERN: Route based on request path and method
        if r.path.endswith('/api/latency'):
            return self.get_latency_data(settings)
        elif r.path.endswith('/api/ip'):
            return self.get_ip_info()
        else:
            # PATTERN: Serve static HTML dashboard
            return send_from_directory('static', 'index.html')
    
    def get_latency_data(self, settings: Mapping) -> Response:
        # PATTERN: Test each configured AI platform
        results = {}
        
        # CRITICAL: Get API keys from Dify settings
        openai_key = settings.get('openai_api_key')
        azure_key = settings.get('azure_api_key')
        gemini_key = settings.get('gemini_api_key')  
        deepseek_key = settings.get('deepseek_api_key')
        
        # PATTERN: Test each platform with timeout and error handling
        if openai_key:
            results['openai'] = self.test_openai_latency(openai_key)
        if azure_key:
            results['azure'] = self.test_azure_latency(azure_key, settings)
        if gemini_key:
            results['gemini'] = self.test_gemini_latency(gemini_key)
        if deepseek_key:
            results['deepseek'] = self.test_deepseek_latency(deepseek_key)
            
        return jsonify(results)
    
    def test_openai_latency(self, api_key: str) -> LatencyResult:
        # CRITICAL: Precise timing measurement 
        start_time = time.time()
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                timeout=30
            )
            latency_ms = (time.time() - start_time) * 1000
            
            # PATTERN: Log successful request 
            logger.info(f"OpenAI latency test successful: {latency_ms:.2f}ms")
            return LatencyResult("openai", latency_ms, True)
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            # PATTERN: Log errors with context
            logger.error(f"OpenAI latency test failed after {latency_ms:.2f}ms: {str(e)}")
            return LatencyResult("openai", latency_ms, False, str(e))

    def get_ip_info(self) -> Response:
        # PATTERN: Use external service for IP geolocation
        try:
            # GOTCHA: Use free service that doesn't require API key
            response = requests.get('https://ipapi.co/json/', timeout=10)
            ip_data = response.json()
            
            ip_info = IPInfo(
                ip=ip_data.get('ip', 'Unknown'),
                country=ip_data.get('country_name', 'Unknown'),
                region=ip_data.get('region', 'Unknown'), 
                city=ip_data.get('city', 'Unknown'),
                latitude=ip_data.get('latitude', 0.0),
                longitude=ip_data.get('longitude', 0.0)
            )
            
            logger.info(f"IP info retrieved: {ip_info.ip} ({ip_info.city}, {ip_info.country})")
            return jsonify(asdict(ip_info))
            
        except Exception as e:
            logger.error(f"Failed to get IP info: {str(e)}")
            return jsonify({"error": "Failed to retrieve IP information"})
```

### Integration Points
```yaml
DIFY_SETTINGS:
  - add to: group/ai_monitor.yaml
  - pattern: |
      settings:
        - name: openai_api_key
          type: secret-input
          required: false
        - name: azure_api_key  
          type: secret-input
          required: false
        - name: gemini_api_key
          type: secret-input
          required: false
        - name: deepseek_api_key
          type: secret-input
          required: false

MANIFEST_CONFIG:
  - update: manifest.yaml
  - pattern: |
      name: ai_latency_monitor
      label:
        en_US: AI Latency Monitor
      description:
        en_US: Monitor real-time latency for popular AI platforms
      plugins:
        endpoints:
          - group/ai_monitor.yaml

FRONTEND_INTEGRATION:
  - create: static/index.html with real-time dashboard
  - pattern: "Fetch /api/latency every 10 seconds, display results in responsive grid"
  - include: Charts.js or similar for latency visualization
```

## Validation Loop

### Level 1: Syntax & Style  
```bash
# Run these FIRST - fix any errors before proceeding
python -m py_compile endpoints/ai_monitor.py  # Basic syntax check
# Expected: No syntax errors. If errors, READ the error and fix.
```

### Level 2: Dify Plugin Validation
```bash
# Test plugin structure validation (simulated)
find . -name "manifest.yaml" -exec echo "Checking manifest structure..." \;
find . -name "*.py" -exec echo "Found Python file: {}" \;
find . -name "requirements.txt" -exec echo "Found requirements file" \;

# Expected: All required files present with correct naming
```

### Level 3: Manual Testing
```bash
# Test AI platform connections (with real API keys)
python3 -c "
import sys, os
sys.path.append('endpoints')
from ai_monitor import AiMonitorEndpoint

# Test initialization
endpoint = AiMonitorEndpoint()
print('Endpoint initialized successfully')
"

# Expected: No import errors or initialization failures
```

### Level 4: Web Interface Test
```bash
# Serve static files locally for testing (simulation)
python3 -m http.server 8000 --directory endpoints/static &
sleep 2
curl -s http://localhost:8000/ | grep -q "AI Latency Monitor" && echo "HTML served successfully" || echo "HTML serving failed"
pkill -f "python3 -m http.server"

# Expected: HTML dashboard loads and displays title correctly
```

## Final validation Checklist
- [ ] All Python files have valid syntax: `python -m py_compile endpoints/*.py`
- [ ] manifest.yaml follows Dify structure requirements
- [ ] All required dependencies listed in requirements.txt
- [ ] API key configuration properly set up in group YAML
- [ ] Static files (HTML/CSS/JS) are present and functional
- [ ] Error handling implemented for all API calls
- [ ] Logging follows Dify plugin standards
- [ ] Dashboard displays placeholder content when API keys not configured

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode API keys - always use Dify settings system
- ❌ Don't ignore API timeouts - implement proper timeout handling
- ❌ Don't skip error logging - all failures should be logged with context  
- ❌ Don't create overly complex frontend - keep it simple and functional
- ❌ Don't assume all API platforms will work - handle partial failures gracefully
- ❌ Don't use synchronous requests without timeouts - always set reasonable timeouts
- ❌ Don't forget IP geolocation fallbacks - external services can fail

## PRP Confidence Score: 9/10

This PRP provides comprehensive context including:
✅ Complete Dify platform documentation and standards
✅ Specific AI platform API integration patterns  
✅ Exact file structure and modification requirements
✅ Detailed pseudocode with critical implementation details
✅ Validation steps that can be executed by AI
✅ Real codebase examples to follow
✅ Error handling and logging patterns
✅ Known gotchas and library quirks documented

The high confidence score reflects the thorough research and detailed implementation blueprint that should enable successful one-pass implementation.