"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import grpc


class IRService:
    name = 'AbstractService'
    short_name = 'as'
    stub_cls = None
    media_types = []
    _unhandled_error_message = """
There is an unhandled error in grpc.
status: {status}, details: {details}
This error may be produced if:
  *  You have wrong key to connect to the server. Generate new one and try again
  *  Something really bad happens with our server. If generating a new keys doesn't help, please let us know
    """

    def __init__(self, auth):
        ssl_cred = grpc.ssl_channel_credentials(auth.ssl_credentials().ca(),
                                                auth.ssl_credentials().key(),
                                                auth.ssl_credentials().cert())

        token_cred = grpc.access_token_call_credentials(auth.token())

        channel_cred = grpc.composite_channel_credentials(ssl_cred, token_cred)
        self.channel = grpc.secure_channel(auth.host(), channel_cred,
                                           options=[('grpc.max_send_message_length', -1),
                                                    ('grpc.max_receive_message_length', -1)])

        self.stub = self.stub_cls(self.channel)

    def _handle_error(self, error):
        raise Exception(self._unhandled_error_message.format(status=error.code(), details=error.details()))
