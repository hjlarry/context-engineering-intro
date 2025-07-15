import os
import json
import time
from typing import Mapping, Optional, Dict, Any
from dataclasses import dataclass, asdict
from werkzeug import Request, Response
from werkzeug.utils import send_from_directory
from dify_plugin import Endpoint
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
import requests

# Initialize logging as specified in INITIAL.md
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)

@dataclass
class LatencyResult:
    """Data structure for latency test results"""
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
    """Data structure for IP geolocation information"""
    ip: str
    country: str
    region: str
    city: str
    latitude: float
    longitude: float


class AILatencyTester:
    """Class for testing latency of different AI platforms"""
    
    def __init__(self):
        self.timeout = 30  # 30 second timeout for all API calls
    
    def test_openai_latency(self, api_key: str) -> LatencyResult:
        """Test OpenAI API latency"""
        start_time = time.time()
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key, timeout=self.timeout)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            latency_ms = (time.time() - start_time) * 1000
            
            logger.info(f"OpenAI latency test successful: {latency_ms:.2f}ms")
            return LatencyResult("openai", latency_ms, True)
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"OpenAI latency test failed after {latency_ms:.2f}ms: {str(e)}")
            return LatencyResult("openai", latency_ms, False, str(e))
    
    def test_azure_latency(self, api_key: str, endpoint: str) -> LatencyResult:
        """Test Azure OpenAI API latency"""
        start_time = time.time()
        try:
            from openai import AzureOpenAI
            
            if not endpoint:
                raise ValueError("Azure endpoint is required")
            
            client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-01",
                azure_endpoint=endpoint,
                timeout=self.timeout
            )
            response = client.chat.completions.create(
                model="gpt-35-turbo",  # Common Azure deployment name
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            latency_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Azure OpenAI latency test successful: {latency_ms:.2f}ms")
            return LatencyResult("azure", latency_ms, True)
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Azure OpenAI latency test failed after {latency_ms:.2f}ms: {str(e)}")
            return LatencyResult("azure", latency_ms, False, str(e))
    
    def test_gemini_latency(self, api_key: str) -> LatencyResult:
        """Test Google Gemini API latency"""
        start_time = time.time()
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(
                "Hello",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10,
                    temperature=0.1,
                )
            )
            latency_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Gemini latency test successful: {latency_ms:.2f}ms")
            return LatencyResult("gemini", latency_ms, True)
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Gemini latency test failed after {latency_ms:.2f}ms: {str(e)}")
            return LatencyResult("gemini", latency_ms, False, str(e))
    
    def test_deepseek_latency(self, api_key: str) -> LatencyResult:
        """Test DeepSeek API latency using OpenAI SDK with different base_url"""
        start_time = time.time()
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com",
                timeout=self.timeout
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            latency_ms = (time.time() - start_time) * 1000
            
            logger.info(f"DeepSeek latency test successful: {latency_ms:.2f}ms")
            return LatencyResult("deepseek", latency_ms, True)
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"DeepSeek latency test failed after {latency_ms:.2f}ms: {str(e)}")
            return LatencyResult("deepseek", latency_ms, False, str(e))


class IPGeolocator:
    """Class for IP geolocation information retrieval"""
    
    def __init__(self):
        self.timeout = 10  # 10 second timeout for IP API calls
    
    def get_ip_info(self) -> Dict[str, Any]:
        """Get IP geolocation information using free service"""
        try:
            # Use ipapi.co free service (no API key required)
            response = requests.get('https://ipapi.co/json/', timeout=self.timeout)
            response.raise_for_status()
            ip_data = response.json()
            
            ip_info = IPInfo(
                ip=ip_data.get('ip', 'Unknown'),
                country=ip_data.get('country_name', 'Unknown'),
                region=ip_data.get('region', 'Unknown'), 
                city=ip_data.get('city', 'Unknown'),
                latitude=float(ip_data.get('latitude', 0.0)),
                longitude=float(ip_data.get('longitude', 0.0))
            )
            
            logger.info(f"IP info retrieved: {ip_info.ip} ({ip_info.city}, {ip_info.country})")
            return asdict(ip_info)
            
        except Exception as e:
            logger.error(f"Failed to get IP info: {str(e)}")
            return {"error": "Failed to retrieve IP information"}


