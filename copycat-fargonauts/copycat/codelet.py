class Codelet(object):
    def __init__(self, name, urgency, arguments, currentTime):
        self.name = name
        self.urgency = urgency
        self.arguments = arguments
        self.birthdate = currentTime

    def __repr__(self):
        return '<Codelet: %s>' % self.name
