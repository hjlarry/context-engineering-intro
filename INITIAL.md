## FEATURE:

Implement an endpoint plugin of dify platform, which has its own run environment and standard, you need to follow the standard.

This plugin is to run a website in the environment, the running server connect to different popular AI platform, the website can display the delay time of each request.

Must included AI platform: 
- OpenAI
- Azure OpenAI
- Google Gemini
- deepseek

User also can add its own AI platform

The website should also display its ip information.

## EXAMPLES:

In the `examples/` folder, there is a basic dify plugin template. 

You need to change the code and config in the `examples/your_plugin` folder.

This is the plugin structure:
```
your_plugin/
├── group/            
│   └── your_extension.yaml  # To config the endpoint required input
├── endpoints/               
│   ├── your_extension.py   # The core logic
│   ├── your_extension.yaml # To config the endpoint path
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation, you need to write the document of your plugin. 
├── PRIVACY.md           # PRIVACY, you need to write the PRIVACY of your plugin.
└── requirements.txt     # Dependency list
```

## DOCUMENTATION:

https://docs.dify.ai/plugin-dev-en/9231-extension-plugin

## OTHER CONSIDERATIONS:

- you need to log key infomation when send a http request or other important science data, this is how to log:

```python
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)
```
