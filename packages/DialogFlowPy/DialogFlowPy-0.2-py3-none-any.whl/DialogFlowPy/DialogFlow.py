from typing import List
from .Context import Context
from .Message import Message
from .Text import Text
from .Image import Image
from .QuickReplies import QuickReplies
from .Card import Card
from .SimpleResponse import SimpleResponse
from .BasicCard import BasicCard
from .Suggestions import Suggestions
from .LinkOutSuggestion import LinkOutSuggestion
from .ListSelect import ListSelect
from .CarouselSelect import CarouselSelect
from .CarouselItem import CarouselItem
from .ListItem import ListItem
from .Suggestion import Suggestion
from .Button import Button
from . import PlatformEnum


class DialogFlow(dict):
    """

    Main class to handle interface with google actions
    Dialogflow Request:
    {
  "responseId": "c4b863dd-aafe-41ad-a115-91736b665cb9",
  "queryResult": {
    "queryText": "GOOGLE_ASSISTANT_WELCOME",
    "action": "input.welcome",
    "parameters": {},
    "allRequiredParamsPresent": true,
    "fulfillmentText": "",
    "fulfillmentMessages": [],
    "outputContexts": [
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/google_assistant_welcome"
      },
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_screen_output"
      },
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/google_assistant_input_type_voice"
      },
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_audio_output"
      },
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_web_browser"
      },
      {
        "name": "projects/${PROJECTID}/agent/sessions/${SESSIONID}/contexts/actions_capability_media_response_audio"
      }
    ],
    "intent": {
      "name": "projects/${PROJECTID}/agent/intents/8b006880-0af7-4ec9-a4c3-1cc503ea8260",
      "displayName": "Default Welcome Intent"
    },
    "intentDetectionConfidence": 1,
    "diagnosticInfo": {},
    "languageCode": "en-us"
  },
  "originalDetectIntentRequest": {
    "source": "google",
    "version": "2",
    "payload": {
      "isInSandbox": true,
      "surface": {
        "capabilities": [
          {
            "name": "actions.capability.SCREEN_OUTPUT"
          },
          {
            "name": "actions.capability.AUDIO_OUTPUT"
          },
          {
            "name": "actions.capability.WEB_BROWSER"
          },
          {
            "name": "actions.capability.MEDIA_RESPONSE_AUDIO"
          }
        ]
      },
      "inputs": [
        {
          "rawInputs": [
            {
              "query": "query from the user",
              "inputType": "KEYBOARD"
            }
          ],
          "arguments": [
            {
              "rawText": "query from the user",
              "textValue": "query from the user",
              "name": "text"
            }
          ],
          "intent": "actions.intent.TEXT"
        }
      ],
      "user": {
        "lastSeen": "2018-03-16T22:08:48Z",
        "permissions": [
          "UPDATE"
        ],
        "locale": "en-US",
        "userId": "ABwppHEvwoXs18xBNzumk18p5h02bhRDp_riW0kTZKYdxB6-LfP3BJRjgPjHf1xqy1lxqS2uL8Z36gT6JLXSrSCZ"
      },
      "conversation": {
        "conversationId": "${SESSIONID}",
        "type": "NEW"
      },
      "availableSurfaces": [
        {
          "capabilities": [
            {
              "name": "actions.capability.SCREEN_OUTPUT"
            },
            {
              "name": "actions.capability.AUDIO_OUTPUT"
            }
          ]
        }
      ]
    }
  },
  "session": "projects/${PROJECTID}/agent/sessions/${SESSIONID}"
}

    Dialogflow response:
    {
      "fulfillmentText": string,
      "fulfillmentMessages": [
        {
          object(Message)
        }
      ],
      "source": string,
      "payload": {
        object
      },
      "outputContexts": [
        {
          object(Context)
        }
      ],
      "followupEventInput": {
        object(EventInput)
      }
    }
    """

    def __init__(self, platform: PlatformEnum, request_data_json: dict, version: str = 'v1'):
        super().__init__()

        self._platform = platform.name

        print('initializing Dialogflow with: ', version, request_data_json)
        assert isinstance(request_data_json, dict)
        super(DialogFlow, self).__init__(request_data_json)

        self._session_id = request_data_json.get('session')
        print('session_id : ', self._session_id)

        self._result = request_data_json.get('queryResult') or request_data_json.get('result')
        print('result: ', self._result)

        self['parameters'] = self._result.get('parameters')
        print('parameters: ', self['parameters'])

        self._action = self._result.get('action')
        if self._action == 'input.welcome':
            self._action = 'welcome'
        print('action: ', self._action)

        self['context']: List[Context] = []
        contexts = self._result.get('outputContexts') or self._result.get('contexts')
        for context in contexts:
            self['context'].append(Context(context.name))
        print('context: ', self['context'])

        self._max_msg_length = 550
        self['fulfillmentMessages']: List[Message] = []
        self['source'] = None
        self['payload'] = None
        self['followupEventInput'] = None
        self['fulfillmentText'] = ''

    @property
    def payload(self):
        return self['payload']

    @property
    def contexts(self) -> List[Context]:
        return self['context']

    @property
    def source(self) -> str:
        return self['source']

    def add_fulfillment_messages(self, *messages: Message) -> List[Message]:
        for item in messages:
            self['fulfillmentMessages'].append(item)
        return self['fulfillmentMessages']

    def delete_messages(self):
        self['fulfillmentMessages'] = []
        return self

    def add_text_message(self, text) -> Text:
        self['fulfillmentText'] = text
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=Text(text)))
        return text

    def add_image(self, uri: str = None, accessibility_text: str = None) -> Image:
        image = Image(uri=uri, accessibility_text=accessibility_text)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=image))
        return image

    def add_quick_reply(self, title, *quick_replies: str) -> QuickReplies:
        quick_reply: QuickReplies = QuickReplies(title=title)
        quick_reply.add_quick_replies(*quick_replies)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=quick_reply))
        return quick_reply

    def add_card(self, title: str, subtitle: str, image_uri: str, *buttons: Button) -> Card:
        card: Card = Card(title=title, subtitle=subtitle, image_uri=image_uri, *buttons)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=card))
        return card

    def add_payload(self, payload):
        self['payload'] = payload
        return self['payload']

    def add_simple_response(self, text_to_speech: str = None, ssml: str = None, display_text: str = None) \
            -> SimpleResponse:
        simple_response: SimpleResponse = SimpleResponse(text_to_speech=text_to_speech, ssml=ssml,
                                                         display_text=display_text)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=simple_response))
        return simple_response

    def add_basic_card(self, title: str = None, formatted_text: str = None, subtitle: str = None, image_uri: str = None,
                       image_text: str = None, *buttons: Button) -> BasicCard:
        basic_card: BasicCard = BasicCard(title=title, formatted_text=formatted_text, subtitle=subtitle,
                                          image=Image(uri=image_uri, accessibility_text=image_text),
                                          *buttons)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=basic_card))
        return basic_card

    def add_suggestions(self, *titles: str) -> Suggestions:
        suggestions_list: List[Suggestion] = [Suggestion(title=item) for item in titles]
        suggestions: Suggestions = Suggestions(*suggestions_list)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=suggestions))
        return suggestions

    def add_link_out_suggestion(self, uri: str, destination_name: str) -> LinkOutSuggestion:
        link_out_suggestion: LinkOutSuggestion = LinkOutSuggestion(uri=uri, destination_name=destination_name)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=link_out_suggestion))
        return link_out_suggestion

    def add_list_select(self, title: str, *list_items: ListItem) -> ListSelect:
        list_select: ListSelect = ListSelect(title=title, *list_items)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=list_select))
        return list_select

    def add_carousel_select(self, *carousel_items: CarouselItem) -> CarouselSelect:
        carousel_select: CarouselSelect = CarouselSelect(*carousel_items)
        self['fulfillmentMessages'].append(Message(platform=self._platform, message_object=carousel_select))
        return carousel_select

    def add_source(self, source: str):
        assert isinstance(source, str)
        self['source'] = source
        return self

    def add_context(self, context_name: str, lifespan: int = 0, **parameters) -> List[Context]:
        assert isinstance(context_name, str)
        assert isinstance(lifespan, int)

        for context in self['context']:
            if context.name == context_name:
                context.update_parameters(**parameters)
                context.lifespan = lifespan
                return self['context']

        self['context'].append(Context(name=context_name, lifespan_count=lifespan, **parameters))
        print('context: ', self['context'])
        return self['context']

    def update_context(self, context_name: str, lifespan: int = 0, **parameters) -> List[Context]:
        assert isinstance(context_name, str)
        assert isinstance(lifespan, int)

        for context in self['context']:
            if context.name == context_name:
                context.lifespan_count = lifespan
                context.update_parameters(**parameters)

        return self['context']

    def delete_context(self, *context_names) -> bool:

        if len(context_names) == 0:
            self['context'] = list()

        else:
            for context_name in context_names:
                assert isinstance(context_name, str)

                for context in self['context']:
                    if context.name == context_name:
                        self['context'].remove(context)

        return True
