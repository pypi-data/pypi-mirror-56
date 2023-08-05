from typing import List
from .ListItem import ListItem
from .Image import Image
from .SelectItemInfo import SelectItemInfo


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

        self['item_list'] = list()
        for item in list_items:
            assert isinstance(item, ListItem)
            self['item_list'].append(item)

        self['title'] = title

    def add_items(self, *list_items: ListItem) -> List[ListItem]:
        for item in list_items:
            assert isinstance(item, ListItem)
            self['item_list'].append(item)
        return self['item_list']

    def add_item(self, key: str, title: str, description: str = None, image_uri: str = None, image_text: str = None,
                 *synonyms: str) -> ListItem:

        list_item: ListItem = ListItem(title=title, description=description, image=Image(uri=image_uri,
                                                                                         accessibility_text=image_text
                                                                                         ),
                                       info=SelectItemInfo(key=key, *synonyms))
        self['item_list'].append(list_item)
        return list_item
