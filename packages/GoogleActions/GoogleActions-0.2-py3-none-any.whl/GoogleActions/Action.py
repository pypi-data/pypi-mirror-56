from .Button import Button
from . import ActionType
from .OpenUrlAction import OpenUrlAction


class Action(dict):
    """
    {
      "type": enum(ActionType),
      "button": {
        object(Button)
      },
    }
    type
    enum(ActionType)
    Type of action.

    button
    object(Button)
    Button label and link.
    """

    def __init__(self, button: Button = None, action_type: ActionType = None):
        super().__init__()

        if button is not None:
            self['button'] = button

        if action_type is not None:
            self['type'] = action_type

    def add_button(self, title: str, url: str) -> Button:
        assert isinstance(title, str)
        assert isinstance(url, str)

        self['button'] = Button(title=title, open_url_action=OpenUrlAction(url=url))

        return self['button']
