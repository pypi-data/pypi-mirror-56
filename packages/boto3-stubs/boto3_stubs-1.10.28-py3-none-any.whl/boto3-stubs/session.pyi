# pylint: disable=unused-argument,multiple-statements,unused-import
from typing import Any, List, Union
from typing_extensions import Literal, overload
import boto3
from boto3.exceptions import ResourceNotExistsError, UnknownAPIVersionError
from boto3.resources.base import ServiceResource
from boto3.resources.factory import ResourceFactory
import boto3.utils
from botocore.client import BaseClient
from botocore.config import Config
from botocore.credentials import Credentials
from botocore.loaders import Loader
from botocore.model import ServiceModel
from botocore.waiter import Waiter

try:
    from mypy_boto3.acm import Client as ACMClient
except (ImportError, ModuleNotFoundError):
    ACMClient = Any
try:
    from mypy_boto3.acm_pca import Client as AcmPcaClient
except (ImportError, ModuleNotFoundError):
    AcmPcaClient = Any
try:
    from mypy_boto3.alexaforbusiness import Client as AlexaforbusinessClient
except (ImportError, ModuleNotFoundError):
    AlexaforbusinessClient = Any
try:
    from mypy_boto3.amplify import Client as AmplifyClient
except (ImportError, ModuleNotFoundError):
    AmplifyClient = Any
try:
    from mypy_boto3.apigateway import Client as ApigatewayClient
except (ImportError, ModuleNotFoundError):
    ApigatewayClient = Any
try:
    from mypy_boto3.apigatewaymanagementapi import Client as ApigatewaymanagementapiClient
except (ImportError, ModuleNotFoundError):
    ApigatewaymanagementapiClient = Any
try:
    from mypy_boto3.apigatewayv2 import Client as Apigatewayv2Client
except (ImportError, ModuleNotFoundError):
    Apigatewayv2Client = Any
try:
    from mypy_boto3.application_autoscaling import Client as ApplicationAutoscalingClient
except (ImportError, ModuleNotFoundError):
    ApplicationAutoscalingClient = Any
try:
    from mypy_boto3.application_insights import Client as ApplicationInsightsClient
except (ImportError, ModuleNotFoundError):
    ApplicationInsightsClient = Any
try:
    from mypy_boto3.appmesh import Client as AppmeshClient
except (ImportError, ModuleNotFoundError):
    AppmeshClient = Any
try:
    from mypy_boto3.appstream import Client as AppstreamClient
except (ImportError, ModuleNotFoundError):
    AppstreamClient = Any
try:
    from mypy_boto3.appsync import Client as AppsyncClient
except (ImportError, ModuleNotFoundError):
    AppsyncClient = Any
try:
    from mypy_boto3.athena import Client as AthenaClient
except (ImportError, ModuleNotFoundError):
    AthenaClient = Any
try:
    from mypy_boto3.autoscaling import Client as AutoscalingClient
except (ImportError, ModuleNotFoundError):
    AutoscalingClient = Any
try:
    from mypy_boto3.autoscaling_plans import Client as AutoscalingPlansClient
except (ImportError, ModuleNotFoundError):
    AutoscalingPlansClient = Any
try:
    from mypy_boto3.backup import Client as BackupClient
except (ImportError, ModuleNotFoundError):
    BackupClient = Any
try:
    from mypy_boto3.batch import Client as BatchClient
except (ImportError, ModuleNotFoundError):
    BatchClient = Any
try:
    from mypy_boto3.budgets import Client as BudgetsClient
except (ImportError, ModuleNotFoundError):
    BudgetsClient = Any
try:
    from mypy_boto3.ce import Client as CEClient
except (ImportError, ModuleNotFoundError):
    CEClient = Any
try:
    from mypy_boto3.chime import Client as ChimeClient
except (ImportError, ModuleNotFoundError):
    ChimeClient = Any
try:
    from mypy_boto3.cloud9 import Client as Cloud9Client
except (ImportError, ModuleNotFoundError):
    Cloud9Client = Any
try:
    from mypy_boto3.clouddirectory import Client as ClouddirectoryClient
except (ImportError, ModuleNotFoundError):
    ClouddirectoryClient = Any
try:
    from mypy_boto3.cloudformation import Client as CloudformationClient
except (ImportError, ModuleNotFoundError):
    CloudformationClient = Any
try:
    from mypy_boto3.cloudformation import ServiceResource as CloudformationServiceResource
except (ImportError, ModuleNotFoundError):
    CloudformationServiceResource = Any
try:
    from mypy_boto3.cloudfront import Client as CloudfrontClient
except (ImportError, ModuleNotFoundError):
    CloudfrontClient = Any
try:
    from mypy_boto3.cloudhsm import Client as CloudhsmClient
except (ImportError, ModuleNotFoundError):
    CloudhsmClient = Any
try:
    from mypy_boto3.cloudhsmv2 import Client as Cloudhsmv2Client
except (ImportError, ModuleNotFoundError):
    Cloudhsmv2Client = Any
try:
    from mypy_boto3.cloudsearch import Client as CloudsearchClient
except (ImportError, ModuleNotFoundError):
    CloudsearchClient = Any
