class ServerException(BaseException):
    def __init__(self, code, message, description, **kwargs):
        self.code = code
        self.message = message
        self.description = description
        self.arguments = kwargs

    def __iter__(self):
            yield ('code', self.code)
            yield ('message', self.message)
            yield ('description', self.description)

            for key, value in self.arguments.items():
                yield (key, value)
