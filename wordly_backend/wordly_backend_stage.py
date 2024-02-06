from aws_cdk import (
    Stage
)

from wordly_backend.wordly_backend_stack import WordlyBackendStack
from constructs import Construct


class WordlyBackendStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        WordlyBackendStack(self, "WordlyBackend",
            stack_name=f"wordly-backend-dev"
        )