try:
    from mypy_boto3.cloudsearchdomain import Client as CloudsearchdomainClient
except (ImportError, ModuleNotFoundError):
    CloudsearchdomainClient = Any
try:
    from mypy_boto3.cloudtrail import Client as CloudtrailClient
except (ImportError, ModuleNotFoundError):
    CloudtrailClient = Any
try:
    from mypy_boto3.cloudwatch import Client as CloudwatchClient
except (ImportError, ModuleNotFoundError):
    CloudwatchClient = Any
try:
    from mypy_boto3.cloudwatch import ServiceResource as CloudwatchServiceResource
except (ImportError, ModuleNotFoundError):
    CloudwatchServiceResource = Any
try:
    from mypy_boto3.codebuild import Client as CodebuildClient
except (ImportError, ModuleNotFoundError):
    CodebuildClient = Any
try:
    from mypy_boto3.codecommit import Client as CodecommitClient
except (ImportError, ModuleNotFoundError):
    CodecommitClient = Any
try:
    from mypy_boto3.codedeploy import Client as CodedeployClient
except (ImportError, ModuleNotFoundError):
    CodedeployClient = Any
try:
    from mypy_boto3.codepipeline import Client as CodepipelineClient
except (ImportError, ModuleNotFoundError):
    CodepipelineClient = Any
try:
    from mypy_boto3.codestar import Client as CodestarClient
except (ImportError, ModuleNotFoundError):
    CodestarClient = Any
try:
    from mypy_boto3.codestar_notifications import Client as CodestarNotificationsClient
except (ImportError, ModuleNotFoundError):
    CodestarNotificationsClient = Any
try:
    from mypy_boto3.cognito_identity import Client as CognitoIdentityClient
except (ImportError, ModuleNotFoundError):
    CognitoIdentityClient = Any
try:
    from mypy_boto3.cognito_idp import Client as CognitoIdpClient
except (ImportError, ModuleNotFoundError):
    CognitoIdpClient = Any
try:
    from mypy_boto3.cognito_sync import Client as CognitoSyncClient
except (ImportError, ModuleNotFoundError):
    CognitoSyncClient = Any
try:
    from mypy_boto3.comprehend import Client as ComprehendClient
except (ImportError, ModuleNotFoundError):
    ComprehendClient = Any
try:
    from mypy_boto3.comprehendmedical import Client as ComprehendmedicalClient
except (ImportError, ModuleNotFoundError):
    ComprehendmedicalClient = Any
try:
    from mypy_boto3.config import Client as ConfigClient
except (ImportError, ModuleNotFoundError):
    ConfigClient = Any
try:
    from mypy_boto3.connect import Client as ConnectClient
except (ImportError, ModuleNotFoundError):
    ConnectClient = Any
try:
    from mypy_boto3.cur import Client as CURClient
except (ImportError, ModuleNotFoundError):
    CURClient = Any
try:
    from mypy_boto3.datapipeline import Client as DatapipelineClient
except (ImportError, ModuleNotFoundError):
    DatapipelineClient = Any
try:
    from mypy_boto3.datasync import Client as DatasyncClient
except (ImportError, ModuleNotFoundError):
    DatasyncClient = Any
try:
    from mypy_boto3.dax import Client as DAXClient
except (ImportError, ModuleNotFoundError):
    DAXClient = Any
try:
    from mypy_boto3.devicefarm import Client as DevicefarmClient
except (ImportError, ModuleNotFoundError):
    DevicefarmClient = Any
try:
    from mypy_boto3.directconnect import Client as DirectconnectClient
except (ImportError, ModuleNotFoundError):
    DirectconnectClient = Any
try:
    from mypy_boto3.discovery import Client as DiscoveryClient
except (ImportError, ModuleNotFoundError):
    DiscoveryClient = Any
try:
    from mypy_boto3.dlm import Client as DLMClient
except (ImportError, ModuleNotFoundError):
    DLMClient = Any
try:
    from mypy_boto3.dms import Client as DMSClient
except (ImportError, ModuleNotFoundError):
    DMSClient = Any
try:
    from mypy_boto3.docdb import Client as DocdbClient
except (ImportError, ModuleNotFoundError):
    DocdbClient = Any
try:
    from mypy_boto3.ds import Client as DSClient
except (ImportError, ModuleNotFoundError):
    DSClient = Any
try:
    from mypy_boto3.dynamodb import Client as DynamodbClient
except (ImportError, ModuleNotFoundError):
    DynamodbClient = Any
try:
    from mypy_boto3.dynamodb import ServiceResource as DynamodbServiceResource
except (ImportError, ModuleNotFoundError):
    DynamodbServiceResource = Any
try:
    from mypy_boto3.dynamodbstreams import Client as DynamodbstreamsClient
except (ImportError, ModuleNotFoundError):
    DynamodbstreamsClient = Any
try:
    from mypy_boto3.ec2 import Client as EC2Client
except (ImportError, ModuleNotFoundError):
    EC2Client = Any
try:
    from mypy_boto3.ec2 import ServiceResource as EC2ServiceResource
