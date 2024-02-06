
import aws_cdk.aws_apigateway as _apigw
import aws_cdk.aws_lambda as _lambda
from constructs import Construct
class Store_Match_Result_Gateway(Construct):
    
    def __init__(self, scope: Construct, id:str, stage_name: str, users_table, user_played_matches, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        storeMatchResult_lambdafunction = _lambda.Function(
            self, "Store_Match_Result_Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="storeMatchResult.storeMatchResult_handler",
            code= _lambda.Code.from_asset("./lambda/user")
        )
                
        storeMatchResultApi = _apigw.RestApi(
                self,'Store Match Result',
                description="Play Macthes gateway",
                deploy_options=_apigw.StageOptions(stage_name=stage_name),
                default_cors_preflight_options=_apigw.CorsOptions(
                        allow_origins=_apigw.Cors.ALL_ORIGINS,
                        allow_methods=_apigw.Cors.ALL_METHODS,
                        allow_credentials= True,
                        allow_headers= _apigw.Cors.DEFAULT_HEADERS
                    ))
        users_table.grant_read_write_data(storeMatchResult_lambdafunction)
        user_played_matches.grant_read_write_data(storeMatchResult_lambdafunction)
        integration = _apigw.LambdaIntegration(storeMatchResult_lambdafunction)
        storeMatchResultApi_resource = storeMatchResultApi.root.add_resource('storeMatchResult')
        storeMatchResultApi_resource.add_method("POST", integration, request_parameters={
                "method.request.querystring.email": True,
                "method.request.querystring.result": True,
            },authorization_type=_apigw.AuthorizationType.NONE)

        


