#!/usr/bin/env python3
import os

import aws_cdk as cdk

from wordly_backend import (awsSetUpIsUp, WordlyBackendStack, WordlyBackendStage, All_Gateways, BackupS3Stack)
from dotenv import load_dotenv

load_dotenv()

aws_account_id = os.getenv("AWS_ACCOUNT_ID")
aws_current_region = os.getenv("AWS_USER_REGION")
stage = os.getenv("CURRENT_STAGE")
app = cdk.App()

APP_ENV = cdk.Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')
)



BackupS3Stack(app,"Storage")
awsSetUpIsUp()
WordlyBackendStack(app, "WordlyBackendStack")
All_Gateways(app,"Gateways",stage_name=stage)
WordlyBackendStage(app, "dev", env=APP_ENV)


app.synth()