except (ImportError, ModuleNotFoundError):
    EC2ServiceResource = Any
try:
    from mypy_boto3.ec2_instance_connect import Client as Ec2InstanceConnectClient
except (ImportError, ModuleNotFoundError):
    Ec2InstanceConnectClient = Any
try:
    from mypy_boto3.ecr import Client as ECRClient
except (ImportError, ModuleNotFoundError):
    ECRClient = Any
try:
    from mypy_boto3.ecs import Client as ECSClient
except (ImportError, ModuleNotFoundError):
    ECSClient = Any
try:
    from mypy_boto3.efs import Client as EFSClient
except (ImportError, ModuleNotFoundError):
    EFSClient = Any
try:
    from mypy_boto3.eks import Client as EKSClient
except (ImportError, ModuleNotFoundError):
    EKSClient = Any
try:
    from mypy_boto3.elasticache import Client as ElasticacheClient
except (ImportError, ModuleNotFoundError):
    ElasticacheClient = Any
try:
    from mypy_boto3.elasticbeanstalk import Client as ElasticbeanstalkClient
except (ImportError, ModuleNotFoundError):
    ElasticbeanstalkClient = Any
try:
    from mypy_boto3.elastictranscoder import Client as ElastictranscoderClient
except (ImportError, ModuleNotFoundError):
    ElastictranscoderClient = Any
try:
    from mypy_boto3.elb import Client as ELBClient
except (ImportError, ModuleNotFoundError):
    ELBClient = Any
try:
    from mypy_boto3.elbv2 import Client as Elbv2Client
except (ImportError, ModuleNotFoundError):
    Elbv2Client = Any
try:
    from mypy_boto3.emr import Client as EMRClient
except (ImportError, ModuleNotFoundError):
    EMRClient = Any
try:
    from mypy_boto3.es import Client as ESClient
except (ImportError, ModuleNotFoundError):
    ESClient = Any
try:
    from mypy_boto3.events import Client as EventsClient
except (ImportError, ModuleNotFoundError):
    EventsClient = Any
try:
    from mypy_boto3.firehose import Client as FirehoseClient
except (ImportError, ModuleNotFoundError):
    FirehoseClient = Any
try:
    from mypy_boto3.fms import Client as FMSClient
except (ImportError, ModuleNotFoundError):
    FMSClient = Any
try:
    from mypy_boto3.forecast import Client as ForecastClient
except (ImportError, ModuleNotFoundError):
    ForecastClient = Any
try:
    from mypy_boto3.forecastquery import Client as ForecastqueryClient
except (ImportError, ModuleNotFoundError):
    ForecastqueryClient = Any
try:
    from mypy_boto3.fsx import Client as FSXClient
except (ImportError, ModuleNotFoundError):
    FSXClient = Any
try:
    from mypy_boto3.gamelift import Client as GameliftClient
except (ImportError, ModuleNotFoundError):
    GameliftClient = Any
try:
    from mypy_boto3.glacier import Client as GlacierClient
except (ImportError, ModuleNotFoundError):
    GlacierClient = Any
try:
    from mypy_boto3.glacier import ServiceResource as GlacierServiceResource
except (ImportError, ModuleNotFoundError):
    GlacierServiceResource = Any
try:
    from mypy_boto3.globalaccelerator import Client as GlobalacceleratorClient
except (ImportError, ModuleNotFoundError):
    GlobalacceleratorClient = Any
try:
    from mypy_boto3.glue import Client as GlueClient
except (ImportError, ModuleNotFoundError):
    GlueClient = Any
try:
    from mypy_boto3.greengrass import Client as GreengrassClient
except (ImportError, ModuleNotFoundError):
    GreengrassClient = Any
try:
    from mypy_boto3.groundstation import Client as GroundstationClient
except (ImportError, ModuleNotFoundError):
    GroundstationClient = Any
try:
    from mypy_boto3.guardduty import Client as GuarddutyClient
except (ImportError, ModuleNotFoundError):
    GuarddutyClient = Any
try:
    from mypy_boto3.health import Client as HealthClient
except (ImportError, ModuleNotFoundError):
    HealthClient = Any
try:
    from mypy_boto3.iam import Client as IAMClient
except (ImportError, ModuleNotFoundError):
    IAMClient = Any
try:
    from mypy_boto3.iam import ServiceResource as IAMServiceResource
except (ImportError, ModuleNotFoundError):
    IAMServiceResource = Any
try:
    from mypy_boto3.importexport import Client as ImportexportClient
except (ImportError, ModuleNotFoundError):
    ImportexportClient = Any
try:
    from mypy_boto3.inspector import Client as InspectorClient
except (ImportError, ModuleNotFoundError):
    InspectorClient = Any
try:
    from mypy_boto3.iot import Client as IOTClient
except (ImportError, ModuleNotFoundError):
    IOTClient = Any
try:
    from mypy_boto3.iot1click_devices import Client as Iot1clickDevicesClient
except (ImportError, ModuleNotFoundError):
    Iot1clickDevicesClient = Any
try:
    from mypy_boto3.iot1click_projects import Client as Iot1clickProjectsClient
except (ImportError, ModuleNotFoundError):
    Iot1clickProjectsClient = Any
