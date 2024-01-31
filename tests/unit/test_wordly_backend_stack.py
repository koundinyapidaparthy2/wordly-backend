import aws_cdk as core
import aws_cdk.assertions as assertions

from wordly_backend.wordly_backend_stack import WordlyBackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in wordly_backend/wordly_backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WordlyBackendStack(app, "wordly-backend")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
