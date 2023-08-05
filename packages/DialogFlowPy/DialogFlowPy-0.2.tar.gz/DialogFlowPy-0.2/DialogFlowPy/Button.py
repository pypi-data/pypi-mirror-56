from .OpenUriAction import OpenUriAction


class Button(dict):
    """
    {
      "title": string,
      "openUriAction": {
        object(OpenUriAction)
      }
    }
    """

    def __init__(self, title: str = None, open_uri_action: OpenUriAction = None):
        super().__init__()
        if title is not None:
            self['title'] = title

        if open_uri_action is not None:
            self['openUriAction'] = open_uri_action

    def add_open_uri_action(self, uri: str = None):
        self['openUriAction'] = OpenUriAction(uri=uri)
        return self['openUriAction']
