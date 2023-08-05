from typing import List
from .RichResponse import RichResponse
from .SimpleResponse import SimpleResponse


class InputPrompt(dict):
    """
    Input Prompt

    class for Google
    {
      "richInitialPrompt": {
        object(RichResponse)
      },
      "noInputPrompts": [
        {
          object(SimpleResponse)
        }
      ],
    }
    """

    def __init__(self, rich_initial_prompt: RichResponse = None, *no_input_prompts: SimpleResponse):
        super().__init__()
        self['_no_input_prompts = []

        self['_rich_initial_prompt = rich_initial_prompt
        for item in no_input_prompts:
            self['_no_input_prompts.append(item)

    def add_rich_initial_prompt(self) -> RichResponse:
        self['_rich_initial_prompt = RichResponse()
        return self['_rich_initial_prompt

    def add_no_input_prompts(self, *no_input_prompts: SimpleResponse) -> List[SimpleResponse]:
        for item in no_input_prompts:
            assert isinstance(item, SimpleResponse)
            self['_no_input_prompts.append(item)

        return self['_no_input_prompts

    def add_no_input_prompt(self, text_to_speech: str = None, ssml: str = None,
                            display_text: str = None) -> SimpleResponse:
        no_input_prompt = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text)
        self['_no_input_prompts.append(no_input_prompt)

        return no_input_prompt
