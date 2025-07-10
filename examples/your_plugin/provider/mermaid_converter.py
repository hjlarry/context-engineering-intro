from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class MermaidConverterProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        No API key validation needed for mermaid.ink service.
        This method is required by the ToolProvider interface but left empty
        since mermaid.ink is a free public service requiring no authentication.
        """
        pass