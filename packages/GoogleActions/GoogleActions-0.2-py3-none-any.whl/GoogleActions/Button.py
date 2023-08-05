from .OpenUrlAction import OpenUrlAction
from .AndroidApp import AndroidApp
from . import UrlTypeHint
from .VersionsFilter import VersionsFilter


class Button(dict):
    """
    {
      "title": string,
      "openUrlAction": {
        object(OpenUrlAction)
      },
    }
    """

    def __init__(self, title: str = None, open_url_action: OpenUrlAction = None):
        super(Button, self).__init__()

        if title is not None:
            self['title'] = title
        if open_url_action is not None:
            self['openUrlAction'] = open_url_action

    def add_open_url_action(self, url: str = None, package_name: str = None, type_hint: UrlTypeHint = None,
                            *versions_list: VersionsFilter):

        self['openUrlAction'] = OpenUrlAction(url=url,
                                              android_app=AndroidApp(package_name=package_name, *versions_list),
                                              type_hint=type_hint)

        return self['openUrlAction']
