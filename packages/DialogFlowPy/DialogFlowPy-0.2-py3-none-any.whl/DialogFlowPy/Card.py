from .Button import Button
from .OpenUriAction import OpenUriAction


class Card(dict):
    """
    {
      "title": string,
      "subtitle": string,
      "imageUri": string,
      "buttons": [
        {
          object(Button)
        }
      ],
    }
    """

    def __init__(self, title: str = None, image_uri: str = None, subtitle: str = None, *buttons: Button):
        super().__init__()

        self['buttons'] = []

        for item in buttons:
            assert isinstance(item, Button)
            self['buttons'].append(item)

        if title is not None:
            self['title'] = title

        if image_uri is not None:
            self['imageUri'] = image_uri

        if subtitle is not None:
            self['subtitle'] = subtitle

    def add_button(self, title: str, uri: str) -> Button:
        button = Button(title=title, open_uri_action=OpenUriAction(uri=uri))
        self['buttons'].append(button)

        return button
