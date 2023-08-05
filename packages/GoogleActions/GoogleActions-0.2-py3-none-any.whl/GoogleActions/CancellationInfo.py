class CancellationInfo(dict):
    """
    {
      "reason": string,
    }
    """

    def __init__(self, reason: str = None):
        super(CancellationInfo, self).__init__()

        if reason is not None:
            self['reason'] = reason
