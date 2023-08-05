from .Argument import Argument
from .Extension import Extension
from .Location import Location
from .Status import Status


class Target(dict):
    """
    {
      "userId": string,
      "intent": string,
      "argument": {
        object(Argument)
      },
    }
    """

    def __init__(self, intent: str = None, argument: Argument = None, user_id: str = None):
        super().__init__()

        if intent is not None:
            self['intent'] = intent
        if argument is not None:
            self['argument'] = argument
        if user_id is not None:
            self['userId'] = user_id

    def add_argument(self, name: str = None, raw_text: str = None, text_value: str = None, status: Status = None,
                     int_value: str = None,
                     float_value: str = None, bool_value: bool = False, datetime_value: str = None,
                     place_value: Location = None,
                     extension: Extension = None, **structure_values) -> Argument:
        self['argument'] = Argument(name=name, raw_text=raw_text, text_value=text_value, status=status,
                                    int_value=int_value, float_value=float_value, bool_value=bool_value,
                                    datetime_value=datetime_value, place_value=place_value, extension=extension,
                                    **structure_values)

        return self['argument']
