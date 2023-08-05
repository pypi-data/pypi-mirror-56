class Text:
    """
    {
      "text": [
        string
      ]
    }
    """

    def __init__(self, *texts: str):
        self['text'] = []
        for text in texts:
            self['text'].append(text)
