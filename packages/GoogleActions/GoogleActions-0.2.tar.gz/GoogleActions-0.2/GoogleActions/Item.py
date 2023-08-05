from .SimpleResponse import SimpleResponse
from .BasicCard import BasicCard
from .StructuredResponse import StructuredResponse
from .MediaResponse import MediaResponse
from .CarouselBrowse import CarouselBrowse
from .TableCard import TableCard
from .Image import Image
from .Button import Button
from . import ImageDisplayOptions


class Item(dict):
    """
    {

      // Union field item can be only one of the following:
      "simpleResponse": {
        object(SimpleResponse)
      },
      "basicCard": {
        object(BasicCard)
      },
      "structuredResponse": {
        object(StructuredResponse)
      },
      "mediaResponse": {
        object(MediaResponse)
      },
      "carouselBrowse": {
        object(CarouselBrowse)
      },
      "tableCard": {
        object(TableCard)
      }
      // End of list of possible types for union field item.
    }
    """

    def __init__(self, member_object=None):
        super().__init__()

        assert isinstance(member_object, (StructuredResponse, SimpleResponse, BasicCard, MediaResponse))
        if isinstance(member_object, SimpleResponse):
            self['simpleResponse'] = member_object
        elif isinstance(member_object, BasicCard):
            self['basicCard'] = member_object
        elif isinstance(member_object, StructuredResponse):
            self['structuredResponse'] = member_object
        elif isinstance(member_object, MediaResponse):
            self['mediaResponse'] = member_object
        elif isinstance(member_object, CarouselBrowse):
            self['carouselBrowse'] = member_object
        elif isinstance(member_object, TableCard):
            self['tableCard'] = member_object

    def add(self, member_object):
        if isinstance(member_object, SimpleResponse):
            self['simpleResponse'] = member_object
        elif isinstance(member_object, BasicCard):
            self['basicCard'] = member_object
        elif isinstance(member_object, StructuredResponse):
            self['structuredResponse'] = member_object
        elif isinstance(member_object, MediaResponse):
            self['mediaResponse'] = member_object
        elif isinstance(member_object, CarouselBrowse):
            self['carouselBrowse'] = member_object
        elif isinstance(member_object, TableCard):
            self['tableCard'] = member_object

        return self

    def add_simple_response(self, text_to_speech: str, ssml: str, display_text: str) -> SimpleResponse:
        self['simpleResponse'] = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml,
                                                display_text=display_text)

        return self['simpleResponse']

    def add_basic_card(self, title: str = None, formatted_text: str = None, subtitle: str = None, image: Image = None,
                       image_display_options: ImageDisplayOptions = None, *buttons: Button) -> BasicCard:

        self['basicCard'] = BasicCard(title=title, formatted_text=formatted_text,
                                      subtitle=subtitle, image=image,
                                      image_display_options=image_display_options, *buttons)

        return self['basicCard']
