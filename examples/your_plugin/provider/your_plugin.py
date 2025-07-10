from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class YourPluginProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            implement your validations here, if don't require validation, you can leave it empty.
            you can get the credentials from credentials['api_key']
            """
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