try:
    from mypy_boto3.iot_data import Client as IotDataClient
except (ImportError, ModuleNotFoundError):
    IotDataClient = Any
try:
    from mypy_boto3.iot_jobs_data import Client as IotJobsDataClient
except (ImportError, ModuleNotFoundError):
    IotJobsDataClient = Any
try:
    from mypy_boto3.iotanalytics import Client as IotanalyticsClient
except (ImportError, ModuleNotFoundError):
    IotanalyticsClient = Any
try:
    from mypy_boto3.iotevents import Client as IoteventsClient
except (ImportError, ModuleNotFoundError):
    IoteventsClient = Any
try:
    from mypy_boto3.iotevents_data import Client as IoteventsDataClient
except (ImportError, ModuleNotFoundError):
    IoteventsDataClient = Any
try:
    from mypy_boto3.iotthingsgraph import Client as IotthingsgraphClient
except (ImportError, ModuleNotFoundError):
    IotthingsgraphClient = Any
try:
    from mypy_boto3.kafka import Client as KafkaClient
except (ImportError, ModuleNotFoundError):
    KafkaClient = Any
try:
    from mypy_boto3.kinesis import Client as KinesisClient
except (ImportError, ModuleNotFoundError):
    KinesisClient = Any
try:
    from mypy_boto3.kinesis_video_archived_media import Client as KinesisVideoArchivedMediaClient
except (ImportError, ModuleNotFoundError):
    KinesisVideoArchivedMediaClient = Any
try:
    from mypy_boto3.kinesis_video_media import Client as KinesisVideoMediaClient
except (ImportError, ModuleNotFoundError):
    KinesisVideoMediaClient = Any
try:
    from mypy_boto3.kinesisanalytics import Client as KinesisanalyticsClient
except (ImportError, ModuleNotFoundError):
    KinesisanalyticsClient = Any
try:
    from mypy_boto3.kinesisanalyticsv2 import Client as Kinesisanalyticsv2Client
except (ImportError, ModuleNotFoundError):
    Kinesisanalyticsv2Client = Any
try:
    from mypy_boto3.kinesisvideo import Client as KinesisvideoClient
except (ImportError, ModuleNotFoundError):
    KinesisvideoClient = Any
try:
    from mypy_boto3.kms import Client as KMSClient
except (ImportError, ModuleNotFoundError):
    KMSClient = Any
try:
    from mypy_boto3.lakeformation import Client as LakeformationClient
except (ImportError, ModuleNotFoundError):
    LakeformationClient = Any
try:
    from mypy_boto3.lambda_ import Client as LambdaClient
except (ImportError, ModuleNotFoundError):
    LambdaClient = Any
try:
    from mypy_boto3.lex_models import Client as LexModelsClient
except (ImportError, ModuleNotFoundError):
    LexModelsClient = Any
try:
    from mypy_boto3.lex_runtime import Client as LexRuntimeClient
except (ImportError, ModuleNotFoundError):
    LexRuntimeClient = Any
try:
    from mypy_boto3.license_manager import Client as LicenseManagerClient
except (ImportError, ModuleNotFoundError):
    LicenseManagerClient = Any
try:
    from mypy_boto3.lightsail import Client as LightsailClient
except (ImportError, ModuleNotFoundError):
    LightsailClient = Any
try:
    from mypy_boto3.logs import Client as LogsClient
except (ImportError, ModuleNotFoundError):
    LogsClient = Any
try:
    from mypy_boto3.machinelearning import Client as MachinelearningClient
except (ImportError, ModuleNotFoundError):
    MachinelearningClient = Any
try:
    from mypy_boto3.macie import Client as MacieClient
except (ImportError, ModuleNotFoundError):
    MacieClient = Any
try:
    from mypy_boto3.managedblockchain import Client as ManagedblockchainClient
except (ImportError, ModuleNotFoundError):
    ManagedblockchainClient = Any
try:
    from mypy_boto3.marketplace_entitlement import Client as MarketplaceEntitlementClient
except (ImportError, ModuleNotFoundError):
    MarketplaceEntitlementClient = Any
try:
    from mypy_boto3.marketplacecommerceanalytics import Client as MarketplacecommerceanalyticsClient
except (ImportError, ModuleNotFoundError):
    MarketplacecommerceanalyticsClient = Any
try:
    from mypy_boto3.mediaconnect import Client as MediaconnectClient
except (ImportError, ModuleNotFoundError):
    MediaconnectClient = Any
try:
    from mypy_boto3.mediaconvert import Client as MediaconvertClient
except (ImportError, ModuleNotFoundError):
    MediaconvertClient = Any
try:
    from mypy_boto3.medialive import Client as MedialiveClient
except (ImportError, ModuleNotFoundError):
    MedialiveClient = Any
try:
    from mypy_boto3.mediapackage import Client as MediapackageClient
except (ImportError, ModuleNotFoundError):
    MediapackageClient = Any
try:
    from mypy_boto3.mediapackage_vod import Client as MediapackageVodClient
except (ImportError, ModuleNotFoundError):
    MediapackageVodClient = Any
