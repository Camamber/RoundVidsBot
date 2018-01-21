class User:
    state=''
    _id=''
    token=''
    
    def __init__(self, _id):
        self.state = 'token'
        self._id=_id
        
