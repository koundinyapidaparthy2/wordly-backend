import aws_cdk as cdk
from aws_cdk import (
    Stack
)
from .user import Login_User_Gateway, SignIn_User_Gateway, Play_Gateway, Played_Matches_Gateway, Store_Match_Result_Gateway
from constructs import Construct
from wordly_backend.dynamo_tables import create_user_table, played_User_Matches
class All_Gateways(Stack):
    def __init__(self, scope: Construct, id: str, stage_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)      

        users_table = create_user_table(self, 'users')
        user_played_matches = played_User_Matches(self,'matches')
        
        Login_User_Gateway(self,"logingateway",stage_name=stage_name, users_table=users_table)
        SignIn_User_Gateway(self,"signingateway",stage_name=stage_name, users_table=users_table)
        Play_Gateway(self,"playgateway",stage_name=stage_name,users_table=users_table)
        Played_Matches_Gateway(self,"playedMatches",stage_name=stage_name,users_table=users_table,user_played_matches=user_played_matches)
        Store_Match_Result_Gateway(self,"storeMatchResult",stage_name=stage_name,users_table=users_table, user_played_matches=user_played_matches)