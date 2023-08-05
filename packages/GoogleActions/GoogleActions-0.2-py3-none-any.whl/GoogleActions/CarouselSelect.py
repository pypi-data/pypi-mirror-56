from typing import List
from .CarouselItem import CarouselItem
from .Image import Image
from .OptionInfo import OptionInfo
from . import ImageDisplayOptions


class CarouselSelect(dict):
    """
    {
      'imageDisplayOptions': enum(ImageDisplayOptions),
      'item_list': [
        {
          object(carouselItem)
        }
      ]
    }
    """

    def __init__(self, image_display_options: ImageDisplayOptions, *carousel_items: CarouselItem):
        super(CarouselSelect, self).__init__()

        self['item_list'] = []
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['item_list'].append(item)

        if image_display_options is not None:
            self['imageDisplayOptions'] = image_display_options

    def add_carousel_items(self, *carousel_items: CarouselItem) -> List[CarouselItem]:
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['item_list'].append(item)
        return self['item_list']

    def add_carousel_item(self, key: str, title: str, description: str = None, image_url: str = None,
                          image_text: str = None,
                          image_height: int = 0, image_width: int = 0, *synonyms: str) -> CarouselItem:

        carousel_item = CarouselItem(title=title, description=description, image=Image(url=image_url,
                                                                                       accessibility_text=image_text,
                                                                                       height=image_height,
                                                                                       width=image_width),
                                     option_info=OptionInfo(key=key, *synonyms))
        self['item_list'].append(carousel_item)
        return carousel_item
