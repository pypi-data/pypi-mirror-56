from . import ReasonType


class RejectionInfo(dict):
    """
    {
      "type": enum(ReasonType),
      "reason": string,
    }
    """

    def __init__(self, rejection_type: ReasonType, reason: str):
        super(RejectionInfo, self).__init__()

        self['type'] = rejection_type
        self['reason'] = reason