try:
    from mypy_boto3.mediastore import Client as MediastoreClient
except (ImportError, ModuleNotFoundError):
    MediastoreClient = Any
try:
    from mypy_boto3.mediastore_data import Client as MediastoreDataClient
except (ImportError, ModuleNotFoundError):
    MediastoreDataClient = Any
try:
    from mypy_boto3.mediatailor import Client as MediatailorClient
except (ImportError, ModuleNotFoundError):
    MediatailorClient = Any
try:
    from mypy_boto3.meteringmarketplace import Client as MeteringmarketplaceClient
except (ImportError, ModuleNotFoundError):
    MeteringmarketplaceClient = Any
try:
    from mypy_boto3.mgh import Client as MGHClient
except (ImportError, ModuleNotFoundError):
    MGHClient = Any
try:
    from mypy_boto3.mobile import Client as MobileClient
except (ImportError, ModuleNotFoundError):
    MobileClient = Any
try:
    from mypy_boto3.mq import Client as MQClient
except (ImportError, ModuleNotFoundError):
    MQClient = Any
try:
    from mypy_boto3.mturk import Client as MturkClient
except (ImportError, ModuleNotFoundError):
    MturkClient = Any
try:
    from mypy_boto3.neptune import Client as NeptuneClient
except (ImportError, ModuleNotFoundError):
    NeptuneClient = Any
try:
    from mypy_boto3.opsworks import Client as OpsworksClient
except (ImportError, ModuleNotFoundError):
    OpsworksClient = Any
try:
    from mypy_boto3.opsworks import ServiceResource as OpsworksServiceResource
except (ImportError, ModuleNotFoundError):
    OpsworksServiceResource = Any
try:
    from mypy_boto3.opsworkscm import Client as OpsworkscmClient
except (ImportError, ModuleNotFoundError):
    OpsworkscmClient = Any
try:
    from mypy_boto3.organizations import Client as OrganizationsClient
except (ImportError, ModuleNotFoundError):
    OrganizationsClient = Any
try:
    from mypy_boto3.personalize import Client as PersonalizeClient
except (ImportError, ModuleNotFoundError):
    PersonalizeClient = Any
try:
    from mypy_boto3.personalize_events import Client as PersonalizeEventsClient
except (ImportError, ModuleNotFoundError):
    PersonalizeEventsClient = Any
try:
    from mypy_boto3.personalize_runtime import Client as PersonalizeRuntimeClient
except (ImportError, ModuleNotFoundError):
    PersonalizeRuntimeClient = Any
try:
    from mypy_boto3.pi import Client as PIClient
except (ImportError, ModuleNotFoundError):
    PIClient = Any
try:
    from mypy_boto3.pinpoint import Client as PinpointClient
except (ImportError, ModuleNotFoundError):
    PinpointClient = Any
try:
    from mypy_boto3.pinpoint_email import Client as PinpointEmailClient
except (ImportError, ModuleNotFoundError):
    PinpointEmailClient = Any
try:
    from mypy_boto3.pinpoint_sms_voice import Client as PinpointSmsVoiceClient
except (ImportError, ModuleNotFoundError):
    PinpointSmsVoiceClient = Any
try:
    from mypy_boto3.polly import Client as PollyClient
except (ImportError, ModuleNotFoundError):
    PollyClient = Any
try:
    from mypy_boto3.pricing import Client as PricingClient
except (ImportError, ModuleNotFoundError):
    PricingClient = Any
try:
    from mypy_boto3.qldb import Client as QldbClient
except (ImportError, ModuleNotFoundError):
    QldbClient = Any
try:
    from mypy_boto3.qldb_session import Client as QldbSessionClient
except (ImportError, ModuleNotFoundError):
    QldbSessionClient = Any
try:
    from mypy_boto3.quicksight import Client as QuicksightClient
except (ImportError, ModuleNotFoundError):
    QuicksightClient = Any
try:
    from mypy_boto3.ram import Client as RAMClient
except (ImportError, ModuleNotFoundError):
    RAMClient = Any
try:
    from mypy_boto3.rds import Client as RDSClient
except (ImportError, ModuleNotFoundError):
    RDSClient = Any
try:
    from mypy_boto3.rds_data import Client as RdsDataClient
except (ImportError, ModuleNotFoundError):
    RdsDataClient = Any
try:
    from mypy_boto3.redshift import Client as RedshiftClient
except (ImportError, ModuleNotFoundError):
    RedshiftClient = Any
try:
    from mypy_boto3.rekognition import Client as RekognitionClient
except (ImportError, ModuleNotFoundError):
    RekognitionClient = Any
try:
    from mypy_boto3.resource_groups import Client as ResourceGroupsClient
except (ImportError, ModuleNotFoundError):
    ResourceGroupsClient = Any
try:
    from mypy_boto3.resourcegroupstaggingapi import Client as ResourcegroupstaggingapiClient
except (ImportError, ModuleNotFoundError):
    ResourcegroupstaggingapiClient = Any
try:
    from mypy_boto3.robomaker import Client as RobomakerClient
except (ImportError, ModuleNotFoundError):
    RobomakerClient = Any
