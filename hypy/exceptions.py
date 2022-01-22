class HypyException(Exception):
    """A Hypy Exception"""

class InvalidHTTPCode(HypyException):
    """Exception to raise when an HTTP code is not what it was expected to be"""

    def __init__(self, code, acceptable_codes) -> None:
        super().__init__(
            "Received HTTP Code {} while only codes {} were expected".format(code, ', '.join(acceptable_codes))
        )

class UsernameNotFound(HypyException):
    """Exception to raise when a minecraft user was not found"""

    def __init__(self, username) -> None:
        super().__init__(
            "A minecraft user with the name '{}' could not be found".format(username)
        )
        self.username = username


class UUIDNotFound(HypyException):
    """Exception to raise when a minecraft user was not found"""

    def __init__(self, uuid) -> None:
        super().__init__(
            "A minecraft user with the UUID '{}' could not be found".format(uuid)
        )
        self.uuid = uuid


class InvalidAccountDescriptor(HypyException):
    """Exception to raise when an invalid account descriptor was passed"""

    def __init__(self, account) -> None:
        super().__init__(
            "The passed argument '{}' cannot be an account's name or UUID".format(
                account
            )
        )


class HypixelNoSuccess(HypyException):
    """Exception to raise when Hypixel returns success=false"""

    def __init__(self, cause) -> None:
        super().__init__("Hypixel returned success=false, cause: {}".format(cause))


class NotEnoughArguments(HypyException):
    """Exception to raise when not enough arguments were passed in"""

    def __init__(self, cause) -> None:
        super().__init__(
            "You did not pass enough arguments, at least one of {} is required".format(
                cause
            )
        )


class ApiOffException(HypyException):
    """Exception to raise when a disabled API gets queried"""

    def __init__(self, cause) -> None:
        super().__init__("Api {} is turned off and cant be queried".format(cause))


class MalformedIDException(HypyException):
    """Exception to raise when a malformed Item ID was passed in"""

    def __init__(self, cause) -> None:
        super().__init__("ID {} is malformed".format(cause))


class ContentTypeException(HypyException):
    """Exception to raise when Hypixel API returned the wrong content type"""

    def __init__(self, cause) -> None:
        super().__init__("Hypixel API returned wrong content type: {}".format(cause))


class MissingParamException(HypyException):
    """Exception to raise when parameters are missing"""

    def __init__(self, cause) -> None:
        super().__init__("Missing any parameter from {}".format(cause))


class InvalidSkillException(HypyException):
    """Exception to raise when an invalid skill was passed in"""

    def __init__(self, cause) -> None:
        super().__init__("The skill {} is invalid".format(cause))


class InvalidProfileException(HypyException):
    """Exception to raise when a profile was not found"""

    def __init__(self, cause) -> None:
        super().__init__("The profile {} is invalid".format(cause))


class InvalidProfileNameException(HypyException):
    """Exception to raise when an invalid profile name was passed in"""

    def __init__(self, cause) -> None:
        super().__init__("The profile name {} is invalid".format(cause))


class ExceededMaxRetries(HypyException):
    """Exception to raise when max retries were exceeded"""

    def __init__(self, cause) -> None:
        super().__init__("Exceeded max retries: {}".format(str(cause)))


class InvalidQueryTypeException(HypyException):
    """Exception to raise when an invalid query type was passed in"""

    def __init__(self, cause) -> None:
        super().__init__("Invalid query type: {}".format(cause))


class NoProfilesFoundException(HypyException):
    """Exception to raise when no profiles were found"""

    def __init__(self, cause) -> None:
        super().__init__("Couldnt find any profiles for uuid: {}".format(cause))


class NoProfileInfoAvailableException(HypyException):
    """Exception to raise when no profiles provide any skill information"""

    def __init__(self) -> None:
        super().__init__(
            "None of the available profiles had any of the information needed to find profile"
        )


class NotInGuildException(HypyException):
    """Exception to raise a person is not in guild but guild is queried for person"""  # this docstring sucks?

    def __init__(self, cause) -> None:
        super().__init__("{} is not in the guild".format(cause))


class MaroNoSuccess(HypyException):
    """Exception to raise when the Maro API returns success=false"""

    def __init__(self, status, cause) -> None:
        super().__init__("Maro returned status={}, cause: {}".format(status, cause))
