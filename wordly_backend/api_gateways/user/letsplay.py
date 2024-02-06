
import aws_cdk.aws_apigateway as _apigw
import aws_cdk.aws_lambda as _lambda
from constructs import Construct
class Play_Gateway(Construct):
    
    def __init__(self, scope: Construct, id:str, stage_name: str, users_table, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        play_lambdafunction = _lambda.Function(
            self, "Play_Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="letsplay.play_handler",
            code= _lambda.Code.from_asset("./lambda/user")
        )
                
        letsplay = _apigw.RestApi(
                self,'Play',
                description="Play gateway",
                deploy_options=_apigw.StageOptions(stage_name=stage_name),
                default_cors_preflight_options=_apigw.CorsOptions(
                        allow_origins=_apigw.Cors.ALL_ORIGINS,
                        allow_methods=_apigw.Cors.ALL_METHODS,
                        allow_credentials= True,
                        allow_headers= _apigw.Cors.DEFAULT_HEADERS
                    )
                )
        users_table.grant_read_write_data(play_lambdafunction)
        integration = _apigw.LambdaIntegration(play_lambdafunction)
        letsplay_resource = letsplay.root.add_resource('letsplay')
        letsplay_resource.add_method("POST", integration, request_parameters={
                "method.request.querystring.email": True,
                "method.request.querystring.word": True,
            },authorization_type=_apigw.AuthorizationType.NONE)

        


