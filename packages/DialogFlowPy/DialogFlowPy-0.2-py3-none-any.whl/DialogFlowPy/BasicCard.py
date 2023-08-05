from .Button import Button
from .Image import Image
from .OpenUriAction import OpenUriAction


class BasicCard(dict):
    """
    {
      "title": string,
      "subtitle": string,
      "formattedText": string,
      "image": {
        object(Image)
      },
      "buttons": [
        {
          object(Button)
        }
      ],
    }
    """

    def __init__(self, title: str = None, formatted_text: str = None, subtitle: str = None, image: Image = None,
                 *buttons: Button):

        super().__init__()
        self['buttons'] = []

        for item in buttons:
            assert isinstance(item, Button)
            self['buttons'].append(item)

        if title is not None:
            self['title'] = title

        if formatted_text is not None:
            self['formattedText'] = formatted_text

        if subtitle is not None:
            self['subtitle'] = subtitle

        if image is not None:
            self['image'] = image

    def add_button(self, title: str, uri: str) -> Button:
        button = Button(title=title, open_uri_action=OpenUriAction(uri=uri))
        self['buttons'].append(button)

        return button
