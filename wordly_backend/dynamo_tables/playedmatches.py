from aws_cdk import aws_dynamodb as dynamodb
import aws_cdk as cdk
def played_User_Matches(scope, table_name):
    MatchesPlayed= dynamodb.Table(
        scope, 'Matches Played',
        table_name=table_name,
         partition_key=dynamodb.Attribute(
                name='email',
                type=dynamodb.AttributeType.STRING
            ),
        removal_policy=cdk.RemovalPolicy.RETAIN,
        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    )
    return MatchesPlayed
    
