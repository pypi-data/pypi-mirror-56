from typing import List
from . import MediaType
from .MediaObject import MediaObject
from .Image import Image


class MediaResponse(dict):
    """
    {
      "mediaType": enum(MediaType),
      "mediaObjects": [
        {
          object(MediaObject)
        }
      ]
    }
    """

    def __init__(self, media_type: MediaType, *objects: MediaObject):
        super().__init__()

        for media_object in objects:
            self['mediaObjects'].append(media_object)

            self['mediaType'] = media_type

    def add_media_objects(self, *objects: MediaObject) -> List[MediaObject]:
        for item in objects:
            self['mediaObjects'].append(item)

        return self['mediaObjects']

    def add_media_object(self, name: str, description: str = None, content_url: str = None, image_url: str = None,
                         image_text: str = None, image_height: int = 0, image_width: int = 0, icon_url: str = None,
                         icon_text: str = None, icon_height: int = 0, icon_width: int = 0) -> MediaObject:

        media_object = MediaObject(name=name, description=description, content_url=content_url,
                                   large_image=Image(url=image_url, accessibility_text=image_text,
                                                     height=image_height, width=image_width),
                                   icon=Image(url=icon_url,
                                              accessibility_text=icon_text,
                                              height=icon_height,
                                              width=icon_width))
        self['mediaObjects'].append(media_object)
        return media_object
