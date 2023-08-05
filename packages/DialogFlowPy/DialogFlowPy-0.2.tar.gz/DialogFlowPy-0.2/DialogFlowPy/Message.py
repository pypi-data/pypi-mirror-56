from typing import Union
from .Text import Text
from .Image import Image
from .QuickReplies import QuickReplies
from .Card import Card
from .SimpleResponse import SimpleResponse
from .BasicCard import BasicCard
from .Suggestions import Suggestions
from .LinkOutSuggestion import LinkOutSuggestion
from .ListSelect import ListSelect
from .CarouselSelect import CarouselSelect
from . import PlatformEnum


class Message(dict):
    """
    {
      "platform": enum(Platform),

      // Union field message can be only one of the following:
      "text": {
        object(Text)
      },
      "image": {
        object(Image)
      },
      "quickReplies": {
        object(QuickReplies)
      },
      "card": {
        object(Card)
      },
      "payload": {
        object
      },
      "simpleResponses": {
        object(SimpleResponses)
      },
      "basicCard": {
        object(BasicCard)
      },
      "suggestions": {
        object(Suggestions)
      },
      "linkOutSuggestion": {
        object(LinkOutSuggestion)
      },
      "listSelect": {
        object(ListSelect)
      },
      "carouselSelect": {
        object(CarouselSelect)
      }
      // End of list of possible types for union field message.
    }
    """

    def __init__(self, platform: str,
                 message_object: Union[Text, Image, QuickReplies, Card, SimpleResponse, BasicCard, Suggestions,
                                       LinkOutSuggestion, ListSelect, CarouselSelect]):
        super().__init__()

        self['platform'] = platform

        if isinstance(message_object, Text):
            self['text'] = message_object
        elif isinstance(message_object, Image):
            self['image'] = message_object
        elif isinstance(message_object, QuickReplies):
            self['quick_replies'] = message_object
        elif isinstance(message_object, Card):
            self['card'] = message_object
        elif isinstance(message_object, SimpleResponse):
            self['simple_responses'] = message_object
        elif isinstance(message_object, BasicCard):
            self['basic_card'] = message_object
        elif isinstance(message_object, Suggestions):
            self['suggestions'] = message_object
        elif isinstance(message_object, LinkOutSuggestion):
            self['link_out_suggestion'] = message_object
        elif isinstance(message_object, ListSelect):
            self['list_select'] = message_object
        elif isinstance(message_object, CarouselSelect):
            self['carousel_select'] = message_object
        else:
            self['payload'] = message_object