try:
    from mypy_boto3.route53 import Client as Route53Client
except (ImportError, ModuleNotFoundError):
    Route53Client = Any
try:
    from mypy_boto3.route53domains import Client as Route53domainsClient
except (ImportError, ModuleNotFoundError):
    Route53domainsClient = Any
try:
    from mypy_boto3.route53resolver import Client as Route53resolverClient
except (ImportError, ModuleNotFoundError):
    Route53resolverClient = Any
try:
    from mypy_boto3.s3 import Client as S3Client
except (ImportError, ModuleNotFoundError):
    S3Client = Any
try:
    from mypy_boto3.s3 import ServiceResource as S3ServiceResource
except (ImportError, ModuleNotFoundError):
    S3ServiceResource = Any
try:
    from mypy_boto3.s3control import Client as S3controlClient
except (ImportError, ModuleNotFoundError):
    S3controlClient = Any
try:
    from mypy_boto3.sagemaker import Client as SagemakerClient
except (ImportError, ModuleNotFoundError):
    SagemakerClient = Any
try:
    from mypy_boto3.sagemaker_runtime import Client as SagemakerRuntimeClient
except (ImportError, ModuleNotFoundError):
    SagemakerRuntimeClient = Any
try:
    from mypy_boto3.savingsplans import Client as SavingsplansClient
except (ImportError, ModuleNotFoundError):
    SavingsplansClient = Any
try:
    from mypy_boto3.sdb import Client as SDBClient
except (ImportError, ModuleNotFoundError):
    SDBClient = Any
try:
    from mypy_boto3.secretsmanager import Client as SecretsmanagerClient
except (ImportError, ModuleNotFoundError):
    SecretsmanagerClient = Any
try:
    from mypy_boto3.securityhub import Client as SecurityhubClient
except (ImportError, ModuleNotFoundError):
    SecurityhubClient = Any
try:
    from mypy_boto3.serverlessrepo import Client as ServerlessrepoClient
except (ImportError, ModuleNotFoundError):
    ServerlessrepoClient = Any
try:
    from mypy_boto3.service_quotas import Client as ServiceQuotasClient
except (ImportError, ModuleNotFoundError):
    ServiceQuotasClient = Any
try:
    from mypy_boto3.servicecatalog import Client as ServicecatalogClient
except (ImportError, ModuleNotFoundError):
    ServicecatalogClient = Any
try:
    from mypy_boto3.servicediscovery import Client as ServicediscoveryClient
except (ImportError, ModuleNotFoundError):
    ServicediscoveryClient = Any
try:
    from mypy_boto3.ses import Client as SESClient
except (ImportError, ModuleNotFoundError):
    SESClient = Any
try:
    from mypy_boto3.shield import Client as ShieldClient
except (ImportError, ModuleNotFoundError):
    ShieldClient = Any
try:
    from mypy_boto3.signer import Client as SignerClient
except (ImportError, ModuleNotFoundError):
    SignerClient = Any
try:
    from mypy_boto3.sms import Client as SMSClient
except (ImportError, ModuleNotFoundError):
    SMSClient = Any
try:
    from mypy_boto3.sms_voice import Client as SmsVoiceClient
except (ImportError, ModuleNotFoundError):
    SmsVoiceClient = Any
try:
    from mypy_boto3.snowball import Client as SnowballClient
except (ImportError, ModuleNotFoundError):
    SnowballClient = Any
try:
    from mypy_boto3.sns import Client as SNSClient
except (ImportError, ModuleNotFoundError):
    SNSClient = Any
try:
    from mypy_boto3.sns import ServiceResource as SNSServiceResource
except (ImportError, ModuleNotFoundError):
    SNSServiceResource = Any
try:
    from mypy_boto3.sqs import Client as SQSClient
except (ImportError, ModuleNotFoundError):
    SQSClient = Any
try:
    from mypy_boto3.sqs import ServiceResource as SQSServiceResource
except (ImportError, ModuleNotFoundError):
    SQSServiceResource = Any
try:
    from mypy_boto3.ssm import Client as SSMClient
except (ImportError, ModuleNotFoundError):
    SSMClient = Any
try:
    from mypy_boto3.stepfunctions import Client as StepfunctionsClient
except (ImportError, ModuleNotFoundError):
    StepfunctionsClient = Any
try:
    from mypy_boto3.storagegateway import Client as StoragegatewayClient
except (ImportError, ModuleNotFoundError):
    StoragegatewayClient = Any
try:
    from mypy_boto3.sts import Client as STSClient
except (ImportError, ModuleNotFoundError):
    STSClient = Any
try:
    from mypy_boto3.support import Client as SupportClient
except (ImportError, ModuleNotFoundError):
    SupportClient = Any
try:
    from mypy_boto3.swf import Client as SWFClient
except (ImportError, ModuleNotFoundError):
    SWFClient = Any
try:
    from mypy_boto3.textract import Client as TextractClient
except (ImportError, ModuleNotFoundError):
    TextractClient = Any
try:
    from mypy_boto3.transcribe import Client as TranscribeClient
except (ImportError, ModuleNotFoundError):
    TranscribeClient = Any
