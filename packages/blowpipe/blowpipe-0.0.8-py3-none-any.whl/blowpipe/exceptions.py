class BlowpipeError(BaseException):
    def __init__(self, *args, **kwargs):
        super(BlowpipeError, self).__init__(args, kwargs)
