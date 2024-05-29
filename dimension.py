class dimension:
    def __init__(self, shape=[]):
        self.shape = shape
    def __item__(self, index):
        if index >= len(self.shape):
            return 1
        return self.shape[index]