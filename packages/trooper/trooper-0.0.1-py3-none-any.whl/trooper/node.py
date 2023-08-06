import logging

from tornado.websocket import WebSocketHandler

from trooper.base import TrooperBaseClass

logger = logging.getLogger(__name__)


class Node(TrooperBaseClass, WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        TrooperBaseClass.__init__(self)
        # hold references to server and cluster (for quick access)
        self.server = None  # set by server on initialization
        self.cluster = None  # set and reset by cluster's add method
        self.state = None
        WebSocketHandler.__init__(self, application, request, **kwargs)

    def initialize(self, server):
        self.server = server
        self.state = server.get_init_state()
        self.cluster = None
        logger.info(str(self) + "connected")

    def check_origin(self, origin):  # Only for debug. Remove in prod. [for CSRF]
        if not self.server.csrf_check:
            return True
        return WebSocketHandler.check_origin(self, origin)

    def open(self):
        self.server.handle_node_init(self)

    def on_message(self, message_string):
        logger.info("Node " + str(id(self)) + " received : " + message_string)
        self.server.handle_node_message(self, message_string)

    def send_message(self, message):
        self.write_message(message.to_json())

    def send_message_to_cluster(self, message):
        self.cluster.send_message(self, message)


class Cluster(TrooperBaseClass):
    def __init__(self):
        super(Cluster, self).__init__()
        self.node_set = set()

    def get_id_as_string(self):
        return str(self.get_id())

    def add_node(self, node):
        self.node_set.add(node)
        node.cluster = self
        logger.info("Adding " + str(node) + " to " + str(self)
                    + " [node count=" + str(self.get_node_count()) + "]")

    def remove_node(self, node):
        self.node_set.remove(node)
        node.cluster = None
        logger.info("Removing " + str(node) + " from " + str(self)
                    + " [node count=" + str(self.get_node_count()) + "]")

    def get_node_count(self):
        return len(self.node_set)

    def send_message(self, sender_node, message):
        for node in self.node_set:
            if node is not sender_node:
                node.send_message(message)
        logger.debug(str(sender_node) + "sending message to " + str(self))
