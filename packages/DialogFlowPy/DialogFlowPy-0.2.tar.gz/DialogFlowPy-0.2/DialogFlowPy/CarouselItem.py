from .SelectItemInfo import SelectItemInfo
from .Image import Image


class CarouselItem(dict):
    """
    {
      'info': {
        object(SelectItemInfo)
      },
      'title': string,
      'description': string,
      'image': {
        object(Image)
      }
    }
    """

    def __init__(self, title: str = None, description: str = None, image: Image = None, info: SelectItemInfo = None):
        super().__init__()

        if info is not None:
            self['info'] = info

        if image is not None:
            self['image'] = image

        if title is not None:
            self['title'] = title

        if description is not None:
            self['description'] = description

    def add_info(self, key: str, *synonyms: str) -> SelectItemInfo:
        self['info'] = SelectItemInfo(key=key, *synonyms)
        return self['info']

    def add_image(self, uri: str, accessibility_text: str = None) -> Image:
        self['image'] = Image(uri=uri, accessibility_text=accessibility_text)
        return self['image']
