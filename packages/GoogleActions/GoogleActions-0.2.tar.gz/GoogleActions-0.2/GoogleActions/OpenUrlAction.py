from . import UrlTypeHint
from .AndroidApp import AndroidApp


class OpenUrlAction(dict):
    """
    {
      "url": string,
      "androidApp": {
        object(AndroidApp)
      },
      "urlTypeHint": enum(UrlTypeHint)
    }
    """

    def __init__(self, url: str = None, android_app: AndroidApp = None, type_hint: UrlTypeHint = None):
        super().__init__()

        if android_app is not None:
            self['androidApp'] = android_app

        if type_hint is not None:
            self['urlTypeHint'] = type_hint

        if url is not None:
            self['url'] = url

    def add_android_app(self, package_name: str, *versions_list) -> AndroidApp:
        self['androidApp'] = AndroidApp(package_name=package_name, *versions_list)

        return self['androidApp']
