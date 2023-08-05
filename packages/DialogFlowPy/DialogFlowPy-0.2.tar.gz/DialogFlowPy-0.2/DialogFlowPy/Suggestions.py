from typing import List
from .Suggestion import Suggestion


class Suggestions(dict):
    """
    {
      "suggestions": [
        {
          object(Suggestion)
        }
      ]
    }
    """

    def __init__(self, *suggestions: List[Suggestion]):
        super().__init__()
        
        self['suggestions'] = []
        for item in suggestions:
            self['suggestions'].append(item)

    def add_suggestions(self, *suggestions: List[Suggestion]):
        for item in suggestions:
            self['suggestions'].append(item)
        return self
