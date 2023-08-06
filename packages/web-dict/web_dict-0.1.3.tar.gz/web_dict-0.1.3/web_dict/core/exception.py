class NoProviderError:
    def __init__(self, dict_type: str):
        super(NoProviderError, self).__init__(f"No provider named: {dict_type}")


class NoTranslationSegmentError(Exception):
    def __init__(self, bp: str, in_: str, tar: str):
        super(NoTranslationSegmentError, self).__init__(f"No segment of {bp} for: {in_} -> {tar}")
