"Main interface for mediapackage type defs"
from __future__ import annotations

from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef",
    "ClientCreateChannelResponseHlsIngestTypeDef",
    "ClientCreateChannelResponseTypeDef",
    "ClientCreateHarvestJobResponseS3DestinationTypeDef",
    "ClientCreateHarvestJobResponseTypeDef",
    "ClientCreateHarvestJobS3DestinationTypeDef",
    "ClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointCmafPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef",
    "ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointCmafPackageTypeDef",
    "ClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointDashPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointDashPackageTypeDef",
    "ClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointHlsPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointHlsPackageTypeDef",
    "ClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointMssPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointMssPackageTypeDef",
    "ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    "ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointResponseCmafPackageTypeDef",
    "ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointResponseDashPackageTypeDef",
    "ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointResponseHlsPackageTypeDef",
    "ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef",
    "ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    "ClientCreateOriginEndpointResponseMssPackageTypeDef",
    "ClientCreateOriginEndpointResponseTypeDef",
    "ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef",
    "ClientDescribeChannelResponseHlsIngestTypeDef",
    "ClientDescribeChannelResponseTypeDef",
    "ClientDescribeHarvestJobResponseS3DestinationTypeDef",
    "ClientDescribeHarvestJobResponseTypeDef",
    "ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef",
    "ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    "ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    "ClientDescribeOriginEndpointResponseCmafPackageTypeDef",
    "ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef",
    "ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    "ClientDescribeOriginEndpointResponseDashPackageTypeDef",
    "ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef",
    "ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    "ClientDescribeOriginEndpointResponseHlsPackageTypeDef",
    "ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef",
    "ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    "ClientDescribeOriginEndpointResponseMssPackageTypeDef",
    "ClientDescribeOriginEndpointResponseTypeDef",
    "ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef",
    "ClientListChannelsResponseChannelsHlsIngestTypeDef",
    "ClientListChannelsResponseChannelsTypeDef",
    "ClientListChannelsResponseTypeDef",
    "ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef",
    "ClientListHarvestJobsResponseHarvestJobsTypeDef",
    "ClientListHarvestJobsResponseTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef",
    "ClientListOriginEndpointsResponseOriginEndpointsTypeDef",
    "ClientListOriginEndpointsResponseTypeDef",
    "ClientListTagsForResourceResponseTypeDef",
    "ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef",
    "ClientRotateChannelCredentialsResponseHlsIngestTypeDef",
    "ClientRotateChannelCredentialsResponseTypeDef",
    "ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef",
    "ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef",
    "ClientRotateIngestEndpointCredentialsResponseTypeDef",
    "ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef",
    "ClientUpdateChannelResponseHlsIngestTypeDef",
    "ClientUpdateChannelResponseTypeDef",
    "ClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointCmafPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef",
    "ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointCmafPackageTypeDef",
    "ClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointDashPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointDashPackageTypeDef",
    "ClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointHlsPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointHlsPackageTypeDef",
    "ClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointMssPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointMssPackageTypeDef",
    "ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    "ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointResponseCmafPackageTypeDef",
    "ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointResponseDashPackageTypeDef",
    "ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointResponseHlsPackageTypeDef",
    "ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef",
    "ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    "ClientUpdateOriginEndpointResponseMssPackageTypeDef",
    "ClientUpdateOriginEndpointResponseTypeDef",
    "ListChannelsPaginatePaginationConfigTypeDef",
    "ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef",
    "ListChannelsPaginateResponseChannelsHlsIngestTypeDef",
    "ListChannelsPaginateResponseChannelsTypeDef",
    "ListChannelsPaginateResponseTypeDef",
    "ListHarvestJobsPaginatePaginationConfigTypeDef",
    "ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef",
    "ListHarvestJobsPaginateResponseHarvestJobsTypeDef",
    "ListHarvestJobsPaginateResponseTypeDef",
    "ListOriginEndpointsPaginatePaginationConfigTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef",
    "ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef",
    "ListOriginEndpointsPaginateResponseTypeDef",
)


_ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef(
    _ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientCreateChannelResponseHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientCreateChannelResponseHlsIngestTypeDef = TypedDict(
    "_ClientCreateChannelResponseHlsIngestTypeDef",
    {"IngestEndpoints": List[ClientCreateChannelResponseHlsIngestIngestEndpointsTypeDef]},
    total=False,
)


class ClientCreateChannelResponseHlsIngestTypeDef(_ClientCreateChannelResponseHlsIngestTypeDef):
    """
    Type definition for `ClientCreateChannelResponse` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientCreateChannelResponseTypeDef = TypedDict(
    "_ClientCreateChannelResponseTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientCreateChannelResponseHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientCreateChannelResponseTypeDef(_ClientCreateChannelResponseTypeDef):
    """
    Type definition for `ClientCreateChannel` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ClientCreateHarvestJobResponseS3DestinationTypeDef = TypedDict(
    "_ClientCreateHarvestJobResponseS3DestinationTypeDef",
    {"BucketName": str, "ManifestKey": str, "RoleArn": str},
    total=False,
)


class ClientCreateHarvestJobResponseS3DestinationTypeDef(
    _ClientCreateHarvestJobResponseS3DestinationTypeDef
):
    """
    Type definition for `ClientCreateHarvestJobResponse` `S3Destination`

    - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
    exported

    - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested top-level
    manifest will be placed.

    - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket
    """


_ClientCreateHarvestJobResponseTypeDef = TypedDict(
    "_ClientCreateHarvestJobResponseTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CreatedAt": str,
        "EndTime": str,
        "Id": str,
        "OriginEndpointId": str,
        "S3Destination": ClientCreateHarvestJobResponseS3DestinationTypeDef,
        "StartTime": str,
        "Status": str,
    },
    total=False,
)


class ClientCreateHarvestJobResponseTypeDef(_ClientCreateHarvestJobResponseTypeDef):
    """
    Type definition for `ClientCreateHarvestJob` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

    - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

    - **CreatedAt** *(string) --* The time the HarvestJob was submitted

    - **EndTime** *(string) --* The end of the time-window which will be harvested.

    - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and it
    cannot be changed after the HarvestJob is submitted.

    - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
    harvest from. This cannot be changed after the HarvestJob is submitted.

    - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place the
    harvested content

      - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
      exported

      - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
      top-level manifest will be placed.

      - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

    - **StartTime** *(string) --* The start of the time-window which will be harvested.

    - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
    CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure, the
    CloudWatch Event will include an explanation of why the HarvestJob failed.
    """


_ClientCreateHarvestJobS3DestinationTypeDef = TypedDict(
    "_ClientCreateHarvestJobS3DestinationTypeDef",
    {"BucketName": str, "ManifestKey": str, "RoleArn": str},
)


class ClientCreateHarvestJobS3DestinationTypeDef(_ClientCreateHarvestJobS3DestinationTypeDef):
    """
    Type definition for `ClientCreateHarvestJob` `S3Destination`

    - **BucketName** *(string) --* **[REQUIRED]** The name of an S3 bucket within which harvested
    content will be exported

    - **ManifestKey** *(string) --* **[REQUIRED]** The key in the specified S3 bucket where the
    harvested top-level manifest will be placed.

    - **RoleArn** *(string) --* **[REQUIRED]** The IAM role used to write to the specified S3 bucket
    """


_RequiredClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointCmafPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientCreateOriginEndpointCmafPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointCmafPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientCreateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientCreateOriginEndpointCmafPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointCmafPackageEncryptionTypeDef",
    {"KeyRotationIntervalSeconds": int},
    total=False,
)


class ClientCreateOriginEndpointCmafPackageEncryptionTypeDef(
    _RequiredClientCreateOriginEndpointCmafPackageEncryptionTypeDef,
    _OptionalClientCreateOriginEndpointCmafPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef", {"Id": str}
)
_OptionalClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
    },
    total=False,
)


class ClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef(
    _RequiredClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef,
    _OptionalClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Id** *(string) --* **[REQUIRED]** The ID of the manifest. The ID must be unique within the
    OriginEndpoint and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.
    """


_ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointCmafPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointCmafPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointCmafPackageTypeDef",
    {
        "Encryption": ClientCreateOriginEndpointCmafPackageEncryptionTypeDef,
        "HlsManifests": List[ClientCreateOriginEndpointCmafPackageHlsManifestsTypeDef],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientCreateOriginEndpointCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointCmafPackageTypeDef(_ClientCreateOriginEndpointCmafPackageTypeDef):
    """
    Type definition for `ClientCreateOriginEndpoint` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers
        in the output. If empty, no ad markers are output. Specify multiple items to create ad
        markers for all of the included message types.

          - *(string) --*

        - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
        flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
        Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
        messages of the types specified in AdTriggers that contain delivery restrictions will be
        treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
        AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
        means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
        that Splice Insert messages do not have these flags and are always treated as ads if
        specified in AdTriggers.

        - **Id** *(string) --* **[REQUIRED]** The ID of the manifest. The ID must be unique within
        the OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_RequiredClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointDashPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientCreateOriginEndpointDashPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointDashPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientCreateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientCreateOriginEndpointDashPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointDashPackageEncryptionTypeDef",
    {"KeyRotationIntervalSeconds": int},
    total=False,
)


class ClientCreateOriginEndpointDashPackageEncryptionTypeDef(
    _RequiredClientCreateOriginEndpointDashPackageEncryptionTypeDef,
    _OptionalClientCreateOriginEndpointDashPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointDashPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointDashPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientCreateOriginEndpointDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientCreateOriginEndpointDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientCreateOriginEndpointDashPackageTypeDef(_ClientCreateOriginEndpointDashPackageTypeDef):
    """
    Type definition for `ClientCreateOriginEndpoint` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_RequiredClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointHlsPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientCreateOriginEndpointHlsPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointHlsPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientCreateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientCreateOriginEndpointHlsPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
    },
    total=False,
)


class ClientCreateOriginEndpointHlsPackageEncryptionTypeDef(
    _RequiredClientCreateOriginEndpointHlsPackageEncryptionTypeDef,
    _OptionalClientCreateOriginEndpointHlsPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointHlsPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointHlsPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientCreateOriginEndpointHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientCreateOriginEndpointHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientCreateOriginEndpointHlsPackageTypeDef(_ClientCreateOriginEndpointHlsPackageTypeDef):
    """
    Type definition for `ClientCreateOriginEndpoint` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_RequiredClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientCreateOriginEndpointMssPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientCreateOriginEndpointMssPackageEncryptionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointMssPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientCreateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef},
)


class ClientCreateOriginEndpointMssPackageEncryptionTypeDef(
    _ClientCreateOriginEndpointMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointMssPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointMssPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointMssPackageTypeDef",
    {
        "Encryption": ClientCreateOriginEndpointMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientCreateOriginEndpointMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointMssPackageTypeDef(_ClientCreateOriginEndpointMssPackageTypeDef):
    """
    Type definition for `ClientCreateOriginEndpoint` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseCmafPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientCreateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef(
    _ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "Id": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "Url": str,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef(
    _ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **Id** *(string) --* The ID of the manifest. The ID must be unique within the OriginEndpoint
    and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.
    """


_ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseCmafPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointResponseCmafPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseCmafPackageTypeDef",
    {
        "Encryption": ClientCreateOriginEndpointResponseCmafPackageEncryptionTypeDef,
        "HlsManifests": List[ClientCreateOriginEndpointResponseCmafPackageHlsManifestsTypeDef],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientCreateOriginEndpointResponseCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseCmafPackageTypeDef(
    _ClientCreateOriginEndpointResponseCmafPackageTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponse` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
        OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseDashPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientCreateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef(
    _ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseDashPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointResponseDashPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientCreateOriginEndpointResponseDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientCreateOriginEndpointResponseDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseDashPackageTypeDef(
    _ClientCreateOriginEndpointResponseDashPackageTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponse` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseHlsPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "SpekeKeyProvider": ClientCreateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef(
    _ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseHlsPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointResponseHlsPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientCreateOriginEndpointResponseHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientCreateOriginEndpointResponseHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseHlsPackageTypeDef(
    _ClientCreateOriginEndpointResponseHlsPackageTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponse` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseMssPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef",
    {
        "SpekeKeyProvider": ClientCreateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
    },
    total=False,
)


class ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef(
    _ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef(
    _ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponseMssPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientCreateOriginEndpointResponseMssPackageTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseMssPackageTypeDef",
    {
        "Encryption": ClientCreateOriginEndpointResponseMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientCreateOriginEndpointResponseMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientCreateOriginEndpointResponseMssPackageTypeDef(
    _ClientCreateOriginEndpointResponseMssPackageTypeDef
):
    """
    Type definition for `ClientCreateOriginEndpointResponse` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientCreateOriginEndpointResponseTypeDef = TypedDict(
    "_ClientCreateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CmafPackage": ClientCreateOriginEndpointResponseCmafPackageTypeDef,
        "DashPackage": ClientCreateOriginEndpointResponseDashPackageTypeDef,
        "Description": str,
        "HlsPackage": ClientCreateOriginEndpointResponseHlsPackageTypeDef,
        "Id": str,
        "ManifestName": str,
        "MssPackage": ClientCreateOriginEndpointResponseMssPackageTypeDef,
        "Origination": str,
        "StartoverWindowSeconds": int,
        "Tags": Dict[str, str],
        "TimeDelaySeconds": int,
        "Url": str,
        "Whitelist": List[str],
    },
    total=False,
)


class ClientCreateOriginEndpointResponseTypeDef(_ClientCreateOriginEndpointResponseTypeDef):
    """
    Type definition for `ClientCreateOriginEndpoint` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

    - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

    - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging configuration.

      - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **HlsManifests** *(list) --* A list of HLS manifest configurations

        - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
          OriginEndpoint and it cannot be changed after it is created.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **ManifestName** *(string) --* An optional short string appended to the end of the
          OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
      each segment. If not specified, it defaults to the ChannelId.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
    configuration.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
      Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
      ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
      are combined and presented at the AdaptationSet level.

      - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
      manifest.

      - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
      buffer media before starting the presentation.

      - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
      changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description
      (MPD).

      - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
      Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
      into multiple periods. If empty, the content will not be partitioned into more than one
      period. If the list contains "ADS", new periods will be created where the Channel source
      contains SCTE-35 ad markers.

        - *(string) --*

      - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
      set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in
      the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
      presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
      full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
      NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
      URLs.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
      content before presentation.

    - **Description** *(string) --* A short text description of the OriginEndpoint.

    - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

      - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
      packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
      "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments) taken
      directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad
      markers and blackout tags based on SCTE-35 messages in the input source.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

        - **ConstantInitializationVector** *(string) --* A constant initialization vector for
        encryption (optional). When not specified the initialization vector will be periodically
        rotated.

        - **EncryptionMethod** *(string) --* The encryption method to use.

        - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
        encryption key rotation.

        - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
        output manifests.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
      included in the output.

      - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
      "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
      the media playlist.

      - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
      manifest.

      - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
      EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
      specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
      of the content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME
      tags will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note
      that irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming
      (HLS) input, it will be passed through to HLS output.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
      fragments will be rounded to the nearest multiple of the source fragment duration.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
      rendition groups in the output.

    - **Id** *(string) --* The ID of the OriginEndpoint.

    - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint URL.

    - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

      - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
      manifest.

      - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **Origination** *(string) --* Control whether origination of video is allowed for this
    OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other form
    of access control. If set to DENY, the OriginEndpoint may not be requested. This can be helpful
    for Live to VOD harvesting, or for temporarily disabling origination

    - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain for
    startover playback. If not specified, startover playback will be disabled for the
    OriginEndpoint.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*

    - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback of
    live content. If not specified, there will be no time delay in effect for the OriginEndpoint.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access the
    OriginEndpoint.

      - *(string) --*
    """


_ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef(
    _ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientDescribeChannelResponseHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientDescribeChannelResponseHlsIngestTypeDef = TypedDict(
    "_ClientDescribeChannelResponseHlsIngestTypeDef",
    {"IngestEndpoints": List[ClientDescribeChannelResponseHlsIngestIngestEndpointsTypeDef]},
    total=False,
)


class ClientDescribeChannelResponseHlsIngestTypeDef(_ClientDescribeChannelResponseHlsIngestTypeDef):
    """
    Type definition for `ClientDescribeChannelResponse` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientDescribeChannelResponseTypeDef = TypedDict(
    "_ClientDescribeChannelResponseTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientDescribeChannelResponseHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientDescribeChannelResponseTypeDef(_ClientDescribeChannelResponseTypeDef):
    """
    Type definition for `ClientDescribeChannel` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ClientDescribeHarvestJobResponseS3DestinationTypeDef = TypedDict(
    "_ClientDescribeHarvestJobResponseS3DestinationTypeDef",
    {"BucketName": str, "ManifestKey": str, "RoleArn": str},
    total=False,
)


class ClientDescribeHarvestJobResponseS3DestinationTypeDef(
    _ClientDescribeHarvestJobResponseS3DestinationTypeDef
):
    """
    Type definition for `ClientDescribeHarvestJobResponse` `S3Destination`

    - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
    exported

    - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested top-level
    manifest will be placed.

    - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket
    """


_ClientDescribeHarvestJobResponseTypeDef = TypedDict(
    "_ClientDescribeHarvestJobResponseTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CreatedAt": str,
        "EndTime": str,
        "Id": str,
        "OriginEndpointId": str,
        "S3Destination": ClientDescribeHarvestJobResponseS3DestinationTypeDef,
        "StartTime": str,
        "Status": str,
    },
    total=False,
)


class ClientDescribeHarvestJobResponseTypeDef(_ClientDescribeHarvestJobResponseTypeDef):
    """
    Type definition for `ClientDescribeHarvestJob` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

    - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

    - **CreatedAt** *(string) --* The time the HarvestJob was submitted

    - **EndTime** *(string) --* The end of the time-window which will be harvested.

    - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and it
    cannot be changed after the HarvestJob is submitted.

    - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
    harvest from. This cannot be changed after the HarvestJob is submitted.

    - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place the
    harvested content

      - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
      exported

      - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
      top-level manifest will be placed.

      - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

    - **StartTime** *(string) --* The start of the time-window which will be harvested.

    - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
    CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure, the
    CloudWatch Event will include an explanation of why the HarvestJob failed.
    """


_ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseCmafPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientDescribeOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef(
    _ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "Id": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "Url": str,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef(
    _ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **Id** *(string) --* The ID of the manifest. The ID must be unique within the OriginEndpoint
    and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.
    """


_ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef(
    _ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseCmafPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientDescribeOriginEndpointResponseCmafPackageTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseCmafPackageTypeDef",
    {
        "Encryption": ClientDescribeOriginEndpointResponseCmafPackageEncryptionTypeDef,
        "HlsManifests": List[ClientDescribeOriginEndpointResponseCmafPackageHlsManifestsTypeDef],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientDescribeOriginEndpointResponseCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseCmafPackageTypeDef(
    _ClientDescribeOriginEndpointResponseCmafPackageTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponse` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
        OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseDashPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientDescribeOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef(
    _ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef(
    _ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseDashPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientDescribeOriginEndpointResponseDashPackageTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientDescribeOriginEndpointResponseDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientDescribeOriginEndpointResponseDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseDashPackageTypeDef(
    _ClientDescribeOriginEndpointResponseDashPackageTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponse` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseHlsPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "SpekeKeyProvider": ClientDescribeOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef(
    _ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef(
    _ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseHlsPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientDescribeOriginEndpointResponseHlsPackageTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientDescribeOriginEndpointResponseHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientDescribeOriginEndpointResponseHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseHlsPackageTypeDef(
    _ClientDescribeOriginEndpointResponseHlsPackageTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponse` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseMssPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef",
    {
        "SpekeKeyProvider": ClientDescribeOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef(
    _ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef(
    _ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponseMssPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientDescribeOriginEndpointResponseMssPackageTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseMssPackageTypeDef",
    {
        "Encryption": ClientDescribeOriginEndpointResponseMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientDescribeOriginEndpointResponseMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseMssPackageTypeDef(
    _ClientDescribeOriginEndpointResponseMssPackageTypeDef
):
    """
    Type definition for `ClientDescribeOriginEndpointResponse` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientDescribeOriginEndpointResponseTypeDef = TypedDict(
    "_ClientDescribeOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CmafPackage": ClientDescribeOriginEndpointResponseCmafPackageTypeDef,
        "DashPackage": ClientDescribeOriginEndpointResponseDashPackageTypeDef,
        "Description": str,
        "HlsPackage": ClientDescribeOriginEndpointResponseHlsPackageTypeDef,
        "Id": str,
        "ManifestName": str,
        "MssPackage": ClientDescribeOriginEndpointResponseMssPackageTypeDef,
        "Origination": str,
        "StartoverWindowSeconds": int,
        "Tags": Dict[str, str],
        "TimeDelaySeconds": int,
        "Url": str,
        "Whitelist": List[str],
    },
    total=False,
)


class ClientDescribeOriginEndpointResponseTypeDef(_ClientDescribeOriginEndpointResponseTypeDef):
    """
    Type definition for `ClientDescribeOriginEndpoint` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

    - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

    - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging configuration.

      - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **HlsManifests** *(list) --* A list of HLS manifest configurations

        - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
          OriginEndpoint and it cannot be changed after it is created.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **ManifestName** *(string) --* An optional short string appended to the end of the
          OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
      each segment. If not specified, it defaults to the ChannelId.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
    configuration.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
      Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
      ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
      are combined and presented at the AdaptationSet level.

      - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
      manifest.

      - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
      buffer media before starting the presentation.

      - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
      changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description
      (MPD).

      - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
      Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
      into multiple periods. If empty, the content will not be partitioned into more than one
      period. If the list contains "ADS", new periods will be created where the Channel source
      contains SCTE-35 ad markers.

        - *(string) --*

      - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
      set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in
      the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
      presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
      full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
      NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
      URLs.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
      content before presentation.

    - **Description** *(string) --* A short text description of the OriginEndpoint.

    - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

      - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
      packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
      "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments) taken
      directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad
      markers and blackout tags based on SCTE-35 messages in the input source.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

        - **ConstantInitializationVector** *(string) --* A constant initialization vector for
        encryption (optional). When not specified the initialization vector will be periodically
        rotated.

        - **EncryptionMethod** *(string) --* The encryption method to use.

        - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
        encryption key rotation.

        - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
        output manifests.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
      included in the output.

      - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
      "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
      the media playlist.

      - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
      manifest.

      - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
      EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
      specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
      of the content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME
      tags will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note
      that irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming
      (HLS) input, it will be passed through to HLS output.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
      fragments will be rounded to the nearest multiple of the source fragment duration.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
      rendition groups in the output.

    - **Id** *(string) --* The ID of the OriginEndpoint.

    - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint URL.

    - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

      - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
      manifest.

      - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **Origination** *(string) --* Control whether origination of video is allowed for this
    OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other form
    of access control. If set to DENY, the OriginEndpoint may not be requested. This can be helpful
    for Live to VOD harvesting, or for temporarily disabling origination

    - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain for
    startover playback. If not specified, startover playback will be disabled for the
    OriginEndpoint.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*

    - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback of
    live content. If not specified, there will be no time delay in effect for the OriginEndpoint.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access the
    OriginEndpoint.

      - *(string) --*
    """


_ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef(
    _ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientListChannelsResponseChannelsHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientListChannelsResponseChannelsHlsIngestTypeDef = TypedDict(
    "_ClientListChannelsResponseChannelsHlsIngestTypeDef",
    {"IngestEndpoints": List[ClientListChannelsResponseChannelsHlsIngestIngestEndpointsTypeDef]},
    total=False,
)


class ClientListChannelsResponseChannelsHlsIngestTypeDef(
    _ClientListChannelsResponseChannelsHlsIngestTypeDef
):
    """
    Type definition for `ClientListChannelsResponseChannels` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientListChannelsResponseChannelsTypeDef = TypedDict(
    "_ClientListChannelsResponseChannelsTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientListChannelsResponseChannelsHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientListChannelsResponseChannelsTypeDef(_ClientListChannelsResponseChannelsTypeDef):
    """
    Type definition for `ClientListChannelsResponse` `Channels`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ClientListChannelsResponseTypeDef = TypedDict(
    "_ClientListChannelsResponseTypeDef",
    {"Channels": List[ClientListChannelsResponseChannelsTypeDef], "NextToken": str},
    total=False,
)


class ClientListChannelsResponseTypeDef(_ClientListChannelsResponseTypeDef):
    """
    Type definition for `ClientListChannels` `Response`

    - **Channels** *(list) --* A list of Channel records.

      - *(dict) --* A Channel resource configuration.

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

        - **Description** *(string) --* A short text description of the Channel.

        - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

          - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
          sent.

            - *(dict) --* An endpoint for ingesting source content for a Channel.

              - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

              - **Password** *(string) --* The system generated password for ingest authentication.

              - **Url** *(string) --* The ingest URL to which the source stream should be sent.

              - **Username** *(string) --* The system generated username for ingest authentication.

        - **Id** *(string) --* The ID of the Channel.

        - **Tags** *(dict) --* A collection of tags associated with a resource

          - *(string) --*

            - *(string) --*

    - **NextToken** *(string) --* A token that can be used to resume pagination from the end of the
    collection.
    """


_ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef = TypedDict(
    "_ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef",
    {"BucketName": str, "ManifestKey": str, "RoleArn": str},
    total=False,
)


class ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef(
    _ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef
):
    """
    Type definition for `ClientListHarvestJobsResponseHarvestJobs` `S3Destination`

    - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
    exported

    - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested top-level
    manifest will be placed.

    - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket
    """


_ClientListHarvestJobsResponseHarvestJobsTypeDef = TypedDict(
    "_ClientListHarvestJobsResponseHarvestJobsTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CreatedAt": str,
        "EndTime": str,
        "Id": str,
        "OriginEndpointId": str,
        "S3Destination": ClientListHarvestJobsResponseHarvestJobsS3DestinationTypeDef,
        "StartTime": str,
        "Status": str,
    },
    total=False,
)


class ClientListHarvestJobsResponseHarvestJobsTypeDef(
    _ClientListHarvestJobsResponseHarvestJobsTypeDef
):
    """
    Type definition for `ClientListHarvestJobsResponse` `HarvestJobs`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

    - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

    - **CreatedAt** *(string) --* The time the HarvestJob was submitted

    - **EndTime** *(string) --* The end of the time-window which will be harvested.

    - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and it
    cannot be changed after the HarvestJob is submitted.

    - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
    harvest from. This cannot be changed after the HarvestJob is submitted.

    - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place the
    harvested content

      - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
      exported

      - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
      top-level manifest will be placed.

      - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

    - **StartTime** *(string) --* The start of the time-window which will be harvested.

    - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
    CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure, the
    CloudWatch Event will include an explanation of why the HarvestJob failed.
    """


_ClientListHarvestJobsResponseTypeDef = TypedDict(
    "_ClientListHarvestJobsResponseTypeDef",
    {"HarvestJobs": List[ClientListHarvestJobsResponseHarvestJobsTypeDef], "NextToken": str},
    total=False,
)


class ClientListHarvestJobsResponseTypeDef(_ClientListHarvestJobsResponseTypeDef):
    """
    Type definition for `ClientListHarvestJobs` `Response`

    - **HarvestJobs** *(list) --* A list of HarvestJob records.

      - *(dict) --* A HarvestJob resource configuration

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

        - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

        - **CreatedAt** *(string) --* The time the HarvestJob was submitted

        - **EndTime** *(string) --* The end of the time-window which will be harvested.

        - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and
        it cannot be changed after the HarvestJob is submitted.

        - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
        harvest from. This cannot be changed after the HarvestJob is submitted.

        - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place
        the harvested content

          - **BucketName** *(string) --* The name of an S3 bucket within which harvested content
          will be exported

          - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
          top-level manifest will be placed.

          - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

        - **StartTime** *(string) --* The start of the time-window which will be harvested.

        - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
        CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure,
        the CloudWatch Event will include an explanation of why the HarvestJob failed.

    - **NextToken** *(string) --* A token that can be used to resume pagination from the end of the
    collection.
    """


_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "Id": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "Url": str,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **Id** *(string) --* The ID of the manifest. The ID must be unique within the OriginEndpoint
    and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.
    """


_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsCmafPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef",
    {
        "Encryption": ClientListOriginEndpointsResponseOriginEndpointsCmafPackageEncryptionTypeDef,
        "HlsManifests": List[
            ClientListOriginEndpointsResponseOriginEndpointsCmafPackageHlsManifestsTypeDef
        ],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientListOriginEndpointsResponseOriginEndpointsCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpoints` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
        OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsDashPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientListOriginEndpointsResponseOriginEndpointsDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientListOriginEndpointsResponseOriginEndpointsDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpoints` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "SpekeKeyProvider": ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsHlsPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientListOriginEndpointsResponseOriginEndpointsHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientListOriginEndpointsResponseOriginEndpointsHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpoints` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef",
    {
        "SpekeKeyProvider": ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpointsMssPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef",
    {
        "Encryption": ClientListOriginEndpointsResponseOriginEndpointsMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientListOriginEndpointsResponseOriginEndpointsMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponseOriginEndpoints` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientListOriginEndpointsResponseOriginEndpointsTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseOriginEndpointsTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CmafPackage": ClientListOriginEndpointsResponseOriginEndpointsCmafPackageTypeDef,
        "DashPackage": ClientListOriginEndpointsResponseOriginEndpointsDashPackageTypeDef,
        "Description": str,
        "HlsPackage": ClientListOriginEndpointsResponseOriginEndpointsHlsPackageTypeDef,
        "Id": str,
        "ManifestName": str,
        "MssPackage": ClientListOriginEndpointsResponseOriginEndpointsMssPackageTypeDef,
        "Origination": str,
        "StartoverWindowSeconds": int,
        "Tags": Dict[str, str],
        "TimeDelaySeconds": int,
        "Url": str,
        "Whitelist": List[str],
    },
    total=False,
)


class ClientListOriginEndpointsResponseOriginEndpointsTypeDef(
    _ClientListOriginEndpointsResponseOriginEndpointsTypeDef
):
    """
    Type definition for `ClientListOriginEndpointsResponse` `OriginEndpoints`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

    - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

    - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging configuration.

      - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **HlsManifests** *(list) --* A list of HLS manifest configurations

        - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
          OriginEndpoint and it cannot be changed after it is created.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **ManifestName** *(string) --* An optional short string appended to the end of the
          OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
      each segment. If not specified, it defaults to the ChannelId.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
    configuration.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
      Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
      ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
      are combined and presented at the AdaptationSet level.

      - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
      manifest.

      - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
      buffer media before starting the presentation.

      - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
      changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description
      (MPD).

      - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
      Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
      into multiple periods. If empty, the content will not be partitioned into more than one
      period. If the list contains "ADS", new periods will be created where the Channel source
      contains SCTE-35 ad markers.

        - *(string) --*

      - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
      set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in
      the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
      presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
      full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
      NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
      URLs.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
      content before presentation.

    - **Description** *(string) --* A short text description of the OriginEndpoint.

    - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

      - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
      packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
      "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments) taken
      directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad
      markers and blackout tags based on SCTE-35 messages in the input source.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

        - **ConstantInitializationVector** *(string) --* A constant initialization vector for
        encryption (optional). When not specified the initialization vector will be periodically
        rotated.

        - **EncryptionMethod** *(string) --* The encryption method to use.

        - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
        encryption key rotation.

        - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
        output manifests.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
      included in the output.

      - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
      "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
      the media playlist.

      - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
      manifest.

      - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
      EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
      specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
      of the content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME
      tags will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note
      that irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming
      (HLS) input, it will be passed through to HLS output.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
      fragments will be rounded to the nearest multiple of the source fragment duration.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
      rendition groups in the output.

    - **Id** *(string) --* The ID of the OriginEndpoint.

    - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint URL.

    - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

      - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
      manifest.

      - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **Origination** *(string) --* Control whether origination of video is allowed for this
    OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other form
    of access control. If set to DENY, the OriginEndpoint may not be requested. This can be helpful
    for Live to VOD harvesting, or for temporarily disabling origination

    - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain for
    startover playback. If not specified, startover playback will be disabled for the
    OriginEndpoint.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*

    - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback of
    live content. If not specified, there will be no time delay in effect for the OriginEndpoint.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access the
    OriginEndpoint.

      - *(string) --*
    """


_ClientListOriginEndpointsResponseTypeDef = TypedDict(
    "_ClientListOriginEndpointsResponseTypeDef",
    {
        "NextToken": str,
        "OriginEndpoints": List[ClientListOriginEndpointsResponseOriginEndpointsTypeDef],
    },
    total=False,
)


class ClientListOriginEndpointsResponseTypeDef(_ClientListOriginEndpointsResponseTypeDef):
    """
    Type definition for `ClientListOriginEndpoints` `Response`

    - **NextToken** *(string) --* A token that can be used to resume pagination from the end of the
    collection.

    - **OriginEndpoints** *(list) --* A list of OriginEndpoint records.

      - *(dict) --* An OriginEndpoint resource configuration.

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

        - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

        - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging
        configuration.

          - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
          configuration.

            - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each
            encryption key rotation.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **HlsManifests** *(list) --* A list of HLS manifest configurations

            - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

              - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
              packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
              "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers
              (comments) taken directly from the input HTTP Live Streaming (HLS) manifest.
              "SCTE35_ENHANCED" generates ad markers and blackout tags based on SCTE-35 messages in
              the input source.

              - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
              OriginEndpoint and it cannot be changed after it is created.

              - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will
              be included in the output.

              - **ManifestName** *(string) --* An optional short string appended to the end of the
              OriginEndpoint URL. If not specified, defaults to the manifestName for the
              OriginEndpoint.

              - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When
              either "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will
              be included in the media playlist.

              - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
              parent manifest.

              - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between
              each EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an
              interval is specified ID3Timed Metadata messages will be generated every 5 seconds
              using the ingest time of the content. If the interval is not specified, or set to 0,
              then no EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed
              Metadata messages will be generated. Note that irrespective of this parameter, if any
              ID3 Timed Metadata is found in HTTP Live Streaming (HLS) input, it will be passed
              through to HLS output.

              - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
          segments will be rounded to the nearest multiple of the source segment duration.

          - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name
          of each segment. If not specified, it defaults to the ChannelId.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

        - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
        configuration.

          - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad
          markers in the output. If empty, no ad markers are output. Specify multiple items to
          create ad markers for all of the included message types.

            - *(string) --*

          - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
          flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
          Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
          messages of the types specified in AdTriggers that contain delivery restrictions will be
          treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
          AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing
          "BOTH" means all SCTE-35 messages of the types specified in AdTriggers will be treated as
          ads. Note that Splice Insert messages do not have these flags and are always treated as
          ads if specified in AdTriggers.

          - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
          configuration.

            - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each
            encryption key rotation.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
          Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
          ContentProtection are included in each Representation. When set to COMPACT, duplicate
          elements are combined and presented at the AdaptationSet level.

          - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          manifest.

          - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
          buffer media before starting the presentation.

          - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between
          potential changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation
          Description (MPD).

          - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing
          Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be
          partitioned into multiple periods. If empty, the content will not be partitioned into more
          than one period. If the list contains "ADS", new periods will be created where the Channel
          source contains SCTE-35 ad markers.

            - *(string) --*

          - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type.
          When set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
          segments will be rounded to the nearest multiple of the source segment duration.

          - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included
          in the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full
          timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to
          TIME_WITH_TIMELINE, a full timeline is presented in each SegmentTemplate, with $Time$
          media URLs. When set to NUMBER_WITH_DURATION, only a duration is included in each
          SegmentTemplate, with $Number$ media URLs.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

          - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
          content before presentation.

        - **Description** *(string) --* A short text description of the OriginEndpoint.

        - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad
          markers in the output. If empty, no ad markers are output. Specify multiple items to
          create ad markers for all of the included message types.

            - *(string) --*

          - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
          flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
          Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
          messages of the types specified in AdTriggers that contain delivery restrictions will be
          treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
          AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing
          "BOTH" means all SCTE-35 messages of the types specified in AdTriggers will be treated as
          ads. Note that Splice Insert messages do not have these flags and are always treated as
          ads if specified in AdTriggers.

          - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

            - **ConstantInitializationVector** *(string) --* A constant initialization vector for
            encryption (optional). When not specified the initialization vector will be periodically
            rotated.

            - **EncryptionMethod** *(string) --* The encryption method to use.

            - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
            encryption key rotation.

            - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
            output manifests.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
          fragments will be rounded to the nearest multiple of the source fragment duration.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

          - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
          rendition groups in the output.

        - **Id** *(string) --* The ID of the OriginEndpoint.

        - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint
        URL.

        - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

          - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
          manifest.

          - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

        - **Origination** *(string) --* Control whether origination of video is allowed for this
        OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other
        form of access control. If set to DENY, the OriginEndpoint may not be requested. This can be
        helpful for Live to VOD harvesting, or for temporarily disabling origination

        - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain
        for startover playback. If not specified, startover playback will be disabled for the
        OriginEndpoint.

        - **Tags** *(dict) --* A collection of tags associated with a resource

          - *(string) --*

            - *(string) --*

        - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback
        of live content. If not specified, there will be no time delay in effect for the
        OriginEndpoint.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

        - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access
        the OriginEndpoint.

          - *(string) --*
    """


_ClientListTagsForResourceResponseTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)


class ClientListTagsForResourceResponseTypeDef(_ClientListTagsForResourceResponseTypeDef):
    """
    Type definition for `ClientListTagsForResource` `Response`

    - **Tags** *(dict) --*

      - *(string) --*

        - *(string) --*
    """


_ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef(
    _ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientRotateChannelCredentialsResponseHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientRotateChannelCredentialsResponseHlsIngestTypeDef = TypedDict(
    "_ClientRotateChannelCredentialsResponseHlsIngestTypeDef",
    {
        "IngestEndpoints": List[
            ClientRotateChannelCredentialsResponseHlsIngestIngestEndpointsTypeDef
        ]
    },
    total=False,
)


class ClientRotateChannelCredentialsResponseHlsIngestTypeDef(
    _ClientRotateChannelCredentialsResponseHlsIngestTypeDef
):
    """
    Type definition for `ClientRotateChannelCredentialsResponse` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientRotateChannelCredentialsResponseTypeDef = TypedDict(
    "_ClientRotateChannelCredentialsResponseTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientRotateChannelCredentialsResponseHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientRotateChannelCredentialsResponseTypeDef(_ClientRotateChannelCredentialsResponseTypeDef):
    """
    Type definition for `ClientRotateChannelCredentials` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef(
    _ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientRotateIngestEndpointCredentialsResponseHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef = TypedDict(
    "_ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef",
    {
        "IngestEndpoints": List[
            ClientRotateIngestEndpointCredentialsResponseHlsIngestIngestEndpointsTypeDef
        ]
    },
    total=False,
)


class ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef(
    _ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef
):
    """
    Type definition for `ClientRotateIngestEndpointCredentialsResponse` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientRotateIngestEndpointCredentialsResponseTypeDef = TypedDict(
    "_ClientRotateIngestEndpointCredentialsResponseTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientRotateIngestEndpointCredentialsResponseHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientRotateIngestEndpointCredentialsResponseTypeDef(
    _ClientRotateIngestEndpointCredentialsResponseTypeDef
):
    """
    Type definition for `ClientRotateIngestEndpointCredentials` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef(
    _ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ClientUpdateChannelResponseHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientUpdateChannelResponseHlsIngestTypeDef = TypedDict(
    "_ClientUpdateChannelResponseHlsIngestTypeDef",
    {"IngestEndpoints": List[ClientUpdateChannelResponseHlsIngestIngestEndpointsTypeDef]},
    total=False,
)


class ClientUpdateChannelResponseHlsIngestTypeDef(_ClientUpdateChannelResponseHlsIngestTypeDef):
    """
    Type definition for `ClientUpdateChannelResponse` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ClientUpdateChannelResponseTypeDef = TypedDict(
    "_ClientUpdateChannelResponseTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ClientUpdateChannelResponseHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ClientUpdateChannelResponseTypeDef(_ClientUpdateChannelResponseTypeDef):
    """
    Type definition for `ClientUpdateChannel` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_RequiredClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointCmafPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientUpdateOriginEndpointCmafPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointCmafPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientUpdateOriginEndpointCmafPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientUpdateOriginEndpointCmafPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointCmafPackageEncryptionTypeDef",
    {"KeyRotationIntervalSeconds": int},
    total=False,
)


class ClientUpdateOriginEndpointCmafPackageEncryptionTypeDef(
    _RequiredClientUpdateOriginEndpointCmafPackageEncryptionTypeDef,
    _OptionalClientUpdateOriginEndpointCmafPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef", {"Id": str}
)
_OptionalClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
    },
    total=False,
)


class ClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef(
    _RequiredClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef,
    _OptionalClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Id** *(string) --* **[REQUIRED]** The ID of the manifest. The ID must be unique within the
    OriginEndpoint and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.
    """


_ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointCmafPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointCmafPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointCmafPackageTypeDef",
    {
        "Encryption": ClientUpdateOriginEndpointCmafPackageEncryptionTypeDef,
        "HlsManifests": List[ClientUpdateOriginEndpointCmafPackageHlsManifestsTypeDef],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientUpdateOriginEndpointCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointCmafPackageTypeDef(_ClientUpdateOriginEndpointCmafPackageTypeDef):
    """
    Type definition for `ClientUpdateOriginEndpoint` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers
        in the output. If empty, no ad markers are output. Specify multiple items to create ad
        markers for all of the included message types.

          - *(string) --*

        - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
        flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
        Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
        messages of the types specified in AdTriggers that contain delivery restrictions will be
        treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
        AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
        means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
        that Splice Insert messages do not have these flags and are always treated as ads if
        specified in AdTriggers.

        - **Id** *(string) --* **[REQUIRED]** The ID of the manifest. The ID must be unique within
        the OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_RequiredClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointDashPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientUpdateOriginEndpointDashPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointDashPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientUpdateOriginEndpointDashPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientUpdateOriginEndpointDashPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointDashPackageEncryptionTypeDef",
    {"KeyRotationIntervalSeconds": int},
    total=False,
)


class ClientUpdateOriginEndpointDashPackageEncryptionTypeDef(
    _RequiredClientUpdateOriginEndpointDashPackageEncryptionTypeDef,
    _OptionalClientUpdateOriginEndpointDashPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointDashPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointDashPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientUpdateOriginEndpointDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientUpdateOriginEndpointDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientUpdateOriginEndpointDashPackageTypeDef(_ClientUpdateOriginEndpointDashPackageTypeDef):
    """
    Type definition for `ClientUpdateOriginEndpoint` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_RequiredClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointHlsPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_RequiredClientUpdateOriginEndpointHlsPackageEncryptionTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointHlsPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientUpdateOriginEndpointHlsPackageEncryptionSpekeKeyProviderTypeDef},
)
_OptionalClientUpdateOriginEndpointHlsPackageEncryptionTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
    },
    total=False,
)


class ClientUpdateOriginEndpointHlsPackageEncryptionTypeDef(
    _RequiredClientUpdateOriginEndpointHlsPackageEncryptionTypeDef,
    _OptionalClientUpdateOriginEndpointHlsPackageEncryptionTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointHlsPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointHlsPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientUpdateOriginEndpointHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientUpdateOriginEndpointHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientUpdateOriginEndpointHlsPackageTypeDef(_ClientUpdateOriginEndpointHlsPackageTypeDef):
    """
    Type definition for `ClientUpdateOriginEndpoint` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_RequiredClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
)
_OptionalClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str},
    total=False,
)


class ClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef(
    _RequiredClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef,
    _OptionalClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef,
):
    """
    Type definition for `ClientUpdateOriginEndpointMssPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

    - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that AWS
    Elemental MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointMssPackageEncryptionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointMssPackageEncryptionTypeDef",
    {"SpekeKeyProvider": ClientUpdateOriginEndpointMssPackageEncryptionSpekeKeyProviderTypeDef},
)


class ClientUpdateOriginEndpointMssPackageEncryptionTypeDef(
    _ClientUpdateOriginEndpointMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
    Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

      - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
      AWS Elemental MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointMssPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointMssPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointMssPackageTypeDef",
    {
        "Encryption": ClientUpdateOriginEndpointMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientUpdateOriginEndpointMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointMssPackageTypeDef(_ClientUpdateOriginEndpointMssPackageTypeDef):
    """
    Type definition for `ClientUpdateOriginEndpoint` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* **[REQUIRED]** A configuration for accessing an external
      Secure Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* **[REQUIRED]** The resource ID to include in key requests.

        - **RoleArn** *(string) --* **[REQUIRED]** An Amazon Resource Name (ARN) of an IAM role that
        AWS Elemental MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* **[REQUIRED]** The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* **[REQUIRED]** The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseCmafPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientUpdateOriginEndpointResponseCmafPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef(
    _ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "Id": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "Url": str,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef(
    _ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseCmafPackage` `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **Id** *(string) --* The ID of the manifest. The ID must be unique within the OriginEndpoint
    and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.
    """


_ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseCmafPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointResponseCmafPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseCmafPackageTypeDef",
    {
        "Encryption": ClientUpdateOriginEndpointResponseCmafPackageEncryptionTypeDef,
        "HlsManifests": List[ClientUpdateOriginEndpointResponseCmafPackageHlsManifestsTypeDef],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ClientUpdateOriginEndpointResponseCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseCmafPackageTypeDef(
    _ClientUpdateOriginEndpointResponseCmafPackageTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponse` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
        OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseDashPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ClientUpdateOriginEndpointResponseDashPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef(
    _ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseDashPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointResponseDashPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientUpdateOriginEndpointResponseDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ClientUpdateOriginEndpointResponseDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseDashPackageTypeDef(
    _ClientUpdateOriginEndpointResponseDashPackageTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponse` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseHlsPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "SpekeKeyProvider": ClientUpdateOriginEndpointResponseHlsPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef(
    _ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseHlsPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointResponseHlsPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ClientUpdateOriginEndpointResponseHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientUpdateOriginEndpointResponseHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseHlsPackageTypeDef(
    _ClientUpdateOriginEndpointResponseHlsPackageTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponse` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef(
    _ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseMssPackageEncryption` `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef",
    {
        "SpekeKeyProvider": ClientUpdateOriginEndpointResponseMssPackageEncryptionSpekeKeyProviderTypeDef
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef(
    _ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef(
    _ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponseMssPackage` `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ClientUpdateOriginEndpointResponseMssPackageTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseMssPackageTypeDef",
    {
        "Encryption": ClientUpdateOriginEndpointResponseMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ClientUpdateOriginEndpointResponseMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseMssPackageTypeDef(
    _ClientUpdateOriginEndpointResponseMssPackageTypeDef
):
    """
    Type definition for `ClientUpdateOriginEndpointResponse` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ClientUpdateOriginEndpointResponseTypeDef = TypedDict(
    "_ClientUpdateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CmafPackage": ClientUpdateOriginEndpointResponseCmafPackageTypeDef,
        "DashPackage": ClientUpdateOriginEndpointResponseDashPackageTypeDef,
        "Description": str,
        "HlsPackage": ClientUpdateOriginEndpointResponseHlsPackageTypeDef,
        "Id": str,
        "ManifestName": str,
        "MssPackage": ClientUpdateOriginEndpointResponseMssPackageTypeDef,
        "Origination": str,
        "StartoverWindowSeconds": int,
        "Tags": Dict[str, str],
        "TimeDelaySeconds": int,
        "Url": str,
        "Whitelist": List[str],
    },
    total=False,
)


class ClientUpdateOriginEndpointResponseTypeDef(_ClientUpdateOriginEndpointResponseTypeDef):
    """
    Type definition for `ClientUpdateOriginEndpoint` `Response`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

    - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

    - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging configuration.

      - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **HlsManifests** *(list) --* A list of HLS manifest configurations

        - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
          OriginEndpoint and it cannot be changed after it is created.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **ManifestName** *(string) --* An optional short string appended to the end of the
          OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
      each segment. If not specified, it defaults to the ChannelId.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
    configuration.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
      Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
      ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
      are combined and presented at the AdaptationSet level.

      - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
      manifest.

      - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
      buffer media before starting the presentation.

      - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
      changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description
      (MPD).

      - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
      Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
      into multiple periods. If empty, the content will not be partitioned into more than one
      period. If the list contains "ADS", new periods will be created where the Channel source
      contains SCTE-35 ad markers.

        - *(string) --*

      - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
      set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in
      the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
      presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
      full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
      NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
      URLs.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
      content before presentation.

    - **Description** *(string) --* A short text description of the OriginEndpoint.

    - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

      - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
      packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
      "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments) taken
      directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad
      markers and blackout tags based on SCTE-35 messages in the input source.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

        - **ConstantInitializationVector** *(string) --* A constant initialization vector for
        encryption (optional). When not specified the initialization vector will be periodically
        rotated.

        - **EncryptionMethod** *(string) --* The encryption method to use.

        - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
        encryption key rotation.

        - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
        output manifests.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
      included in the output.

      - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
      "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
      the media playlist.

      - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
      manifest.

      - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
      EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
      specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
      of the content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME
      tags will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note
      that irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming
      (HLS) input, it will be passed through to HLS output.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
      fragments will be rounded to the nearest multiple of the source fragment duration.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
      rendition groups in the output.

    - **Id** *(string) --* The ID of the OriginEndpoint.

    - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint URL.

    - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

      - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
      manifest.

      - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **Origination** *(string) --* Control whether origination of video is allowed for this
    OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other form
    of access control. If set to DENY, the OriginEndpoint may not be requested. This can be helpful
    for Live to VOD harvesting, or for temporarily disabling origination

    - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain for
    startover playback. If not specified, startover playback will be disabled for the
    OriginEndpoint.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*

    - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback of
    live content. If not specified, there will be no time delay in effect for the OriginEndpoint.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access the
    OriginEndpoint.

      - *(string) --*
    """


_ListChannelsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListChannelsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListChannelsPaginatePaginationConfigTypeDef(_ListChannelsPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListChannelsPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef = TypedDict(
    "_ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef",
    {"Id": str, "Password": str, "Url": str, "Username": str},
    total=False,
)


class ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef(
    _ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef
):
    """
    Type definition for `ListChannelsPaginateResponseChannelsHlsIngest` `IngestEndpoints`

    - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

    - **Password** *(string) --* The system generated password for ingest authentication.

    - **Url** *(string) --* The ingest URL to which the source stream should be sent.

    - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ListChannelsPaginateResponseChannelsHlsIngestTypeDef = TypedDict(
    "_ListChannelsPaginateResponseChannelsHlsIngestTypeDef",
    {"IngestEndpoints": List[ListChannelsPaginateResponseChannelsHlsIngestIngestEndpointsTypeDef]},
    total=False,
)


class ListChannelsPaginateResponseChannelsHlsIngestTypeDef(
    _ListChannelsPaginateResponseChannelsHlsIngestTypeDef
):
    """
    Type definition for `ListChannelsPaginateResponseChannels` `HlsIngest`

    - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be sent.

      - *(dict) --* An endpoint for ingesting source content for a Channel.

        - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

        - **Password** *(string) --* The system generated password for ingest authentication.

        - **Url** *(string) --* The ingest URL to which the source stream should be sent.

        - **Username** *(string) --* The system generated username for ingest authentication.
    """


_ListChannelsPaginateResponseChannelsTypeDef = TypedDict(
    "_ListChannelsPaginateResponseChannelsTypeDef",
    {
        "Arn": str,
        "Description": str,
        "HlsIngest": ListChannelsPaginateResponseChannelsHlsIngestTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)


class ListChannelsPaginateResponseChannelsTypeDef(_ListChannelsPaginateResponseChannelsTypeDef):
    """
    Type definition for `ListChannelsPaginateResponse` `Channels`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

    - **Description** *(string) --* A short text description of the Channel.

    - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

      - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
      sent.

        - *(dict) --* An endpoint for ingesting source content for a Channel.

          - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

          - **Password** *(string) --* The system generated password for ingest authentication.

          - **Url** *(string) --* The ingest URL to which the source stream should be sent.

          - **Username** *(string) --* The system generated username for ingest authentication.

    - **Id** *(string) --* The ID of the Channel.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*
    """


_ListChannelsPaginateResponseTypeDef = TypedDict(
    "_ListChannelsPaginateResponseTypeDef",
    {"Channels": List[ListChannelsPaginateResponseChannelsTypeDef]},
    total=False,
)


class ListChannelsPaginateResponseTypeDef(_ListChannelsPaginateResponseTypeDef):
    """
    Type definition for `ListChannelsPaginate` `Response`

    - **Channels** *(list) --* A list of Channel records.

      - *(dict) --* A Channel resource configuration.

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the Channel.

        - **Description** *(string) --* A short text description of the Channel.

        - **HlsIngest** *(dict) --* An HTTP Live Streaming (HLS) ingest resource configuration.

          - **IngestEndpoints** *(list) --* A list of endpoints to which the source stream should be
          sent.

            - *(dict) --* An endpoint for ingesting source content for a Channel.

              - **Id** *(string) --* The system generated unique identifier for the IngestEndpoint

              - **Password** *(string) --* The system generated password for ingest authentication.

              - **Url** *(string) --* The ingest URL to which the source stream should be sent.

              - **Username** *(string) --* The system generated username for ingest authentication.

        - **Id** *(string) --* The ID of the Channel.

        - **Tags** *(dict) --* A collection of tags associated with a resource

          - *(string) --*

            - *(string) --*
    """


_ListHarvestJobsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListHarvestJobsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListHarvestJobsPaginatePaginationConfigTypeDef(
    _ListHarvestJobsPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListHarvestJobsPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef = TypedDict(
    "_ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef",
    {"BucketName": str, "ManifestKey": str, "RoleArn": str},
    total=False,
)


class ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef(
    _ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef
):
    """
    Type definition for `ListHarvestJobsPaginateResponseHarvestJobs` `S3Destination`

    - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
    exported

    - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested top-level
    manifest will be placed.

    - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket
    """


_ListHarvestJobsPaginateResponseHarvestJobsTypeDef = TypedDict(
    "_ListHarvestJobsPaginateResponseHarvestJobsTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CreatedAt": str,
        "EndTime": str,
        "Id": str,
        "OriginEndpointId": str,
        "S3Destination": ListHarvestJobsPaginateResponseHarvestJobsS3DestinationTypeDef,
        "StartTime": str,
        "Status": str,
    },
    total=False,
)


class ListHarvestJobsPaginateResponseHarvestJobsTypeDef(
    _ListHarvestJobsPaginateResponseHarvestJobsTypeDef
):
    """
    Type definition for `ListHarvestJobsPaginateResponse` `HarvestJobs`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

    - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

    - **CreatedAt** *(string) --* The time the HarvestJob was submitted

    - **EndTime** *(string) --* The end of the time-window which will be harvested.

    - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and it
    cannot be changed after the HarvestJob is submitted.

    - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
    harvest from. This cannot be changed after the HarvestJob is submitted.

    - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place the
    harvested content

      - **BucketName** *(string) --* The name of an S3 bucket within which harvested content will be
      exported

      - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
      top-level manifest will be placed.

      - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

    - **StartTime** *(string) --* The start of the time-window which will be harvested.

    - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
    CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure, the
    CloudWatch Event will include an explanation of why the HarvestJob failed.
    """


_ListHarvestJobsPaginateResponseTypeDef = TypedDict(
    "_ListHarvestJobsPaginateResponseTypeDef",
    {"HarvestJobs": List[ListHarvestJobsPaginateResponseHarvestJobsTypeDef]},
    total=False,
)


class ListHarvestJobsPaginateResponseTypeDef(_ListHarvestJobsPaginateResponseTypeDef):
    """
    Type definition for `ListHarvestJobsPaginate` `Response`

    - **HarvestJobs** *(list) --* A list of HarvestJob records.

      - *(dict) --* A HarvestJob resource configuration

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the HarvestJob.

        - **ChannelId** *(string) --* The ID of the Channel that the HarvestJob will harvest from.

        - **CreatedAt** *(string) --* The time the HarvestJob was submitted

        - **EndTime** *(string) --* The end of the time-window which will be harvested.

        - **Id** *(string) --* The ID of the HarvestJob. The ID must be unique within the region and
        it cannot be changed after the HarvestJob is submitted.

        - **OriginEndpointId** *(string) --* The ID of the OriginEndpoint that the HarvestJob will
        harvest from. This cannot be changed after the HarvestJob is submitted.

        - **S3Destination** *(dict) --* Configuration parameters for where in an S3 bucket to place
        the harvested content

          - **BucketName** *(string) --* The name of an S3 bucket within which harvested content
          will be exported

          - **ManifestKey** *(string) --* The key in the specified S3 bucket where the harvested
          top-level manifest will be placed.

          - **RoleArn** *(string) --* The IAM role used to write to the specified S3 bucket

        - **StartTime** *(string) --* The start of the time-window which will be harvested.

        - **Status** *(string) --* The current status of the HarvestJob. Consider setting up a
        CloudWatch Event to listen for HarvestJobs as they succeed or fail. In the event of failure,
        the CloudWatch Event will include an explanation of why the HarvestJob failed.
    """


_ListOriginEndpointsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListOriginEndpointsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListOriginEndpointsPaginatePaginationConfigTypeDef(
    _ListOriginEndpointsPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef",
    {
        "AdMarkers": str,
        "Id": str,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "Url": str,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackage`
    `HlsManifests`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **Id** *(string) --* The ID of the manifest. The ID must be unique within the OriginEndpoint
    and it cannot be changed after it is created.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **ManifestName** *(string) --* An optional short string appended to the end of the
    OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef",
    {
        "Encryption": ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageEncryptionTypeDef,
        "HlsManifests": List[
            ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageHlsManifestsTypeDef
        ],
        "SegmentDurationSeconds": int,
        "SegmentPrefix": str,
        "StreamSelection": ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpoints` `CmafPackage`

    - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **HlsManifests** *(list) --* A list of HLS manifest configurations

      - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

        - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
        packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
        "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
        taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
        generates ad markers and blackout tags based on SCTE-35 messages in the input source.

        - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
        OriginEndpoint and it cannot be changed after it is created.

        - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
        included in the output.

        - **ManifestName** *(string) --* An optional short string appended to the end of the
        OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

        - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
        "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
        the media playlist.

        - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
        manifest.

        - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
        EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
        specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
        of the content. If the interval is not specified, or set to 0, then no
        EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
        messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
        Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
        output.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
    each segment. If not specified, it defaults to the ChannelId.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef",
    {
        "KeyRotationIntervalSeconds": int,
        "SpekeKeyProvider": ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsDashPackage` `Encryption`

    - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
    rotation.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsDashPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef",
    {
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageEncryptionTypeDef,
        "ManifestLayout": str,
        "ManifestWindowSeconds": int,
        "MinBufferTimeSeconds": int,
        "MinUpdatePeriodSeconds": int,
        "PeriodTriggers": List[str],
        "Profile": str,
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": str,
        "StreamSelection": ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageStreamSelectionTypeDef,
        "SuggestedPresentationDelaySeconds": int,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpoints` `DashPackage`

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
    configuration.

      - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption key
      rotation.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
    Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
    ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
    are combined and presented at the AdaptationSet level.

    - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each manifest.

    - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
    buffer media before starting the presentation.

    - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
    changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD).

    - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
    Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
    into multiple periods. If empty, the content will not be partitioned into more than one period.
    If the list contains "ADS", new periods will be created where the Channel source contains
    SCTE-35 ad markers.

      - *(string) --*

    - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
    set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
    segments will be rounded to the nearest multiple of the source segment duration.

    - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in the
    Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
    presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
    full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
    NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
    URLs.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
    content before presentation.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": str,
        "KeyRotationIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "SpekeKeyProvider": ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionSpekeKeyProviderTypeDef,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackage` `Encryption`

    - **ConstantInitializationVector** *(string) --* A constant initialization vector for encryption
    (optional). When not specified the initialization vector will be periodically rotated.

    - **EncryptionMethod** *(string) --* The encryption method to use.

    - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
    key rotation.

    - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
    manifests.

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef",
    {
        "AdMarkers": str,
        "AdTriggers": List[str],
        "AdsOnDeliveryRestrictions": str,
        "Encryption": ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageEncryptionTypeDef,
        "IncludeIframeOnlyStream": bool,
        "PlaylistType": str,
        "PlaylistWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageStreamSelectionTypeDef,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpoints` `HlsPackage`

    - **AdMarkers** *(string) --* This setting controls how ad markers are included in the packaged
    OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output. "PASSTHROUGH" causes
    the manifest to contain a copy of the SCTE-35 ad markers (comments) taken directly from the
    input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad markers and blackout
    tags based on SCTE-35 messages in the input source.

    - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
    the output. If empty, no ad markers are output. Specify multiple items to create ad markers for
    all of the included message types.

      - *(string) --*

    - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction flags
    on SCTE-35 segmentation descriptors to determine whether a message signals an ad. Choosing
    "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35 messages of the
    types specified in AdTriggers that contain delivery restrictions will be treated as ads.
    Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in AdTriggers that do not
    contain delivery restrictions will be treated as ads. Choosing "BOTH" means all SCTE-35 messages
    of the types specified in AdTriggers will be treated as ads. Note that Splice Insert messages do
    not have these flags and are always treated as ads if specified in AdTriggers.

    - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

      - **ConstantInitializationVector** *(string) --* A constant initialization vector for
      encryption (optional). When not specified the initialization vector will be periodically
      rotated.

      - **EncryptionMethod** *(string) --* The encryption method to use.

      - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each encryption
      key rotation.

      - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in output
      manifests.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
    included in the output.

    - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
    "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in the
    media playlist.

    - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
    manifest.

    - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
    EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is specified
    ID3Timed Metadata messages will be generated every 5 seconds using the ingest time of the
    content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME tags
    will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note that
    irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming (HLS)
    input, it will be passed through to HLS output.

    - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
    fragments will be rounded to the nearest multiple of the source fragment duration.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.

    - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
    rendition groups in the output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef",
    {"CertificateArn": str, "ResourceId": str, "RoleArn": str, "SystemIds": List[str], "Url": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryption`
    `SpekeKeyProvider`

    - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
    certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
    key provider service.

    - **ResourceId** *(string) --* The resource ID to include in key requests.

    - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
    MediaPackage will assume when accessing the key provider service.

    - **SystemIds** *(list) --* The system IDs to include in key requests.

      - *(string) --*

    - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef",
    {
        "SpekeKeyProvider": ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionSpekeKeyProviderTypeDef
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsMssPackage` `Encryption`

    - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager and
    Encoder Key Exchange (SPEKE) service that will provide encryption keys.

      - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
      certificate that MediaPackage will use for enforcing secure end-to-end data transfer with the
      key provider service.

      - **ResourceId** *(string) --* The resource ID to include in key requests.

      - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
      MediaPackage will assume when accessing the key provider service.

      - **SystemIds** *(list) --* The system IDs to include in key requests.

        - *(string) --*

      - **Url** *(string) --* The URL of the external key provider service.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef",
    {"MaxVideoBitsPerSecond": int, "MinVideoBitsPerSecond": int, "StreamOrder": str},
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpointsMssPackage`
    `StreamSelection`

    - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in output.

    - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in output.

    - **StreamOrder** *(string) --* A directive that determines the order of streams in the output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef",
    {
        "Encryption": ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageEncryptionTypeDef,
        "ManifestWindowSeconds": int,
        "SegmentDurationSeconds": int,
        "StreamSelection": ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageStreamSelectionTypeDef,
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponseOriginEndpoints` `MssPackage`

    - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

      - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
      and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

        - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
        certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
        the key provider service.

        - **ResourceId** *(string) --* The resource ID to include in key requests.

        - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS Elemental
        MediaPackage will assume when accessing the key provider service.

        - **SystemIds** *(list) --* The system IDs to include in key requests.

          - *(string) --*

        - **Url** *(string) --* The URL of the external key provider service.

    - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
    manifest.

    - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

    - **StreamSelection** *(dict) --* A StreamSelection configuration.

      - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
      output.

      - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
      output.

      - **StreamOrder** *(string) --* A directive that determines the order of streams in the
      output.
    """


_ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef",
    {
        "Arn": str,
        "ChannelId": str,
        "CmafPackage": ListOriginEndpointsPaginateResponseOriginEndpointsCmafPackageTypeDef,
        "DashPackage": ListOriginEndpointsPaginateResponseOriginEndpointsDashPackageTypeDef,
        "Description": str,
        "HlsPackage": ListOriginEndpointsPaginateResponseOriginEndpointsHlsPackageTypeDef,
        "Id": str,
        "ManifestName": str,
        "MssPackage": ListOriginEndpointsPaginateResponseOriginEndpointsMssPackageTypeDef,
        "Origination": str,
        "StartoverWindowSeconds": int,
        "Tags": Dict[str, str],
        "TimeDelaySeconds": int,
        "Url": str,
        "Whitelist": List[str],
    },
    total=False,
)


class ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef(
    _ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef
):
    """
    Type definition for `ListOriginEndpointsPaginateResponse` `OriginEndpoints`

    - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

    - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

    - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging configuration.

      - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **HlsManifests** *(list) --* A list of HLS manifest configurations

        - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
          OriginEndpoint and it cannot be changed after it is created.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **ManifestName** *(string) --* An optional short string appended to the end of the
          OriginEndpoint URL. If not specified, defaults to the manifestName for the OriginEndpoint.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name of
      each segment. If not specified, it defaults to the ChannelId.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
    configuration.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
      configuration.

        - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each encryption
        key rotation.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
      Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
      ContentProtection are included in each Representation. When set to COMPACT, duplicate elements
      are combined and presented at the AdaptationSet level.

      - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
      manifest.

      - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
      buffer media before starting the presentation.

      - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between potential
      changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description
      (MPD).

      - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing Dynamic
      Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be partitioned
      into multiple periods. If empty, the content will not be partitioned into more than one
      period. If the list contains "ADS", new periods will be created where the Channel source
      contains SCTE-35 ad markers.

        - *(string) --*

      - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type. When
      set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
      segments will be rounded to the nearest multiple of the source segment duration.

      - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included in
      the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full timeline is
      presented in each SegmentTemplate, with $Number$ media URLs. When set to TIME_WITH_TIMELINE, a
      full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to
      NUMBER_WITH_DURATION, only a duration is included in each SegmentTemplate, with $Number$ media
      URLs.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
      content before presentation.

    - **Description** *(string) --* A short text description of the OriginEndpoint.

    - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

      - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
      packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
      "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments) taken
      directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED" generates ad
      markers and blackout tags based on SCTE-35 messages in the input source.

      - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad markers in
      the output. If empty, no ad markers are output. Specify multiple items to create ad markers
      for all of the included message types.

        - *(string) --*

      - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
      flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
      Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
      messages of the types specified in AdTriggers that contain delivery restrictions will be
      treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
      AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing "BOTH"
      means all SCTE-35 messages of the types specified in AdTriggers will be treated as ads. Note
      that Splice Insert messages do not have these flags and are always treated as ads if specified
      in AdTriggers.

      - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

        - **ConstantInitializationVector** *(string) --* A constant initialization vector for
        encryption (optional). When not specified the initialization vector will be periodically
        rotated.

        - **EncryptionMethod** *(string) --* The encryption method to use.

        - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
        encryption key rotation.

        - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
        output manifests.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
      included in the output.

      - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
      "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included in
      the media playlist.

      - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each parent
      manifest.

      - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
      EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
      specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest time
      of the content. If the interval is not specified, or set to 0, then no EXT-X-PROGRAM-DATE-TIME
      tags will be inserted into manifests and no ID3Timed Metadata messages will be generated. Note
      that irrespective of this parameter, if any ID3 Timed Metadata is found in HTTP Live Streaming
      (HLS) input, it will be passed through to HLS output.

      - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
      fragments will be rounded to the nearest multiple of the source fragment duration.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

      - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
      rendition groups in the output.

    - **Id** *(string) --* The ID of the OriginEndpoint.

    - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint URL.

    - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

      - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

        - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure Packager
        and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

          - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate Manager
          certificate that MediaPackage will use for enforcing secure end-to-end data transfer with
          the key provider service.

          - **ResourceId** *(string) --* The resource ID to include in key requests.

          - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
          Elemental MediaPackage will assume when accessing the key provider service.

          - **SystemIds** *(list) --* The system IDs to include in key requests.

            - *(string) --*

          - **Url** *(string) --* The URL of the external key provider service.

      - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
      manifest.

      - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

      - **StreamSelection** *(dict) --* A StreamSelection configuration.

        - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
        output.

        - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
        output.

        - **StreamOrder** *(string) --* A directive that determines the order of streams in the
        output.

    - **Origination** *(string) --* Control whether origination of video is allowed for this
    OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other form
    of access control. If set to DENY, the OriginEndpoint may not be requested. This can be helpful
    for Live to VOD harvesting, or for temporarily disabling origination

    - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain for
    startover playback. If not specified, startover playback will be disabled for the
    OriginEndpoint.

    - **Tags** *(dict) --* A collection of tags associated with a resource

      - *(string) --*

        - *(string) --*

    - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback of
    live content. If not specified, there will be no time delay in effect for the OriginEndpoint.

    - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

    - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access the
    OriginEndpoint.

      - *(string) --*
    """


_ListOriginEndpointsPaginateResponseTypeDef = TypedDict(
    "_ListOriginEndpointsPaginateResponseTypeDef",
    {"OriginEndpoints": List[ListOriginEndpointsPaginateResponseOriginEndpointsTypeDef]},
    total=False,
)


class ListOriginEndpointsPaginateResponseTypeDef(_ListOriginEndpointsPaginateResponseTypeDef):
    """
    Type definition for `ListOriginEndpointsPaginate` `Response`

    - **OriginEndpoints** *(list) --* A list of OriginEndpoint records.

      - *(dict) --* An OriginEndpoint resource configuration.

        - **Arn** *(string) --* The Amazon Resource Name (ARN) assigned to the OriginEndpoint.

        - **ChannelId** *(string) --* The ID of the Channel the OriginEndpoint is associated with.

        - **CmafPackage** *(dict) --* A Common Media Application Format (CMAF) packaging
        configuration.

          - **Encryption** *(dict) --* A Common Media Application Format (CMAF) encryption
          configuration.

            - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each
            encryption key rotation.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **HlsManifests** *(list) --* A list of HLS manifest configurations

            - *(dict) --* A HTTP Live Streaming (HLS) manifest configuration.

              - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
              packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
              "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers
              (comments) taken directly from the input HTTP Live Streaming (HLS) manifest.
              "SCTE35_ENHANCED" generates ad markers and blackout tags based on SCTE-35 messages in
              the input source.

              - **Id** *(string) --* The ID of the manifest. The ID must be unique within the
              OriginEndpoint and it cannot be changed after it is created.

              - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will
              be included in the output.

              - **ManifestName** *(string) --* An optional short string appended to the end of the
              OriginEndpoint URL. If not specified, defaults to the manifestName for the
              OriginEndpoint.

              - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When
              either "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will
              be included in the media playlist.

              - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
              parent manifest.

              - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between
              each EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an
              interval is specified ID3Timed Metadata messages will be generated every 5 seconds
              using the ingest time of the content. If the interval is not specified, or set to 0,
              then no EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed
              Metadata messages will be generated. Note that irrespective of this parameter, if any
              ID3 Timed Metadata is found in HTTP Live Streaming (HLS) input, it will be passed
              through to HLS output.

              - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
          segments will be rounded to the nearest multiple of the source segment duration.

          - **SegmentPrefix** *(string) --* An optional custom string that is prepended to the name
          of each segment. If not specified, it defaults to the ChannelId.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

        - **DashPackage** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) packaging
        configuration.

          - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad
          markers in the output. If empty, no ad markers are output. Specify multiple items to
          create ad markers for all of the included message types.

            - *(string) --*

          - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
          flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
          Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
          messages of the types specified in AdTriggers that contain delivery restrictions will be
          treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
          AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing
          "BOTH" means all SCTE-35 messages of the types specified in AdTriggers will be treated as
          ads. Note that Splice Insert messages do not have these flags and are always treated as
          ads if specified in AdTriggers.

          - **Encryption** *(dict) --* A Dynamic Adaptive Streaming over HTTP (DASH) encryption
          configuration.

            - **KeyRotationIntervalSeconds** *(integer) --* Time (in seconds) between each
            encryption key rotation.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **ManifestLayout** *(string) --* Determines the position of some tags in the Media
          Presentation Description (MPD). When set to FULL, elements like SegmentTemplate and
          ContentProtection are included in each Representation. When set to COMPACT, duplicate
          elements are combined and presented at the AdaptationSet level.

          - **ManifestWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          manifest.

          - **MinBufferTimeSeconds** *(integer) --* Minimum duration (in seconds) that a player will
          buffer media before starting the presentation.

          - **MinUpdatePeriodSeconds** *(integer) --* Minimum duration (in seconds) between
          potential changes to the Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation
          Description (MPD).

          - **PeriodTriggers** *(list) --* A list of triggers that controls when the outgoing
          Dynamic Adaptive Streaming over HTTP (DASH) Media Presentation Description (MPD) will be
          partitioned into multiple periods. If empty, the content will not be partitioned into more
          than one period. If the list contains "ADS", new periods will be created where the Channel
          source contains SCTE-35 ad markers.

            - *(string) --*

          - **Profile** *(string) --* The Dynamic Adaptive Streaming over HTTP (DASH) profile type.
          When set to "HBBTV_1_5", HbbTV 1.5 compliant output is enabled.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each segment. Actual
          segments will be rounded to the nearest multiple of the source segment duration.

          - **SegmentTemplateFormat** *(string) --* Determines the type of SegmentTemplate included
          in the Media Presentation Description (MPD). When set to NUMBER_WITH_TIMELINE, a full
          timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to
          TIME_WITH_TIMELINE, a full timeline is presented in each SegmentTemplate, with $Time$
          media URLs. When set to NUMBER_WITH_DURATION, only a duration is included in each
          SegmentTemplate, with $Number$ media URLs.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

          - **SuggestedPresentationDelaySeconds** *(integer) --* Duration (in seconds) to delay live
          content before presentation.

        - **Description** *(string) --* A short text description of the OriginEndpoint.

        - **HlsPackage** *(dict) --* An HTTP Live Streaming (HLS) packaging configuration.

          - **AdMarkers** *(string) --* This setting controls how ad markers are included in the
          packaged OriginEndpoint. "NONE" will omit all SCTE-35 ad markers from the output.
          "PASSTHROUGH" causes the manifest to contain a copy of the SCTE-35 ad markers (comments)
          taken directly from the input HTTP Live Streaming (HLS) manifest. "SCTE35_ENHANCED"
          generates ad markers and blackout tags based on SCTE-35 messages in the input source.

          - **AdTriggers** *(list) --* A list of SCTE-35 message types that are treated as ad
          markers in the output. If empty, no ad markers are output. Specify multiple items to
          create ad markers for all of the included message types.

            - *(string) --*

          - **AdsOnDeliveryRestrictions** *(string) --* This setting allows the delivery restriction
          flags on SCTE-35 segmentation descriptors to determine whether a message signals an ad.
          Choosing "NONE" means no SCTE-35 messages become ads. Choosing "RESTRICTED" means SCTE-35
          messages of the types specified in AdTriggers that contain delivery restrictions will be
          treated as ads. Choosing "UNRESTRICTED" means SCTE-35 messages of the types specified in
          AdTriggers that do not contain delivery restrictions will be treated as ads. Choosing
          "BOTH" means all SCTE-35 messages of the types specified in AdTriggers will be treated as
          ads. Note that Splice Insert messages do not have these flags and are always treated as
          ads if specified in AdTriggers.

          - **Encryption** *(dict) --* An HTTP Live Streaming (HLS) encryption configuration.

            - **ConstantInitializationVector** *(string) --* A constant initialization vector for
            encryption (optional). When not specified the initialization vector will be periodically
            rotated.

            - **EncryptionMethod** *(string) --* The encryption method to use.

            - **KeyRotationIntervalSeconds** *(integer) --* Interval (in seconds) between each
            encryption key rotation.

            - **RepeatExtXKey** *(boolean) --* When enabled, the EXT-X-KEY tag will be repeated in
            output manifests.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **IncludeIframeOnlyStream** *(boolean) --* When enabled, an I-Frame only stream will be
          included in the output.

          - **PlaylistType** *(string) --* The HTTP Live Streaming (HLS) playlist type. When either
          "EVENT" or "VOD" is specified, a corresponding EXT-X-PLAYLIST-TYPE entry will be included
          in the media playlist.

          - **PlaylistWindowSeconds** *(integer) --* Time window (in seconds) contained in each
          parent manifest.

          - **ProgramDateTimeIntervalSeconds** *(integer) --* The interval (in seconds) between each
          EXT-X-PROGRAM-DATE-TIME tag inserted into manifests. Additionally, when an interval is
          specified ID3Timed Metadata messages will be generated every 5 seconds using the ingest
          time of the content. If the interval is not specified, or set to 0, then no
          EXT-X-PROGRAM-DATE-TIME tags will be inserted into manifests and no ID3Timed Metadata
          messages will be generated. Note that irrespective of this parameter, if any ID3 Timed
          Metadata is found in HTTP Live Streaming (HLS) input, it will be passed through to HLS
          output.

          - **SegmentDurationSeconds** *(integer) --* Duration (in seconds) of each fragment. Actual
          fragments will be rounded to the nearest multiple of the source fragment duration.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

          - **UseAudioRenditionGroup** *(boolean) --* When enabled, audio streams will be placed in
          rendition groups in the output.

        - **Id** *(string) --* The ID of the OriginEndpoint.

        - **ManifestName** *(string) --* A short string appended to the end of the OriginEndpoint
        URL.

        - **MssPackage** *(dict) --* A Microsoft Smooth Streaming (MSS) packaging configuration.

          - **Encryption** *(dict) --* A Microsoft Smooth Streaming (MSS) encryption configuration.

            - **SpekeKeyProvider** *(dict) --* A configuration for accessing an external Secure
            Packager and Encoder Key Exchange (SPEKE) service that will provide encryption keys.

              - **CertificateArn** *(string) --* An Amazon Resource Name (ARN) of a Certificate
              Manager certificate that MediaPackage will use for enforcing secure end-to-end data
              transfer with the key provider service.

              - **ResourceId** *(string) --* The resource ID to include in key requests.

              - **RoleArn** *(string) --* An Amazon Resource Name (ARN) of an IAM role that AWS
              Elemental MediaPackage will assume when accessing the key provider service.

              - **SystemIds** *(list) --* The system IDs to include in key requests.

                - *(string) --*

              - **Url** *(string) --* The URL of the external key provider service.

          - **ManifestWindowSeconds** *(integer) --* The time window (in seconds) contained in each
          manifest.

          - **SegmentDurationSeconds** *(integer) --* The duration (in seconds) of each segment.

          - **StreamSelection** *(dict) --* A StreamSelection configuration.

            - **MaxVideoBitsPerSecond** *(integer) --* The maximum video bitrate (bps) to include in
            output.

            - **MinVideoBitsPerSecond** *(integer) --* The minimum video bitrate (bps) to include in
            output.

            - **StreamOrder** *(string) --* A directive that determines the order of streams in the
            output.

        - **Origination** *(string) --* Control whether origination of video is allowed for this
        OriginEndpoint. If set to ALLOW, the OriginEndpoint may by requested, pursuant to any other
        form of access control. If set to DENY, the OriginEndpoint may not be requested. This can be
        helpful for Live to VOD harvesting, or for temporarily disabling origination

        - **StartoverWindowSeconds** *(integer) --* Maximum duration (seconds) of content to retain
        for startover playback. If not specified, startover playback will be disabled for the
        OriginEndpoint.

        - **Tags** *(dict) --* A collection of tags associated with a resource

          - *(string) --*

            - *(string) --*

        - **TimeDelaySeconds** *(integer) --* Amount of delay (seconds) to enforce on the playback
        of live content. If not specified, there will be no time delay in effect for the
        OriginEndpoint.

        - **Url** *(string) --* The URL of the packaged OriginEndpoint for consumption.

        - **Whitelist** *(list) --* A list of source IP CIDR blocks that will be allowed to access
        the OriginEndpoint.

          - *(string) --*
    """
