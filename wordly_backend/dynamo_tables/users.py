from aws_cdk import aws_dynamodb as dynamodb
import aws_cdk as cdk
def create_user_table(scope, table_name):
    users_table= dynamodb.Table(
        scope, 'Users',
        table_name=table_name,
         partition_key=dynamodb.Attribute(
                name='email',
                type=dynamodb.AttributeType.STRING
            ),
        removal_policy=cdk.RemovalPolicy.RETAIN,
        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    )
    return users_table
    
