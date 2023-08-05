from typing import List


class OptionInfo(dict):
    """
     {
          'key': string,
          'synonyms': [
            string
          ]
        }
    """

    def __init__(self, key: str = None, *synonyms: str):
        super().__init__()

        if key is not None:
            self['key'] = key

        for item in synonyms:
            self['synonyms'].append(item)

    def add_synonyms(self, *synonyms: str) -> List[str]:
        for item in synonyms:
            self['synonyms'].append(item)
        return self['synonyms']
