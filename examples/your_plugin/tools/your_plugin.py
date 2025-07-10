from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class YourPluginTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 1. Get parameters defined in tool
        param = tool_parameters.get("param_name", "")

        # 2. Get parameters defined in provider(optional)
        api_key=self.runtime.credentials["api_key"]

        # 3. Implement business logic
        result = self.my_process_data(param, optional_param1, optional_param2)

        # 4. Return results
        # Text output
        yield self.create_text_message(f"Processed result: {result}")
        # JSON output, result should be a dict
        yield self.create_json_message({"result": result})
        # File output, result should be a blob object
        yield self.create_blob_message(blob=result, meta={"mime_type": "video/mp4", "file_name":"custom.mp4"})
