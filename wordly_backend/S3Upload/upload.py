from aws_cdk import aws_s3, aws_s3_deployment, Stack
from constructs import Construct


class BackupS3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
     
        bucket = aws_s3.Bucket(
                self,
                "wordsFileList",
                bucket_name="wordsfilelist-for-wordly-2024",
                block_public_access=aws_s3.BlockPublicAccess.BLOCK_ACLS
            )  

        bucket.grant_public_access()
       
        # Deploy multiple files into the S3 bucket
        aws_s3_deployment.BucketDeployment(
                self,
                f"DeployWordlyList",
                sources=[aws_s3_deployment.Source.asset('./wordly_backend/S3Upload/WordlyList')],
                destination_bucket=bucket,
                destination_key_prefix='WordlyList'
            )
        


    