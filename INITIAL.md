## FEATURE:

Implement a plugin of dify platform, which has its own run environment and standard, you need to follow the standard.

This plugin is to build a mermaid converter, the input is user's mermaid code, the output is a jpg/png/pdf etc.
Use this website to convert mermaid:  https://mermaid.ink/

## EXAMPLES:

In the `examples/` folder, there is a basic dify plugin template, and I add some comments to explain the dify'API for you. 

You need to change the code and config in the `examples/your_plugin` folder, and some files don't need to modify.

If this file don't need to modify, I will add a comment on the top line of the file, you just copy it

This is the plugin structure:
```
your_plugin/
├── _assets/             # Icons and visual resources
├── provider/            # Provider definitions and validation
│   ├── your_plugin.py   # Credential validation logic
│   └── your_plugin.yaml # Provider configuration
├── tools/               # Tool implementations
│   ├── feature_one.py   # Tool functionality implementation
│   ├── feature_one.yaml # Tool parameters and description
│   ├── feature_two.py   # Another tool implementation
│   └── feature_two.yaml # Another tool configuration
├── utils/               # Helper functions
│   └── helpers.py       # Common functionality logic
├── .env.example         # Environment variable template
├── main.py              # Entry file
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation
├── PRIVACY.md           # PRIVACY
└── requirements.txt     # Dependency list
```

## DOCUMENTATION:

mermaid convert: https://mermaid.ink/
getting started document: https://docs.dify.ai/plugin-dev-zh/0211-getting-started-by-prompt
invoke the LLM: https://docs.dify.ai/plugin-dev-zh/9242-reverse-invocation-model
invoke the APP: https://docs.dify.ai/plugin-dev-zh/9242-reverse-invocation-app

## OTHER CONSIDERATIONS:

- you need to log key infomation when send a http request or other important science data, this is how to log:

```python
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)
```
