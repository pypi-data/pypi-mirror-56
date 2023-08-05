class ScrapingError(Exception):
    def __init__(self, message: str, extra: dict = None):
        self.message = message
        self.extra = extra

    def __str__(self):
        return f'{self.message} with {str(self.extra)}'


class AuthenticationError(ScrapingError):
    """ 인증 프로세스 실패 """


class RetryTaskExitError(ScrapingError):
    """
    Error in retry logic
    Use if no further progress is required
    """
    pass


class RetryTaskSkipAuthError(ScrapingError):
    """
    Error in retry logic
    Use if required except for authentication
    """
    pass


class RetryTaskError(ScrapingError):
    """
    Error in retry logic
    Use if required from authentication
    """
    pass
