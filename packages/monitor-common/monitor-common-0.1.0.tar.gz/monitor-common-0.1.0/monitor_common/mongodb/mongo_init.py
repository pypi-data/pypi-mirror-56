"""Contains utility functions to connect to the MongoDB."""
import mongoengine


def global_init():
    """Initialise the connection to the MongoDB."""
    mongoengine.register_connection(alias="monitor", name="monitor")
