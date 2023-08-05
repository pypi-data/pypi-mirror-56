class Extension(dict):
    """
    {
        "@type": string,
        field1: ...,
        ...
    }
    """

    def __init__(self, extention_type: str, **fields):
        super().__init__()

        if extention_type is not None:
            self['@type'] = extention_type

        self['update(fields)

    def add_fields(self, **kwargs) -> dict:
        self['update(kwargs)

        return self
