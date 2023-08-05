from .OptionInfo import OptionInfo


class SelectItem(dict):
    """
    {
      'optionInfo': object(optioninfo),
      'title': string
    }
    """

    def __init__(self, title: str = None, option_info: OptionInfo = None):
        super().__init__()

        self['optionInfo'] = option_info
        self['title'] = title

    def add_option_info(self, key: str, *synonyms: str) -> OptionInfo:
        self['optionInfo'] = OptionInfo(key=key, *synonyms)
        return self['optionInfo']
