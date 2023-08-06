import logging

from trooper.base import State, Action, Message, TrooperBaseClass
from trooper.node import Cluster, Node

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

logger = logging.getLogger(__name__)


class Server(TrooperBaseClass):
    def __init__(self, url, port=8080, name="TrooperServer", csrf_check=True):  # URL example : '/websocket'
        super(Server, self).__init__()
        self.name = name
        self.url = url
        self.port = port
        self.csrf_check = csrf_check
        self._application = None
        self._ioloop = None
        self._http_server = None

        self._node_states = dict()  # dict of State
        self._node_actions = dict()  # dict of Action
        self._node_clusters = dict()  # dict of Cluster

        self._init_state_key = "_INIT_STATE_"
        self._node_states[self._init_state_key] = State(self._init_state_key)
        self._node_init_handler = None

    def create_node_state(self, state_name):
        if state_name in self._node_states.keys():
            logger.error("[Trooper] State name '" + state_name
                         + "' already exists. Each state should have a unique name on a server.")
            return
        new_state = State(state_name)
        self._node_states[state_name] = new_state
        logger.info("[Trooper] New state with name '" + state_name + "' created on the server")
        return new_state

    def create_node_cluster(self):
        cluster = Cluster()
        self._node_clusters[cluster.get_id_as_string()] = cluster
        logger.info("[Trooper] "+str(cluster)+" created")
        return cluster

    def get_node_cluster(self, cluster_id):
        return self._node_clusters[cluster_id]

    def get_init_state(self):
        return self._node_states[self._init_state_key]

    def set_node_init_handler(self, node_init_handler):
        self._node_init_handler = node_init_handler

    def register_action(self, action_key, begin_state, end_state, message_handler): # need overloaded method to take Action obj
        action = Action(action_key, begin_state, end_state, message_handler)
        self._node_actions[action_key] = action
        logger.info("[Trooper] Action "+action_key+" registered")

    def handle_node_init(self, node):
        if self._node_init_handler is not None:
            self._node_init_handler(node)

    def handle_node_message(self, node, message_string):
        message = Message.to_object(message_string)  # handle exceptions
        action = self._node_actions[message.action]
        if action.begin_state is node.state:
            action.message_handler(node, message)
            node.state = action.end_state

    def start(self):
        handlers = [(self.url, Node, {'server': self}), ]
        self._application = Application(handlers)
        self._http_server = HTTPServer(self._application)
        self._http_server.listen(self.port)
        logger.info("[Trooper] Server " + self.name + " starting at " + self.url + ":" + str(self.port))
        self._ioloop = IOLoop.current()
        self._ioloop.start()  # control waits here when in running state
        self._ioloop.close()
        logger.info("[Trooper] Server successfully stopped")

    def stop(self):
        self._ioloop.add_callback(self._ioloop.stop)
        logger.info("[Trooper] Attempting to stop the server")
