
class ConfigurationError(Exception):

    def __init__(self, *args: object) -> None:
        self.invalid_settings = args
        super().__init__(*args)

    def __str__(self) -> str:
        return 'Improperly configured settings: ' + ', '.join(self.invalid_settings)

class DiscardedAction(Exception):
    pass

class InvalidInstance(Exception):
    pass

class InvalidToken(ValueError):
    pass
