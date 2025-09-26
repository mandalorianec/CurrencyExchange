class ExceptionDTO:
    def __init__(self, exception):
        self.error_name = exception.__class__.__name__
        self.message = str(exception)
