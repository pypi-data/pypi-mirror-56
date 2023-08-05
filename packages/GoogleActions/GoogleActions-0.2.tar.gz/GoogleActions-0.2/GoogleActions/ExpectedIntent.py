from .OpenUrlAction import OpenUrlAction
from . import UrlTypeHint
from .AndroidApp import AndroidApp
from .VersionsFilter import VersionsFilter
from . import Permission
from .Extension import Extension


class ExpectedIntent(dict):
    """
    {
      "intent": string,
      "inputValueData": Extension,
      "parameterName": string,
    }
    """

    def __init__(self, intent: str = None, parameter_name: str = None, input_value: Extension = None):
        super().__init__()

        if intent is not None:
            self['intent'] = intent

        self['inputValueData'] = input_value

        if parameter_name is not None:
            self['parameterName'] = parameter_name

    def add_input_values(self, input_type: str, **fields) -> Extension:
        self['inputValueData'] = Extension(extention_type=input_type, **fields)
        return self['inputValueData']

    def request_confirmation(self, request_confirmation_text: str):
        """
        Obtain a confirmation from the user (for example, an answer to a yes or no question).
        :return:  bool
        """

        self['intent'] = 'actions.intent.CONFIRMATION'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.ConfirmationValueSpec')
        self['inputValueData']['dialogSpec'] = {'requestConfirmationText': request_confirmation_text}

        return self

    def request_date_time(self, date_time_text: str = None, date_text: str = None, time_text: str = None):
        """
        Obtain a date and time input from the user.
        :return: bool
        """

        self['intent'] = 'actions.intent.DATETIME'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.DateTimeValueSpec')
        self['inputValueData']['dialogSpec'] = {
            "requestDatetimeText": date_time_text,
            "requestDateText": date_text,
            "requestTimeText": time_text
        }
        return self

    def request_place(self):
        """
        Obtain an address or saved location from the user.
        :return: bool
        """
        self['intent'] = 'actions.intent.PLACE'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.PlaceValueSpec')
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_delivery_address(self, reason: str = None):
        """
        Obtain a delivery address input from the user.
        :return: bool
        """

        self['intent'] = 'actions.intent.DELIVERY_ADDRESS'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.DeliveryAddressValueSpec')
        self['inputValueData']['addressOptions'] = {
            "reason": reason
        }
        return self

    def request_link(self, url: str = None, package_name: str = None, type_hint: UrlTypeHint = None,
                     *version_tuples: tuple):
        """
        Requests a deep link flow into another platform.
        :return: bool
        """
        self['intent'] = 'actions.intent.LINK'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.LinkValueSpec')
        versions_list = [VersionsFilter(min_version=item[0], max_version=item[1]) for item in version_tuples]
        self['inputValueData']['openUrlAction'] = OpenUrlAction(url=url,
                                                                android_app=AndroidApp(package_name=package_name,
                                                                                       *versions_list),
                                                                type_hint=type_hint)
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_select_option(self):
        """
        Receive the selected item from a list or carousel UI.
        :return: bool
        """
        self['intent'] = 'actions.intent.OPTION'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.OptionValueSpec')
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_permission(self, opt_context_text: str = None, *permissions: Permission):
        """
        Obtain the user's full name, coarse location, or precise location, or all 3.
        :return: bool
        """
        self['intent'] = 'actions.intent.PERMISSION'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.PermissionValueSpec')
        self['inputValueData']['optContext'] = opt_context_text
        self['inputValueData']['permissions'] = permissions
        self['inputValueData']['updatePermissionValueSpec'] = {
            "intent": self['intent'],
            "arguments": []
        }
        return self

    def request_sign_in(self, opt_context_text: str = None):
        """
        Requests an account linking flow to link a user's account.
        :return: bool
        """
        if opt_context_text is not None:
            assert isinstance(opt_context_text, str)

        self['intent'] = 'actions.intent.SIGN_IN'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.SignInValueSpec')
        self['inputValueData']['optContext'] = opt_context_text
        return self

    def request_user_text(self):
        self['intent'] = 'actions.intent.TEXT'
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_new_surface(self):
        self['intent'] = 'actions.intent.NEW_SURFACE'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.NewSurfaceValueSpec')
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_transaction_requirements_check(self):
        self['intent'] = 'actions.intent.TRANSACTION_REQUIREMENTS_CHECK'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.TransactionRequirementsCheckSpec')
        # self['inputValueData']['dialogSpec'] =
        return True

    def request_transaction_decision(self):
        self['intent'] = 'actions.intent.actions.intent.TRANSACTION_DECISION'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.TransactionDecisionValueSpec')
        # self['inputValueData']['dialogSpec'] =
        return self

    def request_register_update(self):
        self['intent'] = 'actions.intent.REGISTER_UPDATE'
        self['inputValueData'] = Extension('type.googleapis.com/google.actions.v2.RegisterUpdateValueSpec')
        # self['i nput_values['dialogSpec'] =
        return self
