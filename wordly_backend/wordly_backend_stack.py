from aws_cdk import (
    Stack,
)
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_apigateway as _apigw
from constructs import Construct



class WordlyBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        first_test_lamda_function = _lambda.Function(
            self, "Test_lambda_function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="testLambda.test_handler",
            code= _lambda.Code.from_asset("./lambda")
        )
        api = _apigw.RestApi(self, "WordlyBackendApi",
            description="API for the Wordly backend",
            deploy_options=_apigw.StageOptions(stage_name="dev"),
            default_cors_preflight_options=_apigw.CorsOptions(
                        allow_origins=_apigw.Cors.ALL_ORIGINS,
                        allow_methods=_apigw.Cors.ALL_METHODS,
                        allow_credentials= True,
                        allow_headers= _apigw.Cors.DEFAULT_HEADERS
                    )
        )
        integration = _apigw.LambdaIntegration(first_test_lamda_function)
        api.root.add_method("GET", integration)


