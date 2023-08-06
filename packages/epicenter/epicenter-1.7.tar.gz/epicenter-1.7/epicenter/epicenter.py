"""Module for Persistence in the Python worker
Note - this is just a stub to allow code to run in a local IDE yet be uploaded to Epicenter.
"""
class Epicenter:


    @staticmethod
    def subscribe(name, function):
        pass

    @staticmethod
    def publish(name, *args, **kwargs):
        pass

    @staticmethod
    def record(name, value):
        pass

    @staticmethod
    def log(level, message):
        pass

    @staticmethod
    def scribble(level, message):
        pass

    @staticmethod
    def callback(name, arguments):
        pass

    @staticmethod
    def register_custom_encoder(custom_type, custom_encoder):
        pass

    @staticmethod
    def register_custom_decoder(custom_type, custom_decoder):
        pass
