class User:
    last_update = ''

    def __init__(self, last_update):
        self.last_update = last_update
        
    def get_last(self):
        return self.last_update

    def set_last(self, last_update):
        self.last_update = last_update
        
