class LinkOutSuggestion(dict):
    """
    {
      "destinationName": string,
      "uri": string,
    }
    """

    def __init__(self, uri: str = None, destination_name: str = None):
        super().__init__()

        self['uri'] = uri
        self['destinationName'] = destination_name
