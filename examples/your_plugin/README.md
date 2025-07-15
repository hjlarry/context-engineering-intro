# AI Latency Monitor

**Author:** AI Assistant  
**Version:** 0.0.1  
**Type:** Monitoring Plugin  

## Overview

A comprehensive Dify plugin that monitors real-time latency for popular AI platforms. This plugin provides a web-based dashboard displaying response times, server location information, and historical performance data for multiple AI services.

## Features

- **Real-time Monitoring**: Live latency testing for 4 major AI platforms
- **Web Dashboard**: Modern, responsive interface with real-time updates
- **Historical Data**: Charts showing latency trends over time
- **IP Geolocation**: Display server location and network information
- **Multi-platform Support**: OpenAI, Azure OpenAI, Google Gemini, and DeepSeek
- **Auto-refresh**: Configurable automatic monitoring (default: 10 seconds)
- **Error Handling**: Graceful handling of API failures and timeouts
- **Secure Configuration**: API keys stored securely through Dify settings

## Supported AI Platforms

| Platform | Model Used | Notes |
|----------|------------|-------|
| **OpenAI** | gpt-3.5-turbo | Standard OpenAI API |
| **Azure OpenAI** | gpt-35-turbo | Requires endpoint URL |
| **Google Gemini** | gemini-pro | Google Generative AI |
| **DeepSeek** | deepseek-chat | OpenAI-compatible API |

## Setup and Configuration

### 1. Plugin Installation

1. Install the plugin in your Dify environment
2. Navigate to the plugin settings page
3. Configure API keys for the platforms you want to monitor

### 2. API Key Configuration

Configure the following settings in the plugin configuration:

#### Required Settings

| Setting | Type | Required | Description |
|---------|------|----------|-------------|
| `OpenAI API Key` | Secret | No | Your OpenAI API key |
| `Azure OpenAI API Key` | Secret | No | Your Azure OpenAI API key |
| `Azure OpenAI Endpoint` | String | No | Azure OpenAI endpoint URL |
| `Google Gemini API Key` | Secret | No | Your Google AI API key |
| `DeepSeek API Key` | Secret | No | Your DeepSeek API key |

#### API Key Setup Instructions

**OpenAI:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and paste into the OpenAI API Key field

**Azure OpenAI:**
1. Access your Azure OpenAI resource
2. Navigate to Keys and Endpoint
3. Copy the API key and endpoint URL
4. Enter both in the respective fields

**Google Gemini:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into the Gemini API Key field

