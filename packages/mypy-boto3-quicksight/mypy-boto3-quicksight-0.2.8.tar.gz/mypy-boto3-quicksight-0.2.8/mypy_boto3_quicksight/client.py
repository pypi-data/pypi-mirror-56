"Main interface for quicksight Client"
from __future__ import annotations

from typing import Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_quicksight.client as client_scope
from mypy_boto3_quicksight.type_defs import (
    ClientCancelIngestionResponseTypeDef,
    ClientCreateDashboardDashboardPublishOptionsTypeDef,
    ClientCreateDashboardParametersTypeDef,
    ClientCreateDashboardPermissionsTypeDef,
    ClientCreateDashboardResponseTypeDef,
    ClientCreateDashboardSourceEntityTypeDef,
    ClientCreateDashboardTagsTypeDef,
    ClientCreateDataSetColumnGroupsTypeDef,
    ClientCreateDataSetLogicalTableMapTypeDef,
    ClientCreateDataSetPermissionsTypeDef,
    ClientCreateDataSetPhysicalTableMapTypeDef,
    ClientCreateDataSetResponseTypeDef,
    ClientCreateDataSetRowLevelPermissionDataSetTypeDef,
    ClientCreateDataSetTagsTypeDef,
    ClientCreateDataSourceCredentialsTypeDef,
    ClientCreateDataSourceDataSourceParametersTypeDef,
    ClientCreateDataSourcePermissionsTypeDef,
    ClientCreateDataSourceResponseTypeDef,
    ClientCreateDataSourceSslPropertiesTypeDef,
    ClientCreateDataSourceTagsTypeDef,
    ClientCreateDataSourceVpcConnectionPropertiesTypeDef,
    ClientCreateGroupMembershipResponseTypeDef,
    ClientCreateGroupResponseTypeDef,
    ClientCreateIamPolicyAssignmentResponseTypeDef,
    ClientCreateIngestionResponseTypeDef,
    ClientCreateTemplateAliasResponseTypeDef,
    ClientCreateTemplatePermissionsTypeDef,
    ClientCreateTemplateResponseTypeDef,
    ClientCreateTemplateSourceEntityTypeDef,
    ClientCreateTemplateTagsTypeDef,
    ClientDeleteDashboardResponseTypeDef,
    ClientDeleteDataSetResponseTypeDef,
    ClientDeleteDataSourceResponseTypeDef,
    ClientDeleteGroupMembershipResponseTypeDef,
    ClientDeleteGroupResponseTypeDef,
    ClientDeleteIamPolicyAssignmentResponseTypeDef,
    ClientDeleteTemplateAliasResponseTypeDef,
    ClientDeleteTemplateResponseTypeDef,
    ClientDeleteUserByPrincipalIdResponseTypeDef,
    ClientDeleteUserResponseTypeDef,
    ClientDescribeDashboardPermissionsResponseTypeDef,
    ClientDescribeDashboardResponseTypeDef,
    ClientDescribeDataSetPermissionsResponseTypeDef,
    ClientDescribeDataSetResponseTypeDef,
    ClientDescribeDataSourcePermissionsResponseTypeDef,
    ClientDescribeDataSourceResponseTypeDef,
    ClientDescribeGroupResponseTypeDef,
    ClientDescribeIamPolicyAssignmentResponseTypeDef,
    ClientDescribeIngestionResponseTypeDef,
    ClientDescribeTemplateAliasResponseTypeDef,
    ClientDescribeTemplatePermissionsResponseTypeDef,
    ClientDescribeTemplateResponseTypeDef,
    ClientDescribeUserResponseTypeDef,
    ClientGetDashboardEmbedUrlResponseTypeDef,
    ClientListDashboardVersionsResponseTypeDef,
    ClientListDashboardsResponseTypeDef,
    ClientListDataSetsResponseTypeDef,
    ClientListDataSourcesResponseTypeDef,
    ClientListGroupMembershipsResponseTypeDef,
    ClientListGroupsResponseTypeDef,
    ClientListIamPolicyAssignmentsForUserResponseTypeDef,
    ClientListIamPolicyAssignmentsResponseTypeDef,
    ClientListIngestionsResponseTypeDef,
    ClientListTagsForResourceResponseTypeDef,
    ClientListTemplateAliasesResponseTypeDef,
    ClientListTemplateVersionsResponseTypeDef,
    ClientListTemplatesResponseTypeDef,
    ClientListUserGroupsResponseTypeDef,
    ClientListUsersResponseTypeDef,
    ClientRegisterUserResponseTypeDef,
    ClientTagResourceResponseTypeDef,
    ClientTagResourceTagsTypeDef,
    ClientUntagResourceResponseTypeDef,
    ClientUpdateDashboardDashboardPublishOptionsTypeDef,
    ClientUpdateDashboardParametersTypeDef,
    ClientUpdateDashboardPermissionsGrantPermissionsTypeDef,
    ClientUpdateDashboardPermissionsResponseTypeDef,
    ClientUpdateDashboardPermissionsRevokePermissionsTypeDef,
    ClientUpdateDashboardPublishedVersionResponseTypeDef,
    ClientUpdateDashboardResponseTypeDef,
    ClientUpdateDashboardSourceEntityTypeDef,
    ClientUpdateDataSetColumnGroupsTypeDef,
    ClientUpdateDataSetLogicalTableMapTypeDef,
    ClientUpdateDataSetPermissionsGrantPermissionsTypeDef,
    ClientUpdateDataSetPermissionsResponseTypeDef,
    ClientUpdateDataSetPermissionsRevokePermissionsTypeDef,
    ClientUpdateDataSetPhysicalTableMapTypeDef,
    ClientUpdateDataSetResponseTypeDef,
    ClientUpdateDataSetRowLevelPermissionDataSetTypeDef,
    ClientUpdateDataSourceCredentialsTypeDef,
    ClientUpdateDataSourceDataSourceParametersTypeDef,
    ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef,
    ClientUpdateDataSourcePermissionsResponseTypeDef,
    ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef,
    ClientUpdateDataSourceResponseTypeDef,
    ClientUpdateDataSourceSslPropertiesTypeDef,
    ClientUpdateDataSourceVpcConnectionPropertiesTypeDef,
    ClientUpdateGroupResponseTypeDef,
    ClientUpdateIamPolicyAssignmentResponseTypeDef,
    ClientUpdateTemplateAliasResponseTypeDef,
    ClientUpdateTemplatePermissionsGrantPermissionsTypeDef,
    ClientUpdateTemplatePermissionsResponseTypeDef,
    ClientUpdateTemplatePermissionsRevokePermissionsTypeDef,
    ClientUpdateTemplateResponseTypeDef,
    ClientUpdateTemplateSourceEntityTypeDef,
    ClientUpdateUserResponseTypeDef,
)


__all__ = ("Client",)


