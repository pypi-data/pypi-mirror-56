from typing import List
from .CarouselItem import CarouselItem
from .Image import Image
from .SelectItemInfo import SelectItemInfo


class CarouselSelect(dict):
    """
    {
      'item_list': [
        {
          object(carouselItem)
        }
      ]
    }
    """

    def __init__(self, *carousel_items: CarouselItem):
        super().__init__()

        self['item_list'] = []
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['item_list'].append(item)

    def add_carousel_items(self, *carousel_items: CarouselItem) -> List[CarouselItem]:
        for item in carousel_items:
            assert isinstance(item, CarouselItem)
            self['item_list'].append(item)
        return self['item_list']

    def add_carousel_item(self, key: str, title: str, description: str = None, image_uri: str = None,
                          image_text: str = None,
                          *synonyms: str) -> CarouselItem:

        carousel_item = CarouselItem(title=title, description=description, image=Image(uri=image_uri,
                                                                                       accessibility_text=image_text
                                                                                       ),
                                     info=SelectItemInfo(key=key, *synonyms))
        self['item_list'].append(carousel_item)
        return carousel_item
