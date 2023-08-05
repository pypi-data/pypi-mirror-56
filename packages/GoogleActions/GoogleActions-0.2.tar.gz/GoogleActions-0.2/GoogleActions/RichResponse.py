from typing import List
from .LinkOutSuggestion import LinkOutSuggestion
from .Item import Item
from .Suggestion import Suggestion
from .SimpleResponse import SimpleResponse
from .StructuredResponse import StructuredResponse
from .MediaResponse import MediaResponse
from .BasicCard import BasicCard
from .Image import Image
from . import ImageDisplayOptions, MediaType
from .MediaObject import MediaObject
from .OrderUpdate import OrderUpdate
from .Button import Button


class RichResponse(dict):
    """
    {
      "items": [
        {
          object(Item)
        }
      ],
      "suggestions": [
        {
          object(Suggestion)
        }
      ],
      "linkOutSuggestion": {
        object(LinkOutSuggestion)
      },
    }
    """

    def __init__(self, item_list: list = None, suggestions: list = None, link_out_suggestion: LinkOutSuggestion = None):
        super().__init__()

        if item_list is not None:
            if self.check_structure_validity(item_list):
                self['items'] = item_list
        else:
            self['items'] = []

        if suggestions is not None:
            self['suggestions'] = suggestions
        else:
            self['suggestions'] = []

        self['linkOutSuggestion'] = link_out_suggestion

    def add_items(self, *items) -> List[Item]:
        print('adding item_list')
        temp_item_list = []
        temp_item_list.extend(self['items'])
        for item in items:
            temp_item_list.append(item)

        if self.check_structure_validity(temp_item_list):
            self['items'].extend(items)

        return self['items']

    def add_simple_response(self, text_to_speech: str, ssml: str, display_text: str) -> Item:
        print('adding simple response to')
        print('items_list: ', self['items'])
        temp_item_list = []
        temp_item_list.extend(self['items'])
        print('temp_item_list: ', temp_item_list)
        item = Item(SimpleResponse(text_to_speech=text_to_speech, ssml=ssml, display_text=display_text))
        temp_item_list.append(item)
        print('temp_item_list: ', temp_item_list)
        print('items_list: ', self['items'])

        if self.check_structure_validity(temp_item_list):
            print('items_list: ', self['items'])
            print('item: ', item)
            self['items'].append(item)

        print('items_list: ', self['items'])

        return item

    def add_basic_card(self, title: str, formatted_text: str, subtitle: str, image_url: str,
                       image_text: str, image_height: int, image_width: int,
                       image_display_options: ImageDisplayOptions, *buttons: Button) -> Item:
        print('adding basic card')
        temp_item_list = []
        temp_item_list.extend(self['items'])
        item = Item(BasicCard(title=title, formatted_text=formatted_text,
                              subtitle=subtitle, image=Image(url=image_url,
                                                             accessibility_text=image_text,
                                                             height=image_height,
                                                             width=image_width),
                              image_display_options=image_display_options,
                              *buttons))
        temp_item_list.append(item)

        if self.check_structure_validity(temp_item_list):
            self['items'].append(item)

        return item

    def add_structured_response(self, receipt=None, info_extension=None,
                                return_info=None,
                                user_notification=None, rejection_info=None, update_time=None,
                                line_item_updates=None, fulfillment_info=None,
                                total_price=None,
                                in_transit_info=None, action_order_id=None,
                                cancellation_info=None,
                                order_state=None, google_order_id=None,
                                order_management_actions_list=None) -> Item:
        print('adding structured_response')
        temp_item_list = []
        temp_item_list.extend(self['items'])
        item = Item(StructuredResponse(
            order_update=OrderUpdate(receipt=receipt, info_extension=info_extension, return_info=return_info,
                                     user_notification=user_notification, rejection_info=rejection_info,
                                     update_time=update_time, line_item_updates=line_item_updates,
                                     fulfillment_info=fulfillment_info, total_price=total_price,
                                     in_transit_info=in_transit_info, action_order_id=action_order_id,
                                     cancellation_info=cancellation_info, order_state=order_state,
                                     google_order_id=google_order_id,
                                     order_management_actions_list=order_management_actions_list)))
        temp_item_list.append(item)

        if self.check_structure_validity(temp_item_list):
            self['items'].append(item)

        return item

    def add_media_response(self, media_type: MediaType, *media_objects: MediaObject) -> Item:
        print('adding media response: ', media_type, media_objects)
        media_objects_list = []
        for media_object in media_objects:
            media_objects_list.append(media_object)
        temp_item_list = []
        temp_item_list.extend(self['items'])
        item = Item(MediaResponse(media_type=media_type, *media_objects_list))

        temp_item_list.append(item)

        if self.check_structure_validity(temp_item_list):
            self['items'].append(item)

        return item

    def add_suggestions(self, *titles) -> List[Suggestion]:
        print('adding suggestion: ', titles)

        for title in titles:
            self['suggestions'].append(Suggestion(title=title))

        return self['suggestions']

    def add_link_out_suggestion(self, url: str, destination_name: str) -> LinkOutSuggestion:
        print('adding link_out_suggestion ', url, destination_name)

        self['linkOutSuggestion'] = LinkOutSuggestion(url=url, destination_name=destination_name)

        return self['linkOutSuggestion']

    @staticmethod
    def check_structure_validity(items_list: list) -> bool:
        print('checking structure validity for ', items_list)

        num_of_simple_responses = 0
        num_of_card_responses = 0

        for item_object in items_list:
            print('item_object:', item_object)

            if item_object.simple_response is not None:
                num_of_simple_responses += 1
            elif item_object.basic_card is not None:
                num_of_card_responses += 1
            elif item_object.structured_response is not None:
                num_of_card_responses += 1
            elif item_object.media_response is not None:
                num_of_card_responses += 1

        assert (num_of_simple_responses <= 2)
        assert (num_of_card_responses <= 1)
        print('all ok')

        return True
