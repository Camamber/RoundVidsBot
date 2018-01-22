class User:
    state=''
    _id=''
    token=''
    channels=[]
    
    def __init__(self, _id):
        self.state = 'token_adding'
        self._id=_id

    def add_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)
