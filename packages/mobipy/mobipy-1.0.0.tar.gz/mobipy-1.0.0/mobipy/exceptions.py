class DataSelectorException(Exception):
    """Exception raised when the data selector process has failed"""
    def __init__(self, message=None, parameter=None):
        self.name = "Error when passing parameters to dataset_selector"
        self.message = message
        self.parameter = parameter
    def __str__(self):
        message = self.name
        if self.message is not None:
            message += ". " + self.message
        if self.parameter is not None:
            message += " | Missing keyword parameter: " + self.parameter
        return str(message)