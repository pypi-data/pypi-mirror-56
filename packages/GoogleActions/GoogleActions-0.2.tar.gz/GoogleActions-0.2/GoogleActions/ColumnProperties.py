from . import HorizontalAlignment


class ColumnProperties(dict):
    """
    {
      "header": string,
      "horizontalAlignment": enum(HorizontalAlignment)
    }
    """

    def __init__(self, header: str, horizontal_alignment: HorizontalAlignment):
        super(ColumnProperties, self).__init__()

        self['header'] = header
        self['horizontalAlignment'] = horizontal_alignment
