from typing import List

from .ListItem import ListItem
from .Image import Image
from .OptionInfo import OptionInfo


class ListSelect(dict):
    """
    {
      'title': string,
      'item_list': [
        {
          object(ListItem)
        }
      ]
    }
    """

    def __init__(self, title: str, *list_items: ListItem):
        super().__init__()

        for item in list_items:
            assert isinstance(item, ListItem)
            self['item_list'].append(item)

        self['title'] = title

    def add_list_items(self, *list_items: ListItem) -> List[ListItem]:
        for item in list_items:
            assert isinstance(item, ListItem)
            self['item_list'].append(item)
        return self['item_list']

    def add_list_item(self, key: str, title: str, description: str = None, image_url: str = None,
                      image_text: str = None,
                      image_height: int = 0, image_width: int = 0, *synonyms: str) -> bool:

        self['item_list'].append(ListItem(title=title, description=description, image=Image(
            url=image_url, accessibility_text=image_text, height=image_height, width=image_width),
                                          option_info=OptionInfo(key=key, *synonyms)))
        return True
