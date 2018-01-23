class User:
    state=''
    _id=''
    token=''
    channels=[]


    def __init__(self, _id, state='token_adding', token='', channels=[]):
        self._id=_id
        self.state = state
        self.token=token
        self.channels = channels        
        
    def add_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)

    def to_json(self):
        return {'id': self._id, 'state':self.state, 'token':self.token, 'channels':self.channels}