class Client(BaseClient):
    exceptions: client_scope.Exceptions

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def can_paginate(self, operation_name: str) -> None:
        """
        Check if an operation can be paginated.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :return: ``True`` if the operation can be paginated,
            ``False`` otherwise.
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def cancel_ingestion(
        self, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> ClientCancelIngestionResponseTypeDef:
        """
        Cancels an on-going ingestion of data into SPICE.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CancelIngestion>`_

        **Request Syntax**
        ::

          response = client.cancel_ingestion(
              AwsAccountId='string',
              DataSetId='string',
              IngestionId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID of the dataset used in the ingestion.

        :type IngestionId: string
        :param IngestionId: **[REQUIRED]**

          An ID for the ingestion.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'IngestionId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The Amazon Resource Name (ARN) for the data ingestion.

            - **IngestionId** *(string) --*

              An ID for the ingestion.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_dashboard(
        self,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: ClientCreateDashboardSourceEntityTypeDef,
        Parameters: ClientCreateDashboardParametersTypeDef = None,
        Permissions: List[ClientCreateDashboardPermissionsTypeDef] = None,
        Tags: List[ClientCreateDashboardTagsTypeDef] = None,
        VersionDescription: str = None,
        DashboardPublishOptions: ClientCreateDashboardDashboardPublishOptionsTypeDef = None,
    ) -> ClientCreateDashboardResponseTypeDef:
        """
        Creates a dashboard from a template. To first create a template, see the CreateTemplate API.

        A dashboard is an entity in QuickSight which identifies Quicksight reports, created from
        analyses. QuickSight dashboards are sharable. With the right permissions, you can create
        scheduled email reports from them. The ``CreateDashboard`` , ``DescribeDashboard`` and
        ``ListDashboardsByUser`` APIs act on the dashboard entity. If you have the correct
        permissions, you can create a dashboard from a template that exists in a different AWS
        account.

        CLI syntax:

         ``aws quicksight create-dashboard --cli-input-json file://create-dashboard.json``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateDashboard>`_

        **Request Syntax**
        ::

          response = client.create_dashboard(
              AwsAccountId='string',
              DashboardId='string',
              Name='string',
              Parameters={
                  'StringParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              'string',
                          ]
                      },
                  ],
                  'IntegerParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              123,
                          ]
                      },
                  ],
                  'DecimalParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              123.0,
                          ]
                      },
                  ],
                  'DateTimeParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              datetime(2015, 1, 1),
                          ]
                      },
                  ]
              },
              Permissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              SourceEntity={
                  'SourceTemplate': {
                      'DataSetReferences': [
                          {
                              'DataSetPlaceholder': 'string',
                              'DataSetArn': 'string'
                          },
                      ],
                      'Arn': 'string'
                  }
              },
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ],
              VersionDescription='string',
              DashboardPublishOptions={
                  'AdHocFilteringOption': {
                      'AvailabilityStatus': 'ENABLED'|'DISABLED'
                  },
                  'ExportToCSVOption': {
                      'AvailabilityStatus': 'ENABLED'|'DISABLED'
                  },
                  'SheetControlsOption': {
                      'VisibilityState': 'EXPANDED'|'COLLAPSED'
                  }
              }
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID where you want to create the dashboard.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard, also added to IAM policy.

        :type Name: string
        :param Name: **[REQUIRED]**

          The display name of the dashboard.

        :type Parameters: dict
        :param Parameters:

          A structure that contains the parameters of the dashboard. These are parameter overrides
          for a dashboard. A dashboard can have any type of parameters and some parameters might
          accept multiple values. You could use the following structure to override two string
          parameters that accept multiple values:

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

        :type Permissions: list
        :param Permissions:

          A structure that contains the permissions of the dashboard. You can use this for granting
          permissions with principal and action information.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type SourceEntity: dict
        :param SourceEntity: **[REQUIRED]**

          Source entity from which the dashboard is created. The souce entity accepts the ARN of the
          source template or analysis and also references the replacement datasets for the
          placeholders set when creating the template. The replacement datasets need to follow the
          same schema as the datasets for which placeholders were created when creating the
          template.

          If you are creating a dashboard from a source entity in a different AWS account, use the
          ARN of the source template.

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

        :type Tags: list
        :param Tags:

          Contains a map of the key-value pairs for the resource tag or tags assigned to the
          dashboard.

          - *(dict) --*

            The keys of the key-value pairs for the resource tag or tags assigned to the resource.

            - **Key** *(string) --* **[REQUIRED]**

              Tag key.

            - **Value** *(string) --* **[REQUIRED]**

              Tag value.

        :type VersionDescription: string
        :param VersionDescription:

          A description for the first version of the dashboard being created.

        :type DashboardPublishOptions: dict
        :param DashboardPublishOptions:

          Publishing options when creating dashboard.

          * AvailabilityStatus for AdHocFilteringOption - This can be either ``ENABLED`` or
          ``DISABLED`` . When This is set to set to ``DISABLED`` , QuickSight disables the left
          filter pane on the published dashboard, which can be used for AdHoc filtering. Enabled by
          default.

          * AvailabilityStatus for ExportToCSVOption - This can be either ``ENABLED`` or
          ``DISABLED`` . The visual option to export data to CSV is disabled when this is set to
          ``DISABLED`` . Enabled by default.

          * VisibilityState for SheetControlsOption - This can be either ``COLLAPSED`` or
          ``EXPANDED`` . The sheet controls pane is collapsed by default when set to true. Collapsed
          by default.

          Shorthand Syntax:

           ``AdHocFilteringDisabled=boolean,ExportToCSVDisabled=boolean,SheetControlsCollapsed=
               boolean``

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

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'VersionArn': 'string',
                'DashboardId': 'string',
                'CreationStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The ARN of the dashboard.

            - **VersionArn** *(string) --*

              The ARN of the dashboard, including the version number of the first version that is
              created.

            - **DashboardId** *(string) --*

              The ID for the dashboard.

            - **CreationStatus** *(string) --*

              The creation status of the dashboard create request.

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_data_set(
        self,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Dict[str, ClientCreateDataSetPhysicalTableMapTypeDef],
        ImportMode: str,
        LogicalTableMap: Dict[str, ClientCreateDataSetLogicalTableMapTypeDef] = None,
        ColumnGroups: List[ClientCreateDataSetColumnGroupsTypeDef] = None,
        Permissions: List[ClientCreateDataSetPermissionsTypeDef] = None,
        RowLevelPermissionDataSet: ClientCreateDataSetRowLevelPermissionDataSetTypeDef = None,
        Tags: List[ClientCreateDataSetTagsTypeDef] = None,
    ) -> ClientCreateDataSetResponseTypeDef:
        """
        Creates a dataset.

        CLI syntax:

         ``aws quicksight create-data-set \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-set-id=unique-data-set-id \\``

         ``--name='My dataset' \\``

         ``--import-mode=SPICE \\``

         ``--physical-table-map='{``

         ``"physical-table-id": {``

         ``"RelationalTable": {``

         ``"DataSourceArn": "arn:aws:quicksight:us-west-2:111111111111:datasource/data-source-id",``

         ``"Name": "table1",``

         ``"InputColumns": [``

         ``{``

         ``"Name": "column1",``

         ``"Type": "STRING"``

         ``}``

         ``]``

         ``}``

         ``}'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateDataSet>`_

        **Request Syntax**
        ::

          response = client.create_data_set(
              AwsAccountId='string',
              DataSetId='string',
              Name='string',
              PhysicalTableMap={
                  'string': {
                      'RelationalTable': {
                          'DataSourceArn': 'string',
                          'Schema': 'string',
                          'Name': 'string',
                          'InputColumns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      },
                      'CustomSql': {
                          'DataSourceArn': 'string',
                          'Name': 'string',
                          'SqlQuery': 'string',
                          'Columns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      },
                      'S3Source': {
                          'DataSourceArn': 'string',
                          'UploadSettings': {
                              'Format': 'CSV'|'TSV'|'CLF'|'ELF'|'XLSX'|'JSON',
                              'StartFromRow': 123,
                              'ContainsHeader': True|False,
                              'TextQualifier': 'DOUBLE_QUOTE'|'SINGLE_QUOTE',
                              'Delimiter': 'string'
                          },
                          'InputColumns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      }
                  }
              },
              LogicalTableMap={
                  'string': {
                      'Alias': 'string',
                      'DataTransforms': [
                          {
                              'ProjectOperation': {
                                  'ProjectedColumns': [
                                      'string',
                                  ]
                              },
                              'FilterOperation': {
                                  'ConditionExpression': 'string'
                              },
                              'CreateColumnsOperation': {
                                  'Columns': [
                                      {
                                          'ColumnName': 'string',
                                          'ColumnId': 'string',
                                          'Expression': 'string'
                                      },
                                  ]
                              },
                              'RenameColumnOperation': {
                                  'ColumnName': 'string',
                                  'NewColumnName': 'string'
                              },
                              'CastColumnTypeOperation': {
                                  'ColumnName': 'string',
                                  'NewColumnType': 'STRING'|'INTEGER'|'DECIMAL'|'DATETIME',
                                  'Format': 'string'
                              },
                              'TagColumnOperation': {
                                  'ColumnName': 'string',
                                  'Tags': [
                                      {
                                          'ColumnGeographicRole':
                                          'COUNTRY'|'STATE'
                                          |'COUNTY'|'CITY'
                                          |'POSTCODE'|'LONGITUDE'
                                          |'LATITUDE'
                                      },
                                  ]
                              }
                          },
                      ],
                      'Source': {
                          'JoinInstruction': {
                              'LeftOperand': 'string',
                              'RightOperand': 'string',
                              'Type': 'INNER'|'OUTER'|'LEFT'|'RIGHT',
                              'OnClause': 'string'
                          },
                          'PhysicalTableId': 'string'
                      }
                  }
              },
              ImportMode='SPICE'|'DIRECT_QUERY',
              ColumnGroups=[
                  {
                      'GeoSpatialColumnGroup': {
                          'Name': 'string',
                          'CountryCode': 'US',
                          'Columns': [
                              'string',
                          ]
                      }
                  },
              ],
              Permissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              RowLevelPermissionDataSet={
                  'Arn': 'string',
                  'PermissionPolicy': 'GRANT_ACCESS'|'DENY_ACCESS'
              },
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          An ID for the dataset you want to create. This is unique per region per AWS account.

        :type Name: string
        :param Name: **[REQUIRED]**

          The display name for the dataset.

        :type PhysicalTableMap: dict
        :param PhysicalTableMap: **[REQUIRED]**

          Declares the physical tables that are available in the underlying data sources.

          - *(string) --*

            - *(dict) --*

              A view of a data source. Contains information on the shape of the data in the
              underlying source. This is a variant type structure. No more than one of the
              attributes can be non-null for this structure to be valid.

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

        :type LogicalTableMap: dict
        :param LogicalTableMap:

          Configures the combination and transformation of the data from the physical tables.

          - *(string) --*

            - *(dict) --*

              A unit that joins and data transformations operate on. A logical table has a source,
              which can be either a physical table or result of a join. When it points to a physical
              table, a logical table acts as a mutable copy of that table through transform
              operations.

              - **Alias** *(string) --* **[REQUIRED]**

                A display name for the logical table.

              - **DataTransforms** *(list) --*

                Transform operations that act on this logical table.

                - *(dict) --*

                  A data transformation on a logical table. This is a variant type structure. No
                  more than one of the attributes should be non-null for this structure to be valid.

                  - **ProjectOperation** *(dict) --*

                    An operation that projects columns. Operations that come after a projection can
                    only refer to projected columns.

                    - **ProjectedColumns** *(list) --* **[REQUIRED]**

                      Projected columns.

                      - *(string) --*

                  - **FilterOperation** *(dict) --*

                    An operation that filters rows based on some condition.

                    - **ConditionExpression** *(string) --* **[REQUIRED]**

                      An expression that must evaluate to a boolean value. Rows for which the
                      expression is evaluated to true are kept in the dataset.

                  - **CreateColumnsOperation** *(dict) --*

                    An operation that creates calculated columns. Columns created in one such
                    operation form a lexical closure.

                    - **Columns** *(list) --* **[REQUIRED]**

                      Calculated columns to create.

                      - *(dict) --*

                        A calculated column for a dataset.

                        - **ColumnName** *(string) --* **[REQUIRED]**

                          Column name.

                        - **ColumnId** *(string) --* **[REQUIRED]**

                          A unique ID to identify a calculated column. During dataset update, if the
                          column ID of a calculated column matches that of an existing calculated
                          column, QuickSight preserves the existing calculated column.

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

                      When casting a column from string to datetime type, you can supply a
                      QuickSight supported format string to denote the source data format.

                  - **TagColumnOperation** *(dict) --*

                    An operation that tags a column with additional information.

                    - **ColumnName** *(string) --* **[REQUIRED]**

                      The column that this operation acts on.

                    - **Tags** *(list) --* **[REQUIRED]**

                      The dataset column tag, currently only used for geospatial type tagging. .

                      .. note::

                        This is not tags for the AWS tagging feature. .

                      - *(dict) --*

                        A tag for a column in a TagColumnOperation. This is a variant type
                        structure. No more than one of the attributes should be non-null for this
                        structure to be valid.

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

        :type ImportMode: string
        :param ImportMode: **[REQUIRED]**

          Indicates whether or not you want to import the data into SPICE.

        :type ColumnGroups: list
        :param ColumnGroups:

          Groupings of columns that work together in certain QuickSight features. Currently only
          geospatial hierarchy is supported.

          - *(dict) --*

            Groupings of columns that work together in certain QuickSight features. This is a
            variant type structure. No more than one of the attributes should be non-null for this
            structure to be valid.

            - **GeoSpatialColumnGroup** *(dict) --*

              Geospatial column group that denotes a hierarchy.

              - **Name** *(string) --* **[REQUIRED]**

                A display name for the hierarchy.

              - **CountryCode** *(string) --* **[REQUIRED]**

                Country code.

              - **Columns** *(list) --* **[REQUIRED]**

                Columns in this hierarchy.

                - *(string) --*

        :type Permissions: list
        :param Permissions:

          A list of resource permissions on the dataset.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type RowLevelPermissionDataSet: dict
        :param RowLevelPermissionDataSet:

          Row-level security configuration on the data you want to create.

          - **Arn** *(string) --* **[REQUIRED]**

            The Amazon Resource name (ARN) of the permission dataset.

          - **PermissionPolicy** *(string) --* **[REQUIRED]**

            Permission policy.

        :type Tags: list
        :param Tags:

          Contains a map of the key-value pairs for the resource tag or tags assigned to the
          dataset.

          - *(dict) --*

            The keys of the key-value pairs for the resource tag or tags assigned to the resource.

            - **Key** *(string) --* **[REQUIRED]**

              Tag key.

            - **Value** *(string) --* **[REQUIRED]**

              Tag value.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSetId': 'string',
                'IngestionArn': 'string',
                'IngestionId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The ARN of the dataset.

            - **DataSetId** *(string) --*

              The ID for the dataset you want to create. This is unique per region per AWS account.

            - **IngestionArn** *(string) --*

              The Amazon Resource Name (ARN) for the ingestion, which is triggered as a result of
              dataset creation if the import mode is SPICE

            - **IngestionId** *(string) --*

              The ID of the ingestion, which is triggered as a result of dataset creation if the
              import mode is SPICE

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_data_source(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        Type: str,
        DataSourceParameters: ClientCreateDataSourceDataSourceParametersTypeDef = None,
        Credentials: ClientCreateDataSourceCredentialsTypeDef = None,
        Permissions: List[ClientCreateDataSourcePermissionsTypeDef] = None,
        VpcConnectionProperties: ClientCreateDataSourceVpcConnectionPropertiesTypeDef = None,
        SslProperties: ClientCreateDataSourceSslPropertiesTypeDef = None,
        Tags: List[ClientCreateDataSourceTagsTypeDef] = None,
    ) -> ClientCreateDataSourceResponseTypeDef:
        """
        Creates a data source.

        The permissions resource is
        ``arn:aws:quicksight:region:aws-account-id:datasource/data-source-id``

        CLI syntax:

         ``aws quicksight create-data-source \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-source-id=unique-data-source-id \\``

         ``--name='My Data Source' \\``

         ``--type=POSTGRESQL \\``

         ``--data-source-parameters='{ "PostgreSqlParameters": {``

         ``"Host": "my-db-host.example.com",``

         ``"Port": 1234,``

         ``"Database": "my-db" } }' \\``

         ``--credentials='{ "CredentialPair": {``

         ``"Username": "username",``

         ``"Password": "password" } }'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateDataSource>`_

        **Request Syntax**
        ::

          response = client.create_data_source(
              AwsAccountId='string',
              DataSourceId='string',
              Name='string',
              Type=
                  'ADOBE_ANALYTICS'|'AMAZON_ELASTICSEARCH'|'ATHENA'|'AURORA'|'AURORA_POSTGRESQL'
                  |'AWS_IOT_ANALYTICS'|'GITHUB'|'JIRA'|'MARIADB'|'MYSQL'|'POSTGRESQL'|'PRESTO'
                  |'REDSHIFT'|'S3'|'SALESFORCE'|'SERVICENOW'|'SNOWFLAKE'|'SPARK'|'SQLSERVER'
                  |'TERADATA'|'TWITTER',
              DataSourceParameters={
                  'AmazonElasticsearchParameters': {
                      'Domain': 'string'
                  },
                  'AthenaParameters': {
                      'WorkGroup': 'string'
                  },
                  'AuroraParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'AuroraPostgreSqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'AwsIotAnalyticsParameters': {
                      'DataSetName': 'string'
                  },
                  'JiraParameters': {
                      'SiteBaseUrl': 'string'
                  },
                  'MariaDbParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'MySqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'PostgreSqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'PrestoParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Catalog': 'string'
                  },
                  'RdsParameters': {
                      'InstanceId': 'string',
                      'Database': 'string'
                  },
                  'RedshiftParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string',
                      'ClusterId': 'string'
                  },
                  'S3Parameters': {
                      'ManifestFileLocation': {
                          'Bucket': 'string',
                          'Key': 'string'
                      }
                  },
                  'ServiceNowParameters': {
                      'SiteBaseUrl': 'string'
                  },
                  'SnowflakeParameters': {
                      'Host': 'string',
                      'Database': 'string',
                      'Warehouse': 'string'
                  },
                  'SparkParameters': {
                      'Host': 'string',
                      'Port': 123
                  },
                  'SqlServerParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'TeradataParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'TwitterParameters': {
                      'Query': 'string',
                      'MaxRows': 123
                  }
              },
              Credentials={
                  'CredentialPair': {
                      'Username': 'string',
                      'Password': 'string'
                  }
              },
              Permissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              VpcConnectionProperties={
                  'VpcConnectionArn': 'string'
              },
              SslProperties={
                  'DisableSsl': True|False
              },
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          An ID for the data source. This is unique per AWS Region per AWS account.

        :type Name: string
        :param Name: **[REQUIRED]**

          A display name for the data source.

        :type Type: string
        :param Type: **[REQUIRED]**

          The type of the data source. Currently the supported types for this operation are:
          ``ATHENA, AURORA, AURORA_POSTGRESQL, MARIADB, MYSQL, POSTGRESQL, PRESTO, REDSHIFT, S3,
          SNOWFLAKE, SPARK, SQLSERVER, TERADATA`` . Use ``ListDataSources`` to return a list of all
          data sources.

        :type DataSourceParameters: dict
        :param DataSourceParameters:

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

              Location of the Amazon S3 manifest file. This is NULL if the manifest file was
              uploaded in the console.

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

        :type Credentials: dict
        :param Credentials:

          The credentials QuickSight uses to connect to your underlying source. Currently only
          username/password based credentials are supported.

          - **CredentialPair** *(dict) --*

            Credential pair.

            - **Username** *(string) --* **[REQUIRED]**

              Username.

            - **Password** *(string) --* **[REQUIRED]**

              Password.

        :type Permissions: list
        :param Permissions:

          A list of resource permissions on the data source.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type VpcConnectionProperties: dict
        :param VpcConnectionProperties:

          You need to use this parameter only when you want QuickSight to use a VPC connection when
          connecting to your underlying source.

          - **VpcConnectionArn** *(string) --* **[REQUIRED]**

            VPC connection ARN.

        :type SslProperties: dict
        :param SslProperties:

          SSL properties that apply when QuickSight connects to your underlying source.

          - **DisableSsl** *(boolean) --*

            A boolean flag to control whether SSL should be disabled.

        :type Tags: list
        :param Tags:

          Contains a map of the key-value pairs for the resource tag or tags assigned to the data
          source.

          - *(dict) --*

            The keys of the key-value pairs for the resource tag or tags assigned to the resource.

            - **Key** *(string) --* **[REQUIRED]**

              Tag key.

            - **Value** *(string) --* **[REQUIRED]**

              Tag value.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSourceId': 'string',
                'CreationStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = None
    ) -> ClientCreateGroupResponseTypeDef:
        """
        Creates an Amazon QuickSight group.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<relevant-aws-account-id>*
        :group/default/*<group-name>* `` .

        The response is a group object.

         **CLI Sample:**

         ``aws quicksight create-group --aws-account-id=111122223333 --namespace=default
         --group-name="Sales-Management" --description="Sales Management - Forecasting"``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateGroup>`_

        **Request Syntax**
        ::

          response = client.create_group(
              GroupName='string',
              Description='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          A name for the group that you want to create.

        :type Description: string
        :param Description:

          A description for the group that you want to create.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Group': {
                    'Arn': 'string',
                    'GroupName': 'string',
                    'Description': 'string',
                    'PrincipalId': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_group_membership(
        self, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> ClientCreateGroupMembershipResponseTypeDef:
        """
        Adds an Amazon QuickSight user to an Amazon QuickSight group.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*<group-name>* `` .

        The condition resource is the user name.

        The condition key is ``quicksight:UserName`` .

        The response is the group member object.

         **CLI Sample:**

         ``aws quicksight create-group-membership --aws-account-id=111122223333 --namespace=default
         --group-name=Sales --member-name=Pat``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateGroupMembership>`_

        **Request Syntax**
        ::

          response = client.create_group_membership(
              MemberName='string',
              GroupName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type MemberName: string
        :param MemberName: **[REQUIRED]**

          The name of the user that you want to add to the group membership.

        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to add the user to.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'GroupMember': {
                    'Arn': 'string',
                    'MemberName': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_iam_policy_assignment(
        self,
        AwsAccountId: str,
        AssignmentName: str,
        AssignmentStatus: str,
        Namespace: str,
        PolicyArn: str = None,
        Identities: Dict[str, List[str]] = None,
    ) -> ClientCreateIamPolicyAssignmentResponseTypeDef:
        """
        Creates an assignment with one specified IAM policy ARN and will assigned to specified
        groups or users of QuickSight. Users and groups need to be in the same namespace.

        CLI syntax:

         ``aws quicksight create-iam-policy-assignment --aws-account-id=111122223333
         --assignment-name=helpAssignment --policy-arn=arn:aws:iam::aws:policy/AdministratorAccess
         --identities="user=user5,engineer123,group=QS-Admin" --namespace=default
         --region=us-west-2``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateIAMPolicyAssignment>`_

        **Request Syntax**
        ::

          response = client.create_iam_policy_assignment(
              AwsAccountId='string',
              AssignmentName='string',
              AssignmentStatus='ENABLED'|'DRAFT'|'DISABLED',
              PolicyArn='string',
              Identities={
                  'string': [
                      'string',
                  ]
              },
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID where you want to assign QuickSight users or groups to an IAM policy.

        :type AssignmentName: string
        :param AssignmentName: **[REQUIRED]**

          The name of the assignment. It must be unique within an AWS account.

        :type AssignmentStatus: string
        :param AssignmentStatus: **[REQUIRED]**

          The status of an assignment:

          * ENABLED - Anything specified in this assignment is used while creating the data source.

          * DISABLED - This assignment isn't used while creating the data source.

          * DRAFT - Assignment is an unfinished draft and isn't used while creating the data source.

        :type PolicyArn: string
        :param PolicyArn:

          An IAM policy ARN that you want to apply to the QuickSight users and groups specified in
          this assignment.

        :type Identities: dict
        :param Identities:

          QuickSight users and/or groups that you want to assign the policy to.

          - *(string) --*

            - *(list) --*

              - *(string) --*

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace that contains the assignment.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'AssignmentName': 'string',
                'AssignmentId': 'string',
                'AssignmentStatus': 'ENABLED'|'DRAFT'|'DISABLED',
                'PolicyArn': 'string',
                'Identities': {
                    'string': [
                        'string',
                    ]
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **AssignmentName** *(string) --*

              The name of the assignment. Must be unique within an AWS account.

            - **AssignmentId** *(string) --*

              An ID for the assignment.

            - **AssignmentStatus** *(string) --*

              The status of an assignment:

              * ENABLED - Anything specified in this assignment is used while creating the data
              source.

              * DISABLED - This assignment isn't used while creating the data source.

              * DRAFT - Assignment is an unfinished draft and isn't used while creating the data
              source.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_ingestion(
        self, DataSetId: str, IngestionId: str, AwsAccountId: str
    ) -> ClientCreateIngestionResponseTypeDef:
        """
        Creates and starts a new SPICE ingestion on a dataset

        Any ingestions operating on tagged datasets inherit the same tags automatically for use in
        access-control. For an example, see `How do I create an IAM policy to control access to
        Amazon EC2 resources using tags?
        <https://aws.example.com/premiumsupport/knowledge-center/iam-ec2-resource-tags/>`__ . Tags
        will be visible on the tagged dataset, but not on the ingestion resource.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateIngestion>`_

        **Request Syntax**
        ::

          response = client.create_ingestion(
              DataSetId='string',
              IngestionId='string',
              AwsAccountId='string'
          )
        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID of the dataset used in the ingestion.

        :type IngestionId: string
        :param IngestionId: **[REQUIRED]**

          An ID for the ingestion.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'IngestionId': 'string',
                'IngestionStatus':
                'INITIALIZED'|'QUEUED'|'RUNNING'|'FAILED'|'COMPLETED'|'CANCELLED',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_template(
        self,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: ClientCreateTemplateSourceEntityTypeDef,
        Name: str = None,
        Permissions: List[ClientCreateTemplatePermissionsTypeDef] = None,
        Tags: List[ClientCreateTemplateTagsTypeDef] = None,
        VersionDescription: str = None,
    ) -> ClientCreateTemplateResponseTypeDef:
        """
        Creates a template from an existing QuickSight analysis or template. The resulting template
        can be used to create a dashboard.

        A template is an entity in QuickSight which encapsulates the metadata required to create an
        analysis that can be used to create dashboard. It adds a layer of abstraction by use
        placeholders to replace the dataset associated with the analysis. You can use templates to
        create dashboards by replacing dataset placeholders with datasets which follow the same
        schema that was used to create the source analysis and template.

        To create a template from an existing analysis, use the analysis's ARN, ``aws-account-id`` ,
        ``template-id`` , ``source-entity`` , and ``data-set-references`` .

        CLI syntax to create a template:

         ``aws quicksight create-template —cli-input-json file://create-template.json``

        CLI syntax to create a template from another template in the same AWS account:

         ``aws quicksight create-template --aws-account-id 111122223333 --template-id
         reports_test_template --data-set-references
         DataSetPlaceholder=reports,DataSetArn=
             arn:aws:quicksight:us-west-2:111122223333:dataset/0dfc789c-81f6-4f4f-b9ac-7db2453eefc8
         DataSetPlaceholder=Elblogs,DataSetArn=
             arn:aws:quicksight:us-west-2:111122223333:dataset/f60da323-af68-45db-9016-08e0d1d7ded5
         --source-entity
         SourceAnalysis='{Arn=
             arn:aws:quicksight:us-west-2:111122223333:analysis/7fb74527-c36d-4be8-8139-ac1be4c97365}'``

        To create template from another account’s template, you need to grant cross account resource
        permission for DescribeTemplate the account that contains the template.

        You can use a file to pass JSON to the function if you prefer.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateTemplate>`_

        **Request Syntax**
        ::

          response = client.create_template(
              AwsAccountId='string',
              TemplateId='string',
              Name='string',
              Permissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              SourceEntity={
                  'SourceAnalysis': {
                      'Arn': 'string',
                      'DataSetReferences': [
                          {
                              'DataSetPlaceholder': 'string',
                              'DataSetArn': 'string'
                          },
                      ]
                  },
                  'SourceTemplate': {
                      'Arn': 'string'
                  }
              },
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ],
              VersionDescription='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template you want to create. This is unique per AWS region per AWS account.

        :type Name: string
        :param Name:

          A display name for the template.

        :type Permissions: list
        :param Permissions:

          A list of resource permissions to be set on the template. The shorthand syntax should look
          similar to this: ``Shorthand Syntax: Principal=string,Actions=string,string ...``

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type SourceEntity: dict
        :param SourceEntity: **[REQUIRED]**

          The ARN of the source entity from which this template is being created. Templates can be
          currently created from an analysis or another template. If the ARN is for an analysis, you
          must include its dataset references.

          - **SourceAnalysis** *(dict) --*

            The source analysis, if it is based on an analysis.

            - **Arn** *(string) --* **[REQUIRED]**

              The Amazon Resource name (ARN) of the resource.

            - **DataSetReferences** *(list) --* **[REQUIRED]**

              A structure containing information about the dataset references used as placeholders
              in the template.

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

        :type Tags: list
        :param Tags:

          Contains a map of the key-value pairs for the resource tag or tags assigned to the
          resource.

          - *(dict) --*

            The keys of the key-value pairs for the resource tag or tags assigned to the resource.

            - **Key** *(string) --* **[REQUIRED]**

              Tag key.

            - **Value** *(string) --* **[REQUIRED]**

              Tag value.

        :type VersionDescription: string
        :param VersionDescription:

          A description of the current template version being created. This API created the first
          version of the template. Every time UpdateTemplate is called a new version is created.
          Each version of the template maintains a description of the version in the
          VersionDescription field.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'VersionArn': 'string',
                'TemplateId': 'string',
                'CreationStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The Amazon Resource Name (ARN) for the template.

            - **VersionArn** *(string) --*

              The Amazon Resource Name (ARN) for the template, including the version information of
              the first version.

            - **TemplateId** *(string) --*

              The ID of the template.

            - **CreationStatus** *(string) --*

              The template creation status.

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> ClientCreateTemplateAliasResponseTypeDef:
        """
        Creates a template alias for a template.

        CLI syntax:

         ``aws quicksight create-template-alias --aws-account-id 111122223333 --template-id
         'reports_test_template' --alias-name PROD —version-number 1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/CreateTemplateAlias>`_

        **Request Syntax**
        ::

          response = client.create_template_alias(
              AwsAccountId='string',
              TemplateId='string',
              AliasName='string',
              TemplateVersionNumber=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template you are aliasing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template.

        :type AliasName: string
        :param AliasName: **[REQUIRED]**

          The name you want to give the template's alias. Alias names can't begin with a ``$`` ,
          which is reserved by QuickSight. Alias names that start with ‘$’ sign are QuickSight
          reserved naming and can't be deleted.

        :type TemplateVersionNumber: integer
        :param TemplateVersionNumber: **[REQUIRED]**

          The version number of the template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateAlias': {
                    'AliasName': 'string',
                    'Arn': 'string',
                    'TemplateVersionNumber': 123
                },
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_dashboard(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int = None
    ) -> ClientDeleteDashboardResponseTypeDef:
        """
        Deletes a dashboard.

        CLI syntax:

         ``aws quicksight delete-dashboard --aws-account-id 111122223333 —dashboard-id 123123123``

         ``aws quicksight delete-dashboard --aws-account-id 111122223333 —dashboard-id 123123123
         —version-number 3``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteDashboard>`_

        **Request Syntax**
        ::

          response = client.delete_dashboard(
              AwsAccountId='string',
              DashboardId='string',
              VersionNumber=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are deleting.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type VersionNumber: integer
        :param VersionNumber:

          The version number of the dashboard. If version number property is provided, only the
          specified version of the dashboard is deleted.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Status': 123,
                'Arn': 'string',
                'DashboardId': 'string',
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **Status** *(integer) --*

              The http status of the request.

            - **Arn** *(string) --*

              The ARN of the resource.

            - **DashboardId** *(string) --*

              The ID of the dashboard.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_data_set(
        self, AwsAccountId: str, DataSetId: str
    ) -> ClientDeleteDataSetResponseTypeDef:
        """
        Deletes a dataset.

        CLI syntax:

         ``aws quicksight delete-data-set \\``

         ``--aws-account-id=111111111111 \\``

         ``--data-set-id=unique-data-set-id``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteDataSet>`_

        **Request Syntax**
        ::

          response = client.delete_data_set(
              AwsAccountId='string',
              DataSetId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID for the dataset you want to create. This is unique per region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSetId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The ARN of the dataset.

            - **DataSetId** *(string) --*

              The ID for the dataset you want to create. This is unique per region per AWS account.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_data_source(
        self, AwsAccountId: str, DataSourceId: str
    ) -> ClientDeleteDataSourceResponseTypeDef:
        """
        Deletes the data source permanently. This action breaks all the datasets that reference the
        deleted data source.

        CLI syntax:

         ``aws quicksight delete-data-source \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-source-id=unique-data-source-id``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteDataSource>`_

        **Request Syntax**
        ::

          response = client.delete_data_source(
              AwsAccountId='string',
              DataSourceId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          The ID of the data source. This is unique per AWS Region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSourceId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The ARN of the data source you deleted.

            - **DataSourceId** *(string) --*

              The ID of the data source. This is unique per AWS Region per AWS account.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> ClientDeleteGroupResponseTypeDef:
        """
        Removes a user group from Amazon QuickSight.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*<group-name>* `` .

         **CLI Sample:**

         ``aws quicksight delete-group -\\-aws-account-id=111122223333 -\\-namespace=default
         -\\-group-name=Sales-Management``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteGroup>`_

        **Request Syntax**
        ::

          response = client.delete_group(
              GroupName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to delete.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_group_membership(
        self, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> ClientDeleteGroupMembershipResponseTypeDef:
        """
        Removes a user from a group so that the user is no longer a member of the group.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*<group-name>* `` .

        The condition resource is the user name.

        The condition key is ``quicksight:UserName`` .

         **CLI Sample:**

         ``aws quicksight delete-group-membership --aws-account-id=111122223333 --namespace=default
         --group-name=Sales-Management --member-name=Charlie``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteGroupMembership>`_

        **Request Syntax**
        ::

          response = client.delete_group_membership(
              MemberName='string',
              GroupName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type MemberName: string
        :param MemberName: **[REQUIRED]**

          The name of the user that you want to delete from the group membership.

        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to delete the user from.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_iam_policy_assignment(
        self, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> ClientDeleteIamPolicyAssignmentResponseTypeDef:
        """
        Deletes an existing assignment.

        CLI syntax:

         ``aws quicksight delete-iam-policy-assignment --aws-account-id=111122223333
         --assignment-name=testtest --region=us-east-1 --namespace=default``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteIAMPolicyAssignment>`_

        **Request Syntax**
        ::

          response = client.delete_iam_policy_assignment(
              AwsAccountId='string',
              AssignmentName='string',
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID where you want to delete an IAM policy assignment.

        :type AssignmentName: string
        :param AssignmentName: **[REQUIRED]**

          The name of the assignment.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace that contains the assignment.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'AssignmentName': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **AssignmentName** *(string) --*

              The name of the assignment.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_template(
        self, AwsAccountId: str, TemplateId: str, VersionNumber: int = None
    ) -> ClientDeleteTemplateResponseTypeDef:
        """
        Deletes a template.

        CLI syntax:

        * ``aws quicksight delete-template --aws-account-id 111122223333 —-template-id
        reports_test_template --version-number 2``

        * ``aws quicksight delete-template —aws-account-id 111122223333 —template-id
        reports_test_template —alias-name STAGING``

        * ``aws quicksight delete-template —aws-account-id 111122223333 —template-id
        reports_test_template —alias-name ‘\\$LATEST’``

        * ``aws quicksight delete-template --aws-account-id 111122223333 —-template-id
        reports_test_template``

        If version number which is an optional field is not passed the template (including all the
        versions) is deleted by the API, if version number is provided, the specific template
        version is deleted by the API.

        Users can explicitly describe the latest version of the template by passing ``$LATEST`` to
        the ``alias-name`` parameter. ``$LATEST`` is an internally supported alias, which points to
        the latest version of the template.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteTemplate>`_

        **Request Syntax**
        ::

          response = client.delete_template(
              AwsAccountId='string',
              TemplateId='string',
              VersionNumber=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template you are deleting.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template you want to delete.

        :type VersionNumber: integer
        :param VersionNumber:

          The version number

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Arn': 'string',
                'TemplateId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Arn** *(string) --*

              The ARN of the resource.

            - **TemplateId** *(string) --*

              An ID for the template.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> ClientDeleteTemplateAliasResponseTypeDef:
        """
        Update template alias of given template.

        CLI syntax:

         ``aws quicksight delete-template-alias --aws-account-id 111122223333 --template-id
         'reports_test_template' --alias-name 'STAGING'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteTemplateAlias>`_

        **Request Syntax**
        ::

          response = client.delete_template_alias(
              AwsAccountId='string',
              TemplateId='string',
              AliasName='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template alias you are deleting.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template.

        :type AliasName: string
        :param AliasName: **[REQUIRED]**

          The alias of the template. If alias-name is provided, the version that the alias-name
          points to is deleted. Alias names that start with ``$`` are reserved by QuickSight and
          can't be deleted.”

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Status': 123,
                'TemplateId': 'string',
                'AliasName': 'string',
                'Arn': 'string',
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_user(
        self, UserName: str, AwsAccountId: str, Namespace: str
    ) -> ClientDeleteUserResponseTypeDef:
        """
        Deletes the Amazon QuickSight user that is associated with the identity of the AWS Identity
        and Access Management (IAM) user or role that's making the call. The IAM user isn't deleted
        as a result of this call.

         **CLI Sample:**

         ``aws quicksight delete-user --aws-account-id=111122223333 --namespace=default
         --user-name=Pat``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteUser>`_

        **Request Syntax**
        ::

          response = client.delete_user(
              UserName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**

          The name of the user that you want to delete.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_user_by_principal_id(
        self, PrincipalId: str, AwsAccountId: str, Namespace: str
    ) -> ClientDeleteUserByPrincipalIdResponseTypeDef:
        """
        Deletes a user identified by its principal ID.

         **CLI Sample:**

         ``aws quicksight delete-user-by-principal-id --aws-account-id=111122223333
         --namespace=default --principal-id=ABCDEFJA26JLI7EUUOEHS``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DeleteUserByPrincipalId>`_

        **Request Syntax**
        ::

          response = client.delete_user_by_principal_id(
              PrincipalId='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type PrincipalId: string
        :param PrincipalId: **[REQUIRED]**

          The principal ID of the user.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_dashboard(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int = None, AliasName: str = None
    ) -> ClientDescribeDashboardResponseTypeDef:
        """
        Provides a summary for a dashboard.

        CLI syntax:

        * ``aws quicksight describe-dashboard --aws-account-id 111122223333 —dashboard-id
        reports_test_report -version-number 2``

        * ``aws quicksight describe-dashboard --aws-account-id 111122223333 —dashboard-id
        reports_test_report -alias-name ‘$PUBLISHED’``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDashboard>`_

        **Request Syntax**
        ::

          response = client.describe_dashboard(
              AwsAccountId='string',
              DashboardId='string',
              VersionNumber=123,
              AliasName='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are describing.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type VersionNumber: integer
        :param VersionNumber:

          The version number for the dashboard. If version number isn’t passed the latest published
          dashboard version is described.

        :type AliasName: string
        :param AliasName:

          The alias name.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Dashboard': {
                    'DashboardId': 'string',
                    'Arn': 'string',
                    'Name': 'string',
                    'Version': {
                        'CreatedTime': datetime(2015, 1, 1),
                        'Errors': [
                            {
                                'Type':
                                'DATA_SET_NOT_FOUND'|'INTERNAL_FAILURE'
                                |'PARAMETER_VALUE_INCOMPATIBLE'
                                |'PARAMETER_TYPE_INVALID'
                                |'PARAMETER_NOT_FOUND'
                                |'COLUMN_TYPE_MISMATCH'
                                |'COLUMN_GEOGRAPHIC_ROLE_MISMATCH'
                                |'COLUMN_REPLACEMENT_MISSING',
                                'Message': 'string'
                            },
                        ],
                        'VersionNumber': 123,
                        'Status':
                        'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'
                        |'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'
                        |'UPDATE_FAILED',
                        'Arn': 'string',
                        'SourceEntityArn': 'string',
                        'Description': 'string'
                    },
                    'CreatedTime': datetime(2015, 1, 1),
                    'LastPublishedTime': datetime(2015, 1, 1),
                    'LastUpdatedTime': datetime(2015, 1, 1)
                },
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_dashboard_permissions(
        self, AwsAccountId: str, DashboardId: str
    ) -> ClientDescribeDashboardPermissionsResponseTypeDef:
        """
        Describes read and write permissions on a dashboard.

        CLI syntax:

         ``aws quicksight describe-dashboard-permissions --aws-account-id 735340738645 —dashboard-id
         reports_test_bob_report``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDashboardPermissions>`_

        **Request Syntax**
        ::

          response = client.describe_dashboard_permissions(
              AwsAccountId='string',
              DashboardId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are describing permissions of.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard, also added to IAM policy.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DashboardId': 'string',
                'DashboardArn': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **DashboardId** *(string) --*

              The ID for the dashboard.

            - **DashboardArn** *(string) --*

              The ARN of the dashboard.

            - **Permissions** *(list) --*

              A structure that contains the permissions of the dashboard.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_data_set(
        self, AwsAccountId: str, DataSetId: str
    ) -> ClientDescribeDataSetResponseTypeDef:
        """
        Describes a dataset.

        CLI syntax:

         ``aws quicksight describe-data-set \\``

         ``--aws-account-id=111111111111 \\``

         ``--data-set-id=unique-data-set-id``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDataSet>`_

        **Request Syntax**
        ::

          response = client.describe_data_set(
              AwsAccountId='string',
              DataSetId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID for the dataset you want to create. This is unique per region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSet': {
                    'Arn': 'string',
                    'DataSetId': 'string',
                    'Name': 'string',
                    'CreatedTime': datetime(2015, 1, 1),
                    'LastUpdatedTime': datetime(2015, 1, 1),
                    'PhysicalTableMap': {
                        'string': {
                            'RelationalTable': {
                                'DataSourceArn': 'string',
                                'Schema': 'string',
                                'Name': 'string',
                                'InputColumns': [
                                    {
                                        'Name': 'string',
                                        'Type':
                                        'STRING'|'INTEGER'|'DECIMAL'
                                        |'DATETIME'|'BIT'|'BOOLEAN'
                                        |'JSON'
                                    },
                                ]
                            },
                            'CustomSql': {
                                'DataSourceArn': 'string',
                                'Name': 'string',
                                'SqlQuery': 'string',
                                'Columns': [
                                    {
                                        'Name': 'string',
                                        'Type':
                                        'STRING'|'INTEGER'|'DECIMAL'
                                        |'DATETIME'|'BIT'|'BOOLEAN'
                                        |'JSON'
                                    },
                                ]
                            },
                            'S3Source': {
                                'DataSourceArn': 'string',
                                'UploadSettings': {
                                    'Format': 'CSV'|'TSV'|'CLF'|'ELF'|'XLSX'|'JSON',
                                    'StartFromRow': 123,
                                    'ContainsHeader': True|False,
                                    'TextQualifier': 'DOUBLE_QUOTE'|'SINGLE_QUOTE',
                                    'Delimiter': 'string'
                                },
                                'InputColumns': [
                                    {
                                        'Name': 'string',
                                        'Type':
                                        'STRING'|'INTEGER'|'DECIMAL'
                                        |'DATETIME'|'BIT'|'BOOLEAN'
                                        |'JSON'
                                    },
                                ]
                            }
                        }
                    },
                    'LogicalTableMap': {
                        'string': {
                            'Alias': 'string',
                            'DataTransforms': [
                                {
                                    'ProjectOperation': {
                                        'ProjectedColumns': [
                                            'string',
                                        ]
                                    },
                                    'FilterOperation': {
                                        'ConditionExpression': 'string'
                                    },
                                    'CreateColumnsOperation': {
                                        'Columns': [
                                            {
                                                'ColumnName': 'string',
                                                'ColumnId': 'string',
                                                'Expression': 'string'
                                            },
                                        ]
                                    },
                                    'RenameColumnOperation': {
                                        'ColumnName': 'string',
                                        'NewColumnName': 'string'
                                    },
                                    'CastColumnTypeOperation': {
                                        'ColumnName': 'string',
                                        'NewColumnType': 'STRING'|'INTEGER'|'DECIMAL'|'DATETIME',
                                        'Format': 'string'
                                    },
                                    'TagColumnOperation': {
                                        'ColumnName': 'string',
                                        'Tags': [
                                            {
                                                'ColumnGeographicRole':
                                                'COUNTRY'
                                                |'STATE'
                                                |'COUNTY'
                                                |'CITY'
                                                |'POSTCODE'
                                                |'LONGITUDE'
                                                |'LATITUDE'
                                            },
                                        ]
                                    }
                                },
                            ],
                            'Source': {
                                'JoinInstruction': {
                                    'LeftOperand': 'string',
                                    'RightOperand': 'string',
                                    'Type': 'INNER'|'OUTER'|'LEFT'|'RIGHT',
                                    'OnClause': 'string'
                                },
                                'PhysicalTableId': 'string'
                            }
                        }
                    },
                    'OutputColumns': [
                        {
                            'Name': 'string',
                            'Type': 'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                        },
                    ],
                    'ImportMode': 'SPICE'|'DIRECT_QUERY',
                    'ConsumedSpiceCapacityInBytes': 123,
                    'ColumnGroups': [
                        {
                            'GeoSpatialColumnGroup': {
                                'Name': 'string',
                                'CountryCode': 'US',
                                'Columns': [
                                    'string',
                                ]
                            }
                        },
                    ],
                    'RowLevelPermissionDataSet': {
                        'Arn': 'string',
                        'PermissionPolicy': 'GRANT_ACCESS'|'DENY_ACCESS'
                    }
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                    A view of a data source. Contains information on the shape of the data in the
                    underlying source. This is a variant type structure. No more than one of the
                    attributes can be non-null for this structure to be valid.

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

                    A unit that joins and data transformations operate on. A logical table has a
                    source, which can be either a physical table or result of a join. When it points
                    to a physical table, a logical table acts as a mutable copy of that table
                    through transform operations.

                    - **Alias** *(string) --*

                      A display name for the logical table.

                    - **DataTransforms** *(list) --*

                      Transform operations that act on this logical table.

                      - *(dict) --*

                        A data transformation on a logical table. This is a variant type structure.
                        No more than one of the attributes should be non-null for this structure to
                        be valid.

                        - **ProjectOperation** *(dict) --*

                          An operation that projects columns. Operations that come after a
                          projection can only refer to projected columns.

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

                                A unique ID to identify a calculated column. During dataset update,
                                if the column ID of a calculated column matches that of an existing
                                calculated column, QuickSight preserves the existing calculated
                                column.

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

                            When casting a column from string to datetime type, you can supply a
                            QuickSight supported format string to denote the source data format.

                        - **TagColumnOperation** *(dict) --*

                          An operation that tags a column with additional information.

                          - **ColumnName** *(string) --*

                            The column that this operation acts on.

                          - **Tags** *(list) --*

                            The dataset column tag, currently only used for geospatial type tagging.
                            .

                            .. note::

                              This is not tags for the AWS tagging feature. .

                            - *(dict) --*

                              A tag for a column in a TagColumnOperation. This is a variant type
                              structure. No more than one of the attributes should be non-null for
                              this structure to be valid.

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

                The amount of SPICE capacity used by this dataset. This is 0 if the dataset isn't
                imported into SPICE.

              - **ColumnGroups** *(list) --*

                Groupings of columns that work together in certain QuickSight features. Currently
                only geospatial hierarchy is supported.

                - *(dict) --*

                  Groupings of columns that work together in certain QuickSight features. This is a
                  variant type structure. No more than one of the attributes should be non-null for
                  this structure to be valid.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_data_set_permissions(
        self, AwsAccountId: str, DataSetId: str
    ) -> ClientDescribeDataSetPermissionsResponseTypeDef:
        """
        Describes the permissions on a dataset.

        The permissions resource is ``arn:aws:quicksight:region:aws-account-id:dataset/data-set-id``

        CLI syntax:

         ``aws quicksight describe-data-set-permissions \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-set-id=unique-data-set-id \\``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDataSetPermissions>`_

        **Request Syntax**
        ::

          response = client.describe_data_set_permissions(
              AwsAccountId='string',
              DataSetId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID for the dataset you want to create. This is unique per region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSetArn': 'string',
                'DataSetId': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DataSetArn** *(string) --*

              The ARN of the dataset.

            - **DataSetId** *(string) --*

              The ID for the dataset you want to create. This is unique per region per AWS account.

            - **Permissions** *(list) --*

              A list of resource permissions on the dataset.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_data_source(
        self, AwsAccountId: str, DataSourceId: str
    ) -> ClientDescribeDataSourceResponseTypeDef:
        """
        Describes a data source.

        The permissions resource is
        ``arn:aws:quicksight:region:aws-account-id:datasource/data-source-id``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDataSource>`_

        **Request Syntax**
        ::

          response = client.describe_data_source(
              AwsAccountId='string',
              DataSourceId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          The ID of the data source. This is unique per AWS Region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSource': {
                    'Arn': 'string',
                    'DataSourceId': 'string',
                    'Name': 'string',
                    'Type':
                    'ADOBE_ANALYTICS'|'AMAZON_ELASTICSEARCH'|'ATHENA'|'AURORA'
                    |'AURORA_POSTGRESQL'|'AWS_IOT_ANALYTICS'|'GITHUB'|'JIRA'|'MARIADB'
                    |'MYSQL'|'POSTGRESQL'|'PRESTO'|'REDSHIFT'|'S3'|'SALESFORCE'
                    |'SERVICENOW'|'SNOWFLAKE'|'SPARK'|'SQLSERVER'|'TERADATA'|'TWITTER',
                    'Status':
                    'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                    |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                    'CreatedTime': datetime(2015, 1, 1),
                    'LastUpdatedTime': datetime(2015, 1, 1),
                    'DataSourceParameters': {
                        'AmazonElasticsearchParameters': {
                            'Domain': 'string'
                        },
                        'AthenaParameters': {
                            'WorkGroup': 'string'
                        },
                        'AuroraParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'AuroraPostgreSqlParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'AwsIotAnalyticsParameters': {
                            'DataSetName': 'string'
                        },
                        'JiraParameters': {
                            'SiteBaseUrl': 'string'
                        },
                        'MariaDbParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'MySqlParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'PostgreSqlParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'PrestoParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Catalog': 'string'
                        },
                        'RdsParameters': {
                            'InstanceId': 'string',
                            'Database': 'string'
                        },
                        'RedshiftParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string',
                            'ClusterId': 'string'
                        },
                        'S3Parameters': {
                            'ManifestFileLocation': {
                                'Bucket': 'string',
                                'Key': 'string'
                            }
                        },
                        'ServiceNowParameters': {
                            'SiteBaseUrl': 'string'
                        },
                        'SnowflakeParameters': {
                            'Host': 'string',
                            'Database': 'string',
                            'Warehouse': 'string'
                        },
                        'SparkParameters': {
                            'Host': 'string',
                            'Port': 123
                        },
                        'SqlServerParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'TeradataParameters': {
                            'Host': 'string',
                            'Port': 123,
                            'Database': 'string'
                        },
                        'TwitterParameters': {
                            'Query': 'string',
                            'MaxRows': 123
                        }
                    },
                    'VpcConnectionProperties': {
                        'VpcConnectionArn': 'string'
                    },
                    'SslProperties': {
                        'DisableSsl': True|False
                    },
                    'ErrorInfo': {
                        'Type':
                        'TIMEOUT'|'ENGINE_VERSION_NOT_SUPPORTED'|'UNKNOWN_HOST'
                        |'GENERIC_SQL_FAILURE'|'CONFLICT'|'UNKNOWN',
                        'Message': 'string'
                    }
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DataSource** *(dict) --*

              The information on the data source.

              - **Arn** *(string) --*

                The Amazon Resource name (ARN) of the data source.

              - **DataSourceId** *(string) --*

                The ID of the data source. This is unique per AWS Region per AWS account.

              - **Name** *(string) --*

                A display name for the data source.

              - **Type** *(string) --*

                The type of the data source. This indicates which database engine the data source
                connects to.

              - **Status** *(string) --*

                The http status of the request.

              - **CreatedTime** *(datetime) --*

                The time this was created.

              - **LastUpdatedTime** *(datetime) --*

                The last time this was updated.

              - **DataSourceParameters** *(dict) --*

                The parameters QuickSight uses to connect to your underlying source. This is a
                variant type structure. At most one of the attributes should be non-null for this
                structure to be valid.

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

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_data_source_permissions(
        self, AwsAccountId: str, DataSourceId: str
    ) -> ClientDescribeDataSourcePermissionsResponseTypeDef:
        """
        Describes the resource permissions for a data source.

        The permissions resource is
        ``aws:quicksight:region:aws-account-id:datasource/data-source-id``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeDataSourcePermissions>`_

        **Request Syntax**
        ::

          response = client.describe_data_source_permissions(
              AwsAccountId='string',
              DataSourceId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          The ID of the data source. This is unique per AWS Region per AWS account.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSourceArn': 'string',
                'DataSourceId': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DataSourceArn** *(string) --*

              The ARN of the data source.

            - **DataSourceId** *(string) --*

              The ID of the data source. This is unique per AWS Region per AWS account.

            - **Permissions** *(list) --*

              A list of resource permissions on the data source.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> ClientDescribeGroupResponseTypeDef:
        """
        Returns an Amazon QuickSight group's description and Amazon Resource Name (ARN).

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<relevant-aws-account-id>*
        :group/default/*<group-name>* `` .

        The response is the group object.

         **CLI Sample:**

         ``aws quicksight describe-group -\\-aws-account-id=11112222333 -\\-namespace=default
         -\\-group-name=Sales``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeGroup>`_

        **Request Syntax**
        ::

          response = client.describe_group(
              GroupName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to describe.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Group': {
                    'Arn': 'string',
                    'GroupName': 'string',
                    'Description': 'string',
                    'PrincipalId': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_iam_policy_assignment(
        self, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> ClientDescribeIamPolicyAssignmentResponseTypeDef:
        """
        Describes an existing IAMPolicy Assignment by specified assignment name.

        CLI syntax:

         ``aws quicksight describe-iam-policy-assignment --aws-account-id=111122223333
         --assignment-name=testtest --namespace=default --region=us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeIAMPolicyAssignment>`_

        **Request Syntax**
        ::

          response = client.describe_iam_policy_assignment(
              AwsAccountId='string',
              AssignmentName='string',
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID that contains the assignment you want to describe.

        :type AssignmentName: string
        :param AssignmentName: **[REQUIRED]**

          The name of the assignment.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace that contains the assignment.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'IAMPolicyAssignment': {
                    'AwsAccountId': 'string',
                    'AssignmentId': 'string',
                    'AssignmentName': 'string',
                    'PolicyArn': 'string',
                    'Identities': {
                        'string': [
                            'string',
                        ]
                    },
                    'AssignmentStatus': 'ENABLED'|'DRAFT'|'DISABLED'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_ingestion(
        self, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> ClientDescribeIngestionResponseTypeDef:
        """
        Describes a SPICE ingestion.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeIngestion>`_

        **Request Syntax**
        ::

          response = client.describe_ingestion(
              AwsAccountId='string',
              DataSetId='string',
              IngestionId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID of the dataset used in the ingestion.

        :type IngestionId: string
        :param IngestionId: **[REQUIRED]**

          An ID for the ingestion.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Ingestion': {
                    'Arn': 'string',
                    'IngestionId': 'string',
                    'IngestionStatus':
                    'INITIALIZED'|'QUEUED'|'RUNNING'|'FAILED'|'COMPLETED'|'CANCELLED',
                    'ErrorInfo': {
                        'Type':
                        'FAILURE_TO_ASSUME_ROLE'|'INGESTION_SUPERSEDED'
                        |'INGESTION_CANCELED'|'DATA_SET_DELETED'
                        |'DATA_SET_NOT_SPICE'|'S3_UPLOADED_FILE_DELETED'
                        |'S3_MANIFEST_ERROR'|'DATA_TOLERANCE_EXCEPTION'
                        |'SPICE_TABLE_NOT_FOUND'|'DATA_SET_SIZE_LIMIT_EXCEEDED'
                        |'ROW_SIZE_LIMIT_EXCEEDED'|'ACCOUNT_CAPACITY_LIMIT_EXCEEDED'
                        |'CUSTOMER_ERROR'|'DATA_SOURCE_NOT_FOUND'
                        |'IAM_ROLE_NOT_AVAILABLE'|'CONNECTION_FAILURE'
                        |'SQL_TABLE_NOT_FOUND'|'PERMISSION_DENIED'
                        |'SSL_CERTIFICATE_VALIDATION_FAILURE'|'OAUTH_TOKEN_FAILURE'
                        |'SOURCE_API_LIMIT_EXCEEDED_FAILURE'
                        |'PASSWORD_AUTHENTICATION_FAILURE'
                        |'SQL_SCHEMA_MISMATCH_ERROR'|'INVALID_DATE_FORMAT'
                        |'INVALID_DATAPREP_SYNTAX'|'SOURCE_RESOURCE_LIMIT_EXCEEDED'
                        |'SQL_INVALID_PARAMETER_VALUE'|'QUERY_TIMEOUT'
                        |'SQL_NUMERIC_OVERFLOW'|'UNRESOLVABLE_HOST'
                        |'UNROUTABLE_HOST'|'SQL_EXCEPTION'|'S3_FILE_INACCESSIBLE'
                        |'IOT_FILE_NOT_FOUND'|'IOT_DATA_SET_FILE_EMPTY'
                        |'INVALID_DATA_SOURCE_CONFIG'|'DATA_SOURCE_AUTH_FAILED'
                        |'DATA_SOURCE_CONNECTION_FAILED'
                        |'FAILURE_TO_PROCESS_JSON_FILE'|'INTERNAL_SERVICE_ERROR',
                        'Message': 'string'
                    },
                    'RowInfo': {
                        'RowsIngested': 123,
                        'RowsDropped': 123
                    },
                    'QueueInfo': {
                        'WaitingOnIngestion': 'string',
                        'QueuedIngestion': 'string'
                    },
                    'CreatedTime': datetime(2015, 1, 1),
                    'IngestionTimeInSeconds': 123,
                    'IngestionSizeInBytes': 123,
                    'RequestSource': 'MANUAL'|'SCHEDULED',
                    'RequestType': 'INITIAL_INGESTION'|'EDIT'|'INCREMENTAL_REFRESH'|'FULL_REFRESH'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_template(
        self, AwsAccountId: str, TemplateId: str, VersionNumber: int = None, AliasName: str = None
    ) -> ClientDescribeTemplateResponseTypeDef:
        """
        Describes a template's metadata.

        CLI syntax:

         ``aws quicksight describe-template --aws-account-id 111122223333 --template-id
         reports_test_template``

         ``aws quicksight describe-template --aws-account-id 111122223333 --template-id
         reports_test_template --version-number-2``

         ``aws quicksight describe-template --aws-account-id 111122223333 --template-id
         reports_test_template --alias-name '\\$LATEST'``

        Users can explicitly describe the latest version of the dashboard by passing ``$LATEST`` to
        the ``alias-name`` parameter. ``$LATEST`` is an internally supported alias, which points to
        the latest version of the dashboard.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeTemplate>`_

        **Request Syntax**
        ::

          response = client.describe_template(
              AwsAccountId='string',
              TemplateId='string',
              VersionNumber=123,
              AliasName='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template you are describing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template.

        :type VersionNumber: integer
        :param VersionNumber:

          This is an optional field, when a version number is provided the corresponding version is
          describe, if it's not provided the latest version of the template is described.

        :type AliasName: string
        :param AliasName:

          This is an optional field, when an alias name is provided, the version referenced by the
          alias is described. Refer to ``CreateTemplateAlias`` to create a template alias.
          ``$PUBLISHED`` is not supported for template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Template': {
                    'Arn': 'string',
                    'Name': 'string',
                    'Version': {
                        'CreatedTime': datetime(2015, 1, 1),
                        'Errors': [
                            {
                                'Type': 'DATA_SET_NOT_FOUND'|'INTERNAL_FAILURE',
                                'Message': 'string'
                            },
                        ],
                        'VersionNumber': 123,
                        'Status':
                        'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'
                        |'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'
                        |'UPDATE_FAILED',
                        'DataSetConfigurations': [
                            {
                                'Placeholder': 'string',
                                'DataSetSchema': {
                                    'ColumnSchemaList': [
                                        {
                                            'Name': 'string',
                                            'DataType': 'string',
                                            'GeographicRole': 'string'
                                        },
                                    ]
                                },
                                'ColumnGroupSchemaList': [
                                    {
                                        'Name': 'string',
                                        'ColumnGroupColumnSchemaList': [
                                            {
                                                'Name': 'string'
                                            },
                                        ]
                                    },
                                ]
                            },
                        ],
                        'Description': 'string',
                        'SourceEntityArn': 'string'
                    },
                    'TemplateId': 'string',
                    'LastUpdatedTime': datetime(2015, 1, 1),
                    'CreatedTime': datetime(2015, 1, 1)
                },
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                  Schema of the dataset identified by the placeholder. The idea is that any
                  dashboard created from the template should be bound to new datasets matching the
                  same schema described through this API. .

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

                            A structure describing the name, datatype, and geographic role of the
                            columns.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> ClientDescribeTemplateAliasResponseTypeDef:
        """
        Describes the template aliases of a template.

        CLI syntax:

         ``aws quicksight describe-template-alias --aws-account-id 111122223333 --template-id
         'reports_test_template' --alias-name 'STAGING'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeTemplateAlias>`_

        **Request Syntax**
        ::

          response = client.describe_template_alias(
              AwsAccountId='string',
              TemplateId='string',
              AliasName='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template alias you are describing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          An ID for the template.

        :type AliasName: string
        :param AliasName: **[REQUIRED]**

          The alias name. ``$PUBLISHED`` is not supported for template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateAlias': {
                    'AliasName': 'string',
                    'Arn': 'string',
                    'TemplateVersionNumber': 123
                },
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_template_permissions(
        self, AwsAccountId: str, TemplateId: str
    ) -> ClientDescribeTemplatePermissionsResponseTypeDef:
        """
        Describes read and write permissions on a template.

        CLI syntax:

         ``aws quicksight describe-template-permissions —aws-account-id 735340738645 —template-id
         reports_test_template``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeTemplatePermissions>`_

        **Request Syntax**
        ::

          response = client.describe_template_permissions(
              AwsAccountId='string',
              TemplateId='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template you are describing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateId': 'string',
                'TemplateArn': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **TemplateId** *(string) --*

              The ID for the template.

            - **TemplateArn** *(string) --*

              The ARN of the template.

            - **Permissions** *(list) --*

              A list of resource permissions to be set on the template.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_user(
        self, UserName: str, AwsAccountId: str, Namespace: str
    ) -> ClientDescribeUserResponseTypeDef:
        """
        Returns information about a user, given the user name.

        The response is a user object that contains the user's Amazon Resource Name (ARN), AWS
        Identity and Access Management (IAM) role, and email address.

         **CLI Sample:**

         ``aws quicksight describe-user --aws-account-id=111122223333 --namespace=default
         --user-name=Pat``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/DescribeUser>`_

        **Request Syntax**
        ::

          response = client.describe_user(
              UserName='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**

          The name of the user that you want to describe.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'User': {
                    'Arn': 'string',
                    'UserName': 'string',
                    'Email': 'string',
                    'Role': 'ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER',
                    'IdentityType': 'IAM'|'QUICKSIGHT',
                    'Active': True|False,
                    'PrincipalId': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and
                dashboards.

                * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight
                settings.

                * ``RESTRICTED_READER`` : This role isn't currently available for use.

                * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

              - **IdentityType** *(string) --*

                The type of identity authentication used by the user.

              - **Active** *(boolean) --*

                Active status of user. When you create an Amazon QuickSight user that’s not an IAM
                user or an AD user, that user is inactive until they sign in and provide a password.

              - **PrincipalId** *(string) --*

                The principal ID of the user.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def generate_presigned_url(
        self, ClientMethod: str, Params: Dict = None, ExpiresIn: int = 3600, HttpMethod: str = None
    ) -> None:
        """
        Generate a presigned url given a client, its method, and arguments

        :type ClientMethod: string
        :param ClientMethod: The client method to presign for

        :type Params: dict
        :param Params: The parameters normally passed to
            ``ClientMethod``.

        :type ExpiresIn: int
        :param ExpiresIn: The number of seconds the presigned url is valid
            for. By default it expires in an hour (3600 seconds)

        :type HttpMethod: string
        :param HttpMethod: The http method to use on the generated url. By
            default, the http method is whatever is used in the method's model.

        :returns: The presigned url
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_dashboard_embed_url(
        self,
        AwsAccountId: str,
        DashboardId: str,
        IdentityType: str,
        SessionLifetimeInMinutes: int = None,
        UndoRedoDisabled: bool = None,
        ResetDisabled: bool = None,
        UserArn: str = None,
    ) -> ClientGetDashboardEmbedUrlResponseTypeDef:
        """
        Generates a server-side embeddable URL and authorization code. Before this can work
        properly, first you need to configure the dashboards and user permissions. For more
        information, see `Embedding Amazon QuickSight Dashboards
        <https://docs.aws.example.com/en_us/quicksight/latest/user/embedding.html>`__ .

        Currently, you can use ``GetDashboardEmbedURL`` only from the server, not from the user’s
        browser.

         **CLI Sample:**

        Assume the role with permissions enabled for actions: ``quickSight:RegisterUser`` and
        ``quicksight:GetDashboardEmbedURL`` . You can use assume-role,
        assume-role-with-web-identity, or assume-role-with-saml.

         ``aws sts assume-role --role-arn
         "arn:aws:iam::111122223333:role/embedding_quicksight_dashboard_role" --role-session-name
         embeddingsession``

        If the user does not exist in QuickSight, register the user:

         ``aws quicksight register-user --aws-account-id 111122223333 --namespace default
         --identity-type IAM --iam-arn
         "arn:aws:iam::111122223333:role/embedding_quicksight_dashboard_role" --user-role READER
         --session-name "embeddingsession" --email user123@example.com --region us-east-1``

        Get the URL for the embedded dashboard (``IAM`` identity authentication):

         ``aws quicksight get-dashboard-embed-url --aws-account-id 111122223333 --dashboard-id
         1a1ac2b2-3fc3-4b44-5e5d-c6db6778df89 --identity-type IAM``

        Get the URL for the embedded dashboard (``QUICKSIGHT`` identity authentication):

         ``aws quicksight get-dashboard-embed-url --aws-account-id 111122223333 --dashboard-id
         1a1ac2b2-3fc3-4b44-5e5d-c6db6778df89 --identity-type QUICKSIGHT --user-arn
         arn:aws:quicksight:us-east-1:111122223333:user/default/embedding_quicksight_dashboard_role/embeddingsession``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/GetDashboardEmbedUrl>`_

        **Request Syntax**
        ::

          response = client.get_dashboard_embed_url(
              AwsAccountId='string',
              DashboardId='string',
              IdentityType='IAM'|'QUICKSIGHT',
              SessionLifetimeInMinutes=123,
              UndoRedoDisabled=True|False,
              ResetDisabled=True|False,
              UserArn='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are embedding.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard, also added to IAM policy

        :type IdentityType: string
        :param IdentityType: **[REQUIRED]**

          The authentication method the user uses to sign in (IAM only).

        :type SessionLifetimeInMinutes: integer
        :param SessionLifetimeInMinutes:

          How many minutes the session is valid. The session lifetime must be between 15 and 600
          minutes.

        :type UndoRedoDisabled: boolean
        :param UndoRedoDisabled:

          Remove the undo/redo button on embedded dashboard. The default is FALSE, which enables the
          undo/redo button.

        :type ResetDisabled: boolean
        :param ResetDisabled:

          Remove the reset button on embedded dashboard. The default is FALSE, which allows the
          reset button.

        :type UserArn: string
        :param UserArn:

          The Amazon QuickSight user's ARN, for use with ``QUICKSIGHT`` identity type. You can use
          this for any Amazon QuickSight users in your account (readers, authors, or admins)
          authenticated as one of the following:

          * Active Directory (AD) users or group members

          * Invited non-federated users

          * IAM users and IAM role-based sessions authenticated through Federated Single Sign-On
          using SAML, OpenID Connect, or IAM Federation

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'EmbedUrl': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **EmbedUrl** *(string) --*

              URL that you can put into your server-side webpage to embed your dashboard. This URL
              is valid for 5 minutes, and the resulting session is valid for 10 hours. The API
              provides the URL with an auth_code that enables a single-signon session.

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_dashboard_versions(
        self, AwsAccountId: str, DashboardId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDashboardVersionsResponseTypeDef:
        """
        Lists all the versions of the dashboards in the Quicksight subscription.

        CLI syntax:

        aws quicksight list-template-versions —aws-account-id 111122223333 —template-id
        reports-test-template

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListDashboardVersions>`_

        **Request Syntax**
        ::

          response = client.list_dashboard_versions(
              AwsAccountId='string',
              DashboardId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are listing.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DashboardVersionSummaryList': [
                    {
                        'Arn': 'string',
                        'CreatedTime': datetime(2015, 1, 1),
                        'VersionNumber': 123,
                        'Status':
                        'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'
                        |'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'
                        |'UPDATE_FAILED',
                        'SourceEntityArn': 'string',
                        'Description': 'string'
                    },
                ],
                'NextToken': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_dashboards(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDashboardsResponseTypeDef:
        """
        Lists dashboards in the AWS account.

        CLI syntax:

         ``aws quicksight list-dashboards --aws-account-id 111122223333 --max-results 5 —next-token
         'next-10'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListDashboards>`_

        **Request Syntax**
        ::

          response = client.list_dashboards(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboards you are listing.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DashboardSummaryList': [
                    {
                        'Arn': 'string',
                        'DashboardId': 'string',
                        'Name': 'string',
                        'CreatedTime': datetime(2015, 1, 1),
                        'LastUpdatedTime': datetime(2015, 1, 1),
                        'PublishedVersionNumber': 123,
                        'LastPublishedTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_data_sets(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDataSetsResponseTypeDef:
        """
        Lists all of the datasets belonging to this account in an AWS region.

        The permissions resource is ``arn:aws:quicksight:region:aws-account-id:dataset/*``

        CLI syntax: ``aws quicksight list-data-sets --aws-account-id=111111111111``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListDataSets>`_

        **Request Syntax**
        ::

          response = client.list_data_sets(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSetSummaries': [
                    {
                        'Arn': 'string',
                        'DataSetId': 'string',
                        'Name': 'string',
                        'CreatedTime': datetime(2015, 1, 1),
                        'LastUpdatedTime': datetime(2015, 1, 1),
                        'ImportMode': 'SPICE'|'DIRECT_QUERY',
                        'RowLevelPermissionDataSet': {
                            'Arn': 'string',
                            'PermissionPolicy': 'GRANT_ACCESS'|'DENY_ACCESS'
                        }
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_data_sources(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDataSourcesResponseTypeDef:
        """
        Lists data sources in current AWS region that belong to this AWS account.

        The permissions resource is: ``arn:aws:quicksight:region:aws-account-id:datasource/*``

        CLI syntax: ``aws quicksight list-data-sources --aws-account-id=111122223333``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListDataSources>`_

        **Request Syntax**
        ::

          response = client.list_data_sources(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSources': [
                    {
                        'Arn': 'string',
                        'DataSourceId': 'string',
                        'Name': 'string',
                        'Type':
                        'ADOBE_ANALYTICS'|'AMAZON_ELASTICSEARCH'|'ATHENA'|'AURORA'
                        |'AURORA_POSTGRESQL'|'AWS_IOT_ANALYTICS'|'GITHUB'|'JIRA'
                        |'MARIADB'|'MYSQL'|'POSTGRESQL'|'PRESTO'|'REDSHIFT'|'S3'
                        |'SALESFORCE'|'SERVICENOW'|'SNOWFLAKE'|'SPARK'|'SQLSERVER'
                        |'TERADATA'|'TWITTER',
                        'Status':
                        'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'
                        |'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'
                        |'UPDATE_FAILED',
                        'CreatedTime': datetime(2015, 1, 1),
                        'LastUpdatedTime': datetime(2015, 1, 1),
                        'DataSourceParameters': {
                            'AmazonElasticsearchParameters': {
                                'Domain': 'string'
                            },
                            'AthenaParameters': {
                                'WorkGroup': 'string'
                            },
                            'AuroraParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'AuroraPostgreSqlParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'AwsIotAnalyticsParameters': {
                                'DataSetName': 'string'
                            },
                            'JiraParameters': {
                                'SiteBaseUrl': 'string'
                            },
                            'MariaDbParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'MySqlParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'PostgreSqlParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'PrestoParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Catalog': 'string'
                            },
                            'RdsParameters': {
                                'InstanceId': 'string',
                                'Database': 'string'
                            },
                            'RedshiftParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string',
                                'ClusterId': 'string'
                            },
                            'S3Parameters': {
                                'ManifestFileLocation': {
                                    'Bucket': 'string',
                                    'Key': 'string'
                                }
                            },
                            'ServiceNowParameters': {
                                'SiteBaseUrl': 'string'
                            },
                            'SnowflakeParameters': {
                                'Host': 'string',
                                'Database': 'string',
                                'Warehouse': 'string'
                            },
                            'SparkParameters': {
                                'Host': 'string',
                                'Port': 123
                            },
                            'SqlServerParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'TeradataParameters': {
                                'Host': 'string',
                                'Port': 123,
                                'Database': 'string'
                            },
                            'TwitterParameters': {
                                'Query': 'string',
                                'MaxRows': 123
                            }
                        },
                        'VpcConnectionProperties': {
                            'VpcConnectionArn': 'string'
                        },
                        'SslProperties': {
                            'DisableSsl': True|False
                        },
                        'ErrorInfo': {
                            'Type':
                            'TIMEOUT'|'ENGINE_VERSION_NOT_SUPPORTED'
                            |'UNKNOWN_HOST'|'GENERIC_SQL_FAILURE'|'CONFLICT'
                            |'UNKNOWN',
                            'Message': 'string'
                        }
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                  The type of the data source. This indicates which database engine the data source
                  connects to.

                - **Status** *(string) --*

                  The http status of the request.

                - **CreatedTime** *(datetime) --*

                  The time this was created.

                - **LastUpdatedTime** *(datetime) --*

                  The last time this was updated.

                - **DataSourceParameters** *(dict) --*

                  The parameters QuickSight uses to connect to your underlying source. This is a
                  variant type structure. At most one of the attributes should be non-null for this
                  structure to be valid.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_group_memberships(
        self,
        GroupName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ClientListGroupMembershipsResponseTypeDef:
        """
        Lists member users in a group.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*<group-name>* `` .

        The response is a list of group member objects.

         **CLI Sample:**

         ``aws quicksight list-group-memberships -\\-aws-account-id=111122223333
         -\\-namespace=default``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListGroupMemberships>`_

        **Request Syntax**
        ::

          response = client.list_group_memberships(
              GroupName='string',
              NextToken='string',
              MaxResults=123,
              AwsAccountId='string',
              Namespace='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to see a membership list of.

        :type NextToken: string
        :param NextToken:

          A pagination token that can be used in a subsequent request.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return from this request.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'GroupMemberList': [
                    {
                        'Arn': 'string',
                        'MemberName': 'string'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **GroupMemberList** *(list) --*

              The list of the members of the group.

              - *(dict) --*

                A member of an Amazon QuickSight group. Currently, group members must be users.
                Groups can't be members of another group. .

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_groups(
        self, AwsAccountId: str, Namespace: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListGroupsResponseTypeDef:
        """
        Lists all user groups in Amazon QuickSight.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*`` .

        The response is a list of group objects.

         **CLI Sample:**

         ``aws quicksight list-groups -\\-aws-account-id=111122223333 -\\-namespace=default``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListGroups>`_

        **Request Syntax**
        ::

          response = client.list_groups(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123,
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type NextToken: string
        :param NextToken:

          A pagination token that can be used in a subsequent request.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'GroupList': [
                    {
                        'Arn': 'string',
                        'GroupName': 'string',
                        'Description': 'string',
                        'PrincipalId': 'string'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **GroupList** *(list) --*

              The list of the groups.

              - *(dict) --*

                A *group* in Amazon QuickSight consists of a set of users. You can use groups to
                make it easier to manage access and security. Currently, an Amazon QuickSight
                subscription can't contain more than 500 Amazon QuickSight groups.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_iam_policy_assignments(
        self,
        AwsAccountId: str,
        Namespace: str,
        AssignmentStatus: str = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ClientListIamPolicyAssignmentsResponseTypeDef:
        """
        Lists assignments in current QuickSight account.

        CLI syntax:

         ``aws quicksight list-iam-policy-assignments --aws-account-id=111122223333 --max-result=5
         --assignment-status=ENABLED --namespace=default --region=us-east-1 --next-token=3``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListIAMPolicyAssignments>`_

        **Request Syntax**
        ::

          response = client.list_iam_policy_assignments(
              AwsAccountId='string',
              AssignmentStatus='ENABLED'|'DRAFT'|'DISABLED',
              Namespace='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID that contains this IAM policy assignment.

        :type AssignmentStatus: string
        :param AssignmentStatus:

          The status of the assignment.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace for this assignment.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'IAMPolicyAssignments': [
                    {
                        'AssignmentName': 'string',
                        'AssignmentStatus': 'ENABLED'|'DRAFT'|'DISABLED'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_iam_policy_assignments_for_user(
        self,
        AwsAccountId: str,
        UserName: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ClientListIamPolicyAssignmentsForUserResponseTypeDef:
        """
        Lists all the assignments and the ARNs for the associated IAM policies assigned to the
        specified user and the group or groups that the user belongs to.

        CLI syntax:

         ``aws quicksight list-iam-policy-assignments-for-user --aws-account-id=111122223333
         --user-name=user5 --namespace=default --max-result=6 --region=us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListIAMPolicyAssignmentsForUser>`_

        **Request Syntax**
        ::

          response = client.list_iam_policy_assignments_for_user(
              AwsAccountId='string',
              UserName='string',
              NextToken='string',
              MaxResults=123,
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID that contains the assignment.

        :type UserName: string
        :param UserName: **[REQUIRED]**

          The name of the user.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace of the assignment.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ActiveAssignments': [
                    {
                        'AssignmentName': 'string',
                        'PolicyArn': 'string'
                    },
                ],
                'RequestId': 'string',
                'NextToken': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_ingestions(
        self, DataSetId: str, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListIngestionsResponseTypeDef:
        """
        Lists the history of SPICE ingestions for a dataset.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListIngestions>`_

        **Request Syntax**
        ::

          response = client.list_ingestions(
              DataSetId='string',
              NextToken='string',
              AwsAccountId='string',
              MaxResults=123
          )
        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID of the dataset used in the ingestion.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Ingestions': [
                    {
                        'Arn': 'string',
                        'IngestionId': 'string',
                        'IngestionStatus':
                        'INITIALIZED'|'QUEUED'|'RUNNING'|'FAILED'|'COMPLETED'
                        |'CANCELLED',
                        'ErrorInfo': {
                            'Type':
                            'FAILURE_TO_ASSUME_ROLE'|'INGESTION_SUPERSEDED'
                            |'INGESTION_CANCELED'|'DATA_SET_DELETED'
                            |'DATA_SET_NOT_SPICE'|'S3_UPLOADED_FILE_DELETED'
                            |'S3_MANIFEST_ERROR'|'DATA_TOLERANCE_EXCEPTION'
                            |'SPICE_TABLE_NOT_FOUND'
                            |'DATA_SET_SIZE_LIMIT_EXCEEDED'
                            |'ROW_SIZE_LIMIT_EXCEEDED'
                            |'ACCOUNT_CAPACITY_LIMIT_EXCEEDED'|'CUSTOMER_ERROR'
                            |'DATA_SOURCE_NOT_FOUND'|'IAM_ROLE_NOT_AVAILABLE'
                            |'CONNECTION_FAILURE'|'SQL_TABLE_NOT_FOUND'
                            |'PERMISSION_DENIED'
                            |'SSL_CERTIFICATE_VALIDATION_FAILURE'
                            |'OAUTH_TOKEN_FAILURE'
                            |'SOURCE_API_LIMIT_EXCEEDED_FAILURE'
                            |'PASSWORD_AUTHENTICATION_FAILURE'
                            |'SQL_SCHEMA_MISMATCH_ERROR'|'INVALID_DATE_FORMAT'
                            |'INVALID_DATAPREP_SYNTAX'
                            |'SOURCE_RESOURCE_LIMIT_EXCEEDED'
                            |'SQL_INVALID_PARAMETER_VALUE'|'QUERY_TIMEOUT'
                            |'SQL_NUMERIC_OVERFLOW'|'UNRESOLVABLE_HOST'
                            |'UNROUTABLE_HOST'|'SQL_EXCEPTION'
                            |'S3_FILE_INACCESSIBLE'|'IOT_FILE_NOT_FOUND'
                            |'IOT_DATA_SET_FILE_EMPTY'
                            |'INVALID_DATA_SOURCE_CONFIG'
                            |'DATA_SOURCE_AUTH_FAILED'
                            |'DATA_SOURCE_CONNECTION_FAILED'
                            |'FAILURE_TO_PROCESS_JSON_FILE'
                            |'INTERNAL_SERVICE_ERROR',
                            'Message': 'string'
                        },
                        'RowInfo': {
                            'RowsIngested': 123,
                            'RowsDropped': 123
                        },
                        'QueueInfo': {
                            'WaitingOnIngestion': 'string',
                            'QueuedIngestion': 'string'
                        },
                        'CreatedTime': datetime(2015, 1, 1),
                        'IngestionTimeInSeconds': 123,
                        'IngestionSizeInBytes': 123,
                        'RequestSource': 'MANUAL'|'SCHEDULED',
                        'RequestType':
                        'INITIAL_INGESTION'|'EDIT'|'INCREMENTAL_REFRESH'
                        |'FULL_REFRESH'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_tags_for_resource(self, ResourceArn: str) -> ClientListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to a resource.

        CLI syntax:

        * ``aws quicksight list-tags-for-resource --resource-arn
        arn:aws:quicksight:us-east-1:111111111111:dataset/dataset1 --region us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListTagsForResource>`_

        **Request Syntax**
        ::

          response = client.list_tags_for_resource(
              ResourceArn='string'
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource you want a list of tags for.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Tags** *(list) --*

              Contains a map of the key-value pairs for the resource tag or tags assigned to the
              resource.

              - *(dict) --*

                The keys of the key-value pairs for the resource tag or tags assigned to the
                resource.

                - **Key** *(string) --*

                  Tag key.

                - **Value** *(string) --*

                  Tag value.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_template_aliases(
        self, AwsAccountId: str, TemplateId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListTemplateAliasesResponseTypeDef:
        """
        Lists all the aliases of a template.

        CLI syntax:

         ``aws quicksight list-template-aliases --aws-account-id 111122223333 —template-id
         'reports_test_template'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListTemplateAliases>`_

        **Request Syntax**
        ::

          response = client.list_template_aliases(
              AwsAccountId='string',
              TemplateId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template aliases you are listing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateAliasList': [
                    {
                        'AliasName': 'string',
                        'Arn': 'string',
                        'TemplateVersionNumber': 123
                    },
                ],
                'Status': 123,
                'RequestId': 'string',
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_template_versions(
        self, AwsAccountId: str, TemplateId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListTemplateVersionsResponseTypeDef:
        """
        Lists all the versions of the templates in the Quicksight account.

        CLI syntax:

        aws quicksight list-template-versions --aws-account-id 111122223333 --aws-account-id
        196359894473 --template-id reports-test-template

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListTemplateVersions>`_

        **Request Syntax**
        ::

          response = client.list_template_versions(
              AwsAccountId='string',
              TemplateId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the templates you are listing.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateVersionSummaryList': [
                    {
                        'Arn': 'string',
                        'VersionNumber': 123,
                        'CreatedTime': datetime(2015, 1, 1),
                        'Status':
                        'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'
                        |'CREATION_FAILED'|'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'
                        |'UPDATE_FAILED',
                        'Description': 'string'
                    },
                ],
                'NextToken': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_templates(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListTemplatesResponseTypeDef:
        """
        Lists all the templates in the QuickSight account.

        CLI syntax:

         ``aws quicksight list-templates --aws-account-id 111122223333 --max-results 1 —next-token
         AYADeJuxwOypAndSoOn``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListTemplates>`_

        **Request Syntax**
        ::

          response = client.list_templates(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the templates you are listing.

        :type NextToken: string
        :param NextToken:

          The token for the next set of results, or null if there are no more results.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to be returned per request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateSummaryList': [
                    {
                        'Arn': 'string',
                        'TemplateId': 'string',
                        'Name': 'string',
                        'LatestVersionNumber': 123,
                        'CreatedTime': datetime(2015, 1, 1),
                        'LastUpdatedTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_user_groups(
        self,
        UserName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ClientListUserGroupsResponseTypeDef:
        """
        Lists the Amazon QuickSight groups that an Amazon QuickSight user is a member of.

        The response is a one or more group objects.

         **CLI Sample:**

         ``aws quicksight list-user-groups -\\-user-name=Pat -\\-aws-account-id=111122223333
         -\\-namespace=default -\\-region=us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListUserGroups>`_

        **Request Syntax**
        ::

          response = client.list_user_groups(
              UserName='string',
              AwsAccountId='string',
              Namespace='string',
              NextToken='string',
              MaxResults=123
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**

          The Amazon QuickSight user name that you want to list group memberships for.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID that the user is in. Currently, you use the ID for the AWS account that
          contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :type NextToken: string
        :param NextToken:

          A pagination token that can be used in a subsequent request.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return from this request.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'GroupList': [
                    {
                        'Arn': 'string',
                        'GroupName': 'string',
                        'Description': 'string',
                        'PrincipalId': 'string'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **GroupList** *(list) --*

              The list of groups the user is a member of.

              - *(dict) --*

                A *group* in Amazon QuickSight consists of a set of users. You can use groups to
                make it easier to manage access and security. Currently, an Amazon QuickSight
                subscription can't contain more than 500 Amazon QuickSight groups.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_users(
        self, AwsAccountId: str, Namespace: str, NextToken: str = None, MaxResults: int = None
    ) -> ClientListUsersResponseTypeDef:
        """
        Returns a list of all of the Amazon QuickSight users belonging to this account.

        The response is a list of user objects, containing each user's Amazon Resource Name (ARN),
        AWS Identity and Access Management (IAM) role, and email address.

         **CLI Sample:**

         ``aws quicksight list-users --aws-account-id=111122223333 --namespace=default``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/ListUsers>`_

        **Request Syntax**
        ::

          response = client.list_users(
              AwsAccountId='string',
              NextToken='string',
              MaxResults=123,
              Namespace='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type NextToken: string
        :param NextToken:

          A pagination token that can be used in a subsequent request.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return from this request.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'UserList': [
                    {
                        'Arn': 'string',
                        'UserName': 'string',
                        'Email': 'string',
                        'Role': 'ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER',
                        'IdentityType': 'IAM'|'QUICKSIGHT',
                        'Active': True|False,
                        'PrincipalId': 'string'
                    },
                ],
                'NextToken': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **UserList** *(list) --*

              The list of users.

              - *(dict) --*

                A registered user of Amazon QuickSight. Currently, an Amazon QuickSight subscription
                can't contain more than 20 million users.

                - **Arn** *(string) --*

                  The Amazon Resource name (ARN) for the user.

                - **UserName** *(string) --*

                  The user's user name.

                - **Email** *(string) --*

                  The user's email address.

                - **Role** *(string) --*

                  The Amazon QuickSight role for the user. The user role can be one of the
                  following:.

                  * ``READER`` : A user who has read-only access to dashboards.

                  * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and
                  dashboards.

                  * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight
                  settings.

                  * ``RESTRICTED_READER`` : This role isn't currently available for use.

                  * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

                - **IdentityType** *(string) --*

                  The type of identity authentication used by the user.

                - **Active** *(boolean) --*

                  Active status of user. When you create an Amazon QuickSight user that’s not an IAM
                  user or an AD user, that user is inactive until they sign in and provide a
                  password.

                - **PrincipalId** *(string) --*

                  The principal ID of the user.

            - **NextToken** *(string) --*

              A pagination token that can be used in a subsequent request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def register_user(
        self,
        IdentityType: str,
        Email: str,
        UserRole: str,
        AwsAccountId: str,
        Namespace: str,
        IamArn: str = None,
        SessionName: str = None,
        UserName: str = None,
    ) -> ClientRegisterUserResponseTypeDef:
        """
        .. _https://docs.aws.example.com/cli/latest/reference/sts/assume-role.html:
        https://docs.aws.example.com/cli/latest/reference/sts/assume-role.html

        Creates an Amazon QuickSight user, whose identity is associated with the AWS Identity and
        Access Management (IAM) identity or role specified in the request.

         **CLI Sample:**

         ``aws quicksight register-user -\\-aws-account-id=111122223333 -\\-namespace=default
         -\\-email=pat@example.com -\\-identity-type=IAM -\\-user-role=AUTHOR
         -\\-iam-arn=arn:aws:iam::111122223333:user/Pat``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/RegisterUser>`_

        **Request Syntax**
        ::

          response = client.register_user(
              IdentityType='IAM'|'QUICKSIGHT',
              Email='string',
              UserRole='ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER',
              IamArn='string',
              SessionName='string',
              AwsAccountId='string',
              Namespace='string',
              UserName='string'
          )
        :type IdentityType: string
        :param IdentityType: **[REQUIRED]**

          Amazon QuickSight supports several ways of managing the identity of users. This parameter
          accepts two values:

          * ``IAM`` : A user whose identity maps to an existing IAM user or role.

          * ``QUICKSIGHT`` : A user whose identity is owned and managed internally by Amazon
          QuickSight.

        :type Email: string
        :param Email: **[REQUIRED]**

          The email address of the user that you want to register.

        :type UserRole: string
        :param UserRole: **[REQUIRED]**

          The Amazon QuickSight role for the user. The user role can be one of the following:

          * ``READER`` : A user who has read-only access to dashboards.

          * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

          * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

          * ``RESTRICTED_READER`` : This role isn't currently available for use.

          * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

        :type IamArn: string
        :param IamArn:

          The ARN of the IAM user or role that you are registering with Amazon QuickSight.

        :type SessionName: string
        :param SessionName:

          You need to use this parameter only when you register one or more users using an assumed
          IAM role. You don't need to provide the session name for other scenarios, for example when
          you are registering an IAM user or an Amazon QuickSight user. You can register multiple
          users using the same IAM role if each user has a different session name. For more
          information on assuming IAM roles, see ` ``assume-role``
          https://docs.aws.example.com/cli/latest/reference/sts/assume-role.html`__ in the *AWS CLI
          Reference.*

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :type UserName: string
        :param UserName:

          The Amazon QuickSight user name that you want to create for the user you are registering.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'User': {
                    'Arn': 'string',
                    'UserName': 'string',
                    'Email': 'string',
                    'Role': 'ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER',
                    'IdentityType': 'IAM'|'QUICKSIGHT',
                    'Active': True|False,
                    'PrincipalId': 'string'
                },
                'UserInvitationUrl': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and
                dashboards.

                * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight
                settings.

                * ``RESTRICTED_READER`` : This role isn't currently available for use.

                * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

              - **IdentityType** *(string) --*

                The type of identity authentication used by the user.

              - **Active** *(boolean) --*

                Active status of user. When you create an Amazon QuickSight user that’s not an IAM
                user or an AD user, that user is inactive until they sign in and provide a password.

              - **PrincipalId** *(string) --*

                The principal ID of the user.

            - **UserInvitationUrl** *(string) --*

              The URL the user visits to complete registration and provide a password. This is
              returned only for users with an identity type of ``QUICKSIGHT`` .

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def tag_resource(
        self, ResourceArn: str, Tags: List[ClientTagResourceTagsTypeDef]
    ) -> ClientTagResourceResponseTypeDef:
        """
        Assigns a tag or tags to a resource.

        Assigns one or more tags (key-value pairs) to the specified QuickSight resource. Tags can
        help you organize and categorize your resources. You can also use them to scope user
        permissions, by granting a user permission to access or change only resources with certain
        tag values. You can use the TagResource action with a resource that already has tags. If you
        specify a new tag key for the resource, this tag is appended to the list of tags associated
        with the resource. If you specify a tag key that is already associated with the resource,
        the new tag value that you specify replaces the previous value for that tag.

        You can associate as many as 50 tags with a resource. QuickSight supports tagging on
        data-set, data-source, dashboard, template.

        Tagging for QuickSight works in a similar was to tagging for other AWS services, except for
        the following:

        * You can't use tags to track AWS costs for QuickSight, because QuickSight costs are based
        on users and SPICE capacity, which aren't taggable resources.

        * QuickSight doesn't currently support the Tag Editor for AWS Resource Groups.

        CLI syntax to tag a resource:

        * ``aws quicksight tag-resource --resource-arn
        arn:aws:quicksight:us-east-1:111111111111:dataset/dataset1 --tags Key=K1,Value=V1
        Key=K2,Value=V2 --region us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/TagResource>`_

        **Request Syntax**
        ::

          response = client.tag_resource(
              ResourceArn='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource you want to tag.

        :type Tags: list
        :param Tags: **[REQUIRED]**

          Contains a map of the key-value pairs for the resource tag or tags assigned to the
          resource.

          - *(dict) --*

            The keys of the key-value pairs for the resource tag or tags assigned to the resource.

            - **Key** *(string) --* **[REQUIRED]**

              Tag key.

            - **Value** *(string) --* **[REQUIRED]**

              Tag value.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def untag_resource(
        self, ResourceArn: str, TagKeys: List[str]
    ) -> ClientUntagResourceResponseTypeDef:
        """
        Removes a tag or tags from a resource.

        CLI syntax:

        * ``aws quicksight untag-resource --resource-arn
        arn:aws:quicksight:us-east-1:111111111111:dataset/dataset1 --tag-keys K1 K2 --region
        us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UntagResource>`_

        **Request Syntax**
        ::

          response = client.untag_resource(
              ResourceArn='string',
              TagKeys=[
                  'string',
              ]
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource you to untag.

        :type TagKeys: list
        :param TagKeys: **[REQUIRED]**

          The keys of the key-value pairs for the resource tag or tags assigned to the resource.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_dashboard(
        self,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: ClientUpdateDashboardSourceEntityTypeDef,
        Parameters: ClientUpdateDashboardParametersTypeDef = None,
        VersionDescription: str = None,
        DashboardPublishOptions: ClientUpdateDashboardDashboardPublishOptionsTypeDef = None,
    ) -> ClientUpdateDashboardResponseTypeDef:
        """
        Updates a dashboard in the AWS account.

        CLI syntax:

         ``aws quicksight update-dashboard --aws-account-id 111122223333 --dashboard-id 123123123
         --dashboard-name "test-update102" --source-entity
         SourceTemplate={Arn=
             arn:aws:quicksight:us-west-2:111122223333:template/sales-report-template2}
         --data-set-references
         DataSetPlaceholder=SalesDataSet,DataSetArn=
             arn:aws:quicksight:us-west-2:111122223333:dataset/0e251aef-9ebf-46e1-b852-eb4fa33c1d3a``

         ``aws quicksight update-dashboard --cli-input-json file://update-dashboard.json``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDashboard>`_

        **Request Syntax**
        ::

          response = client.update_dashboard(
              AwsAccountId='string',
              DashboardId='string',
              Name='string',
              SourceEntity={
                  'SourceTemplate': {
                      'DataSetReferences': [
                          {
                              'DataSetPlaceholder': 'string',
                              'DataSetArn': 'string'
                          },
                      ],
                      'Arn': 'string'
                  }
              },
              Parameters={
                  'StringParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              'string',
                          ]
                      },
                  ],
                  'IntegerParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              123,
                          ]
                      },
                  ],
                  'DecimalParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              123.0,
                          ]
                      },
                  ],
                  'DateTimeParameters': [
                      {
                          'Name': 'string',
                          'Values': [
                              datetime(2015, 1, 1),
                          ]
                      },
                  ]
              },
              VersionDescription='string',
              DashboardPublishOptions={
                  'AdHocFilteringOption': {
                      'AvailabilityStatus': 'ENABLED'|'DISABLED'
                  },
                  'ExportToCSVOption': {
                      'AvailabilityStatus': 'ENABLED'|'DISABLED'
                  },
                  'SheetControlsOption': {
                      'VisibilityState': 'EXPANDED'|'COLLAPSED'
                  }
              }
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are updating.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type Name: string
        :param Name: **[REQUIRED]**

          The display name of the dashboard.

        :type SourceEntity: dict
        :param SourceEntity: **[REQUIRED]**

          The template or analysis from which the dashboard is created. The SouceTemplate entity
          accepts the Arn of the template and also references to replacement datasets for the
          placeholders set when creating the template. The replacement datasets need to follow the
          same schema as the datasets for which placeholders were created when creating the
          template.

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

        :type Parameters: dict
        :param Parameters:

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

        :type VersionDescription: string
        :param VersionDescription:

          A description for the first version of the dashboard being created.

        :type DashboardPublishOptions: dict
        :param DashboardPublishOptions:

          Publishing options when creating a dashboard.

          * AvailabilityStatus for AdHocFilteringOption - This can be either ``ENABLED`` or
          ``DISABLED`` . When This is set to set to ``DISABLED`` , QuickSight disables the left
          filter pane on the published dashboard, which can be used for AdHoc filtering. Enabled by
          default.

          * AvailabilityStatus for ExportToCSVOption - This can be either ``ENABLED`` or
          ``DISABLED`` . The visual option to export data to CSV is disabled when this is set to
          ``DISABLED`` . Enabled by default.

          * VisibilityState for SheetControlsOption - This can be either ``COLLAPSED`` or
          ``EXPANDED`` . The sheet controls pane is collapsed by default when set to true. Collapsed
          by default.

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

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'VersionArn': 'string',
                'DashboardId': 'string',
                'CreationStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_dashboard_permissions(
        self,
        AwsAccountId: str,
        DashboardId: str,
        GrantPermissions: List[ClientUpdateDashboardPermissionsGrantPermissionsTypeDef] = None,
        RevokePermissions: List[ClientUpdateDashboardPermissionsRevokePermissionsTypeDef] = None,
    ) -> ClientUpdateDashboardPermissionsResponseTypeDef:
        """
        Updates read and write permissions on a dashboard.

        CLI syntax:

         ``aws quicksight update-dashboard-permissions —cli-input-json
         file://update-permission.json``

        A sample update-permissions.json for granting read only permissions:

         ``{ "AwsAccountId": "111122223333", "DashboardId": "reports_test_report",
         "GrantPermissions": [ { "Principal":
         "arn:aws:quicksight:us-east-1:111122223333:user/default/user2", "Actions": [
         "quicksight:DescribeDashboard", "quicksight:ListDashboardVersions",
         "quicksight:DescribeDashboardVersion", "quicksight:QueryDashboard" ] } ] }``

        A sample update-permissions.json for granting read and write permissions:

         ``{ "AwsAccountId": "111122223333", "DashboardId": "reports_test_report",
         "GrantPermissions": [ { "Principal":
         "arn:aws:quicksight:us-east-1:111122223333:user/default/user2", "Actions": [
         "quicksight:DescribeDashboard", "quicksight:ListDashboardVersions",
         "quicksight:DescribeDashboardVersion", "quicksight:QueryDashboard",
         "quicksight:DescribeDashboardPermissions", "quicksight:UpdateDashboardPermissions",
         "quicksight:DeleteDashboardVersion", "quicksight:DeleteDashboard",
         "quicksight:UpdateDashboard", "quicksight:UpdateDashboardPublishedVersion", ] } ] }``

        A sample update-permissions.json for revoking write permissions:

         ``{ "AwsAccountId": "111122223333", "DashboardId": "reports_test_report",
         "RevokePermissions": [ { "Principal":
         "arn:aws:quicksight:us-east-1:111122223333:user/default/user2", "Actions": [
         "quicksight:DescribeDashboardPermissions", "quicksight:UpdateDashboardPermissions",
         "quicksight:DeleteDashboardVersion", "quicksight:DeleteDashboard",
         "quicksight:UpdateDashboard", "quicksight:UpdateDashboardPublishedVersion", ] } ] }``

        A sample update-permissions.json for revoking read and write permissions:

         ``{ "AwsAccountId": "111122223333", "DashboardId": "reports_test_report",
         "RevokePermissions": [ { "Principal":
         "arn:aws:quicksight:us-east-1:111122223333:user/default/user2", "Actions": [
         "quicksight:DescribeDashboard", "quicksight:ListDashboardVersions",
         "quicksight:DescribeDashboardVersion", "quicksight:QueryDashboard",
         "quicksight:DescribeDashboardPermissions", "quicksight:UpdateDashboardPermissions",
         "quicksight:DeleteDashboardVersion", "quicksight:DeleteDashboard",
         "quicksight:UpdateDashboard", "quicksight:UpdateDashboardPublishedVersion", ] } ] }``

        To obtain the principal name of a QuickSight user or group, you can use describe-group or
        describe-user. For example:

         ``aws quicksight describe-user --aws-account-id 111122223333 --namespace default
         --user-name user2 --region us-east-1 { "User": { "Arn":
         "arn:aws:quicksight:us-east-1:111122223333:user/default/user2", "Active": true, "Email":
         "user2@example.com", "Role": "ADMIN", "UserName": "user2", "PrincipalId":
         "federated/iam/abcd2abcdabcdeabc5ab5" }, "RequestId":
         "8f74bb31-6291-448a-a71c-a765a44bae31", "Status": 200 }``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDashboardPermissions>`_

        **Request Syntax**
        ::

          response = client.update_dashboard_permissions(
              AwsAccountId='string',
              DashboardId='string',
              GrantPermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              RevokePermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are updating.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type GrantPermissions: list
        :param GrantPermissions:

          The permissions that you want to grant on this resource.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type RevokePermissions: list
        :param RevokePermissions:

          The permissions that you want to revoke from this resource.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DashboardArn': 'string',
                'DashboardId': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DashboardArn** *(string) --*

              The ARN of the dashboard.

            - **DashboardId** *(string) --*

              The ID for the dashboard.

            - **Permissions** *(list) --*

              Information about the permissions on the dashboard.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_dashboard_published_version(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int
    ) -> ClientUpdateDashboardPublishedVersionResponseTypeDef:
        """
        Updates the published version of a dashboard.

        CLI syntax:

         ``aws quicksight update-dashboard-published-version --aws-account-id 111122223333
         --dashboard-id dashboard-w1 ---version-number 2``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDashboardPublishedVersion>`_

        **Request Syntax**
        ::

          response = client.update_dashboard_published_version(
              AwsAccountId='string',
              DashboardId='string',
              VersionNumber=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the dashboard you are updating.

        :type DashboardId: string
        :param DashboardId: **[REQUIRED]**

          The ID for the dashboard.

        :type VersionNumber: integer
        :param VersionNumber: **[REQUIRED]**

          The version number of the dashboard.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DashboardId': 'string',
                'DashboardArn': 'string',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **DashboardId** *(string) --*

              The ID for the dashboard.

            - **DashboardArn** *(string) --*

              The ARN of the dashboard.

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_data_set(
        self,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Dict[str, ClientUpdateDataSetPhysicalTableMapTypeDef],
        ImportMode: str,
        LogicalTableMap: Dict[str, ClientUpdateDataSetLogicalTableMapTypeDef] = None,
        ColumnGroups: List[ClientUpdateDataSetColumnGroupsTypeDef] = None,
        RowLevelPermissionDataSet: ClientUpdateDataSetRowLevelPermissionDataSetTypeDef = None,
    ) -> ClientUpdateDataSetResponseTypeDef:
        """
        Updates a dataset.

        CLI syntax:

         ``aws quicksight update-data-set \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-set-id=unique-data-set-id \\``

         ``--name='My dataset' \\``

         ``--import-mode=SPICE \\``

         ``--physical-table-map='{``

         ``"physical-table-id": {``

         ``"RelationalTable": {``

         ``"DataSourceArn": "arn:aws:quicksight:us-west-2:111111111111:datasource/data-source-id",``

         ``"Name": "table1",``

         ``"InputColumns": [``

         ``{``

         ``"Name": "column1",``

         ``"Type": "STRING"``

         ``}``

         ``]``

         ``}``

         ``}'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDataSet>`_

        **Request Syntax**
        ::

          response = client.update_data_set(
              AwsAccountId='string',
              DataSetId='string',
              Name='string',
              PhysicalTableMap={
                  'string': {
                      'RelationalTable': {
                          'DataSourceArn': 'string',
                          'Schema': 'string',
                          'Name': 'string',
                          'InputColumns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      },
                      'CustomSql': {
                          'DataSourceArn': 'string',
                          'Name': 'string',
                          'SqlQuery': 'string',
                          'Columns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      },
                      'S3Source': {
                          'DataSourceArn': 'string',
                          'UploadSettings': {
                              'Format': 'CSV'|'TSV'|'CLF'|'ELF'|'XLSX'|'JSON',
                              'StartFromRow': 123,
                              'ContainsHeader': True|False,
                              'TextQualifier': 'DOUBLE_QUOTE'|'SINGLE_QUOTE',
                              'Delimiter': 'string'
                          },
                          'InputColumns': [
                              {
                                  'Name': 'string',
                                  'Type':
                                  'STRING'|'INTEGER'|'DECIMAL'|'DATETIME'
                                  |'BIT'|'BOOLEAN'|'JSON'
                              },
                          ]
                      }
                  }
              },
              LogicalTableMap={
                  'string': {
                      'Alias': 'string',
                      'DataTransforms': [
                          {
                              'ProjectOperation': {
                                  'ProjectedColumns': [
                                      'string',
                                  ]
                              },
                              'FilterOperation': {
                                  'ConditionExpression': 'string'
                              },
                              'CreateColumnsOperation': {
                                  'Columns': [
                                      {
                                          'ColumnName': 'string',
                                          'ColumnId': 'string',
                                          'Expression': 'string'
                                      },
                                  ]
                              },
                              'RenameColumnOperation': {
                                  'ColumnName': 'string',
                                  'NewColumnName': 'string'
                              },
                              'CastColumnTypeOperation': {
                                  'ColumnName': 'string',
                                  'NewColumnType': 'STRING'|'INTEGER'|'DECIMAL'|'DATETIME',
                                  'Format': 'string'
                              },
                              'TagColumnOperation': {
                                  'ColumnName': 'string',
                                  'Tags': [
                                      {
                                          'ColumnGeographicRole':
                                          'COUNTRY'|'STATE'
                                          |'COUNTY'|'CITY'
                                          |'POSTCODE'|'LONGITUDE'
                                          |'LATITUDE'
                                      },
                                  ]
                              }
                          },
                      ],
                      'Source': {
                          'JoinInstruction': {
                              'LeftOperand': 'string',
                              'RightOperand': 'string',
                              'Type': 'INNER'|'OUTER'|'LEFT'|'RIGHT',
                              'OnClause': 'string'
                          },
                          'PhysicalTableId': 'string'
                      }
                  }
              },
              ImportMode='SPICE'|'DIRECT_QUERY',
              ColumnGroups=[
                  {
                      'GeoSpatialColumnGroup': {
                          'Name': 'string',
                          'CountryCode': 'US',
                          'Columns': [
                              'string',
                          ]
                      }
                  },
              ],
              RowLevelPermissionDataSet={
                  'Arn': 'string',
                  'PermissionPolicy': 'GRANT_ACCESS'|'DENY_ACCESS'
              }
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID for the dataset you want to create. This is unique per region per AWS account.

        :type Name: string
        :param Name: **[REQUIRED]**

          The display name for the dataset.

        :type PhysicalTableMap: dict
        :param PhysicalTableMap: **[REQUIRED]**

          Declares the physical tables that are available in the underlying data sources.

          - *(string) --*

            - *(dict) --*

              A view of a data source. Contains information on the shape of the data in the
              underlying source. This is a variant type structure. No more than one of the
              attributes can be non-null for this structure to be valid.

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

        :type LogicalTableMap: dict
        :param LogicalTableMap:

          Configures the combination and transformation of the data from the physical tables.

          - *(string) --*

            - *(dict) --*

              A unit that joins and data transformations operate on. A logical table has a source,
              which can be either a physical table or result of a join. When it points to a physical
              table, a logical table acts as a mutable copy of that table through transform
              operations.

              - **Alias** *(string) --* **[REQUIRED]**

                A display name for the logical table.

              - **DataTransforms** *(list) --*

                Transform operations that act on this logical table.

                - *(dict) --*

                  A data transformation on a logical table. This is a variant type structure. No
                  more than one of the attributes should be non-null for this structure to be valid.

                  - **ProjectOperation** *(dict) --*

                    An operation that projects columns. Operations that come after a projection can
                    only refer to projected columns.

                    - **ProjectedColumns** *(list) --* **[REQUIRED]**

                      Projected columns.

                      - *(string) --*

                  - **FilterOperation** *(dict) --*

                    An operation that filters rows based on some condition.

                    - **ConditionExpression** *(string) --* **[REQUIRED]**

                      An expression that must evaluate to a boolean value. Rows for which the
                      expression is evaluated to true are kept in the dataset.

                  - **CreateColumnsOperation** *(dict) --*

                    An operation that creates calculated columns. Columns created in one such
                    operation form a lexical closure.

                    - **Columns** *(list) --* **[REQUIRED]**

                      Calculated columns to create.

                      - *(dict) --*

                        A calculated column for a dataset.

                        - **ColumnName** *(string) --* **[REQUIRED]**

                          Column name.

                        - **ColumnId** *(string) --* **[REQUIRED]**

                          A unique ID to identify a calculated column. During dataset update, if the
                          column ID of a calculated column matches that of an existing calculated
                          column, QuickSight preserves the existing calculated column.

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

                      When casting a column from string to datetime type, you can supply a
                      QuickSight supported format string to denote the source data format.

                  - **TagColumnOperation** *(dict) --*

                    An operation that tags a column with additional information.

                    - **ColumnName** *(string) --* **[REQUIRED]**

                      The column that this operation acts on.

                    - **Tags** *(list) --* **[REQUIRED]**

                      The dataset column tag, currently only used for geospatial type tagging. .

                      .. note::

                        This is not tags for the AWS tagging feature. .

                      - *(dict) --*

                        A tag for a column in a TagColumnOperation. This is a variant type
                        structure. No more than one of the attributes should be non-null for this
                        structure to be valid.

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

        :type ImportMode: string
        :param ImportMode: **[REQUIRED]**

          Indicates whether or not you want to import the data into SPICE.

        :type ColumnGroups: list
        :param ColumnGroups:

          Groupings of columns that work together in certain QuickSight features. Currently only
          geospatial hierarchy is supported.

          - *(dict) --*

            Groupings of columns that work together in certain QuickSight features. This is a
            variant type structure. No more than one of the attributes should be non-null for this
            structure to be valid.

            - **GeoSpatialColumnGroup** *(dict) --*

              Geospatial column group that denotes a hierarchy.

              - **Name** *(string) --* **[REQUIRED]**

                A display name for the hierarchy.

              - **CountryCode** *(string) --* **[REQUIRED]**

                Country code.

              - **Columns** *(list) --* **[REQUIRED]**

                Columns in this hierarchy.

                - *(string) --*

        :type RowLevelPermissionDataSet: dict
        :param RowLevelPermissionDataSet:

          Row-level security configuration on the data you want to create.

          - **Arn** *(string) --* **[REQUIRED]**

            The Amazon Resource name (ARN) of the permission dataset.

          - **PermissionPolicy** *(string) --* **[REQUIRED]**

            Permission policy.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSetId': 'string',
                'IngestionArn': 'string',
                'IngestionId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **Arn** *(string) --*

              The ARN of the dataset.

            - **DataSetId** *(string) --*

              The ID for the dataset you want to create. This is unique per region per AWS account.

            - **IngestionArn** *(string) --*

              The Amazon Resource Name (ARN) for the ingestion, which is triggered as a result of
              dataset creation if the import mode is SPICE

            - **IngestionId** *(string) --*

              The ID of the ingestion, which is triggered as a result of dataset creation if the
              import mode is SPICE

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_data_set_permissions(
        self,
        AwsAccountId: str,
        DataSetId: str,
        GrantPermissions: List[ClientUpdateDataSetPermissionsGrantPermissionsTypeDef] = None,
        RevokePermissions: List[ClientUpdateDataSetPermissionsRevokePermissionsTypeDef] = None,
    ) -> ClientUpdateDataSetPermissionsResponseTypeDef:
        """
        Updates the permissions on a dataset.

        The permissions resource is ``arn:aws:quicksight:region:aws-account-id:dataset/data-set-id``

        CLI syntax:

         ``aws quicksight update-data-set-permissions \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-set-id=unique-data-set-id \\``

         ``--grant-permissions=
             '[{"Principal":"arn:aws:quicksight:us-east-1:111122223333:user/default/user1","Actions":["quicksight:DescribeDataSet","quicksight:DescribeDataSetPermissions","quicksight:PassDataSet","quicksight:ListIngestions","quicksight:DescribeIngestion"]}]'
         \\``

         ``--revoke-permissions=
             '[{"Principal":"arn:aws:quicksight:us-east-1:111122223333:user/default/user2","Actions":["quicksight:UpdateDataSet","quicksight:DeleteDataSet","quicksight:UpdateDataSetPermissions","quicksight:CreateIngestion","quicksight:CancelIngestion"]}]'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDataSetPermissions>`_

        **Request Syntax**
        ::

          response = client.update_data_set_permissions(
              AwsAccountId='string',
              DataSetId='string',
              GrantPermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              RevokePermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS Account ID.

        :type DataSetId: string
        :param DataSetId: **[REQUIRED]**

          The ID for the dataset you want to create. This is unique per region per AWS account.

        :type GrantPermissions: list
        :param GrantPermissions:

          The resource permissions that you want to grant to the dataset.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type RevokePermissions: list
        :param RevokePermissions:

          The resource permissions that you want to revoke from the dataset.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSetArn': 'string',
                'DataSetId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DataSetArn** *(string) --*

              The ARN of the dataset.

            - **DataSetId** *(string) --*

              The ID for the dataset you want to create. This is unique per region per AWS account.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_data_source(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        DataSourceParameters: ClientUpdateDataSourceDataSourceParametersTypeDef = None,
        Credentials: ClientUpdateDataSourceCredentialsTypeDef = None,
        VpcConnectionProperties: ClientUpdateDataSourceVpcConnectionPropertiesTypeDef = None,
        SslProperties: ClientUpdateDataSourceSslPropertiesTypeDef = None,
    ) -> ClientUpdateDataSourceResponseTypeDef:
        """
        Updates a data source.

        The permissions resource is
        ``arn:aws:quicksight:region:aws-account-id:datasource/data-source-id``

        CLI syntax:

         ``aws quicksight update-data-source \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-source-id=unique-data-source-id \\``

         ``--name='My Data Source' \\``

         ``--data-source-parameters=
             '{"PostgreSqlParameters":{"Host":"my-db-host.example.com","Port":1234,"Database":"my-db"}}'
         \\``

         ``--credentials='{"CredentialPair":{"Username":"username","Password":"password"}}``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDataSource>`_

        **Request Syntax**
        ::

          response = client.update_data_source(
              AwsAccountId='string',
              DataSourceId='string',
              Name='string',
              DataSourceParameters={
                  'AmazonElasticsearchParameters': {
                      'Domain': 'string'
                  },
                  'AthenaParameters': {
                      'WorkGroup': 'string'
                  },
                  'AuroraParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'AuroraPostgreSqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'AwsIotAnalyticsParameters': {
                      'DataSetName': 'string'
                  },
                  'JiraParameters': {
                      'SiteBaseUrl': 'string'
                  },
                  'MariaDbParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'MySqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'PostgreSqlParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'PrestoParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Catalog': 'string'
                  },
                  'RdsParameters': {
                      'InstanceId': 'string',
                      'Database': 'string'
                  },
                  'RedshiftParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string',
                      'ClusterId': 'string'
                  },
                  'S3Parameters': {
                      'ManifestFileLocation': {
                          'Bucket': 'string',
                          'Key': 'string'
                      }
                  },
                  'ServiceNowParameters': {
                      'SiteBaseUrl': 'string'
                  },
                  'SnowflakeParameters': {
                      'Host': 'string',
                      'Database': 'string',
                      'Warehouse': 'string'
                  },
                  'SparkParameters': {
                      'Host': 'string',
                      'Port': 123
                  },
                  'SqlServerParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'TeradataParameters': {
                      'Host': 'string',
                      'Port': 123,
                      'Database': 'string'
                  },
                  'TwitterParameters': {
                      'Query': 'string',
                      'MaxRows': 123
                  }
              },
              Credentials={
                  'CredentialPair': {
                      'Username': 'string',
                      'Password': 'string'
                  }
              },
              VpcConnectionProperties={
                  'VpcConnectionArn': 'string'
              },
              SslProperties={
                  'DisableSsl': True|False
              }
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          The ID of the data source. This is unique per AWS Region per AWS account.

        :type Name: string
        :param Name: **[REQUIRED]**

          A display name for the data source.

        :type DataSourceParameters: dict
        :param DataSourceParameters:

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

              Location of the Amazon S3 manifest file. This is NULL if the manifest file was
              uploaded in the console.

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

        :type Credentials: dict
        :param Credentials:

          The credentials QuickSight uses to connect to your underlying source. Currently only
          username/password based credentials are supported.

          - **CredentialPair** *(dict) --*

            Credential pair.

            - **Username** *(string) --* **[REQUIRED]**

              Username.

            - **Password** *(string) --* **[REQUIRED]**

              Password.

        :type VpcConnectionProperties: dict
        :param VpcConnectionProperties:

          You need to use this parameter only when you want QuickSight to use a VPC connection when
          connecting to your underlying source.

          - **VpcConnectionArn** *(string) --* **[REQUIRED]**

            VPC connection ARN.

        :type SslProperties: dict
        :param SslProperties:

          SSL properties that apply when QuickSight connects to your underlying source.

          - **DisableSsl** *(boolean) --*

            A boolean flag to control whether SSL should be disabled.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Arn': 'string',
                'DataSourceId': 'string',
                'UpdateStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_data_source_permissions(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        GrantPermissions: List[ClientUpdateDataSourcePermissionsGrantPermissionsTypeDef] = None,
        RevokePermissions: List[ClientUpdateDataSourcePermissionsRevokePermissionsTypeDef] = None,
    ) -> ClientUpdateDataSourcePermissionsResponseTypeDef:
        """
        Updates the permissions to a data source.

        The permissions resource is
        ``arn:aws:quicksight:region:aws-account-id:datasource/data-source-id``

        CLI syntax:

         ``aws quicksight update-data-source-permissions \\``

         ``--aws-account-id=111122223333 \\``

         ``--data-source-id=unique-data-source-id \\``

         ``--name='My Data Source' \\``

         ``--grant-permissions=
             '[{"Principal":"arn:aws:quicksight:us-east-1:111122223333:user/default/user1","Actions":["quicksight:DescribeDataSource","quicksight:DescribeDataSourcePermissions","quicksight:PassDataSource"]}]'
         \\``

         ``--revoke-permissions=
             '[{"Principal":"arn:aws:quicksight:us-east-1:111122223333:user/default/user2","Actions":["quicksight:UpdateDataSource","quicksight:DeleteDataSource","quicksight:UpdateDataSourcePermissions"]}]'``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateDataSourcePermissions>`_

        **Request Syntax**
        ::

          response = client.update_data_source_permissions(
              AwsAccountId='string',
              DataSourceId='string',
              GrantPermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              RevokePermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID.

        :type DataSourceId: string
        :param DataSourceId: **[REQUIRED]**

          The ID of the data source. This is unique per AWS Region per AWS account.

        :type GrantPermissions: list
        :param GrantPermissions:

          A list of resource permissions that you want to grant on the data source.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type RevokePermissions: list
        :param RevokePermissions:

          A list of resource permissions that you want to revoke on the data source.

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DataSourceArn': 'string',
                'DataSourceId': 'string',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **DataSourceArn** *(string) --*

              The ARN of the data source.

            - **DataSourceId** *(string) --*

              The ID of the data source. This is unique per AWS Region per AWS account.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = None
    ) -> ClientUpdateGroupResponseTypeDef:
        """
        Changes a group description.

        The permissions resource is ``arn:aws:quicksight:us-east-1:*<aws-account-id>*
        :group/default/*<group-name>* `` .

        The response is a group object.

         **CLI Sample:**

         ``aws quicksight update-group --aws-account-id=111122223333 --namespace=default
         --group-name=Sales --description="Sales BI Dashboards"``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateGroup>`_

        **Request Syntax**
        ::

          response = client.update_group(
              GroupName='string',
              Description='string',
              AwsAccountId='string',
              Namespace='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**

          The name of the group that you want to update.

        :type Description: string
        :param Description:

          The description for the group that you want to update.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the group is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Group': {
                    'Arn': 'string',
                    'GroupName': 'string',
                    'Description': 'string',
                    'PrincipalId': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_iam_policy_assignment(
        self,
        AwsAccountId: str,
        AssignmentName: str,
        Namespace: str,
        AssignmentStatus: str = None,
        PolicyArn: str = None,
        Identities: Dict[str, List[str]] = None,
    ) -> ClientUpdateIamPolicyAssignmentResponseTypeDef:
        """
        Updates an existing assignment. This operation updates only the optional parameter or
        parameters that are specified in the request.

        CLI syntax:

         aws quicksight update-iam-policy-assignment --aws-account-id=111122223333
         --assignment-name=FullAccessAssignment --assignment-status=DRAFT
         --policy-arns=arn:aws:iam::aws:policy/AdministratorAccess
         --identities="user=user-1,user-2,group=admin" --namespace=default --region=us-east-1

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateIAMPolicyAssignment>`_

        **Request Syntax**
        ::

          response = client.update_iam_policy_assignment(
              AwsAccountId='string',
              AssignmentName='string',
              Namespace='string',
              AssignmentStatus='ENABLED'|'DRAFT'|'DISABLED',
              PolicyArn='string',
              Identities={
                  'string': [
                      'string',
                  ]
              }
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The AWS account ID that contains the IAM policy assignment.

        :type AssignmentName: string
        :param AssignmentName: **[REQUIRED]**

          The name of the assignment. It must be unique within an AWS account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace of the assignment.

        :type AssignmentStatus: string
        :param AssignmentStatus:

          The status of an assignment:

          * ENABLED - Anything specified in this assignment is used while creating the data source.

          * DISABLED - This assignment isn't used while creating the data source.

          * DRAFT - Assignment is an unfinished draft and isn't used while creating the data source.

        :type PolicyArn: string
        :param PolicyArn:

          An IAM policy ARN that will be applied to specified QuickSight users and groups in this
          assignment.

        :type Identities: dict
        :param Identities:

          QuickSight users and/or groups that you want to assign to the specified IAM policy.

          - *(string) --*

            - *(list) --*

              - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'AssignmentName': 'string',
                'AssignmentId': 'string',
                'PolicyArn': 'string',
                'Identities': {
                    'string': [
                        'string',
                    ]
                },
                'AssignmentStatus': 'ENABLED'|'DRAFT'|'DISABLED',
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **AssignmentName** *(string) --*

              The name of the assignment.

            - **AssignmentId** *(string) --*

              The ID of the assignment.

            - **PolicyArn** *(string) --*

              The IAM policy ARN assigned to the QuickSight users and groups specified in this
              request.

            - **Identities** *(dict) --*

              QuickSight users and/or groups that are assigned to this IAM policy.

              - *(string) --*

                - *(list) --*

                  - *(string) --*

            - **AssignmentStatus** *(string) --*

              The status of the assignment:

              * ENABLED - Anything specified in this assignment is used while creating the data
              source.

              * DISABLED - This assignment isn't used while creating the data source.

              * DRAFT - Assignment is an unfinished draft and isn't used while creating the data
              source.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_template(
        self,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: ClientUpdateTemplateSourceEntityTypeDef,
        VersionDescription: str = None,
        Name: str = None,
    ) -> ClientUpdateTemplateResponseTypeDef:
        """
        Updates a template from an existing QuickSight analysis.

        CLI syntax:

         ``aws quicksight update-template --aws-account-id 111122223333 --template-id
         reports_test_template --data-set-references
         DataSetPlaceholder=reports,DataSetArn=
             arn:aws:quicksight:us-west-2:111122223333:dataset/c684a204-d134-4c53-a63c-451f72c60c28
         DataSetPlaceholder=Elblogs,DataSetArn=
             arn:aws:quicksight:us-west-2:111122223333:dataset/15840b7d-b542-4491-937b-602416b367b3
         —source-entity
         SourceAnalysis=’{Arn=
             arn:aws:quicksight:us-west-2:111122223333:analysis/c5731fe9-4708-4598-8f6d-cf2a70875b6d}``

        You can also pass in a json file: ``aws quicksight update-template —cli-input-json
        file://create-template.json``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateTemplate>`_

        **Request Syntax**
        ::

          response = client.update_template(
              AwsAccountId='string',
              TemplateId='string',
              SourceEntity={
                  'SourceAnalysis': {
                      'Arn': 'string',
                      'DataSetReferences': [
                          {
                              'DataSetPlaceholder': 'string',
                              'DataSetArn': 'string'
                          },
                      ]
                  },
                  'SourceTemplate': {
                      'Arn': 'string'
                  }
              },
              VersionDescription='string',
              Name='string'
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template you are updating.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :type SourceEntity: dict
        :param SourceEntity: **[REQUIRED]**

          The source QuickSight entity from which this template is being created. Templates can be
          currently created from an Analysis or another template.

          - **SourceAnalysis** *(dict) --*

            The source analysis, if it is based on an analysis.

            - **Arn** *(string) --* **[REQUIRED]**

              The Amazon Resource name (ARN) of the resource.

            - **DataSetReferences** *(list) --* **[REQUIRED]**

              A structure containing information about the dataset references used as placeholders
              in the template.

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

        :type VersionDescription: string
        :param VersionDescription:

          A description of the current template version being created. This API created the first
          version of the template. Every time UpdateTemplate is called a new version is created.
          Each version of the template maintains a description of the version in the
          VersionDescription field.

        :type Name: string
        :param Name:

          The name for the template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateId': 'string',
                'Arn': 'string',
                'VersionArn': 'string',
                'CreationStatus':
                'CREATION_IN_PROGRESS'|'CREATION_SUCCESSFUL'|'CREATION_FAILED'
                |'UPDATE_IN_PROGRESS'|'UPDATE_SUCCESSFUL'|'UPDATE_FAILED',
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **TemplateId** *(string) --*

              The ID for the template.

            - **Arn** *(string) --*

              The Amazon Resource Name (ARN) for the template.

            - **VersionArn** *(string) --*

              The Amazon Resource Name (ARN) for the template, including the version information of
              the first version.

            - **CreationStatus** *(string) --*

              The creation status of the template.

            - **Status** *(integer) --*

              The http status of the request.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> ClientUpdateTemplateAliasResponseTypeDef:
        """
        Updates the template alias of a template.

        CLI syntax:

         ``aws quicksight update-template-alias --aws-account-id 111122223333 --template-id
         'reports_test_template' --alias-name STAGING —template-version-number 2``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateTemplateAlias>`_

        **Request Syntax**
        ::

          response = client.update_template_alias(
              AwsAccountId='string',
              TemplateId='string',
              AliasName='string',
              TemplateVersionNumber=123
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template aliases you are updating.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :type AliasName: string
        :param AliasName: **[REQUIRED]**

          The alias name.

        :type TemplateVersionNumber: integer
        :param TemplateVersionNumber: **[REQUIRED]**

          The version number of the template.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateAlias': {
                    'AliasName': 'string',
                    'Arn': 'string',
                    'TemplateVersionNumber': 123
                },
                'Status': 123,
                'RequestId': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_template_permissions(
        self,
        AwsAccountId: str,
        TemplateId: str,
        GrantPermissions: List[ClientUpdateTemplatePermissionsGrantPermissionsTypeDef] = None,
        RevokePermissions: List[ClientUpdateTemplatePermissionsRevokePermissionsTypeDef] = None,
    ) -> ClientUpdateTemplatePermissionsResponseTypeDef:
        """
        Updates the permissions on a template.

        CLI syntax:

        * ``aws quicksight describe-template-permissions —aws-account-id 111122223333 —template-id
        reports_test_template``

        * ``aws quicksight update-template-permissions —cli-input-json
        file://update-permission.json``

        * The structure of ``update-permissions.json`` to add permissions:  ``{ "AwsAccountId":
        "111122223333",``    ``"DashboardId": "reports_test_template",``    ``"GrantPermissions":
        [``    ``{ "Principal": "arn:aws:quicksight:us-east-1:196359894473:user/default/user3",``
        ``"Actions": [``    ``"quicksight:DescribeTemplate",``
        ``"quicksight:ListTemplateVersions"``    ``] } ] }``   The structure of
        ``update-permissions.json`` to add permissions:  ``{ "AwsAccountId": "111122223333",``
        ``"DashboardId": "reports_test_template",``    ``"RevokePermissions": [``    ``{
        "Principal": "arn:aws:quicksight:us-east-1:196359894473:user/default/user3",``
        ``"Actions": [``    ``"quicksight:DescribeTemplate",``
        ``"quicksight:ListTemplateVersions"``    ``] } ] }``   To obtain the principal name of a
        QuickSight group or user, use user describe-group or describe-user. For example:  ``aws
        quicksight describe-user``    ``--aws-account-id 111122223333``    ``--namespace default``
        ``--user-name user2``    ``--region us-east-1``    ``{``    ``"User": {``    ``"Arn":
        "arn:aws:quicksight:us-east-1:111122223333:user/default/user2",``    ``"Active": true,``
        ``"Email": "user2@example.com",``    ``"Role": "ADMIN",``    ``"UserName": "user2",``
        ``"PrincipalId": "federated/iam/abcd2abcdabcdeabc5ab5"``    ``},``    ``"RequestId":
        "8f74bb31-6291-448a-a71c-a765a44bae31",``    ``"Status": 200``    ``}``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateTemplatePermissions>`_

        **Request Syntax**
        ::

          response = client.update_template_permissions(
              AwsAccountId='string',
              TemplateId='string',
              GrantPermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ],
              RevokePermissions=[
                  {
                      'Principal': 'string',
                      'Actions': [
                          'string',
                      ]
                  },
              ]
          )
        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          AWS account ID that contains the template.

        :type TemplateId: string
        :param TemplateId: **[REQUIRED]**

          The ID for the template.

        :type GrantPermissions: list
        :param GrantPermissions:

          A list of resource permissions to be granted on the template. The following example shows
          the shorthand syntax:

           ``Shorthand Syntax: Principal=string,Actions=string,string ...``

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :type RevokePermissions: list
        :param RevokePermissions:

          A list of resource permissions to be revoked from the template. Shorthand syntax:
          ``Shorthand Syntax: Principal=string,Actions=string,string ...``

          - *(dict) --*

            Permission for the resource.

            - **Principal** *(string) --* **[REQUIRED]**

              The ARN of a QuickSight user or group, or an IAM ARN. If you are using cross-account
              resource sharing, this is the IAM ARN of an account root. Otherwise, it is the ARN of
              a QuickSight user or group. .

            - **Actions** *(list) --* **[REQUIRED]**

              The action to grant or revoke permissions on. For example,
              "quicksight:DescribeDashboard".

              - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TemplateId': 'string',
                'TemplateArn': 'string',
                'Permissions': [
                    {
                        'Principal': 'string',
                        'Actions': [
                            'string',
                        ]
                    },
                ],
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

            - **TemplateId** *(string) --*

              The ID for the template.

            - **TemplateArn** *(string) --*

              The ARN of the template.

            - **Permissions** *(list) --*

              A list of resource permissions to be set on the template.

              - *(dict) --*

                Permission for the resource.

                - **Principal** *(string) --*

                  The ARN of a QuickSight user or group, or an IAM ARN. If you are using
                  cross-account resource sharing, this is the IAM ARN of an account root. Otherwise,
                  it is the ARN of a QuickSight user or group. .

                - **Actions** *(list) --*

                  The action to grant or revoke permissions on. For example,
                  "quicksight:DescribeDashboard".

                  - *(string) --*

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_user(
        self, UserName: str, AwsAccountId: str, Namespace: str, Email: str, Role: str
    ) -> ClientUpdateUserResponseTypeDef:
        """
        Updates an Amazon QuickSight user.

        The response is a user object that contains the user's Amazon QuickSight user name, email
        address, active or inactive status in Amazon QuickSight, Amazon QuickSight role, and Amazon
        Resource Name (ARN).

         **CLI Sample:**

         ``aws quicksight update-user --user-name=Pat --role=ADMIN --email=new_address@example.com
         --aws-account-id=111122223333 --namespace=default --region=us-east-1``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/quicksight-2018-04-01/UpdateUser>`_

        **Request Syntax**
        ::

          response = client.update_user(
              UserName='string',
              AwsAccountId='string',
              Namespace='string',
              Email='string',
              Role='ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**

          The Amazon QuickSight user name that you want to update.

        :type AwsAccountId: string
        :param AwsAccountId: **[REQUIRED]**

          The ID for the AWS account that the user is in. Currently, you use the ID for the AWS
          account that contains your Amazon QuickSight account.

        :type Namespace: string
        :param Namespace: **[REQUIRED]**

          The namespace. Currently, you should set this to ``default`` .

        :type Email: string
        :param Email: **[REQUIRED]**

          The email address of the user that you want to update.

        :type Role: string
        :param Role: **[REQUIRED]**

          The Amazon QuickSight role of the user. The user role can be one of the following:

          * ``READER`` : A user who has read-only access to dashboards.

          * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and dashboards.

          * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight settings.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'User': {
                    'Arn': 'string',
                    'UserName': 'string',
                    'Email': 'string',
                    'Role': 'ADMIN'|'AUTHOR'|'READER'|'RESTRICTED_AUTHOR'|'RESTRICTED_READER',
                    'IdentityType': 'IAM'|'QUICKSIGHT',
                    'Active': True|False,
                    'PrincipalId': 'string'
                },
                'RequestId': 'string',
                'Status': 123
            }
          **Response Structure**

          - *(dict) --*

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

                * ``AUTHOR`` : A user who can create data sources, datasets, analyses, and
                dashboards.

                * ``ADMIN`` : A user who is an author, who can also manage Amazon QuickSight
                settings.

                * ``RESTRICTED_READER`` : This role isn't currently available for use.

                * ``RESTRICTED_AUTHOR`` : This role isn't currently available for use.

              - **IdentityType** *(string) --*

                The type of identity authentication used by the user.

              - **Active** *(boolean) --*

                Active status of user. When you create an Amazon QuickSight user that’s not an IAM
                user or an AD user, that user is inactive until they sign in and provide a password.

              - **PrincipalId** *(string) --*

                The principal ID of the user.

            - **RequestId** *(string) --*

              The AWS request ID for this operation.

            - **Status** *(integer) --*

              The http status of the request.

        """


class Exceptions:
    AccessDeniedException: Boto3ClientError
    ClientError: Boto3ClientError
    ConcurrentUpdatingException: Boto3ClientError
    ConflictException: Boto3ClientError
    DomainNotWhitelistedException: Boto3ClientError
    IdentityTypeNotSupportedException: Boto3ClientError
    InternalFailureException: Boto3ClientError
    InvalidNextTokenException: Boto3ClientError
    InvalidParameterValueException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    PreconditionNotMetException: Boto3ClientError
    QuickSightUserNotFoundException: Boto3ClientError
    ResourceExistsException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    ResourceUnavailableException: Boto3ClientError
    SessionLifetimeInMinutesInvalidException: Boto3ClientError
    ThrottlingException: Boto3ClientError
    UnsupportedUserEditionException: Boto3ClientError