**DeepSeek:**
1. Visit [DeepSeek Platform](https://platform.deepseek.com/api_keys)
2. Create a new API key
3. Copy and paste into the DeepSeek API Key field

### 3. Access the Dashboard

After configuration, access the monitoring dashboard at:
```
https://your-dify-instance/plugins/ai-latency-monitor
```

## Usage Examples

### Basic Monitoring

1. Configure at least one AI platform API key
2. Open the dashboard URL
3. The system will automatically start testing latency every 10 seconds
4. View real-time results in the platform cards

### API Integration

The plugin also provides REST API endpoints for programmatic access:

#### Get Latency Data
```bash
curl https://your-dify-instance/plugins/ai-latency-monitor/api/latency
```

**Response:**
```json
{
  "openai": {
    "platform": "openai",
    "response_time_ms": 1250.5,
    "success": true,
    "timestamp": 1640995200.0
  },
  "azure": {
    "platform": "azure",
    "response_time_ms": 890.2,
    "success": true,
    "timestamp": 1640995201.0
  },
  "gemini": null,
  "deepseek": {
    "platform": "deepseek",
    "response_time_ms": 2100.8,
    "success": false,
    "error_message": "Authentication failed",
    "timestamp": 1640995202.0
  }
}
```

#### Get IP Information
```bash
curl https://your-dify-instance/plugins/ai-latency-monitor/api/ip
```

**Response:**
```json
{
  "ip": "203.0.113.1",
  "country": "United States",
  "region": "California",
  "city": "San Francisco",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

## Dashboard Features

### Platform Cards
- **Status Indicators**: Green (online), Red (error), Orange (loading)
- **Latency Display**: Color-coded response times (green <1s, orange 1-3s, red >3s)
- **Timestamps**: Last successful test time
- **Error Messages**: Detailed error information for failed tests

### Historical Chart
- **Real-time Updates**: Automatically updated with new data points
- **Multiple Platforms**: All configured platforms on one chart
- **Time Series**: Shows last 20 data points for each platform
- **Interactive**: Hover for detailed values

### Controls
- **Manual Refresh**: Force immediate latency test
- **Auto-refresh Toggle**: Enable/disable automatic updates
- **Status Information**: Last update time and refresh status

## Performance Metrics

### Latency Categories
- **Fast**: < 1000ms (Green)
- **Medium**: 1000-3000ms (Orange)  
- **Slow**: > 3000ms (Red)

### Test Parameters
- **Timeout**: 30 seconds per platform
- **Test Prompt**: Simple "Hello" message
- **Token Limit**: 10 tokens maximum
- **Concurrent Testing**: All platforms tested simultaneously

## Troubleshooting

### Common Issues

#### 1. "Not configured" Status
**Cause:** API key not provided for the platform  
**Solution:** Add the API key in plugin settings

#### 2. "Authentication failed" Error
**Cause:** Invalid or expired API key  
**Solution:** Verify and update the API key

#### 3. "Connection timeout" Error
**Cause:** Network issues or API service unavailable  
**Solution:** Check network connectivity and try again

#### 4. Azure OpenAI "endpoint required" Error
**Cause:** Azure endpoint URL not configured  
**Solution:** Add the Azure OpenAI endpoint URL in settings

#### 5. Dashboard not loading
**Cause:** Plugin not properly installed or configured  
**Solution:** Reinstall plugin and check Dify logs

### Debugging

Check the Dify plugin logs for detailed error information:
```bash
# View plugin logs
tail -f /path/to/dify/logs/plugin.log | grep "ai_monitor"
```

## Technical Details

### Architecture
- **Backend**: Python with Dify plugin framework
- **Frontend**: HTML5, CSS3, JavaScript with Chart.js
- **Data Storage**: In-memory (20 data points per platform)
- **Refresh Rate**: 10 seconds (configurable)

### Dependencies
- `dify_plugin>=0.2.0` - Dify plugin framework
- `openai>=1.0.0` - OpenAI and DeepSeek API client
- `azure-openai>=1.0.0` - Azure OpenAI client
- `google-generativeai>=0.3.0` - Google Gemini client
- `requests` - HTTP client for IP geolocation

### Security
- **API Keys**: Stored securely by Dify framework
- **No Data Persistence**: Latency data not stored permanently
- **HTTPS Required**: Secure communication for all API calls
- **Input Validation**: All user inputs validated and sanitized

### Rate Limits
- **OpenAI**: Respects account rate limits
- **Azure OpenAI**: Follows Azure quotas
- **Google Gemini**: Adheres to API quotas
- **DeepSeek**: No rate limiting (best effort)
- **IP Service**: 1000 requests/month (free tier)

## API Reference

### Endpoints

#### `GET /ai-latency-monitor`
Returns the main dashboard HTML page

#### `GET /ai-latency-monitor/api/latency`
Returns current latency data for all configured platforms

#### `GET /ai-latency-monitor/api/ip`
Returns server IP geolocation information

### Response Formats

All API responses use JSON format with appropriate HTTP status codes:
- `200 OK`: Successful request
- `500 Internal Server Error`: Server or configuration error

## Limitations

- **Internet Required**: All platforms require internet connectivity
- **API Dependencies**: Functionality depends on external API availability
- **Rate Limits**: Subject to individual platform rate limits
- **Memory Usage**: Historical data stored in memory only
- **Concurrent Users**: Dashboard updates are not synchronized between users

## Support

For issues or feature requests, please check:
1. Plugin configuration and API keys
2. Dify plugin logs
3. Network connectivity to AI platforms
4. API key permissions and quotas

---

*This plugin is designed for monitoring purposes only. Response times may vary based on network conditions, geographic location, and API service load.*