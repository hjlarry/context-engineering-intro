# Privacy Policy - AI Latency Monitor Plugin

*Last updated: July 15, 2025*

## Overview

This privacy policy describes how the AI Latency Monitor plugin ("the Plugin") collects, uses, and protects information when you use our monitoring services within the Dify platform.

## Data Collection

### 1. Performance Metrics
The Plugin collects the following performance data:

- **API Response Times**: Latency measurements for AI platform API calls
- **Success/Failure Status**: Whether API calls completed successfully
- **Timestamp Information**: When latency tests were performed
- **Error Messages**: General error information when API calls fail

### 2. Network Information
The Plugin collects basic network information:

- **Server IP Address**: Public IP address of the server running the plugin
- **Geolocation Data**: Country, region, and city based on IP address
- **Geographic Coordinates**: Approximate latitude and longitude

### 3. Configuration Data
The Plugin accesses:

- **API Keys**: Encrypted API keys for AI platforms (stored securely by Dify)
- **Platform Endpoints**: API endpoint URLs for services like Azure OpenAI

## Data Usage

### Primary Purpose
All collected data is used exclusively for:

- **Performance Monitoring**: Measuring and displaying AI platform response times
- **Service Diagnostics**: Identifying connectivity and performance issues
- **User Interface**: Displaying current and historical performance metrics

### No Secondary Use
We do not:

- Analyze API request contents or responses
- Store personal information or sensitive data
- Use data for advertising, marketing, or commercial purposes
- Share data with third parties

## Data Storage and Retention

### Temporary Storage
- **Latency Data**: Stored in memory only, limited to last 20 data points per platform
- **IP Information**: Cached temporarily for dashboard display
- **No Persistent Storage**: Performance data is not saved to databases or files

### API Keys
- **Secure Storage**: API keys are stored and encrypted by the Dify platform
- **No Plugin Access**: The plugin receives API keys only when making authorized requests
- **No Logging**: API keys are never logged or stored by the plugin

### Data Lifetime
- **Session-Based**: All performance data is cleared when the plugin restarts
- **Automatic Cleanup**: Old data points are automatically removed as new ones are added
- **No Long-term Retention**: No historical data is preserved beyond the current session

## Data Security

### Protection Measures
- **Encrypted Transmission**: All API communications use HTTPS/TLS encryption
- **Memory-Only Storage**: Sensitive data exists only in secure memory
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Errors are logged without exposing sensitive information

### API Key Security
- **Dify Framework**: API keys are managed by Dify's secure credential system
- **No Direct Storage**: The plugin never stores API keys independently
- **Minimal Scope**: API keys are used only for authorized latency testing
- **No Transmission**: API keys are never transmitted in logs or responses

## Third-Party Services

### IP Geolocation Service
- **Service Provider**: ipapi.co (free tier)
- **Data Sent**: Only server IP address
- **Purpose**: Geographic location display
- **Privacy Policy**: Subject to ipapi.co's privacy policy

### AI Platform APIs
- **Test Requests**: Minimal test messages sent to configured AI platforms
- **Content**: Simple "Hello" messages with 10-token limit
- **Purpose**: Latency measurement only
- **Platform Policies**: Subject to each platform's privacy policy

## User Rights and Control

### Configuration Control
Users have complete control over:

- **Platform Selection**: Choose which AI platforms to monitor
- **API Key Management**: Add, update, or remove API keys at any time
- **Monitoring Control**: Enable or disable monitoring for any platform
- **Dashboard Access**: Control who can access the monitoring dashboard

### Data Access
- **Real-time Data**: Users can view current performance metrics
- **No Personal Data**: No personally identifiable information is collected
- **Public IP Only**: IP information is limited to public server details

### Opt-Out Options
Users can stop data collection by:

- **Removing API Keys**: Delete API keys from plugin configuration
- **Disabling Plugin**: Deactivate the plugin in Dify settings
- **Selective Monitoring**: Disable specific platforms while keeping others active

## Compliance and Standards

### Data Protection
- **Minimal Collection**: We collect only data necessary for monitoring functionality
- **Purpose Limitation**: Data is used only for stated monitoring purposes
- **Transparency**: All data collection and usage is clearly documented

### Security Standards
- **Industry Best Practices**: Following standard security practices for plugin development
- **Regular Updates**: Security measures are regularly reviewed and updated
- **Dify Integration**: Leveraging Dify's security infrastructure

## Changes to Privacy Policy

### Updates
- **Notification**: Users will be notified of significant privacy policy changes
- **Version Control**: All changes are tracked with dates and version numbers
- **Backward Compatibility**: Changes will not retroactively affect data handling

### Review Schedule
This privacy policy is reviewed annually or when significant changes are made to the plugin functionality.

## Contact and Questions

### Plugin-Specific Questions
For questions about this plugin's privacy practices:

- **Documentation**: Refer to the plugin README.md file
- **Dify Support**: Contact through Dify platform support channels
- **Plugin Logs**: Check Dify plugin logs for operational information

### Data Subject Rights
If you have concerns about data handling:

- **Access**: Review current monitoring configuration in plugin settings
- **Correction**: Update or remove API keys as needed
- **Deletion**: Disable plugin to stop all data collection
- **Portability**: Export monitoring data through dashboard interface

## Limitation of Liability

### External Services
- **Third-party APIs**: We are not responsible for the privacy practices of AI platforms or IP geolocation services
- **Service Availability**: Monitoring depends on external service availability
- **Data Accuracy**: IP geolocation and timing data may vary in accuracy

### Plugin Scope
This privacy policy applies only to the AI Latency Monitor plugin and does not cover:

- **Dify Platform**: General Dify platform privacy practices
- **Other Plugins**: Privacy practices of other Dify plugins
- **External Links**: Privacy policies of linked external services

---

**Important Note**: This plugin is designed for operational monitoring only. It does not access, store, or transmit any content from AI conversations or user data beyond the specific metrics described in this policy.

*For questions about Dify platform privacy practices, please refer to the main Dify privacy policy.*