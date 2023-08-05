


class LinkOutSuggestion(dict):
    """
    {
      "destinationName": string,
      "url": string,
    }
    """
    destination_name: str = DictProperty('destinationName', str)
    url: str = DictProperty('url', str)

    def __init__(self, url:str=None, destination_name:str=None):
        super().__init__()

        self['url = url
        self['destination_name = destination_name