try:
    from mypy_boto3.transfer import Client as TransferClient
except (ImportError, ModuleNotFoundError):
    TransferClient = Any
try:
    from mypy_boto3.translate import Client as TranslateClient
except (ImportError, ModuleNotFoundError):
    TranslateClient = Any
try:
    from mypy_boto3.waf import Client as WAFClient
except (ImportError, ModuleNotFoundError):
    WAFClient = Any
try:
    from mypy_boto3.waf_regional import Client as WafRegionalClient
except (ImportError, ModuleNotFoundError):
    WafRegionalClient = Any
try:
    from mypy_boto3.workdocs import Client as WorkdocsClient
except (ImportError, ModuleNotFoundError):
    WorkdocsClient = Any
try:
    from mypy_boto3.worklink import Client as WorklinkClient
except (ImportError, ModuleNotFoundError):
    WorklinkClient = Any
try:
    from mypy_boto3.workmail import Client as WorkmailClient
except (ImportError, ModuleNotFoundError):
    WorkmailClient = Any
try:
    from mypy_boto3.workmailmessageflow import Client as WorkmailmessageflowClient
except (ImportError, ModuleNotFoundError):
    WorkmailmessageflowClient = Any
try:
    from mypy_boto3.workspaces import Client as WorkspacesClient
except (ImportError, ModuleNotFoundError):
    WorkspacesClient = Any
try:
    from mypy_boto3.xray import Client as XrayClient
except (ImportError, ModuleNotFoundError):
    XrayClient = Any

