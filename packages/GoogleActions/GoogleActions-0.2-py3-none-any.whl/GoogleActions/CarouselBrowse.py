from typing import List
from .CarouselItem import CarouselItem
from . import ImageDisplayOptions, OptionInfo
from .Image import Image


class CarouselBrowse(dict):
    """
    {
      "item_list": [
        {
          object(Item)
        }
      ],
      "imageDisplayOptions": enum(ImageDisplayOptions)
    }
    """

    def __init__(self, image_display_options: ImageDisplayOptions, *items: CarouselItem):
        super().__init__()

        super(CarouselBrowse, self).__init__()

        self['imageDisplayOptions'] = image_display_options
        self['item_list'] = items

    def add_items(self, *items: CarouselItem) -> List[CarouselItem]:
        for item in items:
            assert isinstance(item, CarouselItem)
            self['item_list'].append(item)

        return self['item_list']

    def add_item(self, title: str = None, description: str = None, image_url: str = None, image_text: str = None,
                 image_height: int = 0, image_width: int = 0, option_info: OptionInfo = None) \
            -> CarouselItem:
        item = CarouselItem(title=title, description=description,
                            image=Image(url=image_url, accessibility_text=image_text,
                                        height=image_height, width=image_width), option_info=option_info)
        self['item_list'].append(item)
        return item
