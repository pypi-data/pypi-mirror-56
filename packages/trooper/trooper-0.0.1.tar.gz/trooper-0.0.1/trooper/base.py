import json
import uuid


class ID:
    def __init__(self):
        self.uuid = uuid.uuid4()

    def __str__(self):
        return self.uuid.hex

    def __repr__(self):
        return "ID("+self.uuid.hex+")"

    def __eq__(self, other):
        if isinstance(other, ID):
            return self.uuid.hex == other.uuid.hex
        if isinstance(other, uuid.UUID):
            return self.uuid.hex == other.uuid
        if isinstance(other, str):
            return self.uuid.hex == other

    def __hash__(self):
        return self.uuid.int


class TrooperBaseClass:
    """ Base class for long living object classes """
    def __init__(self):
        self._id = ID()

    def get_id(self):
        return self._id

    def __str__(self):
        return type(self).__name__+"("+str(self._id)+")"

    def __repr__(self):
        return type(self).__name__+"("+str(self._id)+")"


class State:
    def __init__(self, state_name):
        self.state_name = state_name

    def __str__(self):
        return "State('"+self.state_name+"')"


class Action:
    def __init__(self, action_key, begin_state, end_state, message_handler):
        self.action_key = action_key
        self.begin_state = begin_state
        self.end_state = end_state
        self.message_handler = message_handler


class Message:
    def __init__(self, action, data):
        self.action = action
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def to_object(message_string):  # raises JSONDecodeError, KeyError
        json_obj = json.loads(message_string)
        message_obj = Message(action=json_obj['action'], data=json_obj['data'])
        return message_obj
