class Image(dict):
    """
    {
      "imageUri": string,
      "accessibilityText": string
    }
    """

    def __init__(self, uri: str = None, accessibility_text: str = None):
        super().__init__()

        if uri is not None:
            self['imageUri'] = uri
        if accessibility_text is not None:
            self['accessibilityText'] = accessibility_text