class AiMonitorEndpoint(Endpoint):
    """AI Latency Monitor Endpoint for Dify Plugin"""
    
    def __init__(self):
        super().__init__()
        self.latency_tester = AILatencyTester()
        self.ip_geolocator = IPGeolocator()
        logger.info("AI Monitor Endpoint initialized")
    
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Main endpoint handler that routes requests based on path
        """
        try:
            # Route based on request path
            if r.path.endswith('/api/latency'):
                return self._handle_latency_api(settings)
            elif r.path.endswith('/api/ip'):
                return self._handle_ip_api()
            else:
                # Serve static dashboard files
                return self._serve_static_files(r)
                
        except Exception as e:
            logger.error(f"Unexpected error in _invoke: {str(e)}")
            return Response(
                json.dumps({"error": "Internal server error"}),
                status=500,
                content_type="application/json"
            )
    
    def _handle_latency_api(self, settings: Mapping) -> Response:
        """Handle /api/latency endpoint"""
        try:
            logger.info("Processing latency API request")
            results = {}
            
            # Get API keys from Dify settings
            openai_key = settings.get('openai_api_key')
            azure_key = settings.get('azure_api_key')
            azure_endpoint = settings.get('azure_endpoint')
            gemini_key = settings.get('gemini_api_key')
            deepseek_key = settings.get('deepseek_api_key')
            
            # Test each platform if API key is provided
            if openai_key:
                logger.info("Testing OpenAI latency")
                result = self.latency_tester.test_openai_latency(openai_key)
                results['openai'] = asdict(result)
            else:
                logger.info("OpenAI API key not provided")
                results['openai'] = None
            
            if azure_key and azure_endpoint:
                logger.info("Testing Azure OpenAI latency")
                result = self.latency_tester.test_azure_latency(azure_key, azure_endpoint)
                results['azure'] = asdict(result)
            else:
                logger.info("Azure OpenAI API key or endpoint not provided")
                results['azure'] = None
            
            if gemini_key:
                logger.info("Testing Gemini latency")
                result = self.latency_tester.test_gemini_latency(gemini_key)
                results['gemini'] = asdict(result)
            else:
                logger.info("Gemini API key not provided")
                results['gemini'] = None
            
            if deepseek_key:
                logger.info("Testing DeepSeek latency")
                result = self.latency_tester.test_deepseek_latency(deepseek_key)
                results['deepseek'] = asdict(result)
            else:
                logger.info("DeepSeek API key not provided")
                results['deepseek'] = None
            
            logger.info(f"Latency test completed for {len([k for k, v in results.items() if v is not None])} platforms")
            
            return Response(
                json.dumps(results),
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Error in latency API handler: {str(e)}")
            return Response(
                json.dumps({"error": f"Failed to test latency: {str(e)}"}),
                status=500,
                content_type="application/json"
            )
    
    def _handle_ip_api(self) -> Response:
        """Handle /api/ip endpoint"""
        try:
            logger.info("Processing IP geolocation API request")
            ip_data = self.ip_geolocator.get_ip_info()
            
            return Response(
                json.dumps(ip_data),
                content_type="application/json"
            )
            
        except Exception as e:
            logger.error(f"Error in IP API handler: {str(e)}")
            return Response(
                json.dumps({"error": f"Failed to get IP information: {str(e)}"}),
                status=500,
                content_type="application/json"
            )
    
    def _serve_static_files(self, r: Request) -> Response:
        """Serve static files for the dashboard"""
        try:
            # Determine which file to serve
            path = r.path.strip('/')
            
            # Default to index.html for root path
            if not path or path == '/':
                filename = 'index.html'
            else:
                # Extract filename from path
                filename = path.split('/')[-1]
                
                # Security check - only allow specific file types
                allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.svg', '.ico'}
                if not any(filename.endswith(ext) for ext in allowed_extensions):
                    filename = 'index.html'
            
            # Serve file from static directory
            static_dir = os.path.join(os.path.dirname(__file__), "static")
            
            logger.info(f"Serving static file: {filename}")
            return send_from_directory(static_dir, filename)
            
        except FileNotFoundError:
            logger.warning(f"Static file not found: {filename}")
            # Fallback to index.html
            static_dir = os.path.join(os.path.dirname(__file__), "static")
            return send_from_directory(static_dir, "index.html")
            
        except Exception as e:
            logger.error(f"Error serving static files: {str(e)}")
            return Response(
                "Dashboard unavailable",
                status=500,
                content_type="text/plain"
            )