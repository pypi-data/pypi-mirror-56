class UserNotification(dict):
    """
    {
      "title": string,
      "text": string,
    }
    """

    def __init__(self, text: str = None, title: str = None):
        super().__init__()

        self['text'] = text
        self['title'] = title