class Session:
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        region_name: str = None,
        botocore_session: Session = None,
        profile_name: str = None,
    ):
        self._session: ServiceModel
        self.resource_factory: ResourceFactory
        self._loader: Loader
    def __repr__(self) -> str: ...
    @property
    def profile_name(self) -> str: ...
    @property
    def region_name(self) -> str: ...
    @property
    def events(self) -> List[Any]: ...
    @property
    def available_profiles(self) -> List[Any]: ...
    def _setup_loader(self) -> None: ...
    def get_available_services(self) -> List[str]: ...
    def get_available_resources(self) -> List[str]: ...
    def get_available_partitions(self) -> List[str]: ...
    def get_available_regions(
        self, service_name: str, partition_name: str = "aws", allow_non_regional: bool = False,
    ) -> List[str]: ...
    def get_credentials(self) -> Credentials: ...
    def _register_default_handlers(self) -> None: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["acm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ACMClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["acm-pca"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AcmPcaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["alexaforbusiness"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AlexaforbusinessClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["amplify"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AmplifyClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["apigateway"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ApigatewayClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["apigatewaymanagementapi"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ApigatewaymanagementapiClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["apigatewayv2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Apigatewayv2Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["application-autoscaling"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ApplicationAutoscalingClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["application-insights"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ApplicationInsightsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["appmesh"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AppmeshClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["appstream"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AppstreamClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["appsync"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AppsyncClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["athena"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AthenaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["autoscaling"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AutoscalingClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["autoscaling-plans"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> AutoscalingPlansClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["backup"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> BackupClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["batch"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> BatchClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["budgets"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> BudgetsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ce"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CEClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["chime"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ChimeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloud9"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Cloud9Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["clouddirectory"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ClouddirectoryClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudformation"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudformationClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudfront"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudfrontClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudhsm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudhsmClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudhsmv2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Cloudhsmv2Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudsearch"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudsearchClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudsearchdomain"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudsearchdomainClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudtrail"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudtrailClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cloudwatch"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudwatchClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codebuild"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodebuildClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codecommit"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodecommitClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codedeploy"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodedeployClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codepipeline"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodepipelineClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codestar"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodestarClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["codestar-notifications"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CodestarNotificationsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cognito-identity"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CognitoIdentityClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cognito-idp"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CognitoIdpClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cognito-sync"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CognitoSyncClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["comprehend"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ComprehendClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["comprehendmedical"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ComprehendmedicalClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["config"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ConfigClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["connect"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ConnectClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["cur"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CURClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["datapipeline"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DatapipelineClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["datasync"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DatasyncClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["dax"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DAXClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["devicefarm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DevicefarmClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["directconnect"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DirectconnectClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["discovery"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DiscoveryClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["dlm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DLMClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["dms"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DMSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["docdb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DocdbClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ds"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["dynamodb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DynamodbClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["dynamodbstreams"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DynamodbstreamsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ec2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EC2Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ec2-instance-connect"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Ec2InstanceConnectClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ecr"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ECRClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ecs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ECSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["efs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EFSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["eks"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EKSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["elasticache"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ElasticacheClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["elasticbeanstalk"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ElasticbeanstalkClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["elastictranscoder"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ElastictranscoderClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["elb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ELBClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["elbv2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Elbv2Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["emr"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EMRClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["es"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ESClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["events"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EventsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["firehose"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> FirehoseClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["fms"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> FMSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["forecast"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ForecastClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["forecastquery"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ForecastqueryClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["fsx"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> FSXClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["gamelift"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GameliftClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["glacier"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GlacierClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["globalaccelerator"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GlobalacceleratorClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["glue"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GlueClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["greengrass"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GreengrassClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["groundstation"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GroundstationClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["guardduty"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GuarddutyClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["health"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> HealthClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iam"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IAMClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["importexport"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ImportexportClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["inspector"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> InspectorClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iot"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IOTClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iot-data"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IotDataClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iot-jobs-data"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IotJobsDataClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iot1click-devices"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Iot1clickDevicesClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iot1click-projects"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Iot1clickProjectsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iotanalytics"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IotanalyticsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iotevents"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IoteventsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iotevents-data"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IoteventsDataClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["iotthingsgraph"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IotthingsgraphClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kafka"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KafkaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesis"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KinesisClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesis-video-archived-media"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KinesisVideoArchivedMediaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesis-video-media"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KinesisVideoMediaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesisanalytics"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KinesisanalyticsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesisanalyticsv2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Kinesisanalyticsv2Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kinesisvideo"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KinesisvideoClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["kms"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> KMSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["lakeformation"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LakeformationClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["lambda"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LambdaClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["lex-models"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LexModelsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["lex-runtime"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LexRuntimeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["license-manager"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LicenseManagerClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["lightsail"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LightsailClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["logs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> LogsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["machinelearning"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MachinelearningClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["macie"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MacieClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["managedblockchain"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ManagedblockchainClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["marketplace-entitlement"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MarketplaceEntitlementClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["marketplacecommerceanalytics"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MarketplacecommerceanalyticsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediaconnect"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediaconnectClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediaconvert"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediaconvertClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["medialive"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MedialiveClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediapackage"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediapackageClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediapackage-vod"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediapackageVodClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediastore"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediastoreClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediastore-data"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediastoreDataClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mediatailor"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MediatailorClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["meteringmarketplace"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MeteringmarketplaceClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mgh"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MGHClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mobile"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MobileClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mq"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MQClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["mturk"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> MturkClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["neptune"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> NeptuneClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["opsworks"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> OpsworksClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["opsworkscm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> OpsworkscmClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["organizations"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> OrganizationsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["personalize"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PersonalizeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["personalize-events"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PersonalizeEventsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["personalize-runtime"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PersonalizeRuntimeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["pi"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PIClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["pinpoint"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PinpointClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["pinpoint-email"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PinpointEmailClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["pinpoint-sms-voice"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PinpointSmsVoiceClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["polly"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PollyClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["pricing"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> PricingClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["qldb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> QldbClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["qldb-session"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> QldbSessionClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["quicksight"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> QuicksightClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ram"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RAMClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["rds"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RDSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["rds-data"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RdsDataClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["redshift"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RedshiftClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["rekognition"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RekognitionClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["resource-groups"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ResourceGroupsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["resourcegroupstaggingapi"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ResourcegroupstaggingapiClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["robomaker"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> RobomakerClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["route53"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Route53Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["route53domains"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Route53domainsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["route53resolver"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> Route53resolverClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["s3"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> S3Client: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["s3control"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> S3controlClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sagemaker"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SagemakerClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sagemaker-runtime"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SagemakerRuntimeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["savingsplans"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SavingsplansClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sdb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SDBClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["secretsmanager"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SecretsmanagerClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["securityhub"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SecurityhubClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["serverlessrepo"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ServerlessrepoClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["service-quotas"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ServiceQuotasClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["servicecatalog"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ServicecatalogClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["servicediscovery"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ServicediscoveryClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ses"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SESClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["shield"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> ShieldClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["signer"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SignerClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sms"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SMSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sms-voice"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SmsVoiceClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["snowball"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SnowballClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sns"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SNSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sqs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SQSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["ssm"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SSMClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["stepfunctions"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> StepfunctionsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["storagegateway"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> StoragegatewayClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["sts"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> STSClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["support"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SupportClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["swf"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SWFClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["textract"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> TextractClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["transcribe"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> TranscribeClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["transfer"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> TransferClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["translate"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> TranslateClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["waf"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WAFClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["waf-regional"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WafRegionalClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["workdocs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WorkdocsClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["worklink"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WorklinkClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["workmail"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WorkmailClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["workmailmessageflow"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WorkmailmessageflowClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["workspaces"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> WorkspacesClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def client(
        self,
        service_name: Literal["xray"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> XrayClient: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["cloudformation"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudformationServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["cloudwatch"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> CloudwatchServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["dynamodb"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> DynamodbServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["ec2"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> EC2ServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["glacier"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> GlacierServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["iam"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> IAMServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["opsworks"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> OpsworksServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["s3"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> S3ServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["sns"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SNSServiceResource: ...
    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def resource(
        self,
        service_name: Literal["sqs"],
        region_name: str = None,
        api_version: str = None,
        use_ssl: bool = None,
        verify: Union[str, bool] = None,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        config: Config = None,
    ) -> SQSServiceResource: ...
