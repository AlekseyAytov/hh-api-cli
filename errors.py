
class AuthenticationError(Exception):
    """ Need change or get access token """

class SearchRequestError(Exception):
    """ Error while making search request """

class OpenResumeError(Exception):
    """ Error while making request for open resume with contacts"""