from typing import Mapping
from werkzeug import Request, Response
from werkzeug.utils import send_from_directory
from dify_plugin import Endpoint


class YourExtensionEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """
        # get the user setting of endpoint example
        model = settings.get("model")

        # get the request json example
        data = r.get_json()
        prompt = data.get("prompt")

        # invoke the LLM example
        response = self.session.model.llm.invoke(
                model_config=model,
                prompt_messages=prompt_messages,
                stream=False,
            )
        result = json.dumps({
            "result": response.message.content
        })


        # return a HTML example
        directory = os.path.join(os.path.dirname(__file__), "static")
        return send_from_directory(directory, "index.html", r.environ)