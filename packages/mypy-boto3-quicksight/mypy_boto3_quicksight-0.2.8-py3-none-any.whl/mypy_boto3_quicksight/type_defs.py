"Main interface for quicksight type defs"
from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientCancelIngestionResponseTypeDef",
    "ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef",
    "ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef",
    "ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef",
    "ClientCreateDashboardDashboardPublishOptionsTypeDef",
    "ClientCreateDashboardParametersDateTimeParametersTypeDef",
    "ClientCreateDashboardParametersDecimalParametersTypeDef",
    "ClientCreateDashboardParametersIntegerParametersTypeDef",
    "ClientCreateDashboardParametersStringParametersTypeDef",
    "ClientCreateDashboardParametersTypeDef",
    "ClientCreateDashboardPermissionsTypeDef",
    "ClientCreateDashboardResponseTypeDef",
    "ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef",
    "ClientCreateDashboardSourceEntitySourceTemplateTypeDef",
    "ClientCreateDashboardSourceEntityTypeDef",
    "ClientCreateDashboardTagsTypeDef",
    "ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    "ClientCreateDataSetColumnGroupsTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    "ClientCreateDataSetLogicalTableMapDataTransformsTypeDef",
    "ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    "ClientCreateDataSetLogicalTableMapSourceTypeDef",
    "ClientCreateDataSetLogicalTableMapTypeDef",
    "ClientCreateDataSetPermissionsTypeDef",
    "ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef",
    "ClientCreateDataSetPhysicalTableMapCustomSqlTypeDef",
    "ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    "ClientCreateDataSetPhysicalTableMapRelationalTableTypeDef",
    "ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef",
    "ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    "ClientCreateDataSetPhysicalTableMapS3SourceTypeDef",
    "ClientCreateDataSetPhysicalTableMapTypeDef",
    "ClientCreateDataSetResponseTypeDef",
    "ClientCreateDataSetRowLevelPermissionDataSetTypeDef",
    "ClientCreateDataSetTagsTypeDef",
    "ClientCreateDataSourceCredentialsCredentialPairTypeDef",
    "ClientCreateDataSourceCredentialsTypeDef",
    "ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    "ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef",
    "ClientCreateDataSourceDataSourceParametersTypeDef",
    "ClientCreateDataSourcePermissionsTypeDef",
    "ClientCreateDataSourceResponseTypeDef",
    "ClientCreateDataSourceSslPropertiesTypeDef",
    "ClientCreateDataSourceTagsTypeDef",
    "ClientCreateDataSourceVpcConnectionPropertiesTypeDef",
    "ClientCreateGroupMembershipResponseGroupMemberTypeDef",
    "ClientCreateGroupMembershipResponseTypeDef",
    "ClientCreateGroupResponseGroupTypeDef",
    "ClientCreateGroupResponseTypeDef",
    "ClientCreateIamPolicyAssignmentResponseTypeDef",
    "ClientCreateIngestionResponseTypeDef",
    "ClientCreateTemplateAliasResponseTemplateAliasTypeDef",
    "ClientCreateTemplateAliasResponseTypeDef",
    "ClientCreateTemplatePermissionsTypeDef",
    "ClientCreateTemplateResponseTypeDef",
    "ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef",
    "ClientCreateTemplateSourceEntitySourceAnalysisTypeDef",
    "ClientCreateTemplateSourceEntitySourceTemplateTypeDef",
    "ClientCreateTemplateSourceEntityTypeDef",
    "ClientCreateTemplateTagsTypeDef",
    "ClientDeleteDashboardResponseTypeDef",
    "ClientDeleteDataSetResponseTypeDef",
    "ClientDeleteDataSourceResponseTypeDef",
    "ClientDeleteGroupMembershipResponseTypeDef",
    "ClientDeleteGroupResponseTypeDef",
    "ClientDeleteIamPolicyAssignmentResponseTypeDef",
    "ClientDeleteTemplateAliasResponseTypeDef",
    "ClientDeleteTemplateResponseTypeDef",
    "ClientDeleteUserByPrincipalIdResponseTypeDef",
    "ClientDeleteUserResponseTypeDef",
    "ClientDescribeDashboardPermissionsResponsePermissionsTypeDef",
    "ClientDescribeDashboardPermissionsResponseTypeDef",
    "ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef",
    "ClientDescribeDashboardResponseDashboardVersionTypeDef",
    "ClientDescribeDashboardResponseDashboardTypeDef",
    "ClientDescribeDashboardResponseTypeDef",
    "ClientDescribeDataSetPermissionsResponsePermissionsTypeDef",
    "ClientDescribeDataSetPermissionsResponseTypeDef",
    "ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    "ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef",
    "ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef",
    "ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef",
    "ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef",
    "ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef",
    "ClientDescribeDataSetResponseDataSetTypeDef",
    "ClientDescribeDataSetResponseTypeDef",
    "ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef",
    "ClientDescribeDataSourcePermissionsResponseTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef",
    "ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef",
    "ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef",
    "ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef",
    "ClientDescribeDataSourceResponseDataSourceTypeDef",
    "ClientDescribeDataSourceResponseTypeDef",
    "ClientDescribeGroupResponseGroupTypeDef",
    "ClientDescribeGroupResponseTypeDef",
    "ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef",
    "ClientDescribeIamPolicyAssignmentResponseTypeDef",
    "ClientDescribeIngestionResponseIngestionErrorInfoTypeDef",
    "ClientDescribeIngestionResponseIngestionQueueInfoTypeDef",
    "ClientDescribeIngestionResponseIngestionRowInfoTypeDef",
    "ClientDescribeIngestionResponseIngestionTypeDef",
    "ClientDescribeIngestionResponseTypeDef",
    "ClientDescribeTemplateAliasResponseTemplateAliasTypeDef",
    "ClientDescribeTemplateAliasResponseTypeDef",
    "ClientDescribeTemplatePermissionsResponsePermissionsTypeDef",
    "ClientDescribeTemplatePermissionsResponseTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef",
    "ClientDescribeTemplateResponseTemplateVersionTypeDef",
    "ClientDescribeTemplateResponseTemplateTypeDef",
    "ClientDescribeTemplateResponseTypeDef",
    "ClientDescribeUserResponseUserTypeDef",
    "ClientDescribeUserResponseTypeDef",
    "ClientGetDashboardEmbedUrlResponseTypeDef",
    "ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef",
    "ClientListDashboardVersionsResponseTypeDef",
    "ClientListDashboardsResponseDashboardSummaryListTypeDef",
    "ClientListDashboardsResponseTypeDef",
    "ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef",
    "ClientListDataSetsResponseDataSetSummariesTypeDef",
    "ClientListDataSetsResponseTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef",
    "ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef",
    "ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef",
    "ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef",
    "ClientListDataSourcesResponseDataSourcesTypeDef",
    "ClientListDataSourcesResponseTypeDef",
    "ClientListGroupMembershipsResponseGroupMemberListTypeDef",
    "ClientListGroupMembershipsResponseTypeDef",
    "ClientListGroupsResponseGroupListTypeDef",
    "ClientListGroupsResponseTypeDef",
    "ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef",
    "ClientListIamPolicyAssignmentsForUserResponseTypeDef",
    "ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef",
    "ClientListIamPolicyAssignmentsResponseTypeDef",
    "ClientListIngestionsResponseIngestionsErrorInfoTypeDef",
    "ClientListIngestionsResponseIngestionsQueueInfoTypeDef",
    "ClientListIngestionsResponseIngestionsRowInfoTypeDef",
    "ClientListIngestionsResponseIngestionsTypeDef",
    "ClientListIngestionsResponseTypeDef",
    "ClientListTagsForResourceResponseTagsTypeDef",
    "ClientListTagsForResourceResponseTypeDef",
    "ClientListTemplateAliasesResponseTemplateAliasListTypeDef",
    "ClientListTemplateAliasesResponseTypeDef",
    "ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef",
    "ClientListTemplateVersionsResponseTypeDef",
    "ClientListTemplatesResponseTemplateSummaryListTypeDef",
    "ClientListTemplatesResponseTypeDef",
    "ClientListUserGroupsResponseGroupListTypeDef",
    "ClientListUserGroupsResponseTypeDef",
    "ClientListUsersResponseUserListTypeDef",
    "ClientListUsersResponseTypeDef",
    "ClientRegisterUserResponseUserTypeDef",
    "ClientRegisterUserResponseTypeDef",
    "ClientTagResourceResponseTypeDef",
    "ClientTagResourceTagsTypeDef",
    "ClientUntagResourceResponseTypeDef",
    "ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef",
    "ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef",
    "ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef",
    "ClientUpdateDashboardDashboardPublishOptionsTypeDef",
    "ClientUpdateDashboardParametersDateTimeParametersTypeDef",
    "ClientUpdateDashboardParametersDecimalParametersTypeDef",
    "ClientUpdateDashboardParametersIntegerParametersTypeDef",
    "ClientUpdateDashboardParametersStringParametersTypeDef",
    "ClientUpdateDashboardParametersTypeDef",
    "ClientUpdateDashboardPermissionsGrantPermissionsTypeDef",
    "ClientUpdateDashboardPermissionsResponsePermissionsTypeDef",
    "ClientUpdateDashboardPermissionsResponseTypeDef",
    "ClientUpdateDashboardPermissionsRevokePermissionsTypeDef",
    "ClientUpdateDashboardPublishedVersionResponseTypeDef",
    "ClientUpdateDashboardResponseTypeDef",
    "ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef",
    "ClientUpdateDashboardSourceEntitySourceTemplateTypeDef",
    "ClientUpdateDashboardSourceEntityTypeDef",
    "ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    "ClientUpdateDataSetColumnGroupsTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    "ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef",
    "ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    "ClientUpdateDataSetLogicalTableMapSourceTypeDef",
    "ClientUpdateDataSetLogicalTableMapTypeDef",
    "ClientUpdateDataSetPermissionsGrantPermissionsTypeDef",
    "ClientUpdateDataSetPermissionsResponseTypeDef",
    "ClientUpdateDataSetPermissionsRevokePermissionsTypeDef",
    "ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef",
    "ClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef",
    "ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    "ClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef",
    "ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef",
    "ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    "ClientUpdateDataSetPhysicalTableMapS3SourceTypeDef",
    "ClientUpdateDataSetPhysicalTableMapTypeDef",
    "ClientUpdateDataSetResponseTypeDef",
    "ClientUpdateDataSetRowLevelPermissionDataSetTypeDef",
    "ClientUpdateDataSourceCredentialsCredentialPairTypeDef",
    "ClientUpdateDataSourceCredentialsTypeDef",
    "ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    "ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef",
    "ClientUpdateDataSourceDataSourceParametersTypeDef",
    "ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef",
    "ClientUpdateDataSourcePermissionsResponseTypeDef",
    "ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef",
    "ClientUpdateDataSourceResponseTypeDef",
    "ClientUpdateDataSourceSslPropertiesTypeDef",
    "ClientUpdateDataSourceVpcConnectionPropertiesTypeDef",
    "ClientUpdateGroupResponseGroupTypeDef",
    "ClientUpdateGroupResponseTypeDef",
    "ClientUpdateIamPolicyAssignmentResponseTypeDef",
    "ClientUpdateTemplateAliasResponseTemplateAliasTypeDef",
    "ClientUpdateTemplateAliasResponseTypeDef",
    "ClientUpdateTemplatePermissionsGrantPermissionsTypeDef",
    "ClientUpdateTemplatePermissionsResponsePermissionsTypeDef",
    "ClientUpdateTemplatePermissionsResponseTypeDef",
    "ClientUpdateTemplatePermissionsRevokePermissionsTypeDef",
    "ClientUpdateTemplateResponseTypeDef",
    "ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef",
    "ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef",
    "ClientUpdateTemplateSourceEntitySourceTemplateTypeDef",
    "ClientUpdateTemplateSourceEntityTypeDef",
    "ClientUpdateUserResponseUserTypeDef",
    "ClientUpdateUserResponseTypeDef",
)


_ClientCancelIngestionResponseTypeDef = TypedDict(
    "_ClientCancelIngestionResponseTypeDef",
    {"Arn": str, "IngestionId": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientCancelIngestionResponseTypeDef(_ClientCancelIngestionResponseTypeDef):
    """
    Type definition for `ClientCancelIngestion` `Response`

    - **Arn** *(string) --*

      The Amazon Resource Name (ARN) for the data ingestion.

    - **IngestionId** *(string) --*

      An ID for the ingestion.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef = TypedDict(
    "_ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef",
    {"AvailabilityStatus": str},
    total=False,
)


class ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef(
    _ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef
):
    """
    Type definition for `ClientCreateDashboardDashboardPublishOptions` `AdHocFilteringOption`

    Ad hoc filtering option.

    - **AvailabilityStatus** *(string) --*

      Availability status.
    """


_ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef = TypedDict(
    "_ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef",
    {"AvailabilityStatus": str},
    total=False,
)


class ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef(
    _ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef
):
    """
    Type definition for `ClientCreateDashboardDashboardPublishOptions` `ExportToCSVOption`

    Export to CSV option.

    - **AvailabilityStatus** *(string) --*

      Availability status.
    """


_ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef = TypedDict(
    "_ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef",
    {"VisibilityState": str},
    total=False,
)


class ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef(
    _ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef
):
    """
    Type definition for `ClientCreateDashboardDashboardPublishOptions` `SheetControlsOption`

    Sheet controls option.

    - **VisibilityState** *(string) --*

      Visibility state.
    """


_ClientCreateDashboardDashboardPublishOptionsTypeDef = TypedDict(
    "_ClientCreateDashboardDashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": ClientCreateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef,
        "ExportToCSVOption": ClientCreateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef,
        "SheetControlsOption": ClientCreateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef,
    },
    total=False,
)


class ClientCreateDashboardDashboardPublishOptionsTypeDef(
    _ClientCreateDashboardDashboardPublishOptionsTypeDef
):
    """
    Type definition for `ClientCreateDashboard` `DashboardPublishOptions`

    Publishing options when creating dashboard.

    * AvailabilityStatus for AdHocFilteringOption - This can be either ``ENABLED`` or ``DISABLED`` .
    When This is set to set to ``DISABLED`` , QuickSight disables the left filter pane on the
    published dashboard, which can be used for AdHoc filtering. Enabled by default.

    * AvailabilityStatus for ExportToCSVOption - This can be either ``ENABLED`` or ``DISABLED`` .
    The visual option to export data to CSV is disabled when this is set to ``DISABLED`` . Enabled
    by default.

    * VisibilityState for SheetControlsOption - This can be either ``COLLAPSED`` or ``EXPANDED`` .
    The sheet controls pane is collapsed by default when set to true. Collapsed by default.

    Shorthand Syntax:

     ``AdHocFilteringDisabled=boolean,ExportToCSVDisabled=boolean,SheetControlsCollapsed=boolean``

    - **AdHocFilteringOption** *(dict) --*

      Ad hoc filtering option.

      - **AvailabilityStatus** *(string) --*

        Availability status.

    - **ExportToCSVOption** *(dict) --*

      Export to CSV option.

      - **AvailabilityStatus** *(string) --*

        Availability status.

    - **SheetControlsOption** *(dict) --*

      Sheet controls option.

      - **VisibilityState** *(string) --*

        Visibility state.
    """


_ClientCreateDashboardParametersDateTimeParametersTypeDef = TypedDict(
    "_ClientCreateDashboardParametersDateTimeParametersTypeDef",
    {"Name": str, "Values": List[datetime]},
)


class ClientCreateDashboardParametersDateTimeParametersTypeDef(
    _ClientCreateDashboardParametersDateTimeParametersTypeDef
):
    """
    Type definition for `ClientCreateDashboardParameters` `DateTimeParameters`

    Date time parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(datetime) --*
    """


_ClientCreateDashboardParametersDecimalParametersTypeDef = TypedDict(
    "_ClientCreateDashboardParametersDecimalParametersTypeDef", {"Name": str, "Values": List[float]}
)


class ClientCreateDashboardParametersDecimalParametersTypeDef(
    _ClientCreateDashboardParametersDecimalParametersTypeDef
):
    """
    Type definition for `ClientCreateDashboardParameters` `DecimalParameters`

    Decimal parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(float) --*
    """


_ClientCreateDashboardParametersIntegerParametersTypeDef = TypedDict(
    "_ClientCreateDashboardParametersIntegerParametersTypeDef", {"Name": str, "Values": List[int]}
)


class ClientCreateDashboardParametersIntegerParametersTypeDef(
    _ClientCreateDashboardParametersIntegerParametersTypeDef
):
    """
    Type definition for `ClientCreateDashboardParameters` `IntegerParameters`

    Integer parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(integer) --*
    """


_ClientCreateDashboardParametersStringParametersTypeDef = TypedDict(
    "_ClientCreateDashboardParametersStringParametersTypeDef", {"Name": str, "Values": List[str]}
)


class ClientCreateDashboardParametersStringParametersTypeDef(
    _ClientCreateDashboardParametersStringParametersTypeDef
):
    """
    Type definition for `ClientCreateDashboardParameters` `StringParameters`

    String parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(string) --*
    """


_ClientCreateDashboardParametersTypeDef = TypedDict(
    "_ClientCreateDashboardParametersTypeDef",
    {
        "StringParameters": List[ClientCreateDashboardParametersStringParametersTypeDef],
        "IntegerParameters": List[ClientCreateDashboardParametersIntegerParametersTypeDef],
        "DecimalParameters": List[ClientCreateDashboardParametersDecimalParametersTypeDef],
        "DateTimeParameters": List[ClientCreateDashboardParametersDateTimeParametersTypeDef],
    },
    total=False,
)


class ClientCreateDashboardParametersTypeDef(_ClientCreateDashboardParametersTypeDef):
    """
    Type definition for `ClientCreateDashboard` `Parameters`

    A structure that contains the parameters of the dashboard. These are parameter overrides for a
    dashboard. A dashboard can have any type of parameters and some parameters might accept multiple
    values. You could use the following structure to override two string parameters that accept
    multiple values:

    - **StringParameters** *(list) --*

      String parameters.

      - *(dict) --*

        String parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(string) --*

    - **IntegerParameters** *(list) --*

      Integer parameters.

      - *(dict) --*

        Integer parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(integer) --*

    - **DecimalParameters** *(list) --*

      Decimal parameters.

      - *(dict) --*

        Decimal parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(float) --*

    - **DateTimeParameters** *(list) --*

      DateTime parameters.

      - *(dict) --*

        Date time parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(datetime) --*
    """


_ClientCreateDashboardPermissionsTypeDef = TypedDict(
    "_ClientCreateDashboardPermissionsTypeDef", {"Principal": str, "Actions": List[str]}
)


class ClientCreateDashboardPermissionsTypeDef(_ClientCreateDashboardPermissionsTypeDef):
    """
    Type definition for `ClientCreateDashboard` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientCreateDashboardResponseTypeDef = TypedDict(
    "_ClientCreateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientCreateDashboardResponseTypeDef(_ClientCreateDashboardResponseTypeDef):
    """
    Type definition for `ClientCreateDashboard` `Response`

    - **Arn** *(string) --*

      The ARN of the dashboard.

    - **VersionArn** *(string) --*

      The ARN of the dashboard, including the version number of the first version that is created.

    - **DashboardId** *(string) --*

      The ID for the dashboard.

    - **CreationStatus** *(string) --*

      The creation status of the dashboard create request.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef = TypedDict(
    "_ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef",
    {"DataSetPlaceholder": str, "DataSetArn": str},
)


class ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef(
    _ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef
):
    """
    Type definition for `ClientCreateDashboardSourceEntitySourceTemplate` `DataSetReferences`

    Dataset reference.

    - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

      Dataset placeholder.

    - **DataSetArn** *(string) --* **[REQUIRED]**

      Dataset ARN.
    """


_ClientCreateDashboardSourceEntitySourceTemplateTypeDef = TypedDict(
    "_ClientCreateDashboardSourceEntitySourceTemplateTypeDef",
    {
        "DataSetReferences": List[
            ClientCreateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef
        ],
        "Arn": str,
    },
)


class ClientCreateDashboardSourceEntitySourceTemplateTypeDef(
    _ClientCreateDashboardSourceEntitySourceTemplateTypeDef
):
    """
    Type definition for `ClientCreateDashboardSourceEntity` `SourceTemplate`

    Source template.

    - **DataSetReferences** *(list) --* **[REQUIRED]**

      Dataset references.

      - *(dict) --*

        Dataset reference.

        - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

          Dataset placeholder.

        - **DataSetArn** *(string) --* **[REQUIRED]**

          Dataset ARN.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.
    """


_ClientCreateDashboardSourceEntityTypeDef = TypedDict(
    "_ClientCreateDashboardSourceEntityTypeDef",
    {"SourceTemplate": ClientCreateDashboardSourceEntitySourceTemplateTypeDef},
    total=False,
)


class ClientCreateDashboardSourceEntityTypeDef(_ClientCreateDashboardSourceEntityTypeDef):
    """
    Type definition for `ClientCreateDashboard` `SourceEntity`

    Source entity from which the dashboard is created. The souce entity accepts the ARN of the
    source template or analysis and also references the replacement datasets for the placeholders
    set when creating the template. The replacement datasets need to follow the same schema as the
    datasets for which placeholders were created when creating the template.

    If you are creating a dashboard from a source entity in a different AWS account, use the ARN of
    the source template.

    - **SourceTemplate** *(dict) --*

      Source template.

      - **DataSetReferences** *(list) --* **[REQUIRED]**

        Dataset references.

        - *(dict) --*

          Dataset reference.

          - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

            Dataset placeholder.

          - **DataSetArn** *(string) --* **[REQUIRED]**

            Dataset ARN.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.
    """


_ClientCreateDashboardTagsTypeDef = TypedDict(
    "_ClientCreateDashboardTagsTypeDef", {"Key": str, "Value": str}
)


class ClientCreateDashboardTagsTypeDef(_ClientCreateDashboardTagsTypeDef):
    """
    Type definition for `ClientCreateDashboard` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --* **[REQUIRED]**

      Tag key.

    - **Value** *(string) --* **[REQUIRED]**

      Tag value.
    """


_ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef = TypedDict(
    "_ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    {"Name": str, "CountryCode": str, "Columns": List[str]},
)


class ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef(
    _ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef
):
    """
    Type definition for `ClientCreateDataSetColumnGroups` `GeoSpatialColumnGroup`

    Geospatial column group that denotes a hierarchy.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the hierarchy.

    - **CountryCode** *(string) --* **[REQUIRED]**

      Country code.

    - **Columns** *(list) --* **[REQUIRED]**

      Columns in this hierarchy.

      - *(string) --*
    """


_ClientCreateDataSetColumnGroupsTypeDef = TypedDict(
    "_ClientCreateDataSetColumnGroupsTypeDef",
    {"GeoSpatialColumnGroup": ClientCreateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef},
    total=False,
)


class ClientCreateDataSetColumnGroupsTypeDef(_ClientCreateDataSetColumnGroupsTypeDef):
    """
    Type definition for `ClientCreateDataSet` `ColumnGroups`

    Groupings of columns that work together in certain QuickSight features. This is a variant type
    structure. No more than one of the attributes should be non-null for this structure to be valid.

    - **GeoSpatialColumnGroup** *(dict) --*

      Geospatial column group that denotes a hierarchy.

      - **Name** *(string) --* **[REQUIRED]**

        A display name for the hierarchy.

      - **CountryCode** *(string) --* **[REQUIRED]**

        Country code.

      - **Columns** *(list) --* **[REQUIRED]**

        Columns in this hierarchy.

        - *(string) --*
    """


_RequiredClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef = TypedDict(
    "_RequiredClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    {"ColumnName": str, "NewColumnType": str},
)
_OptionalClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef = TypedDict(
    "_OptionalClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    {"Format": str},
    total=False,
)


class ClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef(
    _RequiredClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
    _OptionalClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `CastColumnTypeOperation`

    A transform operation that casts a column to a different type.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Column name.

    - **NewColumnType** *(string) --* **[REQUIRED]**

      New column data type.

    - **Format** *(string) --*

      When casting a column from string to datetime type, you can supply a QuickSight supported
      format string to denote the source data format.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    {"ColumnName": str, "ColumnId": str, "Expression": str},
)


class ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperation`
    `Columns`

    A calculated column for a dataset.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Column name.

    - **ColumnId** *(string) --* **[REQUIRED]**

      A unique ID to identify a calculated column. During dataset update, if the column ID of a
      calculated column matches that of an existing calculated column, QuickSight preserves the
      existing calculated column.

    - **Expression** *(string) --* **[REQUIRED]**

      An expression that defines the calculated column.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    {
        "Columns": List[
            ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
        ]
    },
)


class ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `CreateColumnsOperation`

    An operation that creates calculated columns. Columns created in one such operation form a
    lexical closure.

    - **Columns** *(list) --* **[REQUIRED]**

      Calculated columns to create.

      - *(dict) --*

        A calculated column for a dataset.

        - **ColumnName** *(string) --* **[REQUIRED]**

          Column name.

        - **ColumnId** *(string) --* **[REQUIRED]**

          A unique ID to identify a calculated column. During dataset update, if the column ID of a
          calculated column matches that of an existing calculated column, QuickSight preserves the
          existing calculated column.

        - **Expression** *(string) --* **[REQUIRED]**

          An expression that defines the calculated column.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    {"ConditionExpression": str},
)


class ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `FilterOperation`

    An operation that filters rows based on some condition.

    - **ConditionExpression** *(string) --* **[REQUIRED]**

      An expression that must evaluate to a boolean value. Rows for which the expression is
      evaluated to true are kept in the dataset.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    {"ProjectedColumns": List[str]},
)


class ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `ProjectOperation`

    An operation that projects columns. Operations that come after a projection can only refer to
    projected columns.

    - **ProjectedColumns** *(list) --* **[REQUIRED]**

      Projected columns.

      - *(string) --*
    """


_ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    {"ColumnName": str, "NewColumnName": str},
)


class ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `RenameColumnOperation`

    An operation that renames a column.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Name of the column to be renamed.

    - **NewColumnName** *(string) --* **[REQUIRED]**

      New name for the column.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    {"ColumnGeographicRole": str},
    total=False,
)


class ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperation` `Tags`

    A tag for a column in a TagColumnOperation. This is a variant type structure. No more than one
    of the attributes should be non-null for this structure to be valid.

    - **ColumnGeographicRole** *(string) --*

      A geospatial role for a column.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": List[ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef],
    },
)


class ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapDataTransforms` `TagColumnOperation`

    An operation that tags a column with additional information.

    - **ColumnName** *(string) --* **[REQUIRED]**

      The column that this operation acts on.

    - **Tags** *(list) --* **[REQUIRED]**

      The dataset column tag, currently only used for geospatial type tagging. .

      .. note::

        This is not tags for the AWS tagging feature. .

      - *(dict) --*

        A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
        one of the attributes should be non-null for this structure to be valid.

        - **ColumnGeographicRole** *(string) --*

          A geospatial role for a column.
    """


_ClientCreateDataSetLogicalTableMapDataTransformsTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapDataTransformsTypeDef",
    {
        "ProjectOperation": ClientCreateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef,
        "FilterOperation": ClientCreateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef,
        "CreateColumnsOperation": ClientCreateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef,
        "RenameColumnOperation": ClientCreateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef,
        "CastColumnTypeOperation": ClientCreateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
        "TagColumnOperation": ClientCreateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef,
    },
    total=False,
)


class ClientCreateDataSetLogicalTableMapDataTransformsTypeDef(
    _ClientCreateDataSetLogicalTableMapDataTransformsTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMap` `DataTransforms`

    A data transformation on a logical table. This is a variant type structure. No more than one of
    the attributes should be non-null for this structure to be valid.

    - **ProjectOperation** *(dict) --*

      An operation that projects columns. Operations that come after a projection can only refer to
      projected columns.

      - **ProjectedColumns** *(list) --* **[REQUIRED]**

        Projected columns.

        - *(string) --*

    - **FilterOperation** *(dict) --*

      An operation that filters rows based on some condition.

      - **ConditionExpression** *(string) --* **[REQUIRED]**

        An expression that must evaluate to a boolean value. Rows for which the expression is
        evaluated to true are kept in the dataset.

    - **CreateColumnsOperation** *(dict) --*

      An operation that creates calculated columns. Columns created in one such operation form a
      lexical closure.

      - **Columns** *(list) --* **[REQUIRED]**

        Calculated columns to create.

        - *(dict) --*

          A calculated column for a dataset.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Column name.

          - **ColumnId** *(string) --* **[REQUIRED]**

            A unique ID to identify a calculated column. During dataset update, if the column ID of
            a calculated column matches that of an existing calculated column, QuickSight preserves
            the existing calculated column.

          - **Expression** *(string) --* **[REQUIRED]**

            An expression that defines the calculated column.

    - **RenameColumnOperation** *(dict) --*

      An operation that renames a column.

      - **ColumnName** *(string) --* **[REQUIRED]**

        Name of the column to be renamed.

      - **NewColumnName** *(string) --* **[REQUIRED]**

        New name for the column.

    - **CastColumnTypeOperation** *(dict) --*

      A transform operation that casts a column to a different type.

      - **ColumnName** *(string) --* **[REQUIRED]**

        Column name.

      - **NewColumnType** *(string) --* **[REQUIRED]**

        New column data type.

      - **Format** *(string) --*

        When casting a column from string to datetime type, you can supply a QuickSight supported
        format string to denote the source data format.

    - **TagColumnOperation** *(dict) --*

      An operation that tags a column with additional information.

      - **ColumnName** *(string) --* **[REQUIRED]**

        The column that this operation acts on.

      - **Tags** *(list) --* **[REQUIRED]**

        The dataset column tag, currently only used for geospatial type tagging. .

        .. note::

          This is not tags for the AWS tagging feature. .

        - *(dict) --*

          A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
          one of the attributes should be non-null for this structure to be valid.

          - **ColumnGeographicRole** *(string) --*

            A geospatial role for a column.
    """


_ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    {"LeftOperand": str, "RightOperand": str, "Type": str, "OnClause": str},
)


class ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef(
    _ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMapSource` `JoinInstruction`

    Specifies the result of a join of two logical tables.

    - **LeftOperand** *(string) --* **[REQUIRED]**

      Left operand.

    - **RightOperand** *(string) --* **[REQUIRED]**

      Right operand.

    - **Type** *(string) --* **[REQUIRED]**

      Type.

    - **OnClause** *(string) --* **[REQUIRED]**

      On Clause.
    """


_ClientCreateDataSetLogicalTableMapSourceTypeDef = TypedDict(
    "_ClientCreateDataSetLogicalTableMapSourceTypeDef",
    {
        "JoinInstruction": ClientCreateDataSetLogicalTableMapSourceJoinInstructionTypeDef,
        "PhysicalTableId": str,
    },
    total=False,
)


class ClientCreateDataSetLogicalTableMapSourceTypeDef(
    _ClientCreateDataSetLogicalTableMapSourceTypeDef
):
    """
    Type definition for `ClientCreateDataSetLogicalTableMap` `Source`

    Source of this logical table.

    - **JoinInstruction** *(dict) --*

      Specifies the result of a join of two logical tables.

      - **LeftOperand** *(string) --* **[REQUIRED]**

        Left operand.

      - **RightOperand** *(string) --* **[REQUIRED]**

        Right operand.

      - **Type** *(string) --* **[REQUIRED]**

        Type.

      - **OnClause** *(string) --* **[REQUIRED]**

        On Clause.

    - **PhysicalTableId** *(string) --*

      Physical table ID.
    """


_RequiredClientCreateDataSetLogicalTableMapTypeDef = TypedDict(
    "_RequiredClientCreateDataSetLogicalTableMapTypeDef",
    {"Alias": str, "Source": ClientCreateDataSetLogicalTableMapSourceTypeDef},
)
_OptionalClientCreateDataSetLogicalTableMapTypeDef = TypedDict(
    "_OptionalClientCreateDataSetLogicalTableMapTypeDef",
    {"DataTransforms": List[ClientCreateDataSetLogicalTableMapDataTransformsTypeDef]},
    total=False,
)


class ClientCreateDataSetLogicalTableMapTypeDef(
    _RequiredClientCreateDataSetLogicalTableMapTypeDef,
    _OptionalClientCreateDataSetLogicalTableMapTypeDef,
):
    """
    Type definition for `ClientCreateDataSet` `LogicalTableMap`

    A unit that joins and data transformations operate on. A logical table has a source, which can
    be either a physical table or result of a join. When it points to a physical table, a logical
    table acts as a mutable copy of that table through transform operations.

    - **Alias** *(string) --* **[REQUIRED]**

      A display name for the logical table.

    - **DataTransforms** *(list) --*

      Transform operations that act on this logical table.

      - *(dict) --*

        A data transformation on a logical table. This is a variant type structure. No more than one
        of the attributes should be non-null for this structure to be valid.

        - **ProjectOperation** *(dict) --*

          An operation that projects columns. Operations that come after a projection can only refer
          to projected columns.

          - **ProjectedColumns** *(list) --* **[REQUIRED]**

            Projected columns.

            - *(string) --*

        - **FilterOperation** *(dict) --*

          An operation that filters rows based on some condition.

          - **ConditionExpression** *(string) --* **[REQUIRED]**

            An expression that must evaluate to a boolean value. Rows for which the expression is
            evaluated to true are kept in the dataset.

        - **CreateColumnsOperation** *(dict) --*

          An operation that creates calculated columns. Columns created in one such operation form a
          lexical closure.

          - **Columns** *(list) --* **[REQUIRED]**

            Calculated columns to create.

            - *(dict) --*

              A calculated column for a dataset.

              - **ColumnName** *(string) --* **[REQUIRED]**

                Column name.

              - **ColumnId** *(string) --* **[REQUIRED]**

                A unique ID to identify a calculated column. During dataset update, if the column ID
                of a calculated column matches that of an existing calculated column, QuickSight
                preserves the existing calculated column.

              - **Expression** *(string) --* **[REQUIRED]**

                An expression that defines the calculated column.

        - **RenameColumnOperation** *(dict) --*

          An operation that renames a column.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Name of the column to be renamed.

          - **NewColumnName** *(string) --* **[REQUIRED]**

            New name for the column.

        - **CastColumnTypeOperation** *(dict) --*

          A transform operation that casts a column to a different type.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Column name.

          - **NewColumnType** *(string) --* **[REQUIRED]**

            New column data type.

          - **Format** *(string) --*

            When casting a column from string to datetime type, you can supply a QuickSight
            supported format string to denote the source data format.

        - **TagColumnOperation** *(dict) --*

          An operation that tags a column with additional information.

          - **ColumnName** *(string) --* **[REQUIRED]**

            The column that this operation acts on.

          - **Tags** *(list) --* **[REQUIRED]**

            The dataset column tag, currently only used for geospatial type tagging. .

            .. note::

              This is not tags for the AWS tagging feature. .

            - *(dict) --*

              A tag for a column in a TagColumnOperation. This is a variant type structure. No more
              than one of the attributes should be non-null for this structure to be valid.

              - **ColumnGeographicRole** *(string) --*

                A geospatial role for a column.

    - **Source** *(dict) --* **[REQUIRED]**

      Source of this logical table.

      - **JoinInstruction** *(dict) --*

        Specifies the result of a join of two logical tables.

        - **LeftOperand** *(string) --* **[REQUIRED]**

          Left operand.

        - **RightOperand** *(string) --* **[REQUIRED]**

          Right operand.

        - **Type** *(string) --* **[REQUIRED]**

          Type.

        - **OnClause** *(string) --* **[REQUIRED]**

          On Clause.

      - **PhysicalTableId** *(string) --*

        Physical table ID.
    """


_ClientCreateDataSetPermissionsTypeDef = TypedDict(
    "_ClientCreateDataSetPermissionsTypeDef", {"Principal": str, "Actions": List[str]}
)


class ClientCreateDataSetPermissionsTypeDef(_ClientCreateDataSetPermissionsTypeDef):
    """
    Type definition for `ClientCreateDataSet` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef = TypedDict(
    "_ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef", {"Name": str, "Type": str}
)


class ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef(
    _ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMapCustomSql` `Columns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_RequiredClientCreateDataSetPhysicalTableMapCustomSqlTypeDef = TypedDict(
    "_RequiredClientCreateDataSetPhysicalTableMapCustomSqlTypeDef",
    {"DataSourceArn": str, "Name": str, "SqlQuery": str},
)
_OptionalClientCreateDataSetPhysicalTableMapCustomSqlTypeDef = TypedDict(
    "_OptionalClientCreateDataSetPhysicalTableMapCustomSqlTypeDef",
    {"Columns": List[ClientCreateDataSetPhysicalTableMapCustomSqlColumnsTypeDef]},
    total=False,
)


class ClientCreateDataSetPhysicalTableMapCustomSqlTypeDef(
    _RequiredClientCreateDataSetPhysicalTableMapCustomSqlTypeDef,
    _OptionalClientCreateDataSetPhysicalTableMapCustomSqlTypeDef,
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMap` `CustomSql`

    A physical table type built from the results of the custom SQL query.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      The ARN of the data source.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the SQL query result.

    - **SqlQuery** *(string) --* **[REQUIRED]**

      The SQL query.

    - **Columns** *(list) --*

      The column schema from the SQL query result set.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef = TypedDict(
    "_ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    {"Name": str, "Type": str},
)


class ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef(
    _ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMapRelationalTable` `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_RequiredClientCreateDataSetPhysicalTableMapRelationalTableTypeDef = TypedDict(
    "_RequiredClientCreateDataSetPhysicalTableMapRelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "InputColumns": List[ClientCreateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef],
    },
)
_OptionalClientCreateDataSetPhysicalTableMapRelationalTableTypeDef = TypedDict(
    "_OptionalClientCreateDataSetPhysicalTableMapRelationalTableTypeDef",
    {"Schema": str},
    total=False,
)


class ClientCreateDataSetPhysicalTableMapRelationalTableTypeDef(
    _RequiredClientCreateDataSetPhysicalTableMapRelationalTableTypeDef,
    _OptionalClientCreateDataSetPhysicalTableMapRelationalTableTypeDef,
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMap` `RelationalTable`

    A physical table type for relational data sources.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      Data source ARN.

    - **Schema** *(string) --*

      The schema name. Applies to certain relational database engines.

    - **Name** *(string) --* **[REQUIRED]**

      Name of the relational table.

    - **InputColumns** *(list) --* **[REQUIRED]**

      The column schema of the table.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef = TypedDict(
    "_ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef", {"Name": str, "Type": str}
)


class ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef(
    _ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMapS3Source` `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef = TypedDict(
    "_ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    {
        "Format": str,
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": str,
        "Delimiter": str,
    },
    total=False,
)


class ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef(
    _ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMapS3Source` `UploadSettings`

    Information on the S3 source file(s) format.

    - **Format** *(string) --*

      File format.

    - **StartFromRow** *(integer) --*

      A row number to start reading data from.

    - **ContainsHeader** *(boolean) --*

      Whether or not the file(s) has a header row.

    - **TextQualifier** *(string) --*

      Text qualifier.

    - **Delimiter** *(string) --*

      The delimiter between values in the file.
    """


_RequiredClientCreateDataSetPhysicalTableMapS3SourceTypeDef = TypedDict(
    "_RequiredClientCreateDataSetPhysicalTableMapS3SourceTypeDef",
    {
        "DataSourceArn": str,
        "InputColumns": List[ClientCreateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef],
    },
)
_OptionalClientCreateDataSetPhysicalTableMapS3SourceTypeDef = TypedDict(
    "_OptionalClientCreateDataSetPhysicalTableMapS3SourceTypeDef",
    {"UploadSettings": ClientCreateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef},
    total=False,
)


class ClientCreateDataSetPhysicalTableMapS3SourceTypeDef(
    _RequiredClientCreateDataSetPhysicalTableMapS3SourceTypeDef,
    _OptionalClientCreateDataSetPhysicalTableMapS3SourceTypeDef,
):
    """
    Type definition for `ClientCreateDataSetPhysicalTableMap` `S3Source`

    A physical table type for as S3 data source.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      Data source ARN.

    - **UploadSettings** *(dict) --*

      Information on the S3 source file(s) format.

      - **Format** *(string) --*

        File format.

      - **StartFromRow** *(integer) --*

        A row number to start reading data from.

      - **ContainsHeader** *(boolean) --*

        Whether or not the file(s) has a header row.

      - **TextQualifier** *(string) --*

        Text qualifier.

      - **Delimiter** *(string) --*

        The delimiter between values in the file.

    - **InputColumns** *(list) --* **[REQUIRED]**

      A physical table type for as S3 data source.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientCreateDataSetPhysicalTableMapTypeDef = TypedDict(
    "_ClientCreateDataSetPhysicalTableMapTypeDef",
    {
        "RelationalTable": ClientCreateDataSetPhysicalTableMapRelationalTableTypeDef,
        "CustomSql": ClientCreateDataSetPhysicalTableMapCustomSqlTypeDef,
        "S3Source": ClientCreateDataSetPhysicalTableMapS3SourceTypeDef,
    },
    total=False,
)


class ClientCreateDataSetPhysicalTableMapTypeDef(_ClientCreateDataSetPhysicalTableMapTypeDef):
    """
    Type definition for `ClientCreateDataSet` `PhysicalTableMap`

    A view of a data source. Contains information on the shape of the data in the underlying source.
    This is a variant type structure. No more than one of the attributes can be non-null for this
    structure to be valid.

    - **RelationalTable** *(dict) --*

      A physical table type for relational data sources.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        Data source ARN.

      - **Schema** *(string) --*

        The schema name. Applies to certain relational database engines.

      - **Name** *(string) --* **[REQUIRED]**

        Name of the relational table.

      - **InputColumns** *(list) --* **[REQUIRED]**

        The column schema of the table.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.

    - **CustomSql** *(dict) --*

      A physical table type built from the results of the custom SQL query.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        The ARN of the data source.

      - **Name** *(string) --* **[REQUIRED]**

        A display name for the SQL query result.

      - **SqlQuery** *(string) --* **[REQUIRED]**

        The SQL query.

      - **Columns** *(list) --*

        The column schema from the SQL query result set.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.

    - **S3Source** *(dict) --*

      A physical table type for as S3 data source.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        Data source ARN.

      - **UploadSettings** *(dict) --*

        Information on the S3 source file(s) format.

        - **Format** *(string) --*

          File format.

        - **StartFromRow** *(integer) --*

          A row number to start reading data from.

        - **ContainsHeader** *(boolean) --*

          Whether or not the file(s) has a header row.

        - **TextQualifier** *(string) --*

          Text qualifier.

        - **Delimiter** *(string) --*

          The delimiter between values in the file.

      - **InputColumns** *(list) --* **[REQUIRED]**

        A physical table type for as S3 data source.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.
    """


_ClientCreateDataSetResponseTypeDef = TypedDict(
    "_ClientCreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientCreateDataSetResponseTypeDef(_ClientCreateDataSetResponseTypeDef):
    """
    Type definition for `ClientCreateDataSet` `Response`

    - **Arn** *(string) --*

      The ARN of the dataset.

    - **DataSetId** *(string) --*

      The ID for the dataset you want to create. This is unique per region per AWS account.

    - **IngestionArn** *(string) --*

      The Amazon Resource Name (ARN) for the ingestion, which is triggered as a result of dataset
      creation if the import mode is SPICE

    - **IngestionId** *(string) --*

      The ID of the ingestion, which is triggered as a result of dataset creation if the import mode
      is SPICE

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateDataSetRowLevelPermissionDataSetTypeDef = TypedDict(
    "_ClientCreateDataSetRowLevelPermissionDataSetTypeDef", {"Arn": str, "PermissionPolicy": str}
)


class ClientCreateDataSetRowLevelPermissionDataSetTypeDef(
    _ClientCreateDataSetRowLevelPermissionDataSetTypeDef
):
    """
    Type definition for `ClientCreateDataSet` `RowLevelPermissionDataSet`

    Row-level security configuration on the data you want to create.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the permission dataset.

    - **PermissionPolicy** *(string) --* **[REQUIRED]**

      Permission policy.
    """


_ClientCreateDataSetTagsTypeDef = TypedDict(
    "_ClientCreateDataSetTagsTypeDef", {"Key": str, "Value": str}
)


class ClientCreateDataSetTagsTypeDef(_ClientCreateDataSetTagsTypeDef):
    """
    Type definition for `ClientCreateDataSet` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --* **[REQUIRED]**

      Tag key.

    - **Value** *(string) --* **[REQUIRED]**

      Tag value.
    """


_ClientCreateDataSourceCredentialsCredentialPairTypeDef = TypedDict(
    "_ClientCreateDataSourceCredentialsCredentialPairTypeDef", {"Username": str, "Password": str}
)


class ClientCreateDataSourceCredentialsCredentialPairTypeDef(
    _ClientCreateDataSourceCredentialsCredentialPairTypeDef
):
    """
    Type definition for `ClientCreateDataSourceCredentials` `CredentialPair`

    Credential pair.

    - **Username** *(string) --* **[REQUIRED]**

      Username.

    - **Password** *(string) --* **[REQUIRED]**

      Password.
    """


_ClientCreateDataSourceCredentialsTypeDef = TypedDict(
    "_ClientCreateDataSourceCredentialsTypeDef",
    {"CredentialPair": ClientCreateDataSourceCredentialsCredentialPairTypeDef},
    total=False,
)


class ClientCreateDataSourceCredentialsTypeDef(_ClientCreateDataSourceCredentialsTypeDef):
    """
    Type definition for `ClientCreateDataSource` `Credentials`

    The credentials QuickSight uses to connect to your underlying source. Currently only
    username/password based credentials are supported.

    - **CredentialPair** *(dict) --*

      Credential pair.

      - **Username** *(string) --* **[REQUIRED]**

        Username.

      - **Password** *(string) --* **[REQUIRED]**

        Password.
    """


_ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    {"Domain": str},
)


class ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `AmazonElasticsearchParameters`

    Amazon Elasticsearch parameters.

    - **Domain** *(string) --* **[REQUIRED]**

      The Amazon Elasticsearch domain.
    """


_ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef",
    {"WorkGroup": str},
    total=False,
)


class ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `AthenaParameters`

    Athena parameters.

    - **WorkGroup** *(string) --*

      The workgroup that Athena uses.
    """


_ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `AuroraParameters`

    Aurora MySQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `AuroraPostgreSqlParameters`

    Aurora PostgreSQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    {"DataSetName": str},
)


class ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `AwsIotAnalyticsParameters`

    AWS IoT Analytics parameters.

    - **DataSetName** *(string) --* **[REQUIRED]**

      Dataset name.
    """


_ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef", {"SiteBaseUrl": str}
)


class ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `JiraParameters`

    Jira parameters.

    - **SiteBaseUrl** *(string) --* **[REQUIRED]**

      The base URL of the Jira site.
    """


_ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `MariaDbParameters`

    MariaDB parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `MySqlParameters`

    MySQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `PostgreSqlParameters`

    PostgreSQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef",
    {"Host": str, "Port": int, "Catalog": str},
)


class ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `PrestoParameters`

    Presto parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Catalog** *(string) --* **[REQUIRED]**

      Catalog.
    """


_ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef",
    {"InstanceId": str, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `RdsParameters`

    RDS parameters.

    - **InstanceId** *(string) --* **[REQUIRED]**

      Instance ID.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_RequiredClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_RequiredClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    {"Database": str},
)
_OptionalClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_OptionalClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    {"Host": str, "Port": int, "ClusterId": str},
    total=False,
)


class ClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef(
    _RequiredClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef,
    _OptionalClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef,
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `RedshiftParameters`

    Redshift parameters.

    - **Host** *(string) --*

      Host. This can be blank if the ``ClusterId`` is provided.

    - **Port** *(integer) --*

      Port. This can be blank if the ``ClusterId`` is provided.

    - **Database** *(string) --* **[REQUIRED]**

      Database.

    - **ClusterId** *(string) --*

      Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.
    """


_ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    {"Bucket": str, "Key": str},
)


class ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef(
    _ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParametersS3Parameters`
    `ManifestFileLocation`

    Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
    console.

    - **Bucket** *(string) --* **[REQUIRED]**

      Amazon S3 bucket.

    - **Key** *(string) --* **[REQUIRED]**

      Amazon S3 key that identifies an object.
    """


_ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef",
    {
        "ManifestFileLocation": ClientCreateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
    },
)


class ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `S3Parameters`

    S3 parameters.

    - **ManifestFileLocation** *(dict) --* **[REQUIRED]**

      Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
      console.

      - **Bucket** *(string) --* **[REQUIRED]**

        Amazon S3 bucket.

      - **Key** *(string) --* **[REQUIRED]**

        Amazon S3 key that identifies an object.
    """


_ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef", {"SiteBaseUrl": str}
)


class ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `ServiceNowParameters`

    ServiceNow parameters.

    - **SiteBaseUrl** *(string) --* **[REQUIRED]**

      URL of the base site.
    """


_ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    {"Host": str, "Database": str, "Warehouse": str},
)


class ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `SnowflakeParameters`

    Snowflake parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Database** *(string) --* **[REQUIRED]**

      Database.

    - **Warehouse** *(string) --* **[REQUIRED]**

      Warehouse.
    """


_ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef", {"Host": str, "Port": int}
)


class ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `SparkParameters`

    Spark parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.
    """


_ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `SqlServerParameters`

    SQL Server parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `TeradataParameters`

    Teradata parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef",
    {"Query": str, "MaxRows": int},
)


class ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSourceDataSourceParameters` `TwitterParameters`

    Twitter parameters.

    - **Query** *(string) --* **[REQUIRED]**

      Twitter query string.

    - **MaxRows** *(integer) --* **[REQUIRED]**

      Maximum number of rows to query Twitter.
    """


_ClientCreateDataSourceDataSourceParametersTypeDef = TypedDict(
    "_ClientCreateDataSourceDataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": ClientCreateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef,
        "AthenaParameters": ClientCreateDataSourceDataSourceParametersAthenaParametersTypeDef,
        "AuroraParameters": ClientCreateDataSourceDataSourceParametersAuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": ClientCreateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": ClientCreateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef,
        "JiraParameters": ClientCreateDataSourceDataSourceParametersJiraParametersTypeDef,
        "MariaDbParameters": ClientCreateDataSourceDataSourceParametersMariaDbParametersTypeDef,
        "MySqlParameters": ClientCreateDataSourceDataSourceParametersMySqlParametersTypeDef,
        "PostgreSqlParameters": ClientCreateDataSourceDataSourceParametersPostgreSqlParametersTypeDef,
        "PrestoParameters": ClientCreateDataSourceDataSourceParametersPrestoParametersTypeDef,
        "RdsParameters": ClientCreateDataSourceDataSourceParametersRdsParametersTypeDef,
        "RedshiftParameters": ClientCreateDataSourceDataSourceParametersRedshiftParametersTypeDef,
        "S3Parameters": ClientCreateDataSourceDataSourceParametersS3ParametersTypeDef,
        "ServiceNowParameters": ClientCreateDataSourceDataSourceParametersServiceNowParametersTypeDef,
        "SnowflakeParameters": ClientCreateDataSourceDataSourceParametersSnowflakeParametersTypeDef,
        "SparkParameters": ClientCreateDataSourceDataSourceParametersSparkParametersTypeDef,
        "SqlServerParameters": ClientCreateDataSourceDataSourceParametersSqlServerParametersTypeDef,
        "TeradataParameters": ClientCreateDataSourceDataSourceParametersTeradataParametersTypeDef,
        "TwitterParameters": ClientCreateDataSourceDataSourceParametersTwitterParametersTypeDef,
    },
    total=False,
)


class ClientCreateDataSourceDataSourceParametersTypeDef(
    _ClientCreateDataSourceDataSourceParametersTypeDef
):
    """
    Type definition for `ClientCreateDataSource` `DataSourceParameters`

    The parameters QuickSight uses to connect to your underlying source.

    - **AmazonElasticsearchParameters** *(dict) --*

      Amazon Elasticsearch parameters.

      - **Domain** *(string) --* **[REQUIRED]**

        The Amazon Elasticsearch domain.

    - **AthenaParameters** *(dict) --*

      Athena parameters.

      - **WorkGroup** *(string) --*

        The workgroup that Athena uses.

    - **AuroraParameters** *(dict) --*

      Aurora MySQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **AuroraPostgreSqlParameters** *(dict) --*

      Aurora PostgreSQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **AwsIotAnalyticsParameters** *(dict) --*

      AWS IoT Analytics parameters.

      - **DataSetName** *(string) --* **[REQUIRED]**

        Dataset name.

    - **JiraParameters** *(dict) --*

      Jira parameters.

      - **SiteBaseUrl** *(string) --* **[REQUIRED]**

        The base URL of the Jira site.

    - **MariaDbParameters** *(dict) --*

      MariaDB parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **MySqlParameters** *(dict) --*

      MySQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **PostgreSqlParameters** *(dict) --*

      PostgreSQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **PrestoParameters** *(dict) --*

      Presto parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Catalog** *(string) --* **[REQUIRED]**

        Catalog.

    - **RdsParameters** *(dict) --*

      RDS parameters.

      - **InstanceId** *(string) --* **[REQUIRED]**

        Instance ID.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **RedshiftParameters** *(dict) --*

      Redshift parameters.

      - **Host** *(string) --*

        Host. This can be blank if the ``ClusterId`` is provided.

      - **Port** *(integer) --*

        Port. This can be blank if the ``ClusterId`` is provided.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

      - **ClusterId** *(string) --*

        Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

    - **S3Parameters** *(dict) --*

      S3 parameters.

      - **ManifestFileLocation** *(dict) --* **[REQUIRED]**

        Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
        the console.

        - **Bucket** *(string) --* **[REQUIRED]**

          Amazon S3 bucket.

        - **Key** *(string) --* **[REQUIRED]**

          Amazon S3 key that identifies an object.

    - **ServiceNowParameters** *(dict) --*

      ServiceNow parameters.

      - **SiteBaseUrl** *(string) --* **[REQUIRED]**

        URL of the base site.

    - **SnowflakeParameters** *(dict) --*

      Snowflake parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

      - **Warehouse** *(string) --* **[REQUIRED]**

        Warehouse.

    - **SparkParameters** *(dict) --*

      Spark parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

    - **SqlServerParameters** *(dict) --*

      SQL Server parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **TeradataParameters** *(dict) --*

      Teradata parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **TwitterParameters** *(dict) --*

      Twitter parameters.

      - **Query** *(string) --* **[REQUIRED]**

        Twitter query string.

      - **MaxRows** *(integer) --* **[REQUIRED]**

        Maximum number of rows to query Twitter.
    """


_ClientCreateDataSourcePermissionsTypeDef = TypedDict(
    "_ClientCreateDataSourcePermissionsTypeDef", {"Principal": str, "Actions": List[str]}
)


class ClientCreateDataSourcePermissionsTypeDef(_ClientCreateDataSourcePermissionsTypeDef):
    """
    Type definition for `ClientCreateDataSource` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientCreateDataSourceResponseTypeDef = TypedDict(
    "_ClientCreateDataSourceResponseTypeDef",
    {"Arn": str, "DataSourceId": str, "CreationStatus": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientCreateDataSourceResponseTypeDef(_ClientCreateDataSourceResponseTypeDef):
    """
    Type definition for `ClientCreateDataSource` `Response`

    - **Arn** *(string) --*

      The ARN of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **CreationStatus** *(string) --*

      The status of creating the data source.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateDataSourceSslPropertiesTypeDef = TypedDict(
    "_ClientCreateDataSourceSslPropertiesTypeDef", {"DisableSsl": bool}, total=False
)


class ClientCreateDataSourceSslPropertiesTypeDef(_ClientCreateDataSourceSslPropertiesTypeDef):
    """
    Type definition for `ClientCreateDataSource` `SslProperties`

    SSL properties that apply when QuickSight connects to your underlying source.

    - **DisableSsl** *(boolean) --*

      A boolean flag to control whether SSL should be disabled.
    """


_ClientCreateDataSourceTagsTypeDef = TypedDict(
    "_ClientCreateDataSourceTagsTypeDef", {"Key": str, "Value": str}
)


class ClientCreateDataSourceTagsTypeDef(_ClientCreateDataSourceTagsTypeDef):
    """
    Type definition for `ClientCreateDataSource` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --* **[REQUIRED]**

      Tag key.

    - **Value** *(string) --* **[REQUIRED]**

      Tag value.
    """


_ClientCreateDataSourceVpcConnectionPropertiesTypeDef = TypedDict(
    "_ClientCreateDataSourceVpcConnectionPropertiesTypeDef", {"VpcConnectionArn": str}
)


class ClientCreateDataSourceVpcConnectionPropertiesTypeDef(
    _ClientCreateDataSourceVpcConnectionPropertiesTypeDef
):
    """
    Type definition for `ClientCreateDataSource` `VpcConnectionProperties`

    You need to use this parameter only when you want QuickSight to use a VPC connection when
    connecting to your underlying source.

    - **VpcConnectionArn** *(string) --* **[REQUIRED]**

      VPC connection ARN.
    """


_ClientCreateGroupMembershipResponseGroupMemberTypeDef = TypedDict(
    "_ClientCreateGroupMembershipResponseGroupMemberTypeDef",
    {"Arn": str, "MemberName": str},
    total=False,
)


class ClientCreateGroupMembershipResponseGroupMemberTypeDef(
    _ClientCreateGroupMembershipResponseGroupMemberTypeDef
):
    """
    Type definition for `ClientCreateGroupMembershipResponse` `GroupMember`

    The group member.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group member (user).

    - **MemberName** *(string) --*

      The name of the group member (user).
    """


_ClientCreateGroupMembershipResponseTypeDef = TypedDict(
    "_ClientCreateGroupMembershipResponseTypeDef",
    {
        "GroupMember": ClientCreateGroupMembershipResponseGroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientCreateGroupMembershipResponseTypeDef(_ClientCreateGroupMembershipResponseTypeDef):
    """
    Type definition for `ClientCreateGroupMembership` `Response`

    - **GroupMember** *(dict) --*

      The group member.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the group member (user).

      - **MemberName** *(string) --*

        The name of the group member (user).

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateGroupResponseGroupTypeDef = TypedDict(
    "_ClientCreateGroupResponseGroupTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)


class ClientCreateGroupResponseGroupTypeDef(_ClientCreateGroupResponseGroupTypeDef):
    """
    Type definition for `ClientCreateGroupResponse` `Group`

    The name of the group.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group.

    - **GroupName** *(string) --*

      The name of the group.

    - **Description** *(string) --*

      The group description.

    - **PrincipalId** *(string) --*

      The principal ID of the group.
    """


_ClientCreateGroupResponseTypeDef = TypedDict(
    "_ClientCreateGroupResponseTypeDef",
    {"Group": ClientCreateGroupResponseGroupTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientCreateGroupResponseTypeDef(_ClientCreateGroupResponseTypeDef):
    """
    Type definition for `ClientCreateGroup` `Response`

    The response object for this operation.

    - **Group** *(dict) --*

      The name of the group.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the group.

      - **GroupName** *(string) --*

        The name of the group.

      - **Description** *(string) --*

        The group description.

      - **PrincipalId** *(string) --*

        The principal ID of the group.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateIamPolicyAssignmentResponseTypeDef = TypedDict(
    "_ClientCreateIamPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "AssignmentStatus": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientCreateIamPolicyAssignmentResponseTypeDef(
    _ClientCreateIamPolicyAssignmentResponseTypeDef
):
    """
    Type definition for `ClientCreateIamPolicyAssignment` `Response`

    - **AssignmentName** *(string) --*

      The name of the assignment. Must be unique within an AWS account.

    - **AssignmentId** *(string) --*

      An ID for the assignment.

    - **AssignmentStatus** *(string) --*

      The status of an assignment:

      * ENABLED - Anything specified in this assignment is used while creating the data source.

      * DISABLED - This assignment isn't used while creating the data source.

      * DRAFT - Assignment is an unfinished draft and isn't used while creating the data source.

    - **PolicyArn** *(string) --*

      An IAM policy ARN that is applied to the QuickSight users and groups specified in this
      assignment.

    - **Identities** *(dict) --*

      QuickSight users and/or groups that are assigned to the IAM policy.

      - *(string) --*

        - *(list) --*

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateIngestionResponseTypeDef = TypedDict(
    "_ClientCreateIngestionResponseTypeDef",
    {"Arn": str, "IngestionId": str, "IngestionStatus": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientCreateIngestionResponseTypeDef(_ClientCreateIngestionResponseTypeDef):
    """
    Type definition for `ClientCreateIngestion` `Response`

    - **Arn** *(string) --*

      The Amazon Resource Name (ARN) for the data ingestion.

    - **IngestionId** *(string) --*

      An ID for the ingestion.

    - **IngestionStatus** *(string) --*

      The ingestion status.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientCreateTemplateAliasResponseTemplateAliasTypeDef = TypedDict(
    "_ClientCreateTemplateAliasResponseTemplateAliasTypeDef",
    {"AliasName": str, "Arn": str, "TemplateVersionNumber": int},
    total=False,
)


class ClientCreateTemplateAliasResponseTemplateAliasTypeDef(
    _ClientCreateTemplateAliasResponseTemplateAliasTypeDef
):
    """
    Type definition for `ClientCreateTemplateAliasResponse` `TemplateAlias`

    Information on the template alias.

    - **AliasName** *(string) --*

      The display name of the template alias.

    - **Arn** *(string) --*

      The ARN of the template alias.

    - **TemplateVersionNumber** *(integer) --*

      The version number of the template alias.
    """


_ClientCreateTemplateAliasResponseTypeDef = TypedDict(
    "_ClientCreateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": ClientCreateTemplateAliasResponseTemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientCreateTemplateAliasResponseTypeDef(_ClientCreateTemplateAliasResponseTypeDef):
    """
    Type definition for `ClientCreateTemplateAlias` `Response`

    - **TemplateAlias** *(dict) --*

      Information on the template alias.

      - **AliasName** *(string) --*

        The display name of the template alias.

      - **Arn** *(string) --*

        The ARN of the template alias.

      - **TemplateVersionNumber** *(integer) --*

        The version number of the template alias.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientCreateTemplatePermissionsTypeDef = TypedDict(
    "_ClientCreateTemplatePermissionsTypeDef", {"Principal": str, "Actions": List[str]}
)


class ClientCreateTemplatePermissionsTypeDef(_ClientCreateTemplatePermissionsTypeDef):
    """
    Type definition for `ClientCreateTemplate` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientCreateTemplateResponseTypeDef = TypedDict(
    "_ClientCreateTemplateResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "TemplateId": str,
        "CreationStatus": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientCreateTemplateResponseTypeDef(_ClientCreateTemplateResponseTypeDef):
    """
    Type definition for `ClientCreateTemplate` `Response`

    - **Arn** *(string) --*

      The Amazon Resource Name (ARN) for the template.

    - **VersionArn** *(string) --*

      The Amazon Resource Name (ARN) for the template, including the version information of the
      first version.

    - **TemplateId** *(string) --*

      The ID of the template.

    - **CreationStatus** *(string) --*

      The template creation status.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef = TypedDict(
    "_ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef",
    {"DataSetPlaceholder": str, "DataSetArn": str},
)


class ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef(
    _ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef
):
    """
    Type definition for `ClientCreateTemplateSourceEntitySourceAnalysis` `DataSetReferences`

    Dataset reference.

    - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

      Dataset placeholder.

    - **DataSetArn** *(string) --* **[REQUIRED]**

      Dataset ARN.
    """


_ClientCreateTemplateSourceEntitySourceAnalysisTypeDef = TypedDict(
    "_ClientCreateTemplateSourceEntitySourceAnalysisTypeDef",
    {
        "Arn": str,
        "DataSetReferences": List[
            ClientCreateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef
        ],
    },
)


class ClientCreateTemplateSourceEntitySourceAnalysisTypeDef(
    _ClientCreateTemplateSourceEntitySourceAnalysisTypeDef
):
    """
    Type definition for `ClientCreateTemplateSourceEntity` `SourceAnalysis`

    The source analysis, if it is based on an analysis.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.

    - **DataSetReferences** *(list) --* **[REQUIRED]**

      A structure containing information about the dataset references used as placeholders in the
      template.

      - *(dict) --*

        Dataset reference.

        - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

          Dataset placeholder.

        - **DataSetArn** *(string) --* **[REQUIRED]**

          Dataset ARN.
    """


_ClientCreateTemplateSourceEntitySourceTemplateTypeDef = TypedDict(
    "_ClientCreateTemplateSourceEntitySourceTemplateTypeDef", {"Arn": str}
)


class ClientCreateTemplateSourceEntitySourceTemplateTypeDef(
    _ClientCreateTemplateSourceEntitySourceTemplateTypeDef
):
    """
    Type definition for `ClientCreateTemplateSourceEntity` `SourceTemplate`

    The source template, if it is based on an template.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.
    """


_ClientCreateTemplateSourceEntityTypeDef = TypedDict(
    "_ClientCreateTemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": ClientCreateTemplateSourceEntitySourceAnalysisTypeDef,
        "SourceTemplate": ClientCreateTemplateSourceEntitySourceTemplateTypeDef,
    },
    total=False,
)


class ClientCreateTemplateSourceEntityTypeDef(_ClientCreateTemplateSourceEntityTypeDef):
    """
    Type definition for `ClientCreateTemplate` `SourceEntity`

    The ARN of the source entity from which this template is being created. Templates can be
    currently created from an analysis or another template. If the ARN is for an analysis, you must
    include its dataset references.

    - **SourceAnalysis** *(dict) --*

      The source analysis, if it is based on an analysis.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.

      - **DataSetReferences** *(list) --* **[REQUIRED]**

        A structure containing information about the dataset references used as placeholders in the
        template.

        - *(dict) --*

          Dataset reference.

          - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

            Dataset placeholder.

          - **DataSetArn** *(string) --* **[REQUIRED]**

            Dataset ARN.

    - **SourceTemplate** *(dict) --*

      The source template, if it is based on an template.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.
    """


_ClientCreateTemplateTagsTypeDef = TypedDict(
    "_ClientCreateTemplateTagsTypeDef", {"Key": str, "Value": str}
)


class ClientCreateTemplateTagsTypeDef(_ClientCreateTemplateTagsTypeDef):
    """
    Type definition for `ClientCreateTemplate` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --* **[REQUIRED]**

      Tag key.

    - **Value** *(string) --* **[REQUIRED]**

      Tag value.
    """


_ClientDeleteDashboardResponseTypeDef = TypedDict(
    "_ClientDeleteDashboardResponseTypeDef",
    {"Status": int, "Arn": str, "DashboardId": str, "RequestId": str},
    total=False,
)


class ClientDeleteDashboardResponseTypeDef(_ClientDeleteDashboardResponseTypeDef):
    """
    Type definition for `ClientDeleteDashboard` `Response`

    - **Status** *(integer) --*

      The http status of the request.

    - **Arn** *(string) --*

      The ARN of the resource.

    - **DashboardId** *(string) --*

      The ID of the dashboard.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientDeleteDataSetResponseTypeDef = TypedDict(
    "_ClientDeleteDataSetResponseTypeDef",
    {"Arn": str, "DataSetId": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientDeleteDataSetResponseTypeDef(_ClientDeleteDataSetResponseTypeDef):
    """
    Type definition for `ClientDeleteDataSet` `Response`

    - **Arn** *(string) --*

      The ARN of the dataset.

    - **DataSetId** *(string) --*

      The ID for the dataset you want to create. This is unique per region per AWS account.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteDataSourceResponseTypeDef = TypedDict(
    "_ClientDeleteDataSourceResponseTypeDef",
    {"Arn": str, "DataSourceId": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientDeleteDataSourceResponseTypeDef(_ClientDeleteDataSourceResponseTypeDef):
    """
    Type definition for `ClientDeleteDataSource` `Response`

    - **Arn** *(string) --*

      The ARN of the data source you deleted.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteGroupMembershipResponseTypeDef = TypedDict(
    "_ClientDeleteGroupMembershipResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientDeleteGroupMembershipResponseTypeDef(_ClientDeleteGroupMembershipResponseTypeDef):
    """
    Type definition for `ClientDeleteGroupMembership` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteGroupResponseTypeDef = TypedDict(
    "_ClientDeleteGroupResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientDeleteGroupResponseTypeDef(_ClientDeleteGroupResponseTypeDef):
    """
    Type definition for `ClientDeleteGroup` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteIamPolicyAssignmentResponseTypeDef = TypedDict(
    "_ClientDeleteIamPolicyAssignmentResponseTypeDef",
    {"AssignmentName": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientDeleteIamPolicyAssignmentResponseTypeDef(
    _ClientDeleteIamPolicyAssignmentResponseTypeDef
):
    """
    Type definition for `ClientDeleteIamPolicyAssignment` `Response`

    - **AssignmentName** *(string) --*

      The name of the assignment.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteTemplateAliasResponseTypeDef = TypedDict(
    "_ClientDeleteTemplateAliasResponseTypeDef",
    {"Status": int, "TemplateId": str, "AliasName": str, "Arn": str, "RequestId": str},
    total=False,
)


class ClientDeleteTemplateAliasResponseTypeDef(_ClientDeleteTemplateAliasResponseTypeDef):
    """
    Type definition for `ClientDeleteTemplateAlias` `Response`

    - **Status** *(integer) --*

      The http status of the request.

    - **TemplateId** *(string) --*

      An ID for the template.

    - **AliasName** *(string) --*

      The name of the alias.

    - **Arn** *(string) --*

      The ARN of the resource.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientDeleteTemplateResponseTypeDef = TypedDict(
    "_ClientDeleteTemplateResponseTypeDef",
    {"RequestId": str, "Arn": str, "TemplateId": str, "Status": int},
    total=False,
)


class ClientDeleteTemplateResponseTypeDef(_ClientDeleteTemplateResponseTypeDef):
    """
    Type definition for `ClientDeleteTemplate` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Arn** *(string) --*

      The ARN of the resource.

    - **TemplateId** *(string) --*

      An ID for the template.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteUserByPrincipalIdResponseTypeDef = TypedDict(
    "_ClientDeleteUserByPrincipalIdResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientDeleteUserByPrincipalIdResponseTypeDef(_ClientDeleteUserByPrincipalIdResponseTypeDef):
    """
    Type definition for `ClientDeleteUserByPrincipalId` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDeleteUserResponseTypeDef = TypedDict(
    "_ClientDeleteUserResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientDeleteUserResponseTypeDef(_ClientDeleteUserResponseTypeDef):
    """
    Type definition for `ClientDeleteUser` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeDashboardPermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientDescribeDashboardPermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientDescribeDashboardPermissionsResponsePermissionsTypeDef(
    _ClientDescribeDashboardPermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientDescribeDashboardPermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientDescribeDashboardPermissionsResponseTypeDef = TypedDict(
    "_ClientDescribeDashboardPermissionsResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Permissions": List[ClientDescribeDashboardPermissionsResponsePermissionsTypeDef],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientDescribeDashboardPermissionsResponseTypeDef(
    _ClientDescribeDashboardPermissionsResponseTypeDef
):
    """
    Type definition for `ClientDescribeDashboardPermissions` `Response`

    - **DashboardId** *(string) --*

      The ID for the dashboard.

    - **DashboardArn** *(string) --*

      The ARN of the dashboard.

    - **Permissions** *(list) --*

      A structure that contains the permissions of the dashboard.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef = TypedDict(
    "_ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef(
    _ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef
):
    """
    Type definition for `ClientDescribeDashboardResponseDashboardVersion` `Errors`

    Dashboard error.

    - **Type** *(string) --*

      Type.

    - **Message** *(string) --*

      Message.
    """


_ClientDescribeDashboardResponseDashboardVersionTypeDef = TypedDict(
    "_ClientDescribeDashboardResponseDashboardVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[ClientDescribeDashboardResponseDashboardVersionErrorsTypeDef],
        "VersionNumber": int,
        "Status": str,
        "Arn": str,
        "SourceEntityArn": str,
        "Description": str,
    },
    total=False,
)


class ClientDescribeDashboardResponseDashboardVersionTypeDef(
    _ClientDescribeDashboardResponseDashboardVersionTypeDef
):
    """
    Type definition for `ClientDescribeDashboardResponseDashboard` `Version`

    Version.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **Errors** *(list) --*

      Errors.

      - *(dict) --*

        Dashboard error.

        - **Type** *(string) --*

          Type.

        - **Message** *(string) --*

          Message.

    - **VersionNumber** *(integer) --*

      Version number.

    - **Status** *(string) --*

      The http status of the request.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **SourceEntityArn** *(string) --*

      Source entity ARN.

    - **Description** *(string) --*

      Description.
    """


_ClientDescribeDashboardResponseDashboardTypeDef = TypedDict(
    "_ClientDescribeDashboardResponseDashboardTypeDef",
    {
        "DashboardId": str,
        "Arn": str,
        "Name": str,
        "Version": ClientDescribeDashboardResponseDashboardVersionTypeDef,
        "CreatedTime": datetime,
        "LastPublishedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)


class ClientDescribeDashboardResponseDashboardTypeDef(
    _ClientDescribeDashboardResponseDashboardTypeDef
):
    """
    Type definition for `ClientDescribeDashboardResponse` `Dashboard`

    Information about the dashboard.

    - **DashboardId** *(string) --*

      Dashboard ID.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **Name** *(string) --*

      A display name for the dataset.

    - **Version** *(dict) --*

      Version.

      - **CreatedTime** *(datetime) --*

        The time this was created.

      - **Errors** *(list) --*

        Errors.

        - *(dict) --*

          Dashboard error.

          - **Type** *(string) --*

            Type.

          - **Message** *(string) --*

            Message.

      - **VersionNumber** *(integer) --*

        Version number.

      - **Status** *(string) --*

        The http status of the request.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the resource.

      - **SourceEntityArn** *(string) --*

        Source entity ARN.

      - **Description** *(string) --*

        Description.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastPublishedTime** *(datetime) --*

      The last time this was published.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.
    """


_ClientDescribeDashboardResponseTypeDef = TypedDict(
    "_ClientDescribeDashboardResponseTypeDef",
    {"Dashboard": ClientDescribeDashboardResponseDashboardTypeDef, "Status": int, "RequestId": str},
    total=False,
)


class ClientDescribeDashboardResponseTypeDef(_ClientDescribeDashboardResponseTypeDef):
    """
    Type definition for `ClientDescribeDashboard` `Response`

    - **Dashboard** *(dict) --*

      Information about the dashboard.

      - **DashboardId** *(string) --*

        Dashboard ID.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the resource.

      - **Name** *(string) --*

        A display name for the dataset.

      - **Version** *(dict) --*

        Version.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **Errors** *(list) --*

          Errors.

          - *(dict) --*

            Dashboard error.

            - **Type** *(string) --*

              Type.

            - **Message** *(string) --*

              Message.

        - **VersionNumber** *(integer) --*

          Version number.

        - **Status** *(string) --*

          The http status of the request.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the resource.

        - **SourceEntityArn** *(string) --*

          Source entity ARN.

        - **Description** *(string) --*

          Description.

      - **CreatedTime** *(datetime) --*

        The time this was created.

      - **LastPublishedTime** *(datetime) --*

        The last time this was published.

      - **LastUpdatedTime** *(datetime) --*

        The last time this was updated.

    - **Status** *(integer) --*

      The http status of this request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientDescribeDataSetPermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientDescribeDataSetPermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientDescribeDataSetPermissionsResponsePermissionsTypeDef(
    _ClientDescribeDataSetPermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetPermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientDescribeDataSetPermissionsResponseTypeDef = TypedDict(
    "_ClientDescribeDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "Permissions": List[ClientDescribeDataSetPermissionsResponsePermissionsTypeDef],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientDescribeDataSetPermissionsResponseTypeDef(
    _ClientDescribeDataSetPermissionsResponseTypeDef
):
    """
    Type definition for `ClientDescribeDataSetPermissions` `Response`

    - **DataSetArn** *(string) --*

      The ARN of the dataset.

    - **DataSetId** *(string) --*

      The ID for the dataset you want to create. This is unique per region per AWS account.

    - **Permissions** *(list) --*

      A list of resource permissions on the dataset.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    {"Name": str, "CountryCode": str, "Columns": List[str]},
    total=False,
)


class ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef(
    _ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetColumnGroups` `GeoSpatialColumnGroup`

    Geospatial column group that denotes a hierarchy.

    - **Name** *(string) --*

      A display name for the hierarchy.

    - **CountryCode** *(string) --*

      Country code.

    - **Columns** *(list) --*

      Columns in this hierarchy.

      - *(string) --*
    """


_ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef",
    {
        "GeoSpatialColumnGroup": ClientDescribeDataSetResponseDataSetColumnGroupsGeoSpatialColumnGroupTypeDef
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef(
    _ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSet` `ColumnGroups`

    Groupings of columns that work together in certain QuickSight features. This is a variant type
    structure. No more than one of the attributes should be non-null for this structure to be valid.

    - **GeoSpatialColumnGroup** *(dict) --*

      Geospatial column group that denotes a hierarchy.

      - **Name** *(string) --*

        A display name for the hierarchy.

      - **CountryCode** *(string) --*

        Country code.

      - **Columns** *(list) --*

        Columns in this hierarchy.

        - *(string) --*
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    {"ColumnName": str, "NewColumnType": str, "Format": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `CastColumnTypeOperation`

    A transform operation that casts a column to a different type.

    - **ColumnName** *(string) --*

      Column name.

    - **NewColumnType** *(string) --*

      New column data type.

    - **Format** *(string) --*

      When casting a column from string to datetime type, you can supply a QuickSight supported
      format string to denote the source data format.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    {"ColumnName": str, "ColumnId": str, "Expression": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
):
    """
    Type definition for
    `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperation`
    `Columns`

    A calculated column for a dataset.

    - **ColumnName** *(string) --*

      Column name.

    - **ColumnId** *(string) --*

      A unique ID to identify a calculated column. During dataset update, if the column ID of a
      calculated column matches that of an existing calculated column, QuickSight preserves the
      existing calculated column.

    - **Expression** *(string) --*

      An expression that defines the calculated column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    {
        "Columns": List[
            ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
        ]
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `CreateColumnsOperation`

    An operation that creates calculated columns. Columns created in one such operation form a
    lexical closure.

    - **Columns** *(list) --*

      Calculated columns to create.

      - *(dict) --*

        A calculated column for a dataset.

        - **ColumnName** *(string) --*

          Column name.

        - **ColumnId** *(string) --*

          A unique ID to identify a calculated column. During dataset update, if the column ID of a
          calculated column matches that of an existing calculated column, QuickSight preserves the
          existing calculated column.

        - **Expression** *(string) --*

          An expression that defines the calculated column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    {"ConditionExpression": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `FilterOperation`

    An operation that filters rows based on some condition.

    - **ConditionExpression** *(string) --*

      An expression that must evaluate to a boolean value. Rows for which the expression is
      evaluated to true are kept in the dataset.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    {"ProjectedColumns": List[str]},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `ProjectOperation`

    An operation that projects columns. Operations that come after a projection can only refer to
    projected columns.

    - **ProjectedColumns** *(list) --*

      Projected columns.

      - *(string) --*
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    {"ColumnName": str, "NewColumnName": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `RenameColumnOperation`

    An operation that renames a column.

    - **ColumnName** *(string) --*

      Name of the column to be renamed.

    - **NewColumnName** *(string) --*

      New name for the column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    {"ColumnGeographicRole": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef
):
    """
    Type definition for
    `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperation` `Tags`

    A tag for a column in a TagColumnOperation. This is a variant type structure. No more than one
    of the attributes should be non-null for this structure to be valid.

    - **ColumnGeographicRole** *(string) --*

      A geospatial role for a column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": List[
            ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef
        ],
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransforms`
    `TagColumnOperation`

    An operation that tags a column with additional information.

    - **ColumnName** *(string) --*

      The column that this operation acts on.

    - **Tags** *(list) --*

      The dataset column tag, currently only used for geospatial type tagging. .

      .. note::

        This is not tags for the AWS tagging feature. .

      - *(dict) --*

        A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
        one of the attributes should be non-null for this structure to be valid.

        - **ColumnGeographicRole** *(string) --*

          A geospatial role for a column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef",
    {
        "ProjectOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsProjectOperationTypeDef,
        "FilterOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsFilterOperationTypeDef,
        "CreateColumnsOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef,
        "RenameColumnOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef,
        "CastColumnTypeOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
        "TagColumnOperation": ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMap` `DataTransforms`

    A data transformation on a logical table. This is a variant type structure. No more than one of
    the attributes should be non-null for this structure to be valid.

    - **ProjectOperation** *(dict) --*

      An operation that projects columns. Operations that come after a projection can only refer to
      projected columns.

      - **ProjectedColumns** *(list) --*

        Projected columns.

        - *(string) --*

    - **FilterOperation** *(dict) --*

      An operation that filters rows based on some condition.

      - **ConditionExpression** *(string) --*

        An expression that must evaluate to a boolean value. Rows for which the expression is
        evaluated to true are kept in the dataset.

    - **CreateColumnsOperation** *(dict) --*

      An operation that creates calculated columns. Columns created in one such operation form a
      lexical closure.

      - **Columns** *(list) --*

        Calculated columns to create.

        - *(dict) --*

          A calculated column for a dataset.

          - **ColumnName** *(string) --*

            Column name.

          - **ColumnId** *(string) --*

            A unique ID to identify a calculated column. During dataset update, if the column ID of
            a calculated column matches that of an existing calculated column, QuickSight preserves
            the existing calculated column.

          - **Expression** *(string) --*

            An expression that defines the calculated column.

    - **RenameColumnOperation** *(dict) --*

      An operation that renames a column.

      - **ColumnName** *(string) --*

        Name of the column to be renamed.

      - **NewColumnName** *(string) --*

        New name for the column.

    - **CastColumnTypeOperation** *(dict) --*

      A transform operation that casts a column to a different type.

      - **ColumnName** *(string) --*

        Column name.

      - **NewColumnType** *(string) --*

        New column data type.

      - **Format** *(string) --*

        When casting a column from string to datetime type, you can supply a QuickSight supported
        format string to denote the source data format.

    - **TagColumnOperation** *(dict) --*

      An operation that tags a column with additional information.

      - **ColumnName** *(string) --*

        The column that this operation acts on.

      - **Tags** *(list) --*

        The dataset column tag, currently only used for geospatial type tagging. .

        .. note::

          This is not tags for the AWS tagging feature. .

        - *(dict) --*

          A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
          one of the attributes should be non-null for this structure to be valid.

          - **ColumnGeographicRole** *(string) --*

            A geospatial role for a column.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    {"LeftOperand": str, "RightOperand": str, "Type": str, "OnClause": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMapSource`
    `JoinInstruction`

    Specifies the result of a join of two logical tables.

    - **LeftOperand** *(string) --*

      Left operand.

    - **RightOperand** *(string) --*

      Right operand.

    - **Type** *(string) --*

      Type.

    - **OnClause** *(string) --*

      On Clause.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef",
    {
        "JoinInstruction": ClientDescribeDataSetResponseDataSetLogicalTableMapSourceJoinInstructionTypeDef,
        "PhysicalTableId": str,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetLogicalTableMap` `Source`

    Source of this logical table.

    - **JoinInstruction** *(dict) --*

      Specifies the result of a join of two logical tables.

      - **LeftOperand** *(string) --*

        Left operand.

      - **RightOperand** *(string) --*

        Right operand.

      - **Type** *(string) --*

        Type.

      - **OnClause** *(string) --*

        On Clause.

    - **PhysicalTableId** *(string) --*

      Physical table ID.
    """


_ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef",
    {
        "Alias": str,
        "DataTransforms": List[
            ClientDescribeDataSetResponseDataSetLogicalTableMapDataTransformsTypeDef
        ],
        "Source": ClientDescribeDataSetResponseDataSetLogicalTableMapSourceTypeDef,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef(
    _ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSet` `LogicalTableMap`

    A unit that joins and data transformations operate on. A logical table has a source, which can
    be either a physical table or result of a join. When it points to a physical table, a logical
    table acts as a mutable copy of that table through transform operations.

    - **Alias** *(string) --*

      A display name for the logical table.

    - **DataTransforms** *(list) --*

      Transform operations that act on this logical table.

      - *(dict) --*

        A data transformation on a logical table. This is a variant type structure. No more than one
        of the attributes should be non-null for this structure to be valid.

        - **ProjectOperation** *(dict) --*

          An operation that projects columns. Operations that come after a projection can only refer
          to projected columns.

          - **ProjectedColumns** *(list) --*

            Projected columns.

            - *(string) --*

        - **FilterOperation** *(dict) --*

          An operation that filters rows based on some condition.

          - **ConditionExpression** *(string) --*

            An expression that must evaluate to a boolean value. Rows for which the expression is
            evaluated to true are kept in the dataset.

        - **CreateColumnsOperation** *(dict) --*

          An operation that creates calculated columns. Columns created in one such operation form a
          lexical closure.

          - **Columns** *(list) --*

            Calculated columns to create.

            - *(dict) --*

              A calculated column for a dataset.

              - **ColumnName** *(string) --*

                Column name.

              - **ColumnId** *(string) --*

                A unique ID to identify a calculated column. During dataset update, if the column ID
                of a calculated column matches that of an existing calculated column, QuickSight
                preserves the existing calculated column.

              - **Expression** *(string) --*

                An expression that defines the calculated column.

        - **RenameColumnOperation** *(dict) --*

          An operation that renames a column.

          - **ColumnName** *(string) --*

            Name of the column to be renamed.

          - **NewColumnName** *(string) --*

            New name for the column.

        - **CastColumnTypeOperation** *(dict) --*

          A transform operation that casts a column to a different type.

          - **ColumnName** *(string) --*

            Column name.

          - **NewColumnType** *(string) --*

            New column data type.

          - **Format** *(string) --*

            When casting a column from string to datetime type, you can supply a QuickSight
            supported format string to denote the source data format.

        - **TagColumnOperation** *(dict) --*

          An operation that tags a column with additional information.

          - **ColumnName** *(string) --*

            The column that this operation acts on.

          - **Tags** *(list) --*

            The dataset column tag, currently only used for geospatial type tagging. .

            .. note::

              This is not tags for the AWS tagging feature. .

            - *(dict) --*

              A tag for a column in a TagColumnOperation. This is a variant type structure. No more
              than one of the attributes should be non-null for this structure to be valid.

              - **ColumnGeographicRole** *(string) --*

                A geospatial role for a column.

    - **Source** *(dict) --*

      Source of this logical table.

      - **JoinInstruction** *(dict) --*

        Specifies the result of a join of two logical tables.

        - **LeftOperand** *(string) --*

          Left operand.

        - **RightOperand** *(string) --*

          Right operand.

        - **Type** *(string) --*

          Type.

        - **OnClause** *(string) --*

          On Clause.

      - **PhysicalTableId** *(string) --*

        Physical table ID.
    """


_ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef",
    {"Name": str, "Type": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef(
    _ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSet` `OutputColumns`

    Output column.

    - **Name** *(string) --*

      A display name for the dataset.

    - **Type** *(string) --*

      Type.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef",
    {"Name": str, "Type": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSql` `Columns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --*

      The name of this column in the underlying data source.

    - **Type** *(string) --*

      The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "SqlQuery": str,
        "Columns": List[
            ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlColumnsTypeDef
        ],
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMap` `CustomSql`

    A physical table type built from the results of the custom SQL query.

    - **DataSourceArn** *(string) --*

      The ARN of the data source.

    - **Name** *(string) --*

      A display name for the SQL query result.

    - **SqlQuery** *(string) --*

      The SQL query.

    - **Columns** *(list) --*

      The column schema from the SQL query result set.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --*

          The name of this column in the underlying data source.

        - **Type** *(string) --*

          The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    {"Name": str, "Type": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTable`
    `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --*

      The name of this column in the underlying data source.

    - **Type** *(string) --*

      The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Schema": str,
        "Name": str,
        "InputColumns": List[
            ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef
        ],
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMap` `RelationalTable`

    A physical table type for relational data sources.

    - **DataSourceArn** *(string) --*

      Data source ARN.

    - **Schema** *(string) --*

      The schema name. Applies to certain relational database engines.

    - **Name** *(string) --*

      Name of the relational table.

    - **InputColumns** *(list) --*

      The column schema of the table.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --*

          The name of this column in the underlying data source.

        - **Type** *(string) --*

          The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef",
    {"Name": str, "Type": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMapS3Source`
    `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --*

      The name of this column in the underlying data source.

    - **Type** *(string) --*

      The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    {
        "Format": str,
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": str,
        "Delimiter": str,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMapS3Source`
    `UploadSettings`

    Information on the S3 source file(s) format.

    - **Format** *(string) --*

      File format.

    - **StartFromRow** *(integer) --*

      A row number to start reading data from.

    - **ContainsHeader** *(boolean) --*

      Whether or not the file(s) has a header row.

    - **TextQualifier** *(string) --*

      Text qualifier.

    - **Delimiter** *(string) --*

      The delimiter between values in the file.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef",
    {
        "DataSourceArn": str,
        "UploadSettings": ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef,
        "InputColumns": List[
            ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceInputColumnsTypeDef
        ],
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSetPhysicalTableMap` `S3Source`

    A physical table type for as S3 data source.

    - **DataSourceArn** *(string) --*

      Data source ARN.

    - **UploadSettings** *(dict) --*

      Information on the S3 source file(s) format.

      - **Format** *(string) --*

        File format.

      - **StartFromRow** *(integer) --*

        A row number to start reading data from.

      - **ContainsHeader** *(boolean) --*

        Whether or not the file(s) has a header row.

      - **TextQualifier** *(string) --*

        Text qualifier.

      - **Delimiter** *(string) --*

        The delimiter between values in the file.

    - **InputColumns** *(list) --*

      A physical table type for as S3 data source.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --*

          The name of this column in the underlying data source.

        - **Type** *(string) --*

          The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef",
    {
        "RelationalTable": ClientDescribeDataSetResponseDataSetPhysicalTableMapRelationalTableTypeDef,
        "CustomSql": ClientDescribeDataSetResponseDataSetPhysicalTableMapCustomSqlTypeDef,
        "S3Source": ClientDescribeDataSetResponseDataSetPhysicalTableMapS3SourceTypeDef,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef(
    _ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSet` `PhysicalTableMap`

    A view of a data source. Contains information on the shape of the data in the underlying source.
    This is a variant type structure. No more than one of the attributes can be non-null for this
    structure to be valid.

    - **RelationalTable** *(dict) --*

      A physical table type for relational data sources.

      - **DataSourceArn** *(string) --*

        Data source ARN.

      - **Schema** *(string) --*

        The schema name. Applies to certain relational database engines.

      - **Name** *(string) --*

        Name of the relational table.

      - **InputColumns** *(list) --*

        The column schema of the table.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --*

            The name of this column in the underlying data source.

          - **Type** *(string) --*

            The data type of the column.

    - **CustomSql** *(dict) --*

      A physical table type built from the results of the custom SQL query.

      - **DataSourceArn** *(string) --*

        The ARN of the data source.

      - **Name** *(string) --*

        A display name for the SQL query result.

      - **SqlQuery** *(string) --*

        The SQL query.

      - **Columns** *(list) --*

        The column schema from the SQL query result set.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --*

            The name of this column in the underlying data source.

          - **Type** *(string) --*

            The data type of the column.

    - **S3Source** *(dict) --*

      A physical table type for as S3 data source.

      - **DataSourceArn** *(string) --*

        Data source ARN.

      - **UploadSettings** *(dict) --*

        Information on the S3 source file(s) format.

        - **Format** *(string) --*

          File format.

        - **StartFromRow** *(integer) --*

          A row number to start reading data from.

        - **ContainsHeader** *(boolean) --*

          Whether or not the file(s) has a header row.

        - **TextQualifier** *(string) --*

          Text qualifier.

        - **Delimiter** *(string) --*

          The delimiter between values in the file.

      - **InputColumns** *(list) --*

        A physical table type for as S3 data source.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --*

            The name of this column in the underlying data source.

          - **Type** *(string) --*

            The data type of the column.
    """


_ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef",
    {"Arn": str, "PermissionPolicy": str},
    total=False,
)


class ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef(
    _ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef
):
    """
    Type definition for `ClientDescribeDataSetResponseDataSet` `RowLevelPermissionDataSet`

    Row-level security configuration on the dataset.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the permission dataset.

    - **PermissionPolicy** *(string) --*

      Permission policy.
    """


_ClientDescribeDataSetResponseDataSetTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseDataSetTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PhysicalTableMap": Dict[str, ClientDescribeDataSetResponseDataSetPhysicalTableMapTypeDef],
        "LogicalTableMap": Dict[str, ClientDescribeDataSetResponseDataSetLogicalTableMapTypeDef],
        "OutputColumns": List[ClientDescribeDataSetResponseDataSetOutputColumnsTypeDef],
        "ImportMode": str,
        "ConsumedSpiceCapacityInBytes": int,
        "ColumnGroups": List[ClientDescribeDataSetResponseDataSetColumnGroupsTypeDef],
        "RowLevelPermissionDataSet": ClientDescribeDataSetResponseDataSetRowLevelPermissionDataSetTypeDef,
    },
    total=False,
)


class ClientDescribeDataSetResponseDataSetTypeDef(_ClientDescribeDataSetResponseDataSetTypeDef):
    """
    Type definition for `ClientDescribeDataSetResponse` `DataSet`

    Information on the dataset.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **DataSetId** *(string) --*

      The ID of the dataset.

    - **Name** *(string) --*

      A display name for the dataset.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.

    - **PhysicalTableMap** *(dict) --*

      Declares the physical tables that are available in the underlying data sources.

      - *(string) --*

        - *(dict) --*

          A view of a data source. Contains information on the shape of the data in the underlying
          source. This is a variant type structure. No more than one of the attributes can be
          non-null for this structure to be valid.

          - **RelationalTable** *(dict) --*

            A physical table type for relational data sources.

            - **DataSourceArn** *(string) --*

              Data source ARN.

            - **Schema** *(string) --*

              The schema name. Applies to certain relational database engines.

            - **Name** *(string) --*

              Name of the relational table.

            - **InputColumns** *(list) --*

              The column schema of the table.

              - *(dict) --*

                Metadata on a column that is used as the input of a transform operation.

                - **Name** *(string) --*

                  The name of this column in the underlying data source.

                - **Type** *(string) --*

                  The data type of the column.

          - **CustomSql** *(dict) --*

            A physical table type built from the results of the custom SQL query.

            - **DataSourceArn** *(string) --*

              The ARN of the data source.

            - **Name** *(string) --*

              A display name for the SQL query result.

            - **SqlQuery** *(string) --*

              The SQL query.

            - **Columns** *(list) --*

              The column schema from the SQL query result set.

              - *(dict) --*

                Metadata on a column that is used as the input of a transform operation.

                - **Name** *(string) --*

                  The name of this column in the underlying data source.

                - **Type** *(string) --*

                  The data type of the column.

          - **S3Source** *(dict) --*

            A physical table type for as S3 data source.

            - **DataSourceArn** *(string) --*

              Data source ARN.

            - **UploadSettings** *(dict) --*

              Information on the S3 source file(s) format.

              - **Format** *(string) --*

                File format.

              - **StartFromRow** *(integer) --*

                A row number to start reading data from.

              - **ContainsHeader** *(boolean) --*

                Whether or not the file(s) has a header row.

              - **TextQualifier** *(string) --*

                Text qualifier.

              - **Delimiter** *(string) --*

                The delimiter between values in the file.

            - **InputColumns** *(list) --*

              A physical table type for as S3 data source.

              - *(dict) --*

                Metadata on a column that is used as the input of a transform operation.

                - **Name** *(string) --*

                  The name of this column in the underlying data source.

                - **Type** *(string) --*

                  The data type of the column.

    - **LogicalTableMap** *(dict) --*

      Configures the combination and transformation of the data from the physical tables.

      - *(string) --*

        - *(dict) --*

          A unit that joins and data transformations operate on. A logical table has a source, which
          can be either a physical table or result of a join. When it points to a physical table, a
          logical table acts as a mutable copy of that table through transform operations.

          - **Alias** *(string) --*

            A display name for the logical table.

          - **DataTransforms** *(list) --*

            Transform operations that act on this logical table.

            - *(dict) --*

              A data transformation on a logical table. This is a variant type structure. No more
              than one of the attributes should be non-null for this structure to be valid.

              - **ProjectOperation** *(dict) --*

                An operation that projects columns. Operations that come after a projection can only
                refer to projected columns.

                - **ProjectedColumns** *(list) --*

                  Projected columns.

                  - *(string) --*

              - **FilterOperation** *(dict) --*

                An operation that filters rows based on some condition.

                - **ConditionExpression** *(string) --*

                  An expression that must evaluate to a boolean value. Rows for which the expression
                  is evaluated to true are kept in the dataset.

              - **CreateColumnsOperation** *(dict) --*

                An operation that creates calculated columns. Columns created in one such operation
                form a lexical closure.

                - **Columns** *(list) --*

                  Calculated columns to create.

                  - *(dict) --*

                    A calculated column for a dataset.

                    - **ColumnName** *(string) --*

                      Column name.

                    - **ColumnId** *(string) --*

                      A unique ID to identify a calculated column. During dataset update, if the
                      column ID of a calculated column matches that of an existing calculated
                      column, QuickSight preserves the existing calculated column.

                    - **Expression** *(string) --*

                      An expression that defines the calculated column.

              - **RenameColumnOperation** *(dict) --*

                An operation that renames a column.

                - **ColumnName** *(string) --*

                  Name of the column to be renamed.

                - **NewColumnName** *(string) --*

                  New name for the column.

              - **CastColumnTypeOperation** *(dict) --*

                A transform operation that casts a column to a different type.

                - **ColumnName** *(string) --*

                  Column name.

                - **NewColumnType** *(string) --*

                  New column data type.

                - **Format** *(string) --*

                  When casting a column from string to datetime type, you can supply a QuickSight
                  supported format string to denote the source data format.

              - **TagColumnOperation** *(dict) --*

                An operation that tags a column with additional information.

                - **ColumnName** *(string) --*

                  The column that this operation acts on.

                - **Tags** *(list) --*

                  The dataset column tag, currently only used for geospatial type tagging. .

                  .. note::

                    This is not tags for the AWS tagging feature. .

                  - *(dict) --*

                    A tag for a column in a TagColumnOperation. This is a variant type structure. No
                    more than one of the attributes should be non-null for this structure to be
                    valid.

                    - **ColumnGeographicRole** *(string) --*

                      A geospatial role for a column.

          - **Source** *(dict) --*

            Source of this logical table.

            - **JoinInstruction** *(dict) --*

              Specifies the result of a join of two logical tables.

              - **LeftOperand** *(string) --*

                Left operand.

              - **RightOperand** *(string) --*

                Right operand.

              - **Type** *(string) --*

                Type.

              - **OnClause** *(string) --*

                On Clause.

            - **PhysicalTableId** *(string) --*

              Physical table ID.

    - **OutputColumns** *(list) --*

      The list of columns after all transforms. These columns are available in templates, analyses,
      and dashboards.

      - *(dict) --*

        Output column.

        - **Name** *(string) --*

          A display name for the dataset.

        - **Type** *(string) --*

          Type.

    - **ImportMode** *(string) --*

      Indicates whether or not you want to import the data into SPICE.

    - **ConsumedSpiceCapacityInBytes** *(integer) --*

      The amount of SPICE capacity used by this dataset. This is 0 if the dataset isn't imported
      into SPICE.

    - **ColumnGroups** *(list) --*

      Groupings of columns that work together in certain QuickSight features. Currently only
      geospatial hierarchy is supported.

      - *(dict) --*

        Groupings of columns that work together in certain QuickSight features. This is a variant
        type structure. No more than one of the attributes should be non-null for this structure to
        be valid.

        - **GeoSpatialColumnGroup** *(dict) --*

          Geospatial column group that denotes a hierarchy.

          - **Name** *(string) --*

            A display name for the hierarchy.

          - **CountryCode** *(string) --*

            Country code.

          - **Columns** *(list) --*

            Columns in this hierarchy.

            - *(string) --*

    - **RowLevelPermissionDataSet** *(dict) --*

      Row-level security configuration on the dataset.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the permission dataset.

      - **PermissionPolicy** *(string) --*

        Permission policy.
    """


_ClientDescribeDataSetResponseTypeDef = TypedDict(
    "_ClientDescribeDataSetResponseTypeDef",
    {"DataSet": ClientDescribeDataSetResponseDataSetTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientDescribeDataSetResponseTypeDef(_ClientDescribeDataSetResponseTypeDef):
    """
    Type definition for `ClientDescribeDataSet` `Response`

    - **DataSet** *(dict) --*

      Information on the dataset.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the resource.

      - **DataSetId** *(string) --*

        The ID of the dataset.

      - **Name** *(string) --*

        A display name for the dataset.

      - **CreatedTime** *(datetime) --*

        The time this was created.

      - **LastUpdatedTime** *(datetime) --*

        The last time this was updated.

      - **PhysicalTableMap** *(dict) --*

        Declares the physical tables that are available in the underlying data sources.

        - *(string) --*

          - *(dict) --*

            A view of a data source. Contains information on the shape of the data in the underlying
            source. This is a variant type structure. No more than one of the attributes can be
            non-null for this structure to be valid.

            - **RelationalTable** *(dict) --*

              A physical table type for relational data sources.

              - **DataSourceArn** *(string) --*

                Data source ARN.

              - **Schema** *(string) --*

                The schema name. Applies to certain relational database engines.

              - **Name** *(string) --*

                Name of the relational table.

              - **InputColumns** *(list) --*

                The column schema of the table.

                - *(dict) --*

                  Metadata on a column that is used as the input of a transform operation.

                  - **Name** *(string) --*

                    The name of this column in the underlying data source.

                  - **Type** *(string) --*

                    The data type of the column.

            - **CustomSql** *(dict) --*

              A physical table type built from the results of the custom SQL query.

              - **DataSourceArn** *(string) --*

                The ARN of the data source.

              - **Name** *(string) --*

                A display name for the SQL query result.

              - **SqlQuery** *(string) --*

                The SQL query.

              - **Columns** *(list) --*

                The column schema from the SQL query result set.

                - *(dict) --*

                  Metadata on a column that is used as the input of a transform operation.

                  - **Name** *(string) --*

                    The name of this column in the underlying data source.

                  - **Type** *(string) --*

                    The data type of the column.

            - **S3Source** *(dict) --*

              A physical table type for as S3 data source.

              - **DataSourceArn** *(string) --*

                Data source ARN.

              - **UploadSettings** *(dict) --*

                Information on the S3 source file(s) format.

                - **Format** *(string) --*

                  File format.

                - **StartFromRow** *(integer) --*

                  A row number to start reading data from.

                - **ContainsHeader** *(boolean) --*

                  Whether or not the file(s) has a header row.

                - **TextQualifier** *(string) --*

                  Text qualifier.

                - **Delimiter** *(string) --*

                  The delimiter between values in the file.

              - **InputColumns** *(list) --*

                A physical table type for as S3 data source.

                - *(dict) --*

                  Metadata on a column that is used as the input of a transform operation.

                  - **Name** *(string) --*

                    The name of this column in the underlying data source.

                  - **Type** *(string) --*

                    The data type of the column.

      - **LogicalTableMap** *(dict) --*

        Configures the combination and transformation of the data from the physical tables.

        - *(string) --*

          - *(dict) --*

            A unit that joins and data transformations operate on. A logical table has a source,
            which can be either a physical table or result of a join. When it points to a physical
            table, a logical table acts as a mutable copy of that table through transform
            operations.

            - **Alias** *(string) --*

              A display name for the logical table.

            - **DataTransforms** *(list) --*

              Transform operations that act on this logical table.

              - *(dict) --*

                A data transformation on a logical table. This is a variant type structure. No more
                than one of the attributes should be non-null for this structure to be valid.

                - **ProjectOperation** *(dict) --*

                  An operation that projects columns. Operations that come after a projection can
                  only refer to projected columns.

                  - **ProjectedColumns** *(list) --*

                    Projected columns.

                    - *(string) --*

                - **FilterOperation** *(dict) --*

                  An operation that filters rows based on some condition.

                  - **ConditionExpression** *(string) --*

                    An expression that must evaluate to a boolean value. Rows for which the
                    expression is evaluated to true are kept in the dataset.

                - **CreateColumnsOperation** *(dict) --*

                  An operation that creates calculated columns. Columns created in one such
                  operation form a lexical closure.

                  - **Columns** *(list) --*

                    Calculated columns to create.

                    - *(dict) --*

                      A calculated column for a dataset.

                      - **ColumnName** *(string) --*

                        Column name.

                      - **ColumnId** *(string) --*

                        A unique ID to identify a calculated column. During dataset update, if the
                        column ID of a calculated column matches that of an existing calculated
                        column, QuickSight preserves the existing calculated column.

                      - **Expression** *(string) --*

                        An expression that defines the calculated column.

                - **RenameColumnOperation** *(dict) --*

                  An operation that renames a column.

                  - **ColumnName** *(string) --*

                    Name of the column to be renamed.

                  - **NewColumnName** *(string) --*

                    New name for the column.

                - **CastColumnTypeOperation** *(dict) --*

                  A transform operation that casts a column to a different type.

                  - **ColumnName** *(string) --*

                    Column name.

                  - **NewColumnType** *(string) --*

                    New column data type.

                  - **Format** *(string) --*

                    When casting a column from string to datetime type, you can supply a QuickSight
                    supported format string to denote the source data format.

                - **TagColumnOperation** *(dict) --*

                  An operation that tags a column with additional information.

                  - **ColumnName** *(string) --*

                    The column that this operation acts on.

                  - **Tags** *(list) --*

                    The dataset column tag, currently only used for geospatial type tagging. .

                    .. note::

                      This is not tags for the AWS tagging feature. .

                    - *(dict) --*

                      A tag for a column in a TagColumnOperation. This is a variant type structure.
                      No more than one of the attributes should be non-null for this structure to be
                      valid.

                      - **ColumnGeographicRole** *(string) --*

                        A geospatial role for a column.

            - **Source** *(dict) --*

              Source of this logical table.

              - **JoinInstruction** *(dict) --*

                Specifies the result of a join of two logical tables.

                - **LeftOperand** *(string) --*

                  Left operand.

                - **RightOperand** *(string) --*

                  Right operand.

                - **Type** *(string) --*

                  Type.

                - **OnClause** *(string) --*

                  On Clause.

              - **PhysicalTableId** *(string) --*

                Physical table ID.

      - **OutputColumns** *(list) --*

        The list of columns after all transforms. These columns are available in templates,
        analyses, and dashboards.

        - *(dict) --*

          Output column.

          - **Name** *(string) --*

            A display name for the dataset.

          - **Type** *(string) --*

            Type.

      - **ImportMode** *(string) --*

        Indicates whether or not you want to import the data into SPICE.

      - **ConsumedSpiceCapacityInBytes** *(integer) --*

        The amount of SPICE capacity used by this dataset. This is 0 if the dataset isn't imported
        into SPICE.

      - **ColumnGroups** *(list) --*

        Groupings of columns that work together in certain QuickSight features. Currently only
        geospatial hierarchy is supported.

        - *(dict) --*

          Groupings of columns that work together in certain QuickSight features. This is a variant
          type structure. No more than one of the attributes should be non-null for this structure
          to be valid.

          - **GeoSpatialColumnGroup** *(dict) --*

            Geospatial column group that denotes a hierarchy.

            - **Name** *(string) --*

              A display name for the hierarchy.

            - **CountryCode** *(string) --*

              Country code.

            - **Columns** *(list) --*

              Columns in this hierarchy.

              - *(string) --*

      - **RowLevelPermissionDataSet** *(dict) --*

        Row-level security configuration on the dataset.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the permission dataset.

        - **PermissionPolicy** *(string) --*

          Permission policy.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef(
    _ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientDescribeDataSourcePermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientDescribeDataSourcePermissionsResponseTypeDef = TypedDict(
    "_ClientDescribeDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "Permissions": List[ClientDescribeDataSourcePermissionsResponsePermissionsTypeDef],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientDescribeDataSourcePermissionsResponseTypeDef(
    _ClientDescribeDataSourcePermissionsResponseTypeDef
):
    """
    Type definition for `ClientDescribeDataSourcePermissions` `Response`

    - **DataSourceArn** *(string) --*

      The ARN of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **Permissions** *(list) --*

      A list of resource permissions on the data source.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    {"Domain": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `AmazonElasticsearchParameters`

    Amazon Elasticsearch parameters.

    - **Domain** *(string) --*

      The Amazon Elasticsearch domain.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef",
    {"WorkGroup": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `AthenaParameters`

    Athena parameters.

    - **WorkGroup** *(string) --*

      The workgroup that Athena uses.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `AuroraParameters`

    Aurora MySQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `AuroraPostgreSqlParameters`

    Aurora PostgreSQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    {"DataSetName": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `AwsIotAnalyticsParameters`

    AWS IoT Analytics parameters.

    - **DataSetName** *(string) --*

      Dataset name.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef",
    {"SiteBaseUrl": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `JiraParameters`

    Jira parameters.

    - **SiteBaseUrl** *(string) --*

      The base URL of the Jira site.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `MariaDbParameters`

    MariaDB parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `MySqlParameters`

    MySQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `PostgreSqlParameters`

    PostgreSQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef",
    {"Host": str, "Port": int, "Catalog": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `PrestoParameters`

    Presto parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Catalog** *(string) --*

      Catalog.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef",
    {"InstanceId": str, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `RdsParameters`

    RDS parameters.

    - **InstanceId** *(string) --*

      Instance ID.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef",
    {"Host": str, "Port": int, "Database": str, "ClusterId": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `RedshiftParameters`

    Redshift parameters.

    - **Host** *(string) --*

      Host. This can be blank if the ``ClusterId`` is provided.

    - **Port** *(integer) --*

      Port. This can be blank if the ``ClusterId`` is provided.

    - **Database** *(string) --*

      Database.

    - **ClusterId** *(string) --*

      Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    {"Bucket": str, "Key": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3Parameters`
    `ManifestFileLocation`

    Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
    console.

    - **Bucket** *(string) --*

      Amazon S3 bucket.

    - **Key** *(string) --*

      Amazon S3 key that identifies an object.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef",
    {
        "ManifestFileLocation": ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
    },
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `S3Parameters`

    S3 parameters.

    - **ManifestFileLocation** *(dict) --*

      Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
      console.

      - **Bucket** *(string) --*

        Amazon S3 bucket.

      - **Key** *(string) --*

        Amazon S3 key that identifies an object.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef",
    {"SiteBaseUrl": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `ServiceNowParameters`

    ServiceNow parameters.

    - **SiteBaseUrl** *(string) --*

      URL of the base site.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    {"Host": str, "Database": str, "Warehouse": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `SnowflakeParameters`

    Snowflake parameters.

    - **Host** *(string) --*

      Host.

    - **Database** *(string) --*

      Database.

    - **Warehouse** *(string) --*

      Warehouse.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef",
    {"Host": str, "Port": int},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `SparkParameters`

    Spark parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `SqlServerParameters`

    SQL Server parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `TeradataParameters`

    Teradata parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef",
    {"Query": str, "MaxRows": int},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSourceDataSourceParameters`
    `TwitterParameters`

    Twitter parameters.

    - **Query** *(string) --*

      Twitter query string.

    - **MaxRows** *(integer) --*

      Maximum number of rows to query Twitter.
    """


_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef,
        "AthenaParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersAthenaParametersTypeDef,
        "AuroraParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef,
        "JiraParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersJiraParametersTypeDef,
        "MariaDbParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersMariaDbParametersTypeDef,
        "MySqlParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersMySqlParametersTypeDef,
        "PostgreSqlParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersPostgreSqlParametersTypeDef,
        "PrestoParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersPrestoParametersTypeDef,
        "RdsParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersRdsParametersTypeDef,
        "RedshiftParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersRedshiftParametersTypeDef,
        "S3Parameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersS3ParametersTypeDef,
        "ServiceNowParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersServiceNowParametersTypeDef,
        "SnowflakeParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersSnowflakeParametersTypeDef,
        "SparkParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersSparkParametersTypeDef,
        "SqlServerParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersSqlServerParametersTypeDef,
        "TeradataParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersTeradataParametersTypeDef,
        "TwitterParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersTwitterParametersTypeDef,
    },
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef(
    _ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSource` `DataSourceParameters`

    The parameters QuickSight uses to connect to your underlying source. This is a variant type
    structure. At most one of the attributes should be non-null for this structure to be valid.

    - **AmazonElasticsearchParameters** *(dict) --*

      Amazon Elasticsearch parameters.

      - **Domain** *(string) --*

        The Amazon Elasticsearch domain.

    - **AthenaParameters** *(dict) --*

      Athena parameters.

      - **WorkGroup** *(string) --*

        The workgroup that Athena uses.

    - **AuroraParameters** *(dict) --*

      Aurora MySQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **AuroraPostgreSqlParameters** *(dict) --*

      Aurora PostgreSQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **AwsIotAnalyticsParameters** *(dict) --*

      AWS IoT Analytics parameters.

      - **DataSetName** *(string) --*

        Dataset name.

    - **JiraParameters** *(dict) --*

      Jira parameters.

      - **SiteBaseUrl** *(string) --*

        The base URL of the Jira site.

    - **MariaDbParameters** *(dict) --*

      MariaDB parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **MySqlParameters** *(dict) --*

      MySQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **PostgreSqlParameters** *(dict) --*

      PostgreSQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **PrestoParameters** *(dict) --*

      Presto parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Catalog** *(string) --*

        Catalog.

    - **RdsParameters** *(dict) --*

      RDS parameters.

      - **InstanceId** *(string) --*

        Instance ID.

      - **Database** *(string) --*

        Database.

    - **RedshiftParameters** *(dict) --*

      Redshift parameters.

      - **Host** *(string) --*

        Host. This can be blank if the ``ClusterId`` is provided.

      - **Port** *(integer) --*

        Port. This can be blank if the ``ClusterId`` is provided.

      - **Database** *(string) --*

        Database.

      - **ClusterId** *(string) --*

        Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

    - **S3Parameters** *(dict) --*

      S3 parameters.

      - **ManifestFileLocation** *(dict) --*

        Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
        the console.

        - **Bucket** *(string) --*

          Amazon S3 bucket.

        - **Key** *(string) --*

          Amazon S3 key that identifies an object.

    - **ServiceNowParameters** *(dict) --*

      ServiceNow parameters.

      - **SiteBaseUrl** *(string) --*

        URL of the base site.

    - **SnowflakeParameters** *(dict) --*

      Snowflake parameters.

      - **Host** *(string) --*

        Host.

      - **Database** *(string) --*

        Database.

      - **Warehouse** *(string) --*

        Warehouse.

    - **SparkParameters** *(dict) --*

      Spark parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

    - **SqlServerParameters** *(dict) --*

      SQL Server parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **TeradataParameters** *(dict) --*

      Teradata parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **TwitterParameters** *(dict) --*

      Twitter parameters.

      - **Query** *(string) --*

        Twitter query string.

      - **MaxRows** *(integer) --*

        Maximum number of rows to query Twitter.
    """


_ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef(
    _ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSource` `ErrorInfo`

    Error information from the last update or the creation of the data source.

    - **Type** *(string) --*

      Error type.

    - **Message** *(string) --*

      Error message.
    """


_ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef",
    {"DisableSsl": bool},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef(
    _ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSource` `SslProperties`

    SSL properties that apply when QuickSight connects to your underlying source.

    - **DisableSsl** *(boolean) --*

      A boolean flag to control whether SSL should be disabled.
    """


_ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef",
    {"VpcConnectionArn": str},
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef(
    _ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponseDataSource` `VpcConnectionProperties`

    The VPC connection information. You need to use this parameter only when you want QuickSight to
    use a VPC connection when connecting to your underlying source.

    - **VpcConnectionArn** *(string) --*

      VPC connection ARN.
    """


_ClientDescribeDataSourceResponseDataSourceTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseDataSourceTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": str,
        "Status": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "DataSourceParameters": ClientDescribeDataSourceResponseDataSourceDataSourceParametersTypeDef,
        "VpcConnectionProperties": ClientDescribeDataSourceResponseDataSourceVpcConnectionPropertiesTypeDef,
        "SslProperties": ClientDescribeDataSourceResponseDataSourceSslPropertiesTypeDef,
        "ErrorInfo": ClientDescribeDataSourceResponseDataSourceErrorInfoTypeDef,
    },
    total=False,
)


class ClientDescribeDataSourceResponseDataSourceTypeDef(
    _ClientDescribeDataSourceResponseDataSourceTypeDef
):
    """
    Type definition for `ClientDescribeDataSourceResponse` `DataSource`

    The information on the data source.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **Name** *(string) --*

      A display name for the data source.

    - **Type** *(string) --*

      The type of the data source. This indicates which database engine the data source connects to.

    - **Status** *(string) --*

      The http status of the request.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.

    - **DataSourceParameters** *(dict) --*

      The parameters QuickSight uses to connect to your underlying source. This is a variant type
      structure. At most one of the attributes should be non-null for this structure to be valid.

      - **AmazonElasticsearchParameters** *(dict) --*

        Amazon Elasticsearch parameters.

        - **Domain** *(string) --*

          The Amazon Elasticsearch domain.

      - **AthenaParameters** *(dict) --*

        Athena parameters.

        - **WorkGroup** *(string) --*

          The workgroup that Athena uses.

      - **AuroraParameters** *(dict) --*

        Aurora MySQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **AuroraPostgreSqlParameters** *(dict) --*

        Aurora PostgreSQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **AwsIotAnalyticsParameters** *(dict) --*

        AWS IoT Analytics parameters.

        - **DataSetName** *(string) --*

          Dataset name.

      - **JiraParameters** *(dict) --*

        Jira parameters.

        - **SiteBaseUrl** *(string) --*

          The base URL of the Jira site.

      - **MariaDbParameters** *(dict) --*

        MariaDB parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **MySqlParameters** *(dict) --*

        MySQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **PostgreSqlParameters** *(dict) --*

        PostgreSQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **PrestoParameters** *(dict) --*

        Presto parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Catalog** *(string) --*

          Catalog.

      - **RdsParameters** *(dict) --*

        RDS parameters.

        - **InstanceId** *(string) --*

          Instance ID.

        - **Database** *(string) --*

          Database.

      - **RedshiftParameters** *(dict) --*

        Redshift parameters.

        - **Host** *(string) --*

          Host. This can be blank if the ``ClusterId`` is provided.

        - **Port** *(integer) --*

          Port. This can be blank if the ``ClusterId`` is provided.

        - **Database** *(string) --*

          Database.

        - **ClusterId** *(string) --*

          Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

      - **S3Parameters** *(dict) --*

        S3 parameters.

        - **ManifestFileLocation** *(dict) --*

          Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
          the console.

          - **Bucket** *(string) --*

            Amazon S3 bucket.

          - **Key** *(string) --*

            Amazon S3 key that identifies an object.

      - **ServiceNowParameters** *(dict) --*

        ServiceNow parameters.

        - **SiteBaseUrl** *(string) --*

          URL of the base site.

      - **SnowflakeParameters** *(dict) --*

        Snowflake parameters.

        - **Host** *(string) --*

          Host.

        - **Database** *(string) --*

          Database.

        - **Warehouse** *(string) --*

          Warehouse.

      - **SparkParameters** *(dict) --*

        Spark parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

      - **SqlServerParameters** *(dict) --*

        SQL Server parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **TeradataParameters** *(dict) --*

        Teradata parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **TwitterParameters** *(dict) --*

        Twitter parameters.

        - **Query** *(string) --*

          Twitter query string.

        - **MaxRows** *(integer) --*

          Maximum number of rows to query Twitter.

    - **VpcConnectionProperties** *(dict) --*

      The VPC connection information. You need to use this parameter only when you want QuickSight
      to use a VPC connection when connecting to your underlying source.

      - **VpcConnectionArn** *(string) --*

        VPC connection ARN.

    - **SslProperties** *(dict) --*

      SSL properties that apply when QuickSight connects to your underlying source.

      - **DisableSsl** *(boolean) --*

        A boolean flag to control whether SSL should be disabled.

    - **ErrorInfo** *(dict) --*

      Error information from the last update or the creation of the data source.

      - **Type** *(string) --*

        Error type.

      - **Message** *(string) --*

        Error message.
    """


_ClientDescribeDataSourceResponseTypeDef = TypedDict(
    "_ClientDescribeDataSourceResponseTypeDef",
    {
        "DataSource": ClientDescribeDataSourceResponseDataSourceTypeDef,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientDescribeDataSourceResponseTypeDef(_ClientDescribeDataSourceResponseTypeDef):
    """
    Type definition for `ClientDescribeDataSource` `Response`

    - **DataSource** *(dict) --*

      The information on the data source.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the data source.

      - **DataSourceId** *(string) --*

        The ID of the data source. This is unique per AWS Region per AWS account.

      - **Name** *(string) --*

        A display name for the data source.

      - **Type** *(string) --*

        The type of the data source. This indicates which database engine the data source connects
        to.

      - **Status** *(string) --*

        The http status of the request.

      - **CreatedTime** *(datetime) --*

        The time this was created.

      - **LastUpdatedTime** *(datetime) --*

        The last time this was updated.

      - **DataSourceParameters** *(dict) --*

        The parameters QuickSight uses to connect to your underlying source. This is a variant type
        structure. At most one of the attributes should be non-null for this structure to be valid.

        - **AmazonElasticsearchParameters** *(dict) --*

          Amazon Elasticsearch parameters.

          - **Domain** *(string) --*

            The Amazon Elasticsearch domain.

        - **AthenaParameters** *(dict) --*

          Athena parameters.

          - **WorkGroup** *(string) --*

            The workgroup that Athena uses.

        - **AuroraParameters** *(dict) --*

          Aurora MySQL parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **AuroraPostgreSqlParameters** *(dict) --*

          Aurora PostgreSQL parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **AwsIotAnalyticsParameters** *(dict) --*

          AWS IoT Analytics parameters.

          - **DataSetName** *(string) --*

            Dataset name.

        - **JiraParameters** *(dict) --*

          Jira parameters.

          - **SiteBaseUrl** *(string) --*

            The base URL of the Jira site.

        - **MariaDbParameters** *(dict) --*

          MariaDB parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **MySqlParameters** *(dict) --*

          MySQL parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **PostgreSqlParameters** *(dict) --*

          PostgreSQL parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **PrestoParameters** *(dict) --*

          Presto parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Catalog** *(string) --*

            Catalog.

        - **RdsParameters** *(dict) --*

          RDS parameters.

          - **InstanceId** *(string) --*

            Instance ID.

          - **Database** *(string) --*

            Database.

        - **RedshiftParameters** *(dict) --*

          Redshift parameters.

          - **Host** *(string) --*

            Host. This can be blank if the ``ClusterId`` is provided.

          - **Port** *(integer) --*

            Port. This can be blank if the ``ClusterId`` is provided.

          - **Database** *(string) --*

            Database.

          - **ClusterId** *(string) --*

            Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

        - **S3Parameters** *(dict) --*

          S3 parameters.

          - **ManifestFileLocation** *(dict) --*

            Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded
            in the console.

            - **Bucket** *(string) --*

              Amazon S3 bucket.

            - **Key** *(string) --*

              Amazon S3 key that identifies an object.

        - **ServiceNowParameters** *(dict) --*

          ServiceNow parameters.

          - **SiteBaseUrl** *(string) --*

            URL of the base site.

        - **SnowflakeParameters** *(dict) --*

          Snowflake parameters.

          - **Host** *(string) --*

            Host.

          - **Database** *(string) --*

            Database.

          - **Warehouse** *(string) --*

            Warehouse.

        - **SparkParameters** *(dict) --*

          Spark parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

        - **SqlServerParameters** *(dict) --*

          SQL Server parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **TeradataParameters** *(dict) --*

          Teradata parameters.

          - **Host** *(string) --*

            Host.

          - **Port** *(integer) --*

            Port.

          - **Database** *(string) --*

            Database.

        - **TwitterParameters** *(dict) --*

          Twitter parameters.

          - **Query** *(string) --*

            Twitter query string.

          - **MaxRows** *(integer) --*

            Maximum number of rows to query Twitter.

      - **VpcConnectionProperties** *(dict) --*

        The VPC connection information. You need to use this parameter only when you want QuickSight
        to use a VPC connection when connecting to your underlying source.

        - **VpcConnectionArn** *(string) --*

          VPC connection ARN.

      - **SslProperties** *(dict) --*

        SSL properties that apply when QuickSight connects to your underlying source.

        - **DisableSsl** *(boolean) --*

          A boolean flag to control whether SSL should be disabled.

      - **ErrorInfo** *(dict) --*

        Error information from the last update or the creation of the data source.

        - **Type** *(string) --*

          Error type.

        - **Message** *(string) --*

          Error message.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeGroupResponseGroupTypeDef = TypedDict(
    "_ClientDescribeGroupResponseGroupTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)


class ClientDescribeGroupResponseGroupTypeDef(_ClientDescribeGroupResponseGroupTypeDef):
    """
    Type definition for `ClientDescribeGroupResponse` `Group`

    The name of the group.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group.

    - **GroupName** *(string) --*

      The name of the group.

    - **Description** *(string) --*

      The group description.

    - **PrincipalId** *(string) --*

      The principal ID of the group.
    """


_ClientDescribeGroupResponseTypeDef = TypedDict(
    "_ClientDescribeGroupResponseTypeDef",
    {"Group": ClientDescribeGroupResponseGroupTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientDescribeGroupResponseTypeDef(_ClientDescribeGroupResponseTypeDef):
    """
    Type definition for `ClientDescribeGroup` `Response`

    - **Group** *(dict) --*

      The name of the group.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the group.

      - **GroupName** *(string) --*

        The name of the group.

      - **Description** *(string) --*

        The group description.

      - **PrincipalId** *(string) --*

        The principal ID of the group.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef = TypedDict(
    "_ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentId": str,
        "AssignmentName": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": str,
    },
    total=False,
)


class ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef(
    _ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef
):
    """
    Type definition for `ClientDescribeIamPolicyAssignmentResponse` `IAMPolicyAssignment`

    Information describing the IAM policy assignment.

    - **AwsAccountId** *(string) --*

      AWS account ID.

    - **AssignmentId** *(string) --*

      Assignment ID.

    - **AssignmentName** *(string) --*

      Assignment name.

    - **PolicyArn** *(string) --*

      Policy ARN.

    - **Identities** *(dict) --*

      Identities.

      - *(string) --*

        - *(list) --*

          - *(string) --*

    - **AssignmentStatus** *(string) --*

      Assignment status.
    """


_ClientDescribeIamPolicyAssignmentResponseTypeDef = TypedDict(
    "_ClientDescribeIamPolicyAssignmentResponseTypeDef",
    {
        "IAMPolicyAssignment": ClientDescribeIamPolicyAssignmentResponseIAMPolicyAssignmentTypeDef,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientDescribeIamPolicyAssignmentResponseTypeDef(
    _ClientDescribeIamPolicyAssignmentResponseTypeDef
):
    """
    Type definition for `ClientDescribeIamPolicyAssignment` `Response`

    - **IAMPolicyAssignment** *(dict) --*

      Information describing the IAM policy assignment.

      - **AwsAccountId** *(string) --*

        AWS account ID.

      - **AssignmentId** *(string) --*

        Assignment ID.

      - **AssignmentName** *(string) --*

        Assignment name.

      - **PolicyArn** *(string) --*

        Policy ARN.

      - **Identities** *(dict) --*

        Identities.

        - *(string) --*

          - *(list) --*

            - *(string) --*

      - **AssignmentStatus** *(string) --*

        Assignment status.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeIngestionResponseIngestionErrorInfoTypeDef = TypedDict(
    "_ClientDescribeIngestionResponseIngestionErrorInfoTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientDescribeIngestionResponseIngestionErrorInfoTypeDef(
    _ClientDescribeIngestionResponseIngestionErrorInfoTypeDef
):
    """
    Type definition for `ClientDescribeIngestionResponseIngestion` `ErrorInfo`

    Error information for this ingestion.

    - **Type** *(string) --*

      Error type.

    - **Message** *(string) --*

      Error essage.
    """


_ClientDescribeIngestionResponseIngestionQueueInfoTypeDef = TypedDict(
    "_ClientDescribeIngestionResponseIngestionQueueInfoTypeDef",
    {"WaitingOnIngestion": str, "QueuedIngestion": str},
    total=False,
)


class ClientDescribeIngestionResponseIngestionQueueInfoTypeDef(
    _ClientDescribeIngestionResponseIngestionQueueInfoTypeDef
):
    """
    Type definition for `ClientDescribeIngestionResponseIngestion` `QueueInfo`

    Information on queued dataset SPICE ingestion.

    - **WaitingOnIngestion** *(string) --*

      The ID of the queued ingestion.

    - **QueuedIngestion** *(string) --*

      The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing ingestion to
      complete.
    """


_ClientDescribeIngestionResponseIngestionRowInfoTypeDef = TypedDict(
    "_ClientDescribeIngestionResponseIngestionRowInfoTypeDef",
    {"RowsIngested": int, "RowsDropped": int},
    total=False,
)


class ClientDescribeIngestionResponseIngestionRowInfoTypeDef(
    _ClientDescribeIngestionResponseIngestionRowInfoTypeDef
):
    """
    Type definition for `ClientDescribeIngestionResponseIngestion` `RowInfo`

    Information on rows during a data set SPICE ingestion.

    - **RowsIngested** *(integer) --*

      The number of rows that were ingested.

    - **RowsDropped** *(integer) --*

      The number of rows that were not ingested.
    """


_ClientDescribeIngestionResponseIngestionTypeDef = TypedDict(
    "_ClientDescribeIngestionResponseIngestionTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": str,
        "ErrorInfo": ClientDescribeIngestionResponseIngestionErrorInfoTypeDef,
        "RowInfo": ClientDescribeIngestionResponseIngestionRowInfoTypeDef,
        "QueueInfo": ClientDescribeIngestionResponseIngestionQueueInfoTypeDef,
        "CreatedTime": datetime,
        "IngestionTimeInSeconds": int,
        "IngestionSizeInBytes": int,
        "RequestSource": str,
        "RequestType": str,
    },
    total=False,
)


class ClientDescribeIngestionResponseIngestionTypeDef(
    _ClientDescribeIngestionResponseIngestionTypeDef
):
    """
    Type definition for `ClientDescribeIngestionResponse` `Ingestion`

    Information about the ingestion.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **IngestionId** *(string) --*

      Ingestion ID.

    - **IngestionStatus** *(string) --*

      Ingestion status.

    - **ErrorInfo** *(dict) --*

      Error information for this ingestion.

      - **Type** *(string) --*

        Error type.

      - **Message** *(string) --*

        Error essage.

    - **RowInfo** *(dict) --*

      Information on rows during a data set SPICE ingestion.

      - **RowsIngested** *(integer) --*

        The number of rows that were ingested.

      - **RowsDropped** *(integer) --*

        The number of rows that were not ingested.

    - **QueueInfo** *(dict) --*

      Information on queued dataset SPICE ingestion.

      - **WaitingOnIngestion** *(string) --*

        The ID of the queued ingestion.

      - **QueuedIngestion** *(string) --*

        The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing ingestion
        to complete.

    - **CreatedTime** *(datetime) --*

      The time this ingestion started.

    - **IngestionTimeInSeconds** *(integer) --*

      The time this ingestion took, measured in seconds.

    - **IngestionSizeInBytes** *(integer) --*

      Size of the data ingested in bytes.

    - **RequestSource** *(string) --*

      Event source for this ingestion.

    - **RequestType** *(string) --*

      Type of this ingestion.
    """


_ClientDescribeIngestionResponseTypeDef = TypedDict(
    "_ClientDescribeIngestionResponseTypeDef",
    {"Ingestion": ClientDescribeIngestionResponseIngestionTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientDescribeIngestionResponseTypeDef(_ClientDescribeIngestionResponseTypeDef):
    """
    Type definition for `ClientDescribeIngestion` `Response`

    - **Ingestion** *(dict) --*

      Information about the ingestion.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the resource.

      - **IngestionId** *(string) --*

        Ingestion ID.

      - **IngestionStatus** *(string) --*

        Ingestion status.

      - **ErrorInfo** *(dict) --*

        Error information for this ingestion.

        - **Type** *(string) --*

          Error type.

        - **Message** *(string) --*

          Error essage.

      - **RowInfo** *(dict) --*

        Information on rows during a data set SPICE ingestion.

        - **RowsIngested** *(integer) --*

          The number of rows that were ingested.

        - **RowsDropped** *(integer) --*

          The number of rows that were not ingested.

      - **QueueInfo** *(dict) --*

        Information on queued dataset SPICE ingestion.

        - **WaitingOnIngestion** *(string) --*

          The ID of the queued ingestion.

        - **QueuedIngestion** *(string) --*

          The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing ingestion
          to complete.

      - **CreatedTime** *(datetime) --*

        The time this ingestion started.

      - **IngestionTimeInSeconds** *(integer) --*

        The time this ingestion took, measured in seconds.

      - **IngestionSizeInBytes** *(integer) --*

        Size of the data ingested in bytes.

      - **RequestSource** *(string) --*

        Event source for this ingestion.

      - **RequestType** *(string) --*

        Type of this ingestion.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeTemplateAliasResponseTemplateAliasTypeDef = TypedDict(
    "_ClientDescribeTemplateAliasResponseTemplateAliasTypeDef",
    {"AliasName": str, "Arn": str, "TemplateVersionNumber": int},
    total=False,
)


class ClientDescribeTemplateAliasResponseTemplateAliasTypeDef(
    _ClientDescribeTemplateAliasResponseTemplateAliasTypeDef
):
    """
    Type definition for `ClientDescribeTemplateAliasResponse` `TemplateAlias`

    Information about the template alias.

    - **AliasName** *(string) --*

      The display name of the template alias.

    - **Arn** *(string) --*

      The ARN of the template alias.

    - **TemplateVersionNumber** *(integer) --*

      The version number of the template alias.
    """


_ClientDescribeTemplateAliasResponseTypeDef = TypedDict(
    "_ClientDescribeTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": ClientDescribeTemplateAliasResponseTemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientDescribeTemplateAliasResponseTypeDef(_ClientDescribeTemplateAliasResponseTypeDef):
    """
    Type definition for `ClientDescribeTemplateAlias` `Response`

    - **TemplateAlias** *(dict) --*

      Information about the template alias.

      - **AliasName** *(string) --*

        The display name of the template alias.

      - **Arn** *(string) --*

        The ARN of the template alias.

      - **TemplateVersionNumber** *(integer) --*

        The version number of the template alias.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientDescribeTemplatePermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientDescribeTemplatePermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientDescribeTemplatePermissionsResponsePermissionsTypeDef(
    _ClientDescribeTemplatePermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientDescribeTemplatePermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientDescribeTemplatePermissionsResponseTypeDef = TypedDict(
    "_ClientDescribeTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ClientDescribeTemplatePermissionsResponsePermissionsTypeDef],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientDescribeTemplatePermissionsResponseTypeDef(
    _ClientDescribeTemplatePermissionsResponseTypeDef
):
    """
    Type definition for `ClientDescribeTemplatePermissions` `Response`

    - **TemplateId** *(string) --*

      The ID for the template.

    - **TemplateArn** *(string) --*

      The ARN of the template.

    - **Permissions** *(list) --*

      A list of resource permissions to be set on the template.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef",
    {"Name": str},
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef
):
    """
    Type definition for
    `ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaList`
    `ColumnGroupColumnSchemaList`

    A structure describing the name, datatype, and geographic role of the columns.

    - **Name** *(string) --*

      The name of the column group's column schema.
    """


_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef",
    {
        "Name": str,
        "ColumnGroupColumnSchemaList": List[
            ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListColumnGroupColumnSchemaListTypeDef
        ],
    },
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef
):
    """
    Type definition for `ClientDescribeTemplateResponseTemplateVersionDataSetConfigurations`
    `ColumnGroupSchemaList`

    The column group schema.

    - **Name** *(string) --*

      The name of the column group schema.

    - **ColumnGroupColumnSchemaList** *(list) --*

      A structure containing the list of column group column schemas.

      - *(dict) --*

        A structure describing the name, datatype, and geographic role of the columns.

        - **Name** *(string) --*

          The name of the column group's column schema.
    """


_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef",
    {"Name": str, "DataType": str, "GeographicRole": str},
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef
):
    """
    Type definition for
    `ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchema`
    `ColumnSchemaList`

    The column schema.

    - **Name** *(string) --*

      The name of the column schema.

    - **DataType** *(string) --*

      The data type of the column schema.

    - **GeographicRole** *(string) --*

      The geographic role of the column schema.
    """


_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef",
    {
        "ColumnSchemaList": List[
            ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaColumnSchemaListTypeDef
        ]
    },
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef
):
    """
    Type definition for `ClientDescribeTemplateResponseTemplateVersionDataSetConfigurations`
    `DataSetSchema`

    Dataset schema.

    - **ColumnSchemaList** *(list) --*

      A structure containing the list of column schemas.

      - *(dict) --*

        The column schema.

        - **Name** *(string) --*

          The name of the column schema.

        - **DataType** *(string) --*

          The data type of the column schema.

        - **GeographicRole** *(string) --*

          The geographic role of the column schema.
    """


_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef",
    {
        "Placeholder": str,
        "DataSetSchema": ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsDataSetSchemaTypeDef,
        "ColumnGroupSchemaList": List[
            ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsColumnGroupSchemaListTypeDef
        ],
    },
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef
):
    """
    Type definition for `ClientDescribeTemplateResponseTemplateVersion` `DataSetConfigurations`

    Dataset configuration.

    - **Placeholder** *(string) --*

      Placeholder.

    - **DataSetSchema** *(dict) --*

      Dataset schema.

      - **ColumnSchemaList** *(list) --*

        A structure containing the list of column schemas.

        - *(dict) --*

          The column schema.

          - **Name** *(string) --*

            The name of the column schema.

          - **DataType** *(string) --*

            The data type of the column schema.

          - **GeographicRole** *(string) --*

            The geographic role of the column schema.

    - **ColumnGroupSchemaList** *(list) --*

      A structure containing the list of column group schemas.

      - *(dict) --*

        The column group schema.

        - **Name** *(string) --*

          The name of the column group schema.

        - **ColumnGroupColumnSchemaList** *(list) --*

          A structure containing the list of column group column schemas.

          - *(dict) --*

            A structure describing the name, datatype, and geographic role of the columns.

            - **Name** *(string) --*

              The name of the column group's column schema.
    """


_ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef
):
    """
    Type definition for `ClientDescribeTemplateResponseTemplateVersion` `Errors`

    List of errors that occurred when the template version creation failed.

    - **Type** *(string) --*

      Type of error.

    - **Message** *(string) --*

      Description of the error type.
    """


_ClientDescribeTemplateResponseTemplateVersionTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[ClientDescribeTemplateResponseTemplateVersionErrorsTypeDef],
        "VersionNumber": int,
        "Status": str,
        "DataSetConfigurations": List[
            ClientDescribeTemplateResponseTemplateVersionDataSetConfigurationsTypeDef
        ],
        "Description": str,
        "SourceEntityArn": str,
    },
    total=False,
)


class ClientDescribeTemplateResponseTemplateVersionTypeDef(
    _ClientDescribeTemplateResponseTemplateVersionTypeDef
):
    """
    Type definition for `ClientDescribeTemplateResponseTemplate` `Version`

    A structure describing the versions of the template.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **Errors** *(list) --*

      Errors associated with the template.

      - *(dict) --*

        List of errors that occurred when the template version creation failed.

        - **Type** *(string) --*

          Type of error.

        - **Message** *(string) --*

          Description of the error type.

    - **VersionNumber** *(integer) --*

      The version number of the template.

    - **Status** *(string) --*

      The http status of the request.

    - **DataSetConfigurations** *(list) --*

      Schema of the dataset identified by the placeholder. The idea is that any dashboard created
      from the template should be bound to new datasets matching the same schema described through
      this API. .

      - *(dict) --*

        Dataset configuration.

        - **Placeholder** *(string) --*

          Placeholder.

        - **DataSetSchema** *(dict) --*

          Dataset schema.

          - **ColumnSchemaList** *(list) --*

            A structure containing the list of column schemas.

            - *(dict) --*

              The column schema.

              - **Name** *(string) --*

                The name of the column schema.

              - **DataType** *(string) --*

                The data type of the column schema.

              - **GeographicRole** *(string) --*

                The geographic role of the column schema.

        - **ColumnGroupSchemaList** *(list) --*

          A structure containing the list of column group schemas.

          - *(dict) --*

            The column group schema.

            - **Name** *(string) --*

              The name of the column group schema.

            - **ColumnGroupColumnSchemaList** *(list) --*

              A structure containing the list of column group column schemas.

              - *(dict) --*

                A structure describing the name, datatype, and geographic role of the columns.

                - **Name** *(string) --*

                  The name of the column group's column schema.

    - **Description** *(string) --*

      The description of the template.

    - **SourceEntityArn** *(string) --*

      The ARN of the analysis or template which was used to create this template.
    """


_ClientDescribeTemplateResponseTemplateTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTemplateTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Version": ClientDescribeTemplateResponseTemplateVersionTypeDef,
        "TemplateId": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": datetime,
    },
    total=False,
)


class ClientDescribeTemplateResponseTemplateTypeDef(_ClientDescribeTemplateResponseTemplateTypeDef):
    """
    Type definition for `ClientDescribeTemplateResponse` `Template`

    The template structure of the object you want to describe.

    - **Arn** *(string) --*

      The ARN of the template.

    - **Name** *(string) --*

      The display name of the template.

    - **Version** *(dict) --*

      A structure describing the versions of the template.

      - **CreatedTime** *(datetime) --*

        The time this was created.

      - **Errors** *(list) --*

        Errors associated with the template.

        - *(dict) --*

          List of errors that occurred when the template version creation failed.

          - **Type** *(string) --*

            Type of error.

          - **Message** *(string) --*

            Description of the error type.

      - **VersionNumber** *(integer) --*

        The version number of the template.

      - **Status** *(string) --*

        The http status of the request.

      - **DataSetConfigurations** *(list) --*

        Schema of the dataset identified by the placeholder. The idea is that any dashboard created
        from the template should be bound to new datasets matching the same schema described through
        this API. .

        - *(dict) --*

          Dataset configuration.

          - **Placeholder** *(string) --*

            Placeholder.

          - **DataSetSchema** *(dict) --*

            Dataset schema.

            - **ColumnSchemaList** *(list) --*

              A structure containing the list of column schemas.

              - *(dict) --*

                The column schema.

                - **Name** *(string) --*

                  The name of the column schema.

                - **DataType** *(string) --*

                  The data type of the column schema.

                - **GeographicRole** *(string) --*

                  The geographic role of the column schema.

          - **ColumnGroupSchemaList** *(list) --*

            A structure containing the list of column group schemas.

            - *(dict) --*

              The column group schema.

              - **Name** *(string) --*

                The name of the column group schema.

              - **ColumnGroupColumnSchemaList** *(list) --*

                A structure containing the list of column group column schemas.

                - *(dict) --*

                  A structure describing the name, datatype, and geographic role of the columns.

                  - **Name** *(string) --*

                    The name of the column group's column schema.

      - **Description** *(string) --*

        The description of the template.

      - **SourceEntityArn** *(string) --*

        The ARN of the analysis or template which was used to create this template.

    - **TemplateId** *(string) --*

      The ID for the template. This is unique per region per AWS account.

    - **LastUpdatedTime** *(datetime) --*

      Time when this was last updated.

    - **CreatedTime** *(datetime) --*

      Time when this was created.
    """


_ClientDescribeTemplateResponseTypeDef = TypedDict(
    "_ClientDescribeTemplateResponseTypeDef",
    {"Template": ClientDescribeTemplateResponseTemplateTypeDef, "Status": int},
    total=False,
)


class ClientDescribeTemplateResponseTypeDef(_ClientDescribeTemplateResponseTypeDef):
    """
    Type definition for `ClientDescribeTemplate` `Response`

    - **Template** *(dict) --*

      The template structure of the object you want to describe.

      - **Arn** *(string) --*

        The ARN of the template.

      - **Name** *(string) --*

        The display name of the template.

      - **Version** *(dict) --*

        A structure describing the versions of the template.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **Errors** *(list) --*

          Errors associated with the template.

          - *(dict) --*

            List of errors that occurred when the template version creation failed.

            - **Type** *(string) --*

              Type of error.

            - **Message** *(string) --*

              Description of the error type.

        - **VersionNumber** *(integer) --*

          The version number of the template.

        - **Status** *(string) --*

          The http status of the request.

        - **DataSetConfigurations** *(list) --*

          Schema of the dataset identified by the placeholder. The idea is that any dashboard
          created from the template should be bound to new datasets matching the same schema
          described through this API. .

          - *(dict) --*

            Dataset configuration.

            - **Placeholder** *(string) --*

              Placeholder.

            - **DataSetSchema** *(dict) --*

              Dataset schema.

              - **ColumnSchemaList** *(list) --*

                A structure containing the list of column schemas.

                - *(dict) --*

                  The column schema.

                  - **Name** *(string) --*

                    The name of the column schema.

                  - **DataType** *(string) --*

                    The data type of the column schema.

                  - **GeographicRole** *(string) --*

                    The geographic role of the column schema.

            - **ColumnGroupSchemaList** *(list) --*

              A structure containing the list of column group schemas.

              - *(dict) --*

                The column group schema.

                - **Name** *(string) --*

                  The name of the column group schema.

                - **ColumnGroupColumnSchemaList** *(list) --*

                  A structure containing the list of column group column schemas.

                  - *(dict) --*

                    A structure describing the name, datatype, and geographic role of the columns.

                    - **Name** *(string) --*

                      The name of the column group's column schema.

        - **Description** *(string) --*

          The description of the template.

        - **SourceEntityArn** *(string) --*

          The ARN of the analysis or template which was used to create this template.

      - **TemplateId** *(string) --*

        The ID for the template. This is unique per region per AWS account.

      - **LastUpdatedTime** *(datetime) --*

        Time when this was last updated.

      - **CreatedTime** *(datetime) --*

        Time when this was created.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientDescribeUserResponseUserTypeDef = TypedDict(
    "_ClientDescribeUserResponseUserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": str,
        "IdentityType": str,
        "Active": bool,
        "PrincipalId": str,
    },
    total=False,
)


class ClientDescribeUserResponseUserTypeDef(_ClientDescribeUserResponseUserTypeDef):
    """
    Type definition for `ClientDescribeUserResponse` `User`

    The user name.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the user.

    - **UserName** *(string) --*

      The user's user name.

    - **Email** *(string) --*

      The user's email address.

    - **Role** *(string) --*

      The Amazon QuickSight role for the user. The user role can be one of the following:.

      * ``READER`` : A user who has read-only access to dashboards.

      * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

      * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

      * ``RESTRICTED_READER`` : This role isn't currently available for use.

      * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

    - **IdentityType** *(string) --*

      The type of identity authentication used by the user.

    - **Active** *(boolean) --*

      Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or an
      AD user, that user is inactive until they sign in and provide a password.

    - **PrincipalId** *(string) --*

      The principal ID of the user.
    """


_ClientDescribeUserResponseTypeDef = TypedDict(
    "_ClientDescribeUserResponseTypeDef",
    {"User": ClientDescribeUserResponseUserTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientDescribeUserResponseTypeDef(_ClientDescribeUserResponseTypeDef):
    """
    Type definition for `ClientDescribeUser` `Response`

    - **User** *(dict) --*

      The user name.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the user.

      - **UserName** *(string) --*

        The user's user name.

      - **Email** *(string) --*

        The user's email address.

      - **Role** *(string) --*

        The Amazon QuickSight role for the user. The user role can be one of the following:.

        * ``READER`` : A user who has read-only access to dashboards.

        * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

        * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

        * ``RESTRICTED_READER`` : This role isn't currently available for use.

        * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

      - **IdentityType** *(string) --*

        The type of identity authentication used by the user.

      - **Active** *(boolean) --*

        Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or
        an AD user, that user is inactive until they sign in and provide a password.

      - **PrincipalId** *(string) --*

        The principal ID of the user.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientGetDashboardEmbedUrlResponseTypeDef = TypedDict(
    "_ClientGetDashboardEmbedUrlResponseTypeDef",
    {"EmbedUrl": str, "Status": int, "RequestId": str},
    total=False,
)


class ClientGetDashboardEmbedUrlResponseTypeDef(_ClientGetDashboardEmbedUrlResponseTypeDef):
    """
    Type definition for `ClientGetDashboardEmbedUrl` `Response`

    - **EmbedUrl** *(string) --*

      URL that you can put into your server-side webpage to embed your dashboard. This URL is valid
      for 5 minutes, and the resulting session is valid for 10 hours. The API provides the URL with
      an auth_code that enables a single-signon session.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef = TypedDict(
    "_ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "VersionNumber": int,
        "Status": str,
        "SourceEntityArn": str,
        "Description": str,
    },
    total=False,
)


class ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef(
    _ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef
):
    """
    Type definition for `ClientListDashboardVersionsResponse` `DashboardVersionSummaryList`

    Dashboard version summary.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **VersionNumber** *(integer) --*

      Version number.

    - **Status** *(string) --*

      The http status of the request.

    - **SourceEntityArn** *(string) --*

      Source entity ARN.

    - **Description** *(string) --*

      Description.
    """


_ClientListDashboardVersionsResponseTypeDef = TypedDict(
    "_ClientListDashboardVersionsResponseTypeDef",
    {
        "DashboardVersionSummaryList": List[
            ClientListDashboardVersionsResponseDashboardVersionSummaryListTypeDef
        ],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientListDashboardVersionsResponseTypeDef(_ClientListDashboardVersionsResponseTypeDef):
    """
    Type definition for `ClientListDashboardVersions` `Response`

    - **DashboardVersionSummaryList** *(list) --*

      A structure that contains information about each version of the dashboard.

      - *(dict) --*

        Dashboard version summary.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the resource.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **VersionNumber** *(integer) --*

          Version number.

        - **Status** *(string) --*

          The http status of the request.

        - **SourceEntityArn** *(string) --*

          Source entity ARN.

        - **Description** *(string) --*

          Description.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientListDashboardsResponseDashboardSummaryListTypeDef = TypedDict(
    "_ClientListDashboardsResponseDashboardSummaryListTypeDef",
    {
        "Arn": str,
        "DashboardId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PublishedVersionNumber": int,
        "LastPublishedTime": datetime,
    },
    total=False,
)


class ClientListDashboardsResponseDashboardSummaryListTypeDef(
    _ClientListDashboardsResponseDashboardSummaryListTypeDef
):
    """
    Type definition for `ClientListDashboardsResponse` `DashboardSummaryList`

    Dashboard summary.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **DashboardId** *(string) --*

      Dashboard ID.

    - **Name** *(string) --*

      A display name for the dataset.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.

    - **PublishedVersionNumber** *(integer) --*

      Published version number.

    - **LastPublishedTime** *(datetime) --*

      The last time this was published.
    """


_ClientListDashboardsResponseTypeDef = TypedDict(
    "_ClientListDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[ClientListDashboardsResponseDashboardSummaryListTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientListDashboardsResponseTypeDef(_ClientListDashboardsResponseTypeDef):
    """
    Type definition for `ClientListDashboards` `Response`

    - **DashboardSummaryList** *(list) --*

      A structure that contains all of the dashboards shared with the user. Provides basic
      information about the dashboards.

      - *(dict) --*

        Dashboard summary.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the resource.

        - **DashboardId** *(string) --*

          Dashboard ID.

        - **Name** *(string) --*

          A display name for the dataset.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **LastUpdatedTime** *(datetime) --*

          The last time this was updated.

        - **PublishedVersionNumber** *(integer) --*

          Published version number.

        - **LastPublishedTime** *(datetime) --*

          The last time this was published.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef = TypedDict(
    "_ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef",
    {"Arn": str, "PermissionPolicy": str},
    total=False,
)


class ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef(
    _ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef
):
    """
    Type definition for `ClientListDataSetsResponseDataSetSummaries` `RowLevelPermissionDataSet`

    Row-level security configuration on the dataset.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the permission dataset.

    - **PermissionPolicy** *(string) --*

      Permission policy.
    """


_ClientListDataSetsResponseDataSetSummariesTypeDef = TypedDict(
    "_ClientListDataSetsResponseDataSetSummariesTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "ImportMode": str,
        "RowLevelPermissionDataSet": ClientListDataSetsResponseDataSetSummariesRowLevelPermissionDataSetTypeDef,
    },
    total=False,
)


class ClientListDataSetsResponseDataSetSummariesTypeDef(
    _ClientListDataSetsResponseDataSetSummariesTypeDef
):
    """
    Type definition for `ClientListDataSetsResponse` `DataSetSummaries`

    Dataset summary.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the dataset.

    - **DataSetId** *(string) --*

      The ID of the dataset.

    - **Name** *(string) --*

      A display name for the dataset.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.

    - **ImportMode** *(string) --*

      Indicates whether or not you want to import the data into SPICE.

    - **RowLevelPermissionDataSet** *(dict) --*

      Row-level security configuration on the dataset.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) of the permission dataset.

      - **PermissionPolicy** *(string) --*

        Permission policy.
    """


_ClientListDataSetsResponseTypeDef = TypedDict(
    "_ClientListDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[ClientListDataSetsResponseDataSetSummariesTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListDataSetsResponseTypeDef(_ClientListDataSetsResponseTypeDef):
    """
    Type definition for `ClientListDataSets` `Response`

    - **DataSetSummaries** *(list) --*

      The list of dataset summaries.

      - *(dict) --*

        Dataset summary.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the dataset.

        - **DataSetId** *(string) --*

          The ID of the dataset.

        - **Name** *(string) --*

          A display name for the dataset.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **LastUpdatedTime** *(datetime) --*

          The last time this was updated.

        - **ImportMode** *(string) --*

          Indicates whether or not you want to import the data into SPICE.

        - **RowLevelPermissionDataSet** *(dict) --*

          Row-level security configuration on the dataset.

          - **Arn** *(string) --*

            The Amazon Resource name (ARN) of the permission dataset.

          - **PermissionPolicy** *(string) --*

            Permission policy.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef",
    {"Domain": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `AmazonElasticsearchParameters`

    Amazon Elasticsearch parameters.

    - **Domain** *(string) --*

      The Amazon Elasticsearch domain.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef",
    {"WorkGroup": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `AthenaParameters`

    Athena parameters.

    - **WorkGroup** *(string) --*

      The workgroup that Athena uses.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `AuroraParameters`

    Aurora MySQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `AuroraPostgreSqlParameters`

    Aurora PostgreSQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    {"DataSetName": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `AwsIotAnalyticsParameters`

    AWS IoT Analytics parameters.

    - **DataSetName** *(string) --*

      Dataset name.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef",
    {"SiteBaseUrl": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `JiraParameters`

    Jira parameters.

    - **SiteBaseUrl** *(string) --*

      The base URL of the Jira site.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `MariaDbParameters`

    MariaDB parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `MySqlParameters`

    MySQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `PostgreSqlParameters`

    PostgreSQL parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef",
    {"Host": str, "Port": int, "Catalog": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `PrestoParameters`

    Presto parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Catalog** *(string) --*

      Catalog.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef",
    {"InstanceId": str, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `RdsParameters`

    RDS parameters.

    - **InstanceId** *(string) --*

      Instance ID.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef",
    {"Host": str, "Port": int, "Database": str, "ClusterId": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `RedshiftParameters`

    Redshift parameters.

    - **Host** *(string) --*

      Host. This can be blank if the ``ClusterId`` is provided.

    - **Port** *(integer) --*

      Port. This can be blank if the ``ClusterId`` is provided.

    - **Database** *(string) --*

      Database.

    - **ClusterId** *(string) --*

      Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    {"Bucket": str, "Key": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParametersS3Parameters`
    `ManifestFileLocation`

    Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
    console.

    - **Bucket** *(string) --*

      Amazon S3 bucket.

    - **Key** *(string) --*

      Amazon S3 key that identifies an object.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef",
    {
        "ManifestFileLocation": ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersManifestFileLocationTypeDef
    },
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `S3Parameters`

    S3 parameters.

    - **ManifestFileLocation** *(dict) --*

      Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
      console.

      - **Bucket** *(string) --*

        Amazon S3 bucket.

      - **Key** *(string) --*

        Amazon S3 key that identifies an object.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef",
    {"SiteBaseUrl": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `ServiceNowParameters`

    ServiceNow parameters.

    - **SiteBaseUrl** *(string) --*

      URL of the base site.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef",
    {"Host": str, "Database": str, "Warehouse": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `SnowflakeParameters`

    Snowflake parameters.

    - **Host** *(string) --*

      Host.

    - **Database** *(string) --*

      Database.

    - **Warehouse** *(string) --*

      Warehouse.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef",
    {"Host": str, "Port": int},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `SparkParameters`

    Spark parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `SqlServerParameters`

    SQL Server parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `TeradataParameters`

    Teradata parameters.

    - **Host** *(string) --*

      Host.

    - **Port** *(integer) --*

      Port.

    - **Database** *(string) --*

      Database.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef",
    {"Query": str, "MaxRows": int},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSourcesDataSourceParameters`
    `TwitterParameters`

    Twitter parameters.

    - **Query** *(string) --*

      Twitter query string.

    - **MaxRows** *(integer) --*

      Maximum number of rows to query Twitter.
    """


_ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersAmazonElasticsearchParametersTypeDef,
        "AthenaParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersAthenaParametersTypeDef,
        "AuroraParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersAuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersAwsIotAnalyticsParametersTypeDef,
        "JiraParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersJiraParametersTypeDef,
        "MariaDbParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersMariaDbParametersTypeDef,
        "MySqlParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersMySqlParametersTypeDef,
        "PostgreSqlParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersPostgreSqlParametersTypeDef,
        "PrestoParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersPrestoParametersTypeDef,
        "RdsParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersRdsParametersTypeDef,
        "RedshiftParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersRedshiftParametersTypeDef,
        "S3Parameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersS3ParametersTypeDef,
        "ServiceNowParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersServiceNowParametersTypeDef,
        "SnowflakeParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersSnowflakeParametersTypeDef,
        "SparkParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersSparkParametersTypeDef,
        "SqlServerParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersSqlServerParametersTypeDef,
        "TeradataParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersTeradataParametersTypeDef,
        "TwitterParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersTwitterParametersTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef(
    _ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSources` `DataSourceParameters`

    The parameters QuickSight uses to connect to your underlying source. This is a variant type
    structure. At most one of the attributes should be non-null for this structure to be valid.

    - **AmazonElasticsearchParameters** *(dict) --*

      Amazon Elasticsearch parameters.

      - **Domain** *(string) --*

        The Amazon Elasticsearch domain.

    - **AthenaParameters** *(dict) --*

      Athena parameters.

      - **WorkGroup** *(string) --*

        The workgroup that Athena uses.

    - **AuroraParameters** *(dict) --*

      Aurora MySQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **AuroraPostgreSqlParameters** *(dict) --*

      Aurora PostgreSQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **AwsIotAnalyticsParameters** *(dict) --*

      AWS IoT Analytics parameters.

      - **DataSetName** *(string) --*

        Dataset name.

    - **JiraParameters** *(dict) --*

      Jira parameters.

      - **SiteBaseUrl** *(string) --*

        The base URL of the Jira site.

    - **MariaDbParameters** *(dict) --*

      MariaDB parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **MySqlParameters** *(dict) --*

      MySQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **PostgreSqlParameters** *(dict) --*

      PostgreSQL parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **PrestoParameters** *(dict) --*

      Presto parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Catalog** *(string) --*

        Catalog.

    - **RdsParameters** *(dict) --*

      RDS parameters.

      - **InstanceId** *(string) --*

        Instance ID.

      - **Database** *(string) --*

        Database.

    - **RedshiftParameters** *(dict) --*

      Redshift parameters.

      - **Host** *(string) --*

        Host. This can be blank if the ``ClusterId`` is provided.

      - **Port** *(integer) --*

        Port. This can be blank if the ``ClusterId`` is provided.

      - **Database** *(string) --*

        Database.

      - **ClusterId** *(string) --*

        Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

    - **S3Parameters** *(dict) --*

      S3 parameters.

      - **ManifestFileLocation** *(dict) --*

        Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
        the console.

        - **Bucket** *(string) --*

          Amazon S3 bucket.

        - **Key** *(string) --*

          Amazon S3 key that identifies an object.

    - **ServiceNowParameters** *(dict) --*

      ServiceNow parameters.

      - **SiteBaseUrl** *(string) --*

        URL of the base site.

    - **SnowflakeParameters** *(dict) --*

      Snowflake parameters.

      - **Host** *(string) --*

        Host.

      - **Database** *(string) --*

        Database.

      - **Warehouse** *(string) --*

        Warehouse.

    - **SparkParameters** *(dict) --*

      Spark parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

    - **SqlServerParameters** *(dict) --*

      SQL Server parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **TeradataParameters** *(dict) --*

      Teradata parameters.

      - **Host** *(string) --*

        Host.

      - **Port** *(integer) --*

        Port.

      - **Database** *(string) --*

        Database.

    - **TwitterParameters** *(dict) --*

      Twitter parameters.

      - **Query** *(string) --*

        Twitter query string.

      - **MaxRows** *(integer) --*

        Maximum number of rows to query Twitter.
    """


_ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef(
    _ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSources` `ErrorInfo`

    Error information from the last update or the creation of the data source.

    - **Type** *(string) --*

      Error type.

    - **Message** *(string) --*

      Error message.
    """


_ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef",
    {"DisableSsl": bool},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef(
    _ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSources` `SslProperties`

    SSL properties that apply when QuickSight connects to your underlying source.

    - **DisableSsl** *(boolean) --*

      A boolean flag to control whether SSL should be disabled.
    """


_ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef",
    {"VpcConnectionArn": str},
    total=False,
)


class ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef(
    _ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponseDataSources` `VpcConnectionProperties`

    The VPC connection information. You need to use this parameter only when you want QuickSight to
    use a VPC connection when connecting to your underlying source.

    - **VpcConnectionArn** *(string) --*

      VPC connection ARN.
    """


_ClientListDataSourcesResponseDataSourcesTypeDef = TypedDict(
    "_ClientListDataSourcesResponseDataSourcesTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": str,
        "Status": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "DataSourceParameters": ClientListDataSourcesResponseDataSourcesDataSourceParametersTypeDef,
        "VpcConnectionProperties": ClientListDataSourcesResponseDataSourcesVpcConnectionPropertiesTypeDef,
        "SslProperties": ClientListDataSourcesResponseDataSourcesSslPropertiesTypeDef,
        "ErrorInfo": ClientListDataSourcesResponseDataSourcesErrorInfoTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponseDataSourcesTypeDef(
    _ClientListDataSourcesResponseDataSourcesTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponse` `DataSources`

    The structure of a data source.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **Name** *(string) --*

      A display name for the data source.

    - **Type** *(string) --*

      The type of the data source. This indicates which database engine the data source connects to.

    - **Status** *(string) --*

      The http status of the request.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.

    - **DataSourceParameters** *(dict) --*

      The parameters QuickSight uses to connect to your underlying source. This is a variant type
      structure. At most one of the attributes should be non-null for this structure to be valid.

      - **AmazonElasticsearchParameters** *(dict) --*

        Amazon Elasticsearch parameters.

        - **Domain** *(string) --*

          The Amazon Elasticsearch domain.

      - **AthenaParameters** *(dict) --*

        Athena parameters.

        - **WorkGroup** *(string) --*

          The workgroup that Athena uses.

      - **AuroraParameters** *(dict) --*

        Aurora MySQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **AuroraPostgreSqlParameters** *(dict) --*

        Aurora PostgreSQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **AwsIotAnalyticsParameters** *(dict) --*

        AWS IoT Analytics parameters.

        - **DataSetName** *(string) --*

          Dataset name.

      - **JiraParameters** *(dict) --*

        Jira parameters.

        - **SiteBaseUrl** *(string) --*

          The base URL of the Jira site.

      - **MariaDbParameters** *(dict) --*

        MariaDB parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **MySqlParameters** *(dict) --*

        MySQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **PostgreSqlParameters** *(dict) --*

        PostgreSQL parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **PrestoParameters** *(dict) --*

        Presto parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Catalog** *(string) --*

          Catalog.

      - **RdsParameters** *(dict) --*

        RDS parameters.

        - **InstanceId** *(string) --*

          Instance ID.

        - **Database** *(string) --*

          Database.

      - **RedshiftParameters** *(dict) --*

        Redshift parameters.

        - **Host** *(string) --*

          Host. This can be blank if the ``ClusterId`` is provided.

        - **Port** *(integer) --*

          Port. This can be blank if the ``ClusterId`` is provided.

        - **Database** *(string) --*

          Database.

        - **ClusterId** *(string) --*

          Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

      - **S3Parameters** *(dict) --*

        S3 parameters.

        - **ManifestFileLocation** *(dict) --*

          Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
          the console.

          - **Bucket** *(string) --*

            Amazon S3 bucket.

          - **Key** *(string) --*

            Amazon S3 key that identifies an object.

      - **ServiceNowParameters** *(dict) --*

        ServiceNow parameters.

        - **SiteBaseUrl** *(string) --*

          URL of the base site.

      - **SnowflakeParameters** *(dict) --*

        Snowflake parameters.

        - **Host** *(string) --*

          Host.

        - **Database** *(string) --*

          Database.

        - **Warehouse** *(string) --*

          Warehouse.

      - **SparkParameters** *(dict) --*

        Spark parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

      - **SqlServerParameters** *(dict) --*

        SQL Server parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **TeradataParameters** *(dict) --*

        Teradata parameters.

        - **Host** *(string) --*

          Host.

        - **Port** *(integer) --*

          Port.

        - **Database** *(string) --*

          Database.

      - **TwitterParameters** *(dict) --*

        Twitter parameters.

        - **Query** *(string) --*

          Twitter query string.

        - **MaxRows** *(integer) --*

          Maximum number of rows to query Twitter.

    - **VpcConnectionProperties** *(dict) --*

      The VPC connection information. You need to use this parameter only when you want QuickSight
      to use a VPC connection when connecting to your underlying source.

      - **VpcConnectionArn** *(string) --*

        VPC connection ARN.

    - **SslProperties** *(dict) --*

      SSL properties that apply when QuickSight connects to your underlying source.

      - **DisableSsl** *(boolean) --*

        A boolean flag to control whether SSL should be disabled.

    - **ErrorInfo** *(dict) --*

      Error information from the last update or the creation of the data source.

      - **Type** *(string) --*

        Error type.

      - **Message** *(string) --*

        Error message.
    """


_ClientListDataSourcesResponseTypeDef = TypedDict(
    "_ClientListDataSourcesResponseTypeDef",
    {
        "DataSources": List[ClientListDataSourcesResponseDataSourcesTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListDataSourcesResponseTypeDef(_ClientListDataSourcesResponseTypeDef):
    """
    Type definition for `ClientListDataSources` `Response`

    - **DataSources** *(list) --*

      A list of data sources.

      - *(dict) --*

        The structure of a data source.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the data source.

        - **DataSourceId** *(string) --*

          The ID of the data source. This is unique per AWS Region per AWS account.

        - **Name** *(string) --*

          A display name for the data source.

        - **Type** *(string) --*

          The type of the data source. This indicates which database engine the data source connects
          to.

        - **Status** *(string) --*

          The http status of the request.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **LastUpdatedTime** *(datetime) --*

          The last time this was updated.

        - **DataSourceParameters** *(dict) --*

          The parameters QuickSight uses to connect to your underlying source. This is a variant
          type structure. At most one of the attributes should be non-null for this structure to be
          valid.

          - **AmazonElasticsearchParameters** *(dict) --*

            Amazon Elasticsearch parameters.

            - **Domain** *(string) --*

              The Amazon Elasticsearch domain.

          - **AthenaParameters** *(dict) --*

            Athena parameters.

            - **WorkGroup** *(string) --*

              The workgroup that Athena uses.

          - **AuroraParameters** *(dict) --*

            Aurora MySQL parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **AuroraPostgreSqlParameters** *(dict) --*

            Aurora PostgreSQL parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **AwsIotAnalyticsParameters** *(dict) --*

            AWS IoT Analytics parameters.

            - **DataSetName** *(string) --*

              Dataset name.

          - **JiraParameters** *(dict) --*

            Jira parameters.

            - **SiteBaseUrl** *(string) --*

              The base URL of the Jira site.

          - **MariaDbParameters** *(dict) --*

            MariaDB parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **MySqlParameters** *(dict) --*

            MySQL parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **PostgreSqlParameters** *(dict) --*

            PostgreSQL parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **PrestoParameters** *(dict) --*

            Presto parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Catalog** *(string) --*

              Catalog.

          - **RdsParameters** *(dict) --*

            RDS parameters.

            - **InstanceId** *(string) --*

              Instance ID.

            - **Database** *(string) --*

              Database.

          - **RedshiftParameters** *(dict) --*

            Redshift parameters.

            - **Host** *(string) --*

              Host. This can be blank if the ``ClusterId`` is provided.

            - **Port** *(integer) --*

              Port. This can be blank if the ``ClusterId`` is provided.

            - **Database** *(string) --*

              Database.

            - **ClusterId** *(string) --*

              Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

          - **S3Parameters** *(dict) --*

            S3 parameters.

            - **ManifestFileLocation** *(dict) --*

              Location of the Amazon S3 manifest file. This is NULL if the manifest file was
              uploaded in the console.

              - **Bucket** *(string) --*

                Amazon S3 bucket.

              - **Key** *(string) --*

                Amazon S3 key that identifies an object.

          - **ServiceNowParameters** *(dict) --*

            ServiceNow parameters.

            - **SiteBaseUrl** *(string) --*

              URL of the base site.

          - **SnowflakeParameters** *(dict) --*

            Snowflake parameters.

            - **Host** *(string) --*

              Host.

            - **Database** *(string) --*

              Database.

            - **Warehouse** *(string) --*

              Warehouse.

          - **SparkParameters** *(dict) --*

            Spark parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

          - **SqlServerParameters** *(dict) --*

            SQL Server parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **TeradataParameters** *(dict) --*

            Teradata parameters.

            - **Host** *(string) --*

              Host.

            - **Port** *(integer) --*

              Port.

            - **Database** *(string) --*

              Database.

          - **TwitterParameters** *(dict) --*

            Twitter parameters.

            - **Query** *(string) --*

              Twitter query string.

            - **MaxRows** *(integer) --*

              Maximum number of rows to query Twitter.

        - **VpcConnectionProperties** *(dict) --*

          The VPC connection information. You need to use this parameter only when you want
          QuickSight to use a VPC connection when connecting to your underlying source.

          - **VpcConnectionArn** *(string) --*

            VPC connection ARN.

        - **SslProperties** *(dict) --*

          SSL properties that apply when QuickSight connects to your underlying source.

          - **DisableSsl** *(boolean) --*

            A boolean flag to control whether SSL should be disabled.

        - **ErrorInfo** *(dict) --*

          Error information from the last update or the creation of the data source.

          - **Type** *(string) --*

            Error type.

          - **Message** *(string) --*

            Error message.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListGroupMembershipsResponseGroupMemberListTypeDef = TypedDict(
    "_ClientListGroupMembershipsResponseGroupMemberListTypeDef",
    {"Arn": str, "MemberName": str},
    total=False,
)


class ClientListGroupMembershipsResponseGroupMemberListTypeDef(
    _ClientListGroupMembershipsResponseGroupMemberListTypeDef
):
    """
    Type definition for `ClientListGroupMembershipsResponse` `GroupMemberList`

    A member of an Amazon QuickSight group. Currently, group members must be users. Groups can't be
    members of another group. .

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group member (user).

    - **MemberName** *(string) --*

      The name of the group member (user).
    """


_ClientListGroupMembershipsResponseTypeDef = TypedDict(
    "_ClientListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberList": List[ClientListGroupMembershipsResponseGroupMemberListTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListGroupMembershipsResponseTypeDef(_ClientListGroupMembershipsResponseTypeDef):
    """
    Type definition for `ClientListGroupMemberships` `Response`

    - **GroupMemberList** *(list) --*

      The list of the members of the group.

      - *(dict) --*

        A member of an Amazon QuickSight group. Currently, group members must be users. Groups can't
        be members of another group. .

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) for the group member (user).

        - **MemberName** *(string) --*

          The name of the group member (user).

    - **NextToken** *(string) --*

      A pagination token that can be used in a subsequent request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListGroupsResponseGroupListTypeDef = TypedDict(
    "_ClientListGroupsResponseGroupListTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)


class ClientListGroupsResponseGroupListTypeDef(_ClientListGroupsResponseGroupListTypeDef):
    """
    Type definition for `ClientListGroupsResponse` `GroupList`

    A *group* in Amazon QuickSight consists of a set of users. You can use groups to make it easier
    to manage access and security. Currently, an Amazon QuickSight subscription can't contain more
    than 500 Amazon QuickSight groups.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group.

    - **GroupName** *(string) --*

      The name of the group.

    - **Description** *(string) --*

      The group description.

    - **PrincipalId** *(string) --*

      The principal ID of the group.
    """


_ClientListGroupsResponseTypeDef = TypedDict(
    "_ClientListGroupsResponseTypeDef",
    {
        "GroupList": List[ClientListGroupsResponseGroupListTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListGroupsResponseTypeDef(_ClientListGroupsResponseTypeDef):
    """
    Type definition for `ClientListGroups` `Response`

    - **GroupList** *(list) --*

      The list of the groups.

      - *(dict) --*

        A *group* in Amazon QuickSight consists of a set of users. You can use groups to make it
        easier to manage access and security. Currently, an Amazon QuickSight subscription can't
        contain more than 500 Amazon QuickSight groups.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) for the group.

        - **GroupName** *(string) --*

          The name of the group.

        - **Description** *(string) --*

          The group description.

        - **PrincipalId** *(string) --*

          The principal ID of the group.

    - **NextToken** *(string) --*

      A pagination token that can be used in a subsequent request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef = TypedDict(
    "_ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef",
    {"AssignmentName": str, "PolicyArn": str},
    total=False,
)


class ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef(
    _ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef
):
    """
    Type definition for `ClientListIamPolicyAssignmentsForUserResponse` `ActiveAssignments`

    The active IAM policy assignment.

    - **AssignmentName** *(string) --*

      A name for the IAM policy assignment.

    - **PolicyArn** *(string) --*

      The ARN of the resource.
    """


_ClientListIamPolicyAssignmentsForUserResponseTypeDef = TypedDict(
    "_ClientListIamPolicyAssignmentsForUserResponseTypeDef",
    {
        "ActiveAssignments": List[
            ClientListIamPolicyAssignmentsForUserResponseActiveAssignmentsTypeDef
        ],
        "RequestId": str,
        "NextToken": str,
        "Status": int,
    },
    total=False,
)


class ClientListIamPolicyAssignmentsForUserResponseTypeDef(
    _ClientListIamPolicyAssignmentsForUserResponseTypeDef
):
    """
    Type definition for `ClientListIamPolicyAssignmentsForUser` `Response`

    - **ActiveAssignments** *(list) --*

      Active assignments for this user.

      - *(dict) --*

        The active IAM policy assignment.

        - **AssignmentName** *(string) --*

          A name for the IAM policy assignment.

        - **PolicyArn** *(string) --*

          The ARN of the resource.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef = TypedDict(
    "_ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef",
    {"AssignmentName": str, "AssignmentStatus": str},
    total=False,
)


class ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef(
    _ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef
):
    """
    Type definition for `ClientListIamPolicyAssignmentsResponse` `IAMPolicyAssignments`

    IAM policy assignment Summary.

    - **AssignmentName** *(string) --*

      Assignment name.

    - **AssignmentStatus** *(string) --*

      Assignment status.
    """


_ClientListIamPolicyAssignmentsResponseTypeDef = TypedDict(
    "_ClientListIamPolicyAssignmentsResponseTypeDef",
    {
        "IAMPolicyAssignments": List[
            ClientListIamPolicyAssignmentsResponseIAMPolicyAssignmentsTypeDef
        ],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListIamPolicyAssignmentsResponseTypeDef(_ClientListIamPolicyAssignmentsResponseTypeDef):
    """
    Type definition for `ClientListIamPolicyAssignments` `Response`

    - **IAMPolicyAssignments** *(list) --*

      Information describing the IAM policy assignments.

      - *(dict) --*

        IAM policy assignment Summary.

        - **AssignmentName** *(string) --*

          Assignment name.

        - **AssignmentStatus** *(string) --*

          Assignment status.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListIngestionsResponseIngestionsErrorInfoTypeDef = TypedDict(
    "_ClientListIngestionsResponseIngestionsErrorInfoTypeDef",
    {"Type": str, "Message": str},
    total=False,
)


class ClientListIngestionsResponseIngestionsErrorInfoTypeDef(
    _ClientListIngestionsResponseIngestionsErrorInfoTypeDef
):
    """
    Type definition for `ClientListIngestionsResponseIngestions` `ErrorInfo`

    Error information for this ingestion.

    - **Type** *(string) --*

      Error type.

    - **Message** *(string) --*

      Error essage.
    """


_ClientListIngestionsResponseIngestionsQueueInfoTypeDef = TypedDict(
    "_ClientListIngestionsResponseIngestionsQueueInfoTypeDef",
    {"WaitingOnIngestion": str, "QueuedIngestion": str},
    total=False,
)


class ClientListIngestionsResponseIngestionsQueueInfoTypeDef(
    _ClientListIngestionsResponseIngestionsQueueInfoTypeDef
):
    """
    Type definition for `ClientListIngestionsResponseIngestions` `QueueInfo`

    Information on queued dataset SPICE ingestion.

    - **WaitingOnIngestion** *(string) --*

      The ID of the queued ingestion.

    - **QueuedIngestion** *(string) --*

      The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing ingestion to
      complete.
    """


_ClientListIngestionsResponseIngestionsRowInfoTypeDef = TypedDict(
    "_ClientListIngestionsResponseIngestionsRowInfoTypeDef",
    {"RowsIngested": int, "RowsDropped": int},
    total=False,
)


class ClientListIngestionsResponseIngestionsRowInfoTypeDef(
    _ClientListIngestionsResponseIngestionsRowInfoTypeDef
):
    """
    Type definition for `ClientListIngestionsResponseIngestions` `RowInfo`

    Information on rows during a data set SPICE ingestion.

    - **RowsIngested** *(integer) --*

      The number of rows that were ingested.

    - **RowsDropped** *(integer) --*

      The number of rows that were not ingested.
    """


_ClientListIngestionsResponseIngestionsTypeDef = TypedDict(
    "_ClientListIngestionsResponseIngestionsTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": str,
        "ErrorInfo": ClientListIngestionsResponseIngestionsErrorInfoTypeDef,
        "RowInfo": ClientListIngestionsResponseIngestionsRowInfoTypeDef,
        "QueueInfo": ClientListIngestionsResponseIngestionsQueueInfoTypeDef,
        "CreatedTime": datetime,
        "IngestionTimeInSeconds": int,
        "IngestionSizeInBytes": int,
        "RequestSource": str,
        "RequestType": str,
    },
    total=False,
)


class ClientListIngestionsResponseIngestionsTypeDef(_ClientListIngestionsResponseIngestionsTypeDef):
    """
    Type definition for `ClientListIngestionsResponse` `Ingestions`

    Information on the SPICE ingestion for a dataset.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) of the resource.

    - **IngestionId** *(string) --*

      Ingestion ID.

    - **IngestionStatus** *(string) --*

      Ingestion status.

    - **ErrorInfo** *(dict) --*

      Error information for this ingestion.

      - **Type** *(string) --*

        Error type.

      - **Message** *(string) --*

        Error essage.

    - **RowInfo** *(dict) --*

      Information on rows during a data set SPICE ingestion.

      - **RowsIngested** *(integer) --*

        The number of rows that were ingested.

      - **RowsDropped** *(integer) --*

        The number of rows that were not ingested.

    - **QueueInfo** *(dict) --*

      Information on queued dataset SPICE ingestion.

      - **WaitingOnIngestion** *(string) --*

        The ID of the queued ingestion.

      - **QueuedIngestion** *(string) --*

        The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing ingestion
        to complete.

    - **CreatedTime** *(datetime) --*

      The time this ingestion started.

    - **IngestionTimeInSeconds** *(integer) --*

      The time this ingestion took, measured in seconds.

    - **IngestionSizeInBytes** *(integer) --*

      Size of the data ingested in bytes.

    - **RequestSource** *(string) --*

      Event source for this ingestion.

    - **RequestType** *(string) --*

      Type of this ingestion.
    """


_ClientListIngestionsResponseTypeDef = TypedDict(
    "_ClientListIngestionsResponseTypeDef",
    {
        "Ingestions": List[ClientListIngestionsResponseIngestionsTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListIngestionsResponseTypeDef(_ClientListIngestionsResponseTypeDef):
    """
    Type definition for `ClientListIngestions` `Response`

    - **Ingestions** *(list) --*

      A list of the ingestions.

      - *(dict) --*

        Information on the SPICE ingestion for a dataset.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) of the resource.

        - **IngestionId** *(string) --*

          Ingestion ID.

        - **IngestionStatus** *(string) --*

          Ingestion status.

        - **ErrorInfo** *(dict) --*

          Error information for this ingestion.

          - **Type** *(string) --*

            Error type.

          - **Message** *(string) --*

            Error essage.

        - **RowInfo** *(dict) --*

          Information on rows during a data set SPICE ingestion.

          - **RowsIngested** *(integer) --*

            The number of rows that were ingested.

          - **RowsDropped** *(integer) --*

            The number of rows that were not ingested.

        - **QueueInfo** *(dict) --*

          Information on queued dataset SPICE ingestion.

          - **WaitingOnIngestion** *(string) --*

            The ID of the queued ingestion.

          - **QueuedIngestion** *(string) --*

            The ID of the ongoing ingestion. The queued ingestion is waiting for the ongoing
            ingestion to complete.

        - **CreatedTime** *(datetime) --*

          The time this ingestion started.

        - **IngestionTimeInSeconds** *(integer) --*

          The time this ingestion took, measured in seconds.

        - **IngestionSizeInBytes** *(integer) --*

          Size of the data ingested in bytes.

        - **RequestSource** *(string) --*

          Event source for this ingestion.

        - **RequestType** *(string) --*

          Type of this ingestion.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListTagsForResourceResponseTagsTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTagsTypeDef", {"Key": str, "Value": str}, total=False
)


class ClientListTagsForResourceResponseTagsTypeDef(_ClientListTagsForResourceResponseTagsTypeDef):
    """
    Type definition for `ClientListTagsForResourceResponse` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --*

      Tag key.

    - **Value** *(string) --*

      Tag value.
    """


_ClientListTagsForResourceResponseTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTypeDef",
    {"Tags": List[ClientListTagsForResourceResponseTagsTypeDef], "RequestId": str, "Status": int},
    total=False,
)


class ClientListTagsForResourceResponseTypeDef(_ClientListTagsForResourceResponseTypeDef):
    """
    Type definition for `ClientListTagsForResource` `Response`

    - **Tags** *(list) --*

      Contains a map of the key-value pairs for the resource tag or tags assigned to the resource.

      - *(dict) --*

        The keys of the key-value pairs for the resource tag or tags assigned to the resource.

        - **Key** *(string) --*

          Tag key.

        - **Value** *(string) --*

          Tag value.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientListTemplateAliasesResponseTemplateAliasListTypeDef = TypedDict(
    "_ClientListTemplateAliasesResponseTemplateAliasListTypeDef",
    {"AliasName": str, "Arn": str, "TemplateVersionNumber": int},
    total=False,
)


class ClientListTemplateAliasesResponseTemplateAliasListTypeDef(
    _ClientListTemplateAliasesResponseTemplateAliasListTypeDef
):
    """
    Type definition for `ClientListTemplateAliasesResponse` `TemplateAliasList`

    The template alias.

    - **AliasName** *(string) --*

      The display name of the template alias.

    - **Arn** *(string) --*

      The ARN of the template alias.

    - **TemplateVersionNumber** *(integer) --*

      The version number of the template alias.
    """


_ClientListTemplateAliasesResponseTypeDef = TypedDict(
    "_ClientListTemplateAliasesResponseTypeDef",
    {
        "TemplateAliasList": List[ClientListTemplateAliasesResponseTemplateAliasListTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
    },
    total=False,
)


class ClientListTemplateAliasesResponseTypeDef(_ClientListTemplateAliasesResponseTypeDef):
    """
    Type definition for `ClientListTemplateAliases` `Response`

    - **TemplateAliasList** *(list) --*

      A structure containing the list of template aliases.

      - *(dict) --*

        The template alias.

        - **AliasName** *(string) --*

          The display name of the template alias.

        - **Arn** *(string) --*

          The ARN of the template alias.

        - **TemplateVersionNumber** *(integer) --*

          The version number of the template alias.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.
    """


_ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef = TypedDict(
    "_ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef",
    {"Arn": str, "VersionNumber": int, "CreatedTime": datetime, "Status": str, "Description": str},
    total=False,
)


class ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef(
    _ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef
):
    """
    Type definition for `ClientListTemplateVersionsResponse` `TemplateVersionSummaryList`

    The template version.

    - **Arn** *(string) --*

      The ARN of the template version.

    - **VersionNumber** *(integer) --*

      The version number of the template version.

    - **CreatedTime** *(datetime) --*

      The time this was created.

    - **Status** *(string) --*

      The status of the template version.

    - **Description** *(string) --*

      The desription of the template version.
    """


_ClientListTemplateVersionsResponseTypeDef = TypedDict(
    "_ClientListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionSummaryList": List[
            ClientListTemplateVersionsResponseTemplateVersionSummaryListTypeDef
        ],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientListTemplateVersionsResponseTypeDef(_ClientListTemplateVersionsResponseTypeDef):
    """
    Type definition for `ClientListTemplateVersions` `Response`

    - **TemplateVersionSummaryList** *(list) --*

      A structure containing a list of all the versions of the specified template.

      - *(dict) --*

        The template version.

        - **Arn** *(string) --*

          The ARN of the template version.

        - **VersionNumber** *(integer) --*

          The version number of the template version.

        - **CreatedTime** *(datetime) --*

          The time this was created.

        - **Status** *(string) --*

          The status of the template version.

        - **Description** *(string) --*

          The desription of the template version.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientListTemplatesResponseTemplateSummaryListTypeDef = TypedDict(
    "_ClientListTemplatesResponseTemplateSummaryListTypeDef",
    {
        "Arn": str,
        "TemplateId": str,
        "Name": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)


class ClientListTemplatesResponseTemplateSummaryListTypeDef(
    _ClientListTemplatesResponseTemplateSummaryListTypeDef
):
    """
    Type definition for `ClientListTemplatesResponse` `TemplateSummaryList`

    The template summary.

    - **Arn** *(string) --*

      A summary of a template.

    - **TemplateId** *(string) --*

      The ID of the template. This is unique per region per AWS account.

    - **Name** *(string) --*

      A display name for the template.

    - **LatestVersionNumber** *(integer) --*

      A structure containing a list of version numbers for the template summary.

    - **CreatedTime** *(datetime) --*

      The last time this was created.

    - **LastUpdatedTime** *(datetime) --*

      The last time this was updated.
    """


_ClientListTemplatesResponseTypeDef = TypedDict(
    "_ClientListTemplatesResponseTypeDef",
    {
        "TemplateSummaryList": List[ClientListTemplatesResponseTemplateSummaryListTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientListTemplatesResponseTypeDef(_ClientListTemplatesResponseTypeDef):
    """
    Type definition for `ClientListTemplates` `Response`

    - **TemplateSummaryList** *(list) --*

      A structure containing information about the templates in the list.

      - *(dict) --*

        The template summary.

        - **Arn** *(string) --*

          A summary of a template.

        - **TemplateId** *(string) --*

          The ID of the template. This is unique per region per AWS account.

        - **Name** *(string) --*

          A display name for the template.

        - **LatestVersionNumber** *(integer) --*

          A structure containing a list of version numbers for the template summary.

        - **CreatedTime** *(datetime) --*

          The last time this was created.

        - **LastUpdatedTime** *(datetime) --*

          The last time this was updated.

    - **NextToken** *(string) --*

      The token for the next set of results, or null if there are no more results.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientListUserGroupsResponseGroupListTypeDef = TypedDict(
    "_ClientListUserGroupsResponseGroupListTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)


class ClientListUserGroupsResponseGroupListTypeDef(_ClientListUserGroupsResponseGroupListTypeDef):
    """
    Type definition for `ClientListUserGroupsResponse` `GroupList`

    A *group* in Amazon QuickSight consists of a set of users. You can use groups to make it easier
    to manage access and security. Currently, an Amazon QuickSight subscription can't contain more
    than 500 Amazon QuickSight groups.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group.

    - **GroupName** *(string) --*

      The name of the group.

    - **Description** *(string) --*

      The group description.

    - **PrincipalId** *(string) --*

      The principal ID of the group.
    """


_ClientListUserGroupsResponseTypeDef = TypedDict(
    "_ClientListUserGroupsResponseTypeDef",
    {
        "GroupList": List[ClientListUserGroupsResponseGroupListTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListUserGroupsResponseTypeDef(_ClientListUserGroupsResponseTypeDef):
    """
    Type definition for `ClientListUserGroups` `Response`

    - **GroupList** *(list) --*

      The list of groups the user is a member of.

      - *(dict) --*

        A *group* in Amazon QuickSight consists of a set of users. You can use groups to make it
        easier to manage access and security. Currently, an Amazon QuickSight subscription can't
        contain more than 500 Amazon QuickSight groups.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) for the group.

        - **GroupName** *(string) --*

          The name of the group.

        - **Description** *(string) --*

          The group description.

        - **PrincipalId** *(string) --*

          The principal ID of the group.

    - **NextToken** *(string) --*

      A pagination token that can be used in a subsequent request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The HTTP status of the request.
    """


_ClientListUsersResponseUserListTypeDef = TypedDict(
    "_ClientListUsersResponseUserListTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": str,
        "IdentityType": str,
        "Active": bool,
        "PrincipalId": str,
    },
    total=False,
)


class ClientListUsersResponseUserListTypeDef(_ClientListUsersResponseUserListTypeDef):
    """
    Type definition for `ClientListUsersResponse` `UserList`

    A registered user of Amazon QuickSight. Currently, an Amazon QuickSight subscription can't
    contain more than 20 million users.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the user.

    - **UserName** *(string) --*

      The user's user name.

    - **Email** *(string) --*

      The user's email address.

    - **Role** *(string) --*

      The Amazon QuickSight role for the user. The user role can be one of the following:.

      * ``READER`` : A user who has read-only access to dashboards.

      * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

      * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

      * ``RESTRICTED_READER`` : This role isn't currently available for use.

      * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

    - **IdentityType** *(string) --*

      The type of identity authentication used by the user.

    - **Active** *(boolean) --*

      Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or an
      AD user, that user is inactive until they sign in and provide a password.

    - **PrincipalId** *(string) --*

      The principal ID of the user.
    """


_ClientListUsersResponseTypeDef = TypedDict(
    "_ClientListUsersResponseTypeDef",
    {
        "UserList": List[ClientListUsersResponseUserListTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientListUsersResponseTypeDef(_ClientListUsersResponseTypeDef):
    """
    Type definition for `ClientListUsers` `Response`

    - **UserList** *(list) --*

      The list of users.

      - *(dict) --*

        A registered user of Amazon QuickSight. Currently, an Amazon QuickSight subscription can't
        contain more than 20 million users.

        - **Arn** *(string) --*

          The Amazon Resource name (ARN) for the user.

        - **UserName** *(string) --*

          The user's user name.

        - **Email** *(string) --*

          The user's email address.

        - **Role** *(string) --*

          The Amazon QuickSight role for the user. The user role can be one of the following:.

          * ``READER`` : A user who has read-only access to dashboards.

          * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

          * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

          * ``RESTRICTED_READER`` : This role isn't currently available for use.

          * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

        - **IdentityType** *(string) --*

          The type of identity authentication used by the user.

        - **Active** *(boolean) --*

          Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or
          an AD user, that user is inactive until they sign in and provide a password.

        - **PrincipalId** *(string) --*

          The principal ID of the user.

    - **NextToken** *(string) --*

      A pagination token that can be used in a subsequent request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientRegisterUserResponseUserTypeDef = TypedDict(
    "_ClientRegisterUserResponseUserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": str,
        "IdentityType": str,
        "Active": bool,
        "PrincipalId": str,
    },
    total=False,
)


class ClientRegisterUserResponseUserTypeDef(_ClientRegisterUserResponseUserTypeDef):
    """
    Type definition for `ClientRegisterUserResponse` `User`

    The user name.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the user.

    - **UserName** *(string) --*

      The user's user name.

    - **Email** *(string) --*

      The user's email address.

    - **Role** *(string) --*

      The Amazon QuickSight role for the user. The user role can be one of the following:.

      * ``READER`` : A user who has read-only access to dashboards.

      * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

      * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

      * ``RESTRICTED_READER`` : This role isn't currently available for use.

      * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

    - **IdentityType** *(string) --*

      The type of identity authentication used by the user.

    - **Active** *(boolean) --*

      Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or an
      AD user, that user is inactive until they sign in and provide a password.

    - **PrincipalId** *(string) --*

      The principal ID of the user.
    """


_ClientRegisterUserResponseTypeDef = TypedDict(
    "_ClientRegisterUserResponseTypeDef",
    {
        "User": ClientRegisterUserResponseUserTypeDef,
        "UserInvitationUrl": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientRegisterUserResponseTypeDef(_ClientRegisterUserResponseTypeDef):
    """
    Type definition for `ClientRegisterUser` `Response`

    - **User** *(dict) --*

      The user name.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the user.

      - **UserName** *(string) --*

        The user's user name.

      - **Email** *(string) --*

        The user's email address.

      - **Role** *(string) --*

        The Amazon QuickSight role for the user. The user role can be one of the following:.

        * ``READER`` : A user who has read-only access to dashboards.

        * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

        * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

        * ``RESTRICTED_READER`` : This role isn't currently available for use.

        * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

      - **IdentityType** *(string) --*

        The type of identity authentication used by the user.

      - **Active** *(boolean) --*

        Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or
        an AD user, that user is inactive until they sign in and provide a password.

      - **PrincipalId** *(string) --*

        The principal ID of the user.

    - **UserInvitationUrl** *(string) --*

      The URL the user visits to complete registration and provide a password. This is returned only
      for users with an identity type of ``QUICKSIGHT`` .

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientTagResourceResponseTypeDef = TypedDict(
    "_ClientTagResourceResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientTagResourceResponseTypeDef(_ClientTagResourceResponseTypeDef):
    """
    Type definition for `ClientTagResource` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientTagResourceTagsTypeDef = TypedDict(
    "_ClientTagResourceTagsTypeDef", {"Key": str, "Value": str}
)


class ClientTagResourceTagsTypeDef(_ClientTagResourceTagsTypeDef):
    """
    Type definition for `ClientTagResource` `Tags`

    The keys of the key-value pairs for the resource tag or tags assigned to the resource.

    - **Key** *(string) --* **[REQUIRED]**

      Tag key.

    - **Value** *(string) --* **[REQUIRED]**

      Tag value.
    """


_ClientUntagResourceResponseTypeDef = TypedDict(
    "_ClientUntagResourceResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)


class ClientUntagResourceResponseTypeDef(_ClientUntagResourceResponseTypeDef):
    """
    Type definition for `ClientUntagResource` `Response`

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef = TypedDict(
    "_ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef",
    {"AvailabilityStatus": str},
    total=False,
)


class ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef(
    _ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef
):
    """
    Type definition for `ClientUpdateDashboardDashboardPublishOptions` `AdHocFilteringOption`

    Ad hoc filtering option.

    - **AvailabilityStatus** *(string) --*

      Availability status.
    """


_ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef = TypedDict(
    "_ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef",
    {"AvailabilityStatus": str},
    total=False,
)


class ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef(
    _ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef
):
    """
    Type definition for `ClientUpdateDashboardDashboardPublishOptions` `ExportToCSVOption`

    Export to CSV option.

    - **AvailabilityStatus** *(string) --*

      Availability status.
    """


_ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef = TypedDict(
    "_ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef",
    {"VisibilityState": str},
    total=False,
)


class ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef(
    _ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef
):
    """
    Type definition for `ClientUpdateDashboardDashboardPublishOptions` `SheetControlsOption`

    Sheet controls option.

    - **VisibilityState** *(string) --*

      Visibility state.
    """


_ClientUpdateDashboardDashboardPublishOptionsTypeDef = TypedDict(
    "_ClientUpdateDashboardDashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": ClientUpdateDashboardDashboardPublishOptionsAdHocFilteringOptionTypeDef,
        "ExportToCSVOption": ClientUpdateDashboardDashboardPublishOptionsExportToCSVOptionTypeDef,
        "SheetControlsOption": ClientUpdateDashboardDashboardPublishOptionsSheetControlsOptionTypeDef,
    },
    total=False,
)


class ClientUpdateDashboardDashboardPublishOptionsTypeDef(
    _ClientUpdateDashboardDashboardPublishOptionsTypeDef
):
    """
    Type definition for `ClientUpdateDashboard` `DashboardPublishOptions`

    Publishing options when creating a dashboard.

    * AvailabilityStatus for AdHocFilteringOption - This can be either ``ENABLED`` or ``DISABLED`` .
    When This is set to set to ``DISABLED`` , QuickSight disables the left filter pane on the
    published dashboard, which can be used for AdHoc filtering. Enabled by default.

    * AvailabilityStatus for ExportToCSVOption - This can be either ``ENABLED`` or ``DISABLED`` .
    The visual option to export data to CSV is disabled when this is set to ``DISABLED`` . Enabled
    by default.

    * VisibilityState for SheetControlsOption - This can be either ``COLLAPSED`` or ``EXPANDED`` .
    The sheet controls pane is collapsed by default when set to true. Collapsed by default.

    - **AdHocFilteringOption** *(dict) --*

      Ad hoc filtering option.

      - **AvailabilityStatus** *(string) --*

        Availability status.

    - **ExportToCSVOption** *(dict) --*

      Export to CSV option.

      - **AvailabilityStatus** *(string) --*

        Availability status.

    - **SheetControlsOption** *(dict) --*

      Sheet controls option.

      - **VisibilityState** *(string) --*

        Visibility state.
    """


_ClientUpdateDashboardParametersDateTimeParametersTypeDef = TypedDict(
    "_ClientUpdateDashboardParametersDateTimeParametersTypeDef",
    {"Name": str, "Values": List[datetime]},
)


class ClientUpdateDashboardParametersDateTimeParametersTypeDef(
    _ClientUpdateDashboardParametersDateTimeParametersTypeDef
):
    """
    Type definition for `ClientUpdateDashboardParameters` `DateTimeParameters`

    Date time parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(datetime) --*
    """


_ClientUpdateDashboardParametersDecimalParametersTypeDef = TypedDict(
    "_ClientUpdateDashboardParametersDecimalParametersTypeDef", {"Name": str, "Values": List[float]}
)


class ClientUpdateDashboardParametersDecimalParametersTypeDef(
    _ClientUpdateDashboardParametersDecimalParametersTypeDef
):
    """
    Type definition for `ClientUpdateDashboardParameters` `DecimalParameters`

    Decimal parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(float) --*
    """


_ClientUpdateDashboardParametersIntegerParametersTypeDef = TypedDict(
    "_ClientUpdateDashboardParametersIntegerParametersTypeDef", {"Name": str, "Values": List[int]}
)


class ClientUpdateDashboardParametersIntegerParametersTypeDef(
    _ClientUpdateDashboardParametersIntegerParametersTypeDef
):
    """
    Type definition for `ClientUpdateDashboardParameters` `IntegerParameters`

    Integer parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(integer) --*
    """


_ClientUpdateDashboardParametersStringParametersTypeDef = TypedDict(
    "_ClientUpdateDashboardParametersStringParametersTypeDef", {"Name": str, "Values": List[str]}
)


class ClientUpdateDashboardParametersStringParametersTypeDef(
    _ClientUpdateDashboardParametersStringParametersTypeDef
):
    """
    Type definition for `ClientUpdateDashboardParameters` `StringParameters`

    String parameter.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the dataset.

    - **Values** *(list) --* **[REQUIRED]**

      Values.

      - *(string) --*
    """


_ClientUpdateDashboardParametersTypeDef = TypedDict(
    "_ClientUpdateDashboardParametersTypeDef",
    {
        "StringParameters": List[ClientUpdateDashboardParametersStringParametersTypeDef],
        "IntegerParameters": List[ClientUpdateDashboardParametersIntegerParametersTypeDef],
        "DecimalParameters": List[ClientUpdateDashboardParametersDecimalParametersTypeDef],
        "DateTimeParameters": List[ClientUpdateDashboardParametersDateTimeParametersTypeDef],
    },
    total=False,
)


class ClientUpdateDashboardParametersTypeDef(_ClientUpdateDashboardParametersTypeDef):
    """
    Type definition for `ClientUpdateDashboard` `Parameters`

    A structure that contains the parameters of the dashboard.

    - **StringParameters** *(list) --*

      String parameters.

      - *(dict) --*

        String parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(string) --*

    - **IntegerParameters** *(list) --*

      Integer parameters.

      - *(dict) --*

        Integer parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(integer) --*

    - **DecimalParameters** *(list) --*

      Decimal parameters.

      - *(dict) --*

        Decimal parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(float) --*

    - **DateTimeParameters** *(list) --*

      DateTime parameters.

      - *(dict) --*

        Date time parameter.

        - **Name** *(string) --* **[REQUIRED]**

          A display name for the dataset.

        - **Values** *(list) --* **[REQUIRED]**

          Values.

          - *(datetime) --*
    """


_ClientUpdateDashboardPermissionsGrantPermissionsTypeDef = TypedDict(
    "_ClientUpdateDashboardPermissionsGrantPermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDashboardPermissionsGrantPermissionsTypeDef(
    _ClientUpdateDashboardPermissionsGrantPermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDashboardPermissions` `GrantPermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDashboardPermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientUpdateDashboardPermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientUpdateDashboardPermissionsResponsePermissionsTypeDef(
    _ClientUpdateDashboardPermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDashboardPermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDashboardPermissionsResponseTypeDef = TypedDict(
    "_ClientUpdateDashboardPermissionsResponseTypeDef",
    {
        "DashboardArn": str,
        "DashboardId": str,
        "Permissions": List[ClientUpdateDashboardPermissionsResponsePermissionsTypeDef],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientUpdateDashboardPermissionsResponseTypeDef(
    _ClientUpdateDashboardPermissionsResponseTypeDef
):
    """
    Type definition for `ClientUpdateDashboardPermissions` `Response`

    - **DashboardArn** *(string) --*

      The ARN of the dashboard.

    - **DashboardId** *(string) --*

      The ID for the dashboard.

    - **Permissions** *(list) --*

      Information about the permissions on the dashboard.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDashboardPermissionsRevokePermissionsTypeDef = TypedDict(
    "_ClientUpdateDashboardPermissionsRevokePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDashboardPermissionsRevokePermissionsTypeDef(
    _ClientUpdateDashboardPermissionsRevokePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDashboardPermissions` `RevokePermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDashboardPublishedVersionResponseTypeDef = TypedDict(
    "_ClientUpdateDashboardPublishedVersionResponseTypeDef",
    {"DashboardId": str, "DashboardArn": str, "Status": int, "RequestId": str},
    total=False,
)


class ClientUpdateDashboardPublishedVersionResponseTypeDef(
    _ClientUpdateDashboardPublishedVersionResponseTypeDef
):
    """
    Type definition for `ClientUpdateDashboardPublishedVersion` `Response`

    - **DashboardId** *(string) --*

      The ID for the dashboard.

    - **DashboardArn** *(string) --*

      The ARN of the dashboard.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientUpdateDashboardResponseTypeDef = TypedDict(
    "_ClientUpdateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientUpdateDashboardResponseTypeDef(_ClientUpdateDashboardResponseTypeDef):
    """
    Type definition for `ClientUpdateDashboard` `Response`

    - **Arn** *(string) --*

      The ARN of the resource.

    - **VersionArn** *(string) --*

      The ARN of the dashboard, including the version number.

    - **DashboardId** *(string) --*

      The ID for the dashboard.

    - **CreationStatus** *(string) --*

      The creation status of the request.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef = TypedDict(
    "_ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef",
    {"DataSetPlaceholder": str, "DataSetArn": str},
)


class ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef(
    _ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef
):
    """
    Type definition for `ClientUpdateDashboardSourceEntitySourceTemplate` `DataSetReferences`

    Dataset reference.

    - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

      Dataset placeholder.

    - **DataSetArn** *(string) --* **[REQUIRED]**

      Dataset ARN.
    """


_ClientUpdateDashboardSourceEntitySourceTemplateTypeDef = TypedDict(
    "_ClientUpdateDashboardSourceEntitySourceTemplateTypeDef",
    {
        "DataSetReferences": List[
            ClientUpdateDashboardSourceEntitySourceTemplateDataSetReferencesTypeDef
        ],
        "Arn": str,
    },
)


class ClientUpdateDashboardSourceEntitySourceTemplateTypeDef(
    _ClientUpdateDashboardSourceEntitySourceTemplateTypeDef
):
    """
    Type definition for `ClientUpdateDashboardSourceEntity` `SourceTemplate`

    Source template.

    - **DataSetReferences** *(list) --* **[REQUIRED]**

      Dataset references.

      - *(dict) --*

        Dataset reference.

        - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

          Dataset placeholder.

        - **DataSetArn** *(string) --* **[REQUIRED]**

          Dataset ARN.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.
    """


_ClientUpdateDashboardSourceEntityTypeDef = TypedDict(
    "_ClientUpdateDashboardSourceEntityTypeDef",
    {"SourceTemplate": ClientUpdateDashboardSourceEntitySourceTemplateTypeDef},
    total=False,
)


class ClientUpdateDashboardSourceEntityTypeDef(_ClientUpdateDashboardSourceEntityTypeDef):
    """
    Type definition for `ClientUpdateDashboard` `SourceEntity`

    The template or analysis from which the dashboard is created. The SouceTemplate entity accepts
    the Arn of the template and also references to replacement datasets for the placeholders set
    when creating the template. The replacement datasets need to follow the same schema as the
    datasets for which placeholders were created when creating the template.

    - **SourceTemplate** *(dict) --*

      Source template.

      - **DataSetReferences** *(list) --* **[REQUIRED]**

        Dataset references.

        - *(dict) --*

          Dataset reference.

          - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

            Dataset placeholder.

          - **DataSetArn** *(string) --* **[REQUIRED]**

            Dataset ARN.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.
    """


_ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef = TypedDict(
    "_ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef",
    {"Name": str, "CountryCode": str, "Columns": List[str]},
)


class ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef(
    _ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef
):
    """
    Type definition for `ClientUpdateDataSetColumnGroups` `GeoSpatialColumnGroup`

    Geospatial column group that denotes a hierarchy.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the hierarchy.

    - **CountryCode** *(string) --* **[REQUIRED]**

      Country code.

    - **Columns** *(list) --* **[REQUIRED]**

      Columns in this hierarchy.

      - *(string) --*
    """


_ClientUpdateDataSetColumnGroupsTypeDef = TypedDict(
    "_ClientUpdateDataSetColumnGroupsTypeDef",
    {"GeoSpatialColumnGroup": ClientUpdateDataSetColumnGroupsGeoSpatialColumnGroupTypeDef},
    total=False,
)


class ClientUpdateDataSetColumnGroupsTypeDef(_ClientUpdateDataSetColumnGroupsTypeDef):
    """
    Type definition for `ClientUpdateDataSet` `ColumnGroups`

    Groupings of columns that work together in certain QuickSight features. This is a variant type
    structure. No more than one of the attributes should be non-null for this structure to be valid.

    - **GeoSpatialColumnGroup** *(dict) --*

      Geospatial column group that denotes a hierarchy.

      - **Name** *(string) --* **[REQUIRED]**

        A display name for the hierarchy.

      - **CountryCode** *(string) --* **[REQUIRED]**

        Country code.

      - **Columns** *(list) --* **[REQUIRED]**

        Columns in this hierarchy.

        - *(string) --*
    """


_RequiredClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef = TypedDict(
    "_RequiredClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    {"ColumnName": str, "NewColumnType": str},
)
_OptionalClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef = TypedDict(
    "_OptionalClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef",
    {"Format": str},
    total=False,
)


class ClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef(
    _RequiredClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
    _OptionalClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `CastColumnTypeOperation`

    A transform operation that casts a column to a different type.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Column name.

    - **NewColumnType** *(string) --* **[REQUIRED]**

      New column data type.

    - **Format** *(string) --*

      When casting a column from string to datetime type, you can supply a QuickSight supported
      format string to denote the source data format.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef",
    {"ColumnName": str, "ColumnId": str, "Expression": str},
)


class ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperation`
    `Columns`

    A calculated column for a dataset.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Column name.

    - **ColumnId** *(string) --* **[REQUIRED]**

      A unique ID to identify a calculated column. During dataset update, if the column ID of a
      calculated column matches that of an existing calculated column, QuickSight preserves the
      existing calculated column.

    - **Expression** *(string) --* **[REQUIRED]**

      An expression that defines the calculated column.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef",
    {
        "Columns": List[
            ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsTypeDef
        ]
    },
)


class ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `CreateColumnsOperation`

    An operation that creates calculated columns. Columns created in one such operation form a
    lexical closure.

    - **Columns** *(list) --* **[REQUIRED]**

      Calculated columns to create.

      - *(dict) --*

        A calculated column for a dataset.

        - **ColumnName** *(string) --* **[REQUIRED]**

          Column name.

        - **ColumnId** *(string) --* **[REQUIRED]**

          A unique ID to identify a calculated column. During dataset update, if the column ID of a
          calculated column matches that of an existing calculated column, QuickSight preserves the
          existing calculated column.

        - **Expression** *(string) --* **[REQUIRED]**

          An expression that defines the calculated column.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef",
    {"ConditionExpression": str},
)


class ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `FilterOperation`

    An operation that filters rows based on some condition.

    - **ConditionExpression** *(string) --* **[REQUIRED]**

      An expression that must evaluate to a boolean value. Rows for which the expression is
      evaluated to true are kept in the dataset.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef",
    {"ProjectedColumns": List[str]},
)


class ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `ProjectOperation`

    An operation that projects columns. Operations that come after a projection can only refer to
    projected columns.

    - **ProjectedColumns** *(list) --* **[REQUIRED]**

      Projected columns.

      - *(string) --*
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef",
    {"ColumnName": str, "NewColumnName": str},
)


class ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `RenameColumnOperation`

    An operation that renames a column.

    - **ColumnName** *(string) --* **[REQUIRED]**

      Name of the column to be renamed.

    - **NewColumnName** *(string) --* **[REQUIRED]**

      New name for the column.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef",
    {"ColumnGeographicRole": str},
    total=False,
)


class ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperation` `Tags`

    A tag for a column in a TagColumnOperation. This is a variant type structure. No more than one
    of the attributes should be non-null for this structure to be valid.

    - **ColumnGeographicRole** *(string) --*

      A geospatial role for a column.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": List[ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTagsTypeDef],
    },
)


class ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapDataTransforms` `TagColumnOperation`

    An operation that tags a column with additional information.

    - **ColumnName** *(string) --* **[REQUIRED]**

      The column that this operation acts on.

    - **Tags** *(list) --* **[REQUIRED]**

      The dataset column tag, currently only used for geospatial type tagging. .

      .. note::

        This is not tags for the AWS tagging feature. .

      - *(dict) --*

        A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
        one of the attributes should be non-null for this structure to be valid.

        - **ColumnGeographicRole** *(string) --*

          A geospatial role for a column.
    """


_ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef",
    {
        "ProjectOperation": ClientUpdateDataSetLogicalTableMapDataTransformsProjectOperationTypeDef,
        "FilterOperation": ClientUpdateDataSetLogicalTableMapDataTransformsFilterOperationTypeDef,
        "CreateColumnsOperation": ClientUpdateDataSetLogicalTableMapDataTransformsCreateColumnsOperationTypeDef,
        "RenameColumnOperation": ClientUpdateDataSetLogicalTableMapDataTransformsRenameColumnOperationTypeDef,
        "CastColumnTypeOperation": ClientUpdateDataSetLogicalTableMapDataTransformsCastColumnTypeOperationTypeDef,
        "TagColumnOperation": ClientUpdateDataSetLogicalTableMapDataTransformsTagColumnOperationTypeDef,
    },
    total=False,
)


class ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef(
    _ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMap` `DataTransforms`

    A data transformation on a logical table. This is a variant type structure. No more than one of
    the attributes should be non-null for this structure to be valid.

    - **ProjectOperation** *(dict) --*

      An operation that projects columns. Operations that come after a projection can only refer to
      projected columns.

      - **ProjectedColumns** *(list) --* **[REQUIRED]**

        Projected columns.

        - *(string) --*

    - **FilterOperation** *(dict) --*

      An operation that filters rows based on some condition.

      - **ConditionExpression** *(string) --* **[REQUIRED]**

        An expression that must evaluate to a boolean value. Rows for which the expression is
        evaluated to true are kept in the dataset.

    - **CreateColumnsOperation** *(dict) --*

      An operation that creates calculated columns. Columns created in one such operation form a
      lexical closure.

      - **Columns** *(list) --* **[REQUIRED]**

        Calculated columns to create.

        - *(dict) --*

          A calculated column for a dataset.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Column name.

          - **ColumnId** *(string) --* **[REQUIRED]**

            A unique ID to identify a calculated column. During dataset update, if the column ID of
            a calculated column matches that of an existing calculated column, QuickSight preserves
            the existing calculated column.

          - **Expression** *(string) --* **[REQUIRED]**

            An expression that defines the calculated column.

    - **RenameColumnOperation** *(dict) --*

      An operation that renames a column.

      - **ColumnName** *(string) --* **[REQUIRED]**

        Name of the column to be renamed.

      - **NewColumnName** *(string) --* **[REQUIRED]**

        New name for the column.

    - **CastColumnTypeOperation** *(dict) --*

      A transform operation that casts a column to a different type.

      - **ColumnName** *(string) --* **[REQUIRED]**

        Column name.

      - **NewColumnType** *(string) --* **[REQUIRED]**

        New column data type.

      - **Format** *(string) --*

        When casting a column from string to datetime type, you can supply a QuickSight supported
        format string to denote the source data format.

    - **TagColumnOperation** *(dict) --*

      An operation that tags a column with additional information.

      - **ColumnName** *(string) --* **[REQUIRED]**

        The column that this operation acts on.

      - **Tags** *(list) --* **[REQUIRED]**

        The dataset column tag, currently only used for geospatial type tagging. .

        .. note::

          This is not tags for the AWS tagging feature. .

        - *(dict) --*

          A tag for a column in a TagColumnOperation. This is a variant type structure. No more than
          one of the attributes should be non-null for this structure to be valid.

          - **ColumnGeographicRole** *(string) --*

            A geospatial role for a column.
    """


_ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef",
    {"LeftOperand": str, "RightOperand": str, "Type": str, "OnClause": str},
)


class ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef(
    _ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMapSource` `JoinInstruction`

    Specifies the result of a join of two logical tables.

    - **LeftOperand** *(string) --* **[REQUIRED]**

      Left operand.

    - **RightOperand** *(string) --* **[REQUIRED]**

      Right operand.

    - **Type** *(string) --* **[REQUIRED]**

      Type.

    - **OnClause** *(string) --* **[REQUIRED]**

      On Clause.
    """


_ClientUpdateDataSetLogicalTableMapSourceTypeDef = TypedDict(
    "_ClientUpdateDataSetLogicalTableMapSourceTypeDef",
    {
        "JoinInstruction": ClientUpdateDataSetLogicalTableMapSourceJoinInstructionTypeDef,
        "PhysicalTableId": str,
    },
    total=False,
)


class ClientUpdateDataSetLogicalTableMapSourceTypeDef(
    _ClientUpdateDataSetLogicalTableMapSourceTypeDef
):
    """
    Type definition for `ClientUpdateDataSetLogicalTableMap` `Source`

    Source of this logical table.

    - **JoinInstruction** *(dict) --*

      Specifies the result of a join of two logical tables.

      - **LeftOperand** *(string) --* **[REQUIRED]**

        Left operand.

      - **RightOperand** *(string) --* **[REQUIRED]**

        Right operand.

      - **Type** *(string) --* **[REQUIRED]**

        Type.

      - **OnClause** *(string) --* **[REQUIRED]**

        On Clause.

    - **PhysicalTableId** *(string) --*

      Physical table ID.
    """


_RequiredClientUpdateDataSetLogicalTableMapTypeDef = TypedDict(
    "_RequiredClientUpdateDataSetLogicalTableMapTypeDef",
    {"Alias": str, "Source": ClientUpdateDataSetLogicalTableMapSourceTypeDef},
)
_OptionalClientUpdateDataSetLogicalTableMapTypeDef = TypedDict(
    "_OptionalClientUpdateDataSetLogicalTableMapTypeDef",
    {"DataTransforms": List[ClientUpdateDataSetLogicalTableMapDataTransformsTypeDef]},
    total=False,
)


class ClientUpdateDataSetLogicalTableMapTypeDef(
    _RequiredClientUpdateDataSetLogicalTableMapTypeDef,
    _OptionalClientUpdateDataSetLogicalTableMapTypeDef,
):
    """
    Type definition for `ClientUpdateDataSet` `LogicalTableMap`

    A unit that joins and data transformations operate on. A logical table has a source, which can
    be either a physical table or result of a join. When it points to a physical table, a logical
    table acts as a mutable copy of that table through transform operations.

    - **Alias** *(string) --* **[REQUIRED]**

      A display name for the logical table.

    - **DataTransforms** *(list) --*

      Transform operations that act on this logical table.

      - *(dict) --*

        A data transformation on a logical table. This is a variant type structure. No more than one
        of the attributes should be non-null for this structure to be valid.

        - **ProjectOperation** *(dict) --*

          An operation that projects columns. Operations that come after a projection can only refer
          to projected columns.

          - **ProjectedColumns** *(list) --* **[REQUIRED]**

            Projected columns.

            - *(string) --*

        - **FilterOperation** *(dict) --*

          An operation that filters rows based on some condition.

          - **ConditionExpression** *(string) --* **[REQUIRED]**

            An expression that must evaluate to a boolean value. Rows for which the expression is
            evaluated to true are kept in the dataset.

        - **CreateColumnsOperation** *(dict) --*

          An operation that creates calculated columns. Columns created in one such operation form a
          lexical closure.

          - **Columns** *(list) --* **[REQUIRED]**

            Calculated columns to create.

            - *(dict) --*

              A calculated column for a dataset.

              - **ColumnName** *(string) --* **[REQUIRED]**

                Column name.

              - **ColumnId** *(string) --* **[REQUIRED]**

                A unique ID to identify a calculated column. During dataset update, if the column ID
                of a calculated column matches that of an existing calculated column, QuickSight
                preserves the existing calculated column.

              - **Expression** *(string) --* **[REQUIRED]**

                An expression that defines the calculated column.

        - **RenameColumnOperation** *(dict) --*

          An operation that renames a column.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Name of the column to be renamed.

          - **NewColumnName** *(string) --* **[REQUIRED]**

            New name for the column.

        - **CastColumnTypeOperation** *(dict) --*

          A transform operation that casts a column to a different type.

          - **ColumnName** *(string) --* **[REQUIRED]**

            Column name.

          - **NewColumnType** *(string) --* **[REQUIRED]**

            New column data type.

          - **Format** *(string) --*

            When casting a column from string to datetime type, you can supply a QuickSight
            supported format string to denote the source data format.

        - **TagColumnOperation** *(dict) --*

          An operation that tags a column with additional information.

          - **ColumnName** *(string) --* **[REQUIRED]**

            The column that this operation acts on.

          - **Tags** *(list) --* **[REQUIRED]**

            The dataset column tag, currently only used for geospatial type tagging. .

            .. note::

              This is not tags for the AWS tagging feature. .

            - *(dict) --*

              A tag for a column in a TagColumnOperation. This is a variant type structure. No more
              than one of the attributes should be non-null for this structure to be valid.

              - **ColumnGeographicRole** *(string) --*

                A geospatial role for a column.

    - **Source** *(dict) --* **[REQUIRED]**

      Source of this logical table.

      - **JoinInstruction** *(dict) --*

        Specifies the result of a join of two logical tables.

        - **LeftOperand** *(string) --* **[REQUIRED]**

          Left operand.

        - **RightOperand** *(string) --* **[REQUIRED]**

          Right operand.

        - **Type** *(string) --* **[REQUIRED]**

          Type.

        - **OnClause** *(string) --* **[REQUIRED]**

          On Clause.

      - **PhysicalTableId** *(string) --*

        Physical table ID.
    """


_ClientUpdateDataSetPermissionsGrantPermissionsTypeDef = TypedDict(
    "_ClientUpdateDataSetPermissionsGrantPermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDataSetPermissionsGrantPermissionsTypeDef(
    _ClientUpdateDataSetPermissionsGrantPermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPermissions` `GrantPermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDataSetPermissionsResponseTypeDef = TypedDict(
    "_ClientUpdateDataSetPermissionsResponseTypeDef",
    {"DataSetArn": str, "DataSetId": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientUpdateDataSetPermissionsResponseTypeDef(_ClientUpdateDataSetPermissionsResponseTypeDef):
    """
    Type definition for `ClientUpdateDataSetPermissions` `Response`

    - **DataSetArn** *(string) --*

      The ARN of the dataset.

    - **DataSetId** *(string) --*

      The ID for the dataset you want to create. This is unique per region per AWS account.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDataSetPermissionsRevokePermissionsTypeDef = TypedDict(
    "_ClientUpdateDataSetPermissionsRevokePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDataSetPermissionsRevokePermissionsTypeDef(
    _ClientUpdateDataSetPermissionsRevokePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPermissions` `RevokePermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef = TypedDict(
    "_ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef", {"Name": str, "Type": str}
)


class ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef(
    _ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMapCustomSql` `Columns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_RequiredClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef = TypedDict(
    "_RequiredClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef",
    {"DataSourceArn": str, "Name": str, "SqlQuery": str},
)
_OptionalClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef = TypedDict(
    "_OptionalClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef",
    {"Columns": List[ClientUpdateDataSetPhysicalTableMapCustomSqlColumnsTypeDef]},
    total=False,
)


class ClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef(
    _RequiredClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef,
    _OptionalClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef,
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMap` `CustomSql`

    A physical table type built from the results of the custom SQL query.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      The ARN of the data source.

    - **Name** *(string) --* **[REQUIRED]**

      A display name for the SQL query result.

    - **SqlQuery** *(string) --* **[REQUIRED]**

      The SQL query.

    - **Columns** *(list) --*

      The column schema from the SQL query result set.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef = TypedDict(
    "_ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef",
    {"Name": str, "Type": str},
)


class ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef(
    _ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMapRelationalTable` `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_RequiredClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef = TypedDict(
    "_RequiredClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "InputColumns": List[ClientUpdateDataSetPhysicalTableMapRelationalTableInputColumnsTypeDef],
    },
)
_OptionalClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef = TypedDict(
    "_OptionalClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef",
    {"Schema": str},
    total=False,
)


class ClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef(
    _RequiredClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef,
    _OptionalClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef,
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMap` `RelationalTable`

    A physical table type for relational data sources.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      Data source ARN.

    - **Schema** *(string) --*

      The schema name. Applies to certain relational database engines.

    - **Name** *(string) --* **[REQUIRED]**

      Name of the relational table.

    - **InputColumns** *(list) --* **[REQUIRED]**

      The column schema of the table.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef = TypedDict(
    "_ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef", {"Name": str, "Type": str}
)


class ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef(
    _ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMapS3Source` `InputColumns`

    Metadata on a column that is used as the input of a transform operation.

    - **Name** *(string) --* **[REQUIRED]**

      The name of this column in the underlying data source.

    - **Type** *(string) --* **[REQUIRED]**

      The data type of the column.
    """


_ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef = TypedDict(
    "_ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef",
    {
        "Format": str,
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": str,
        "Delimiter": str,
    },
    total=False,
)


class ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef(
    _ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMapS3Source` `UploadSettings`

    Information on the S3 source file(s) format.

    - **Format** *(string) --*

      File format.

    - **StartFromRow** *(integer) --*

      A row number to start reading data from.

    - **ContainsHeader** *(boolean) --*

      Whether or not the file(s) has a header row.

    - **TextQualifier** *(string) --*

      Text qualifier.

    - **Delimiter** *(string) --*

      The delimiter between values in the file.
    """


_RequiredClientUpdateDataSetPhysicalTableMapS3SourceTypeDef = TypedDict(
    "_RequiredClientUpdateDataSetPhysicalTableMapS3SourceTypeDef",
    {
        "DataSourceArn": str,
        "InputColumns": List[ClientUpdateDataSetPhysicalTableMapS3SourceInputColumnsTypeDef],
    },
)
_OptionalClientUpdateDataSetPhysicalTableMapS3SourceTypeDef = TypedDict(
    "_OptionalClientUpdateDataSetPhysicalTableMapS3SourceTypeDef",
    {"UploadSettings": ClientUpdateDataSetPhysicalTableMapS3SourceUploadSettingsTypeDef},
    total=False,
)


class ClientUpdateDataSetPhysicalTableMapS3SourceTypeDef(
    _RequiredClientUpdateDataSetPhysicalTableMapS3SourceTypeDef,
    _OptionalClientUpdateDataSetPhysicalTableMapS3SourceTypeDef,
):
    """
    Type definition for `ClientUpdateDataSetPhysicalTableMap` `S3Source`

    A physical table type for as S3 data source.

    - **DataSourceArn** *(string) --* **[REQUIRED]**

      Data source ARN.

    - **UploadSettings** *(dict) --*

      Information on the S3 source file(s) format.

      - **Format** *(string) --*

        File format.

      - **StartFromRow** *(integer) --*

        A row number to start reading data from.

      - **ContainsHeader** *(boolean) --*

        Whether or not the file(s) has a header row.

      - **TextQualifier** *(string) --*

        Text qualifier.

      - **Delimiter** *(string) --*

        The delimiter between values in the file.

    - **InputColumns** *(list) --* **[REQUIRED]**

      A physical table type for as S3 data source.

      - *(dict) --*

        Metadata on a column that is used as the input of a transform operation.

        - **Name** *(string) --* **[REQUIRED]**

          The name of this column in the underlying data source.

        - **Type** *(string) --* **[REQUIRED]**

          The data type of the column.
    """


_ClientUpdateDataSetPhysicalTableMapTypeDef = TypedDict(
    "_ClientUpdateDataSetPhysicalTableMapTypeDef",
    {
        "RelationalTable": ClientUpdateDataSetPhysicalTableMapRelationalTableTypeDef,
        "CustomSql": ClientUpdateDataSetPhysicalTableMapCustomSqlTypeDef,
        "S3Source": ClientUpdateDataSetPhysicalTableMapS3SourceTypeDef,
    },
    total=False,
)


class ClientUpdateDataSetPhysicalTableMapTypeDef(_ClientUpdateDataSetPhysicalTableMapTypeDef):
    """
    Type definition for `ClientUpdateDataSet` `PhysicalTableMap`

    A view of a data source. Contains information on the shape of the data in the underlying source.
    This is a variant type structure. No more than one of the attributes can be non-null for this
    structure to be valid.

    - **RelationalTable** *(dict) --*

      A physical table type for relational data sources.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        Data source ARN.

      - **Schema** *(string) --*

        The schema name. Applies to certain relational database engines.

      - **Name** *(string) --* **[REQUIRED]**

        Name of the relational table.

      - **InputColumns** *(list) --* **[REQUIRED]**

        The column schema of the table.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.

    - **CustomSql** *(dict) --*

      A physical table type built from the results of the custom SQL query.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        The ARN of the data source.

      - **Name** *(string) --* **[REQUIRED]**

        A display name for the SQL query result.

      - **SqlQuery** *(string) --* **[REQUIRED]**

        The SQL query.

      - **Columns** *(list) --*

        The column schema from the SQL query result set.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.

    - **S3Source** *(dict) --*

      A physical table type for as S3 data source.

      - **DataSourceArn** *(string) --* **[REQUIRED]**

        Data source ARN.

      - **UploadSettings** *(dict) --*

        Information on the S3 source file(s) format.

        - **Format** *(string) --*

          File format.

        - **StartFromRow** *(integer) --*

          A row number to start reading data from.

        - **ContainsHeader** *(boolean) --*

          Whether or not the file(s) has a header row.

        - **TextQualifier** *(string) --*

          Text qualifier.

        - **Delimiter** *(string) --*

          The delimiter between values in the file.

      - **InputColumns** *(list) --* **[REQUIRED]**

        A physical table type for as S3 data source.

        - *(dict) --*

          Metadata on a column that is used as the input of a transform operation.

          - **Name** *(string) --* **[REQUIRED]**

            The name of this column in the underlying data source.

          - **Type** *(string) --* **[REQUIRED]**

            The data type of the column.
    """


_ClientUpdateDataSetResponseTypeDef = TypedDict(
    "_ClientUpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientUpdateDataSetResponseTypeDef(_ClientUpdateDataSetResponseTypeDef):
    """
    Type definition for `ClientUpdateDataSet` `Response`

    - **Arn** *(string) --*

      The ARN of the dataset.

    - **DataSetId** *(string) --*

      The ID for the dataset you want to create. This is unique per region per AWS account.

    - **IngestionArn** *(string) --*

      The Amazon Resource Name (ARN) for the ingestion, which is triggered as a result of dataset
      creation if the import mode is SPICE

    - **IngestionId** *(string) --*

      The ID of the ingestion, which is triggered as a result of dataset creation if the import mode
      is SPICE

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDataSetRowLevelPermissionDataSetTypeDef = TypedDict(
    "_ClientUpdateDataSetRowLevelPermissionDataSetTypeDef", {"Arn": str, "PermissionPolicy": str}
)


class ClientUpdateDataSetRowLevelPermissionDataSetTypeDef(
    _ClientUpdateDataSetRowLevelPermissionDataSetTypeDef
):
    """
    Type definition for `ClientUpdateDataSet` `RowLevelPermissionDataSet`

    Row-level security configuration on the data you want to create.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the permission dataset.

    - **PermissionPolicy** *(string) --* **[REQUIRED]**

      Permission policy.
    """


_ClientUpdateDataSourceCredentialsCredentialPairTypeDef = TypedDict(
    "_ClientUpdateDataSourceCredentialsCredentialPairTypeDef", {"Username": str, "Password": str}
)


class ClientUpdateDataSourceCredentialsCredentialPairTypeDef(
    _ClientUpdateDataSourceCredentialsCredentialPairTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceCredentials` `CredentialPair`

    Credential pair.

    - **Username** *(string) --* **[REQUIRED]**

      Username.

    - **Password** *(string) --* **[REQUIRED]**

      Password.
    """


_ClientUpdateDataSourceCredentialsTypeDef = TypedDict(
    "_ClientUpdateDataSourceCredentialsTypeDef",
    {"CredentialPair": ClientUpdateDataSourceCredentialsCredentialPairTypeDef},
    total=False,
)


class ClientUpdateDataSourceCredentialsTypeDef(_ClientUpdateDataSourceCredentialsTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `Credentials`

    The credentials QuickSight uses to connect to your underlying source. Currently only
    username/password based credentials are supported.

    - **CredentialPair** *(dict) --*

      Credential pair.

      - **Username** *(string) --* **[REQUIRED]**

        Username.

      - **Password** *(string) --* **[REQUIRED]**

        Password.
    """


_ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef",
    {"Domain": str},
)


class ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `AmazonElasticsearchParameters`

    Amazon Elasticsearch parameters.

    - **Domain** *(string) --* **[REQUIRED]**

      The Amazon Elasticsearch domain.
    """


_ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef",
    {"WorkGroup": str},
    total=False,
)


class ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `AthenaParameters`

    Athena parameters.

    - **WorkGroup** *(string) --*

      The workgroup that Athena uses.
    """


_ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `AuroraParameters`

    Aurora MySQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `AuroraPostgreSqlParameters`

    Aurora PostgreSQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef",
    {"DataSetName": str},
)


class ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `AwsIotAnalyticsParameters`

    AWS IoT Analytics parameters.

    - **DataSetName** *(string) --* **[REQUIRED]**

      Dataset name.
    """


_ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef", {"SiteBaseUrl": str}
)


class ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `JiraParameters`

    Jira parameters.

    - **SiteBaseUrl** *(string) --* **[REQUIRED]**

      The base URL of the Jira site.
    """


_ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `MariaDbParameters`

    MariaDB parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `MySqlParameters`

    MySQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `PostgreSqlParameters`

    PostgreSQL parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef",
    {"Host": str, "Port": int, "Catalog": str},
)


class ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `PrestoParameters`

    Presto parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Catalog** *(string) --* **[REQUIRED]**

      Catalog.
    """


_ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef",
    {"InstanceId": str, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `RdsParameters`

    RDS parameters.

    - **InstanceId** *(string) --* **[REQUIRED]**

      Instance ID.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_RequiredClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_RequiredClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    {"Database": str},
)
_OptionalClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef = TypedDict(
    "_OptionalClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef",
    {"Host": str, "Port": int, "ClusterId": str},
    total=False,
)


class ClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef(
    _RequiredClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef,
    _OptionalClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef,
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `RedshiftParameters`

    Redshift parameters.

    - **Host** *(string) --*

      Host. This can be blank if the ``ClusterId`` is provided.

    - **Port** *(integer) --*

      Port. This can be blank if the ``ClusterId`` is provided.

    - **Database** *(string) --* **[REQUIRED]**

      Database.

    - **ClusterId** *(string) --*

      Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.
    """


_ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef",
    {"Bucket": str, "Key": str},
)


class ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef(
    _ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParametersS3Parameters`
    `ManifestFileLocation`

    Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
    console.

    - **Bucket** *(string) --* **[REQUIRED]**

      Amazon S3 bucket.

    - **Key** *(string) --* **[REQUIRED]**

      Amazon S3 key that identifies an object.
    """


_ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef",
    {
        "ManifestFileLocation": ClientUpdateDataSourceDataSourceParametersS3ParametersManifestFileLocationTypeDef
    },
)


class ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `S3Parameters`

    S3 parameters.

    - **ManifestFileLocation** *(dict) --* **[REQUIRED]**

      Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in the
      console.

      - **Bucket** *(string) --* **[REQUIRED]**

        Amazon S3 bucket.

      - **Key** *(string) --* **[REQUIRED]**

        Amazon S3 key that identifies an object.
    """


_ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef", {"SiteBaseUrl": str}
)


class ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `ServiceNowParameters`

    ServiceNow parameters.

    - **SiteBaseUrl** *(string) --* **[REQUIRED]**

      URL of the base site.
    """


_ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef",
    {"Host": str, "Database": str, "Warehouse": str},
)


class ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `SnowflakeParameters`

    Snowflake parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Database** *(string) --* **[REQUIRED]**

      Database.

    - **Warehouse** *(string) --* **[REQUIRED]**

      Warehouse.
    """


_ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef", {"Host": str, "Port": int}
)


class ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `SparkParameters`

    Spark parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.
    """


_ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `SqlServerParameters`

    SQL Server parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef",
    {"Host": str, "Port": int, "Database": str},
)


class ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `TeradataParameters`

    Teradata parameters.

    - **Host** *(string) --* **[REQUIRED]**

      Host.

    - **Port** *(integer) --* **[REQUIRED]**

      Port.

    - **Database** *(string) --* **[REQUIRED]**

      Database.
    """


_ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef",
    {"Query": str, "MaxRows": int},
)


class ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceDataSourceParameters` `TwitterParameters`

    Twitter parameters.

    - **Query** *(string) --* **[REQUIRED]**

      Twitter query string.

    - **MaxRows** *(integer) --* **[REQUIRED]**

      Maximum number of rows to query Twitter.
    """


_ClientUpdateDataSourceDataSourceParametersTypeDef = TypedDict(
    "_ClientUpdateDataSourceDataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": ClientUpdateDataSourceDataSourceParametersAmazonElasticsearchParametersTypeDef,
        "AthenaParameters": ClientUpdateDataSourceDataSourceParametersAthenaParametersTypeDef,
        "AuroraParameters": ClientUpdateDataSourceDataSourceParametersAuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": ClientUpdateDataSourceDataSourceParametersAuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": ClientUpdateDataSourceDataSourceParametersAwsIotAnalyticsParametersTypeDef,
        "JiraParameters": ClientUpdateDataSourceDataSourceParametersJiraParametersTypeDef,
        "MariaDbParameters": ClientUpdateDataSourceDataSourceParametersMariaDbParametersTypeDef,
        "MySqlParameters": ClientUpdateDataSourceDataSourceParametersMySqlParametersTypeDef,
        "PostgreSqlParameters": ClientUpdateDataSourceDataSourceParametersPostgreSqlParametersTypeDef,
        "PrestoParameters": ClientUpdateDataSourceDataSourceParametersPrestoParametersTypeDef,
        "RdsParameters": ClientUpdateDataSourceDataSourceParametersRdsParametersTypeDef,
        "RedshiftParameters": ClientUpdateDataSourceDataSourceParametersRedshiftParametersTypeDef,
        "S3Parameters": ClientUpdateDataSourceDataSourceParametersS3ParametersTypeDef,
        "ServiceNowParameters": ClientUpdateDataSourceDataSourceParametersServiceNowParametersTypeDef,
        "SnowflakeParameters": ClientUpdateDataSourceDataSourceParametersSnowflakeParametersTypeDef,
        "SparkParameters": ClientUpdateDataSourceDataSourceParametersSparkParametersTypeDef,
        "SqlServerParameters": ClientUpdateDataSourceDataSourceParametersSqlServerParametersTypeDef,
        "TeradataParameters": ClientUpdateDataSourceDataSourceParametersTeradataParametersTypeDef,
        "TwitterParameters": ClientUpdateDataSourceDataSourceParametersTwitterParametersTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourceDataSourceParametersTypeDef(
    _ClientUpdateDataSourceDataSourceParametersTypeDef
):
    """
    Type definition for `ClientUpdateDataSource` `DataSourceParameters`

    The parameters QuickSight uses to connect to your underlying source.

    - **AmazonElasticsearchParameters** *(dict) --*

      Amazon Elasticsearch parameters.

      - **Domain** *(string) --* **[REQUIRED]**

        The Amazon Elasticsearch domain.

    - **AthenaParameters** *(dict) --*

      Athena parameters.

      - **WorkGroup** *(string) --*

        The workgroup that Athena uses.

    - **AuroraParameters** *(dict) --*

      Aurora MySQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **AuroraPostgreSqlParameters** *(dict) --*

      Aurora PostgreSQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **AwsIotAnalyticsParameters** *(dict) --*

      AWS IoT Analytics parameters.

      - **DataSetName** *(string) --* **[REQUIRED]**

        Dataset name.

    - **JiraParameters** *(dict) --*

      Jira parameters.

      - **SiteBaseUrl** *(string) --* **[REQUIRED]**

        The base URL of the Jira site.

    - **MariaDbParameters** *(dict) --*

      MariaDB parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **MySqlParameters** *(dict) --*

      MySQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **PostgreSqlParameters** *(dict) --*

      PostgreSQL parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **PrestoParameters** *(dict) --*

      Presto parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Catalog** *(string) --* **[REQUIRED]**

        Catalog.

    - **RdsParameters** *(dict) --*

      RDS parameters.

      - **InstanceId** *(string) --* **[REQUIRED]**

        Instance ID.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **RedshiftParameters** *(dict) --*

      Redshift parameters.

      - **Host** *(string) --*

        Host. This can be blank if the ``ClusterId`` is provided.

      - **Port** *(integer) --*

        Port. This can be blank if the ``ClusterId`` is provided.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

      - **ClusterId** *(string) --*

        Cluster ID. This can be blank if the ``Host`` and ``Port`` are provided.

    - **S3Parameters** *(dict) --*

      S3 parameters.

      - **ManifestFileLocation** *(dict) --* **[REQUIRED]**

        Location of the Amazon S3 manifest file. This is NULL if the manifest file was uploaded in
        the console.

        - **Bucket** *(string) --* **[REQUIRED]**

          Amazon S3 bucket.

        - **Key** *(string) --* **[REQUIRED]**

          Amazon S3 key that identifies an object.

    - **ServiceNowParameters** *(dict) --*

      ServiceNow parameters.

      - **SiteBaseUrl** *(string) --* **[REQUIRED]**

        URL of the base site.

    - **SnowflakeParameters** *(dict) --*

      Snowflake parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

      - **Warehouse** *(string) --* **[REQUIRED]**

        Warehouse.

    - **SparkParameters** *(dict) --*

      Spark parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

    - **SqlServerParameters** *(dict) --*

      SQL Server parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **TeradataParameters** *(dict) --*

      Teradata parameters.

      - **Host** *(string) --* **[REQUIRED]**

        Host.

      - **Port** *(integer) --* **[REQUIRED]**

        Port.

      - **Database** *(string) --* **[REQUIRED]**

        Database.

    - **TwitterParameters** *(dict) --*

      Twitter parameters.

      - **Query** *(string) --* **[REQUIRED]**

        Twitter query string.

      - **MaxRows** *(integer) --* **[REQUIRED]**

        Maximum number of rows to query Twitter.
    """


_ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef = TypedDict(
    "_ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef(
    _ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcePermissions` `GrantPermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDataSourcePermissionsResponseTypeDef = TypedDict(
    "_ClientUpdateDataSourcePermissionsResponseTypeDef",
    {"DataSourceArn": str, "DataSourceId": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientUpdateDataSourcePermissionsResponseTypeDef(
    _ClientUpdateDataSourcePermissionsResponseTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcePermissions` `Response`

    - **DataSourceArn** *(string) --*

      The ARN of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef = TypedDict(
    "_ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef(
    _ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcePermissions` `RevokePermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateDataSourceResponseTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponseTypeDef",
    {"Arn": str, "DataSourceId": str, "UpdateStatus": str, "RequestId": str, "Status": int},
    total=False,
)


class ClientUpdateDataSourceResponseTypeDef(_ClientUpdateDataSourceResponseTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `Response`

    - **Arn** *(string) --*

      The ARN of the data source.

    - **DataSourceId** *(string) --*

      The ID of the data source. This is unique per AWS Region per AWS account.

    - **UpdateStatus** *(string) --*

      The update status of the data source's last update.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateDataSourceSslPropertiesTypeDef = TypedDict(
    "_ClientUpdateDataSourceSslPropertiesTypeDef", {"DisableSsl": bool}, total=False
)


class ClientUpdateDataSourceSslPropertiesTypeDef(_ClientUpdateDataSourceSslPropertiesTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `SslProperties`

    SSL properties that apply when QuickSight connects to your underlying source.

    - **DisableSsl** *(boolean) --*

      A boolean flag to control whether SSL should be disabled.
    """


_ClientUpdateDataSourceVpcConnectionPropertiesTypeDef = TypedDict(
    "_ClientUpdateDataSourceVpcConnectionPropertiesTypeDef", {"VpcConnectionArn": str}
)


class ClientUpdateDataSourceVpcConnectionPropertiesTypeDef(
    _ClientUpdateDataSourceVpcConnectionPropertiesTypeDef
):
    """
    Type definition for `ClientUpdateDataSource` `VpcConnectionProperties`

    You need to use this parameter only when you want QuickSight to use a VPC connection when
    connecting to your underlying source.

    - **VpcConnectionArn** *(string) --* **[REQUIRED]**

      VPC connection ARN.
    """


_ClientUpdateGroupResponseGroupTypeDef = TypedDict(
    "_ClientUpdateGroupResponseGroupTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)


class ClientUpdateGroupResponseGroupTypeDef(_ClientUpdateGroupResponseGroupTypeDef):
    """
    Type definition for `ClientUpdateGroupResponse` `Group`

    The name of the group.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the group.

    - **GroupName** *(string) --*

      The name of the group.

    - **Description** *(string) --*

      The group description.

    - **PrincipalId** *(string) --*

      The principal ID of the group.
    """


_ClientUpdateGroupResponseTypeDef = TypedDict(
    "_ClientUpdateGroupResponseTypeDef",
    {"Group": ClientUpdateGroupResponseGroupTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientUpdateGroupResponseTypeDef(_ClientUpdateGroupResponseTypeDef):
    """
    Type definition for `ClientUpdateGroup` `Response`

    - **Group** *(dict) --*

      The name of the group.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the group.

      - **GroupName** *(string) --*

        The name of the group.

      - **Description** *(string) --*

        The group description.

      - **PrincipalId** *(string) --*

        The principal ID of the group.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateIamPolicyAssignmentResponseTypeDef = TypedDict(
    "_ClientUpdateIamPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientUpdateIamPolicyAssignmentResponseTypeDef(
    _ClientUpdateIamPolicyAssignmentResponseTypeDef
):
    """
    Type definition for `ClientUpdateIamPolicyAssignment` `Response`

    - **AssignmentName** *(string) --*

      The name of the assignment.

    - **AssignmentId** *(string) --*

      The ID of the assignment.

    - **PolicyArn** *(string) --*

      The IAM policy ARN assigned to the QuickSight users and groups specified in this request.

    - **Identities** *(dict) --*

      QuickSight users and/or groups that are assigned to this IAM policy.

      - *(string) --*

        - *(list) --*

          - *(string) --*

    - **AssignmentStatus** *(string) --*

      The status of the assignment:

      * ENABLED - Anything specified in this assignment is used while creating the data source.

      * DISABLED - This assignment isn't used while creating the data source.

      * DRAFT - Assignment is an unfinished draft and isn't used while creating the data source.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateTemplateAliasResponseTemplateAliasTypeDef = TypedDict(
    "_ClientUpdateTemplateAliasResponseTemplateAliasTypeDef",
    {"AliasName": str, "Arn": str, "TemplateVersionNumber": int},
    total=False,
)


class ClientUpdateTemplateAliasResponseTemplateAliasTypeDef(
    _ClientUpdateTemplateAliasResponseTemplateAliasTypeDef
):
    """
    Type definition for `ClientUpdateTemplateAliasResponse` `TemplateAlias`

    The template alias.

    - **AliasName** *(string) --*

      The display name of the template alias.

    - **Arn** *(string) --*

      The ARN of the template alias.

    - **TemplateVersionNumber** *(integer) --*

      The version number of the template alias.
    """


_ClientUpdateTemplateAliasResponseTypeDef = TypedDict(
    "_ClientUpdateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": ClientUpdateTemplateAliasResponseTemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientUpdateTemplateAliasResponseTypeDef(_ClientUpdateTemplateAliasResponseTypeDef):
    """
    Type definition for `ClientUpdateTemplateAlias` `Response`

    - **TemplateAlias** *(dict) --*

      The template alias.

      - **AliasName** *(string) --*

        The display name of the template alias.

      - **Arn** *(string) --*

        The ARN of the template alias.

      - **TemplateVersionNumber** *(integer) --*

        The version number of the template alias.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientUpdateTemplatePermissionsGrantPermissionsTypeDef = TypedDict(
    "_ClientUpdateTemplatePermissionsGrantPermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateTemplatePermissionsGrantPermissionsTypeDef(
    _ClientUpdateTemplatePermissionsGrantPermissionsTypeDef
):
    """
    Type definition for `ClientUpdateTemplatePermissions` `GrantPermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateTemplatePermissionsResponsePermissionsTypeDef = TypedDict(
    "_ClientUpdateTemplatePermissionsResponsePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
    total=False,
)


class ClientUpdateTemplatePermissionsResponsePermissionsTypeDef(
    _ClientUpdateTemplatePermissionsResponsePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateTemplatePermissionsResponse` `Permissions`

    Permission for the resource.

    - **Principal** *(string) --*

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --*

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateTemplatePermissionsResponseTypeDef = TypedDict(
    "_ClientUpdateTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ClientUpdateTemplatePermissionsResponsePermissionsTypeDef],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)


class ClientUpdateTemplatePermissionsResponseTypeDef(
    _ClientUpdateTemplatePermissionsResponseTypeDef
):
    """
    Type definition for `ClientUpdateTemplatePermissions` `Response`

    - **TemplateId** *(string) --*

      The ID for the template.

    - **TemplateArn** *(string) --*

      The ARN of the template.

    - **Permissions** *(list) --*

      A list of resource permissions to be set on the template.

      - *(dict) --*

        Permission for the resource.

        - **Principal** *(string) --*

          The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
          resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a
          QuickSight user or group. .

        - **Actions** *(list) --*

          The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

          - *(string) --*

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """


_ClientUpdateTemplatePermissionsRevokePermissionsTypeDef = TypedDict(
    "_ClientUpdateTemplatePermissionsRevokePermissionsTypeDef",
    {"Principal": str, "Actions": List[str]},
)


class ClientUpdateTemplatePermissionsRevokePermissionsTypeDef(
    _ClientUpdateTemplatePermissionsRevokePermissionsTypeDef
):
    """
    Type definition for `ClientUpdateTemplatePermissions` `RevokePermissions`

    Permission for the resource.

    - **Principal** *(string) --* **[REQUIRED]**

      The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account resource
      sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of a QuickSight user
      or group. .

    - **Actions** *(list) --* **[REQUIRED]**

      The action to grant or revoke permissions on. For example, "quicksight:DescribeDashboard".

      - *(string) --*
    """


_ClientUpdateTemplateResponseTypeDef = TypedDict(
    "_ClientUpdateTemplateResponseTypeDef",
    {
        "TemplateId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)


class ClientUpdateTemplateResponseTypeDef(_ClientUpdateTemplateResponseTypeDef):
    """
    Type definition for `ClientUpdateTemplate` `Response`

    - **TemplateId** *(string) --*

      The ID for the template.

    - **Arn** *(string) --*

      The Amazon Resource Name (ARN) for the template.

    - **VersionArn** *(string) --*

      The Amazon Resource Name (ARN) for the template, including the version information of the
      first version.

    - **CreationStatus** *(string) --*

      The creation status of the template.

    - **Status** *(integer) --*

      The http status of the request.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.
    """


_ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef = TypedDict(
    "_ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef",
    {"DataSetPlaceholder": str, "DataSetArn": str},
)


class ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef(
    _ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef
):
    """
    Type definition for `ClientUpdateTemplateSourceEntitySourceAnalysis` `DataSetReferences`

    Dataset reference.

    - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

      Dataset placeholder.

    - **DataSetArn** *(string) --* **[REQUIRED]**

      Dataset ARN.
    """


_ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef = TypedDict(
    "_ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef",
    {
        "Arn": str,
        "DataSetReferences": List[
            ClientUpdateTemplateSourceEntitySourceAnalysisDataSetReferencesTypeDef
        ],
    },
)


class ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef(
    _ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef
):
    """
    Type definition for `ClientUpdateTemplateSourceEntity` `SourceAnalysis`

    The source analysis, if it is based on an analysis.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.

    - **DataSetReferences** *(list) --* **[REQUIRED]**

      A structure containing information about the dataset references used as placeholders in the
      template.

      - *(dict) --*

        Dataset reference.

        - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

          Dataset placeholder.

        - **DataSetArn** *(string) --* **[REQUIRED]**

          Dataset ARN.
    """


_ClientUpdateTemplateSourceEntitySourceTemplateTypeDef = TypedDict(
    "_ClientUpdateTemplateSourceEntitySourceTemplateTypeDef", {"Arn": str}
)


class ClientUpdateTemplateSourceEntitySourceTemplateTypeDef(
    _ClientUpdateTemplateSourceEntitySourceTemplateTypeDef
):
    """
    Type definition for `ClientUpdateTemplateSourceEntity` `SourceTemplate`

    The source template, if it is based on an template.

    - **Arn** *(string) --* **[REQUIRED]**

      The Amazon Resource name (ARN) of the resource.
    """


_ClientUpdateTemplateSourceEntityTypeDef = TypedDict(
    "_ClientUpdateTemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": ClientUpdateTemplateSourceEntitySourceAnalysisTypeDef,
        "SourceTemplate": ClientUpdateTemplateSourceEntitySourceTemplateTypeDef,
    },
    total=False,
)


class ClientUpdateTemplateSourceEntityTypeDef(_ClientUpdateTemplateSourceEntityTypeDef):
    """
    Type definition for `ClientUpdateTemplate` `SourceEntity`

    The source QuickSight entity from which this template is being created. Templates can be
    currently created from an Analysis or another template.

    - **SourceAnalysis** *(dict) --*

      The source analysis, if it is based on an analysis.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.

      - **DataSetReferences** *(list) --* **[REQUIRED]**

        A structure containing information about the dataset references used as placeholders in the
        template.

        - *(dict) --*

          Dataset reference.

          - **DataSetPlaceholder** *(string) --* **[REQUIRED]**

            Dataset placeholder.

          - **DataSetArn** *(string) --* **[REQUIRED]**

            Dataset ARN.

    - **SourceTemplate** *(dict) --*

      The source template, if it is based on an template.

      - **Arn** *(string) --* **[REQUIRED]**

        The Amazon Resource name (ARN) of the resource.
    """


_ClientUpdateUserResponseUserTypeDef = TypedDict(
    "_ClientUpdateUserResponseUserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": str,
        "IdentityType": str,
        "Active": bool,
        "PrincipalId": str,
    },
    total=False,
)


class ClientUpdateUserResponseUserTypeDef(_ClientUpdateUserResponseUserTypeDef):
    """
    Type definition for `ClientUpdateUserResponse` `User`

    The Amazon QuickSight user.

    - **Arn** *(string) --*

      The Amazon Resource name (ARN) for the user.

    - **UserName** *(string) --*

      The user's user name.

    - **Email** *(string) --*

      The user's email address.

    - **Role** *(string) --*

      The Amazon QuickSight role for the user. The user role can be one of the following:.

      * ``READER`` : A user who has read-only access to dashboards.

      * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

      * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

      * ``RESTRICTED_READER`` : This role isn't currently available for use.

      * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

    - **IdentityType** *(string) --*

      The type of identity authentication used by the user.

    - **Active** *(boolean) --*

      Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or an
      AD user, that user is inactive until they sign in and provide a password.

    - **PrincipalId** *(string) --*

      The principal ID of the user.
    """


_ClientUpdateUserResponseTypeDef = TypedDict(
    "_ClientUpdateUserResponseTypeDef",
    {"User": ClientUpdateUserResponseUserTypeDef, "RequestId": str, "Status": int},
    total=False,
)


class ClientUpdateUserResponseTypeDef(_ClientUpdateUserResponseTypeDef):
    """
    Type definition for `ClientUpdateUser` `Response`

    - **User** *(dict) --*

      The Amazon QuickSight user.

      - **Arn** *(string) --*

        The Amazon Resource name (ARN) for the user.

      - **UserName** *(string) --*

        The user's user name.

      - **Email** *(string) --*

        The user's email address.

      - **Role** *(string) --*

        The Amazon QuickSight role for the user. The user role can be one of the following:.

        * ``READER`` : A user who has read-only access to dashboards.

        * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

        * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

        * ``RESTRICTED_READER`` : This role isn't currently available for use.

        * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

      - **IdentityType** *(string) --*

        The type of identity authentication used by the user.

      - **Active** *(boolean) --*

        Active status of user. When you create an Amazon QuickSight user that’s not an IAM user or
        an AD user, that user is inactive until they sign in and provide a password.

      - **PrincipalId** *(string) --*

        The principal ID of the user.

    - **RequestId** *(string) --*

      The AWS request ID for this operation.

    - **Status** *(integer) --*

      The http status of the request.
    """
