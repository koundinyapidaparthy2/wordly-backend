
import aws_cdk.aws_apigateway as _apigw
import aws_cdk.aws_lambda as _lambda
from constructs import Construct
class Played_Matches_Gateway(Construct):
    
    def __init__(self, scope: Construct, id:str, stage_name: str, users_table, user_played_matches, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        played_matches_lambdafunction = _lambda.Function(
            self, "Played_Matches_Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="playedMatches.playedMatches_handler",
            code= _lambda.Code.from_asset("./lambda/user")
        )
                
        playedMatchesApi = _apigw.RestApi(
                self,'Played Macthes',
                description="Play Macthes gateway",
                deploy_options=_apigw.StageOptions(stage_name=stage_name),
                default_cors_preflight_options=_apigw.CorsOptions(
                        allow_origins=_apigw.Cors.ALL_ORIGINS,
                        allow_methods=_apigw.Cors.ALL_METHODS,
                        allow_credentials= True,
                        allow_headers= _apigw.Cors.DEFAULT_HEADERS
                    )
                )
        users_table.grant_read_write_data(played_matches_lambdafunction)
        user_played_matches.grant_read_write_data(played_matches_lambdafunction)
        integration = _apigw.LambdaIntegration(played_matches_lambdafunction)
        playedMatchesApi_resource = playedMatchesApi.root.add_resource('playedMatches')
        playedMatchesApi_resource.add_method("GET", integration, request_parameters={
                "method.request.querystring.email": True,
            },authorization_type=_apigw.AuthorizationType.NONE)

        


