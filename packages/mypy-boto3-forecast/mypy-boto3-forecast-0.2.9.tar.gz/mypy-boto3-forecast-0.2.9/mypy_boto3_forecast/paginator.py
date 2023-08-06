"Main interface for forecast Paginators"
from __future__ import annotations

from typing import List
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_forecast.type_defs import (
    ListDatasetGroupsPaginatePaginationConfigTypeDef,
    ListDatasetGroupsPaginateResponseTypeDef,
    ListDatasetImportJobsPaginateFiltersTypeDef,
    ListDatasetImportJobsPaginatePaginationConfigTypeDef,
    ListDatasetImportJobsPaginateResponseTypeDef,
    ListDatasetsPaginatePaginationConfigTypeDef,
    ListDatasetsPaginateResponseTypeDef,
    ListForecastExportJobsPaginateFiltersTypeDef,
    ListForecastExportJobsPaginatePaginationConfigTypeDef,
    ListForecastExportJobsPaginateResponseTypeDef,
    ListForecastsPaginateFiltersTypeDef,
    ListForecastsPaginatePaginationConfigTypeDef,
    ListForecastsPaginateResponseTypeDef,
    ListPredictorsPaginateFiltersTypeDef,
    ListPredictorsPaginatePaginationConfigTypeDef,
    ListPredictorsPaginateResponseTypeDef,
)


__all__ = (
    "ListDatasetGroupsPaginator",
    "ListDatasetImportJobsPaginator",
    "ListDatasetsPaginator",
    "ListForecastExportJobsPaginator",
    "ListForecastsPaginator",
    "ListPredictorsPaginator",
)


class ListDatasetGroupsPaginator(Boto3Paginator):
    """
    Paginator for `list_dataset_groups`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self, PaginationConfig: ListDatasetGroupsPaginatePaginationConfigTypeDef = None
    ) -> ListDatasetGroupsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_dataset_groups`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasetGroups>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetGroups': [
                    {
                        'DatasetGroupArn': 'string',
                        'DatasetGroupName': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **DatasetGroups** *(list) --*

              An array of objects that summarize each dataset group's properties.

              - *(dict) --*

                Provides a summary of the dataset group properties used in the  ListDatasetGroups
                operation. To get the complete set of properties, call the  DescribeDatasetGroup
                operation, and provide the ``DatasetGroupArn`` .

                - **DatasetGroupArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset group.

                - **DatasetGroupName** *(string) --*

                  The name of the dataset group.

                - **CreationTime** *(datetime) --*

                  When the dataset group was created.

                - **LastModificationTime** *(datetime) --*

                  When the dataset group was created or last updated from a call to the
                  UpdateDatasetGroup operation. While the dataset group is being updated,
                  ``LastModificationTime`` is the current time of the ``ListDatasetGroups`` call.

        """


class ListDatasetImportJobsPaginator(Boto3Paginator):
    """
    Paginator for `list_dataset_import_jobs`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        Filters: List[ListDatasetImportJobsPaginateFiltersTypeDef] = None,
        PaginationConfig: ListDatasetImportJobsPaginatePaginationConfigTypeDef = None,
    ) -> ListDatasetImportJobsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_dataset_import_jobs`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasetImportJobs>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type Filters: list
        :param Filters:

          An array of filters. For each filter, you provide a condition and a match statement. The
          condition is either ``IS`` or ``IS_NOT`` , which specifies whether to include or exclude
          the datasets that match the statement from the list, respectively. The match statement
          consists of a key and a value.

           **Filter properties**

          * ``Condition`` - The condition to apply. Valid values are ``IS`` and ``IS_NOT`` . To
          include the datasets that match the statement, specify ``IS`` . To exclude matching
          datasets, specify ``IS_NOT`` .

          * ``Key`` - The name of the parameter to filter on. Valid values are ``DatasetArn`` and
          ``Status`` .

          * ``Value`` - The value to match.

          For example, to list all dataset import jobs whose status is ACTIVE, you specify the
          following filter:

           ``"Filters": [ { "Condition": "IS", "Key": "Status", "Value": "ACTIVE" } ]``

          - *(dict) --*

            Describes a filter for choosing a subset of objects. Each filter consists of a condition
            and a match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies
            whether to include or exclude the objects that match the statement, respectively. The
            match statement consists of a key and a value.

            - **Key** *(string) --* **[REQUIRED]**

              The name of the parameter to filter on.

            - **Value** *(string) --* **[REQUIRED]**

              The value to match.

            - **Condition** *(string) --* **[REQUIRED]**

              The condition to apply. To include the objects that match the statement, specify
              ``IS`` . To exclude matching objects, specify ``IS_NOT`` .

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetImportJobs': [
                    {
                        'DatasetImportJobArn': 'string',
                        'DatasetImportJobName': 'string',
                        'DataSource': {
                            'S3Config': {
                                'Path': 'string',
                                'RoleArn': 'string',
                                'KMSKeyArn': 'string'
                            }
                        },
                        'Status': 'string',
                        'Message': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **DatasetImportJobs** *(list) --*

              An array of objects that summarize each dataset import job's properties.

              - *(dict) --*

                Provides a summary of the dataset import job properties used in the
                ListDatasetImportJobs operation. To get the complete set of properties, call the
                DescribeDatasetImportJob operation, and provide the ``DatasetImportJobArn`` .

                - **DatasetImportJobArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset import job.

                - **DatasetImportJobName** *(string) --*

                  The name of the dataset import job.

                - **DataSource** *(dict) --*

                  The location of the training data to import and an AWS Identity and Access
                  Management (IAM) role that Amazon Forecast can assume to access the data. The
                  training data must be stored in an Amazon S3 bucket.

                  If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS)
                  key.

                  - **S3Config** *(dict) --*

                    The path to the training data stored in an Amazon Simple Storage Service (Amazon
                    S3) bucket along with the credentials to access the data.

                    - **Path** *(string) --*

                      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in
                      an Amazon S3 bucket.

                    - **RoleArn** *(string) --*

                      The ARN of the AWS Identity and Access Management (IAM) role that Amazon
                      Forecast can assume to access the Amazon S3 bucket or files. If you provide a
                      value for the ``KMSKeyArn`` key, the role must allow access to the key.

                      Passing a role across AWS accounts is not allowed. If you pass a role that
                      isn't in your account, you get an ``InvalidInputException`` error.

                    - **KMSKeyArn** *(string) --*

                      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

                - **Status** *(string) --*

                  The status of the dataset import job. The status is reflected in the status of the
                  dataset. For example, when the import job status is ``CREATE_IN_PROGRESS`` , the
                  status of the dataset is ``UPDATE_IN_PROGRESS`` . States include:

                  * ``ACTIVE``

                  * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

                  * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

                - **Message** *(string) --*

                  If an error occurred, an informational message about the error.

                - **CreationTime** *(datetime) --*

                  When the dataset import job was created.

                - **LastModificationTime** *(datetime) --*

                  The last time that the dataset was modified. The time depends on the status of the
                  job, as follows:

                  * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

                  * ``CREATE_IN_PROGRESS`` - The current timestamp.

                  * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.

        """


class ListDatasetsPaginator(Boto3Paginator):
    """
    Paginator for `list_datasets`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self, PaginationConfig: ListDatasetsPaginatePaginationConfigTypeDef = None
    ) -> ListDatasetsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_datasets`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasets>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Datasets': [
                    {
                        'DatasetArn': 'string',
                        'DatasetName': 'string',
                        'DatasetType': 'TARGET_TIME_SERIES'|'RELATED_TIME_SERIES'|'ITEM_METADATA',
                        'Domain':
                        'RETAIL'|'CUSTOM'|'INVENTORY_PLANNING'|'EC2_CAPACITY'
                        |'WORK_FORCE'|'WEB_TRAFFIC'|'METRICS',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **Datasets** *(list) --*

              An array of objects that summarize each dataset's properties.

              - *(dict) --*

                Provides a summary of the dataset properties used in the  ListDatasets operation. To
                get the complete set of properties, call the  DescribeDataset operation, and provide
                the ``DatasetArn`` .

                - **DatasetArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset.

                - **DatasetName** *(string) --*

                  The name of the dataset.

                - **DatasetType** *(string) --*

                  The dataset type.

                - **Domain** *(string) --*

                  The domain associated with the dataset.

                - **CreationTime** *(datetime) --*

                  When the dataset was created.

                - **LastModificationTime** *(datetime) --*

                  When you create a dataset, ``LastModificationTime`` is the same as
                  ``CreationTime`` . While data is being imported to the dataset,
                  ``LastModificationTime`` is the current time of the ``ListDatasets`` call. After a
                  CreateDatasetImportJob operation has finished, ``LastModificationTime`` is when
                  the import job completed or failed.

        """


class ListForecastExportJobsPaginator(Boto3Paginator):
    """
    Paginator for `list_forecast_export_jobs`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        Filters: List[ListForecastExportJobsPaginateFiltersTypeDef] = None,
        PaginationConfig: ListForecastExportJobsPaginatePaginationConfigTypeDef = None,
    ) -> ListForecastExportJobsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_forecast_export_jobs`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListForecastExportJobs>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type Filters: list
        :param Filters:

          An array of filters. For each filter, you provide a condition and a match statement. The
          condition is either ``IS`` or ``IS_NOT`` , which specifies whether to include or exclude
          the forecast export jobs that match the statement from the list, respectively. The match
          statement consists of a key and a value.

           **Filter properties**

          * ``Condition`` - The condition to apply. Valid values are ``IS`` and ``IS_NOT`` . To
          include the forecast export jobs that match the statement, specify ``IS`` . To exclude
          matching forecast export jobs, specify ``IS_NOT`` .

          * ``Key`` - The name of the parameter to filter on. Valid values are ``ForecastArn`` and
          ``Status`` .

          * ``Value`` - The value to match.

          For example, to list all jobs that export a forecast named *electricityforecast* , specify
          the following filter:

           ``"Filters": [ { "Condition": "IS", "Key": "ForecastArn", "Value":
           "arn:aws:forecast:us-west-2:<acct-id>:forecast/electricityforecast" } ]``

          - *(dict) --*

            Describes a filter for choosing a subset of objects. Each filter consists of a condition
            and a match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies
            whether to include or exclude the objects that match the statement, respectively. The
            match statement consists of a key and a value.

            - **Key** *(string) --* **[REQUIRED]**

              The name of the parameter to filter on.

            - **Value** *(string) --* **[REQUIRED]**

              The value to match.

            - **Condition** *(string) --* **[REQUIRED]**

              The condition to apply. To include the objects that match the statement, specify
              ``IS`` . To exclude matching objects, specify ``IS_NOT`` .

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ForecastExportJobs': [
                    {
                        'ForecastExportJobArn': 'string',
                        'ForecastExportJobName': 'string',
                        'Destination': {
                            'S3Config': {
                                'Path': 'string',
                                'RoleArn': 'string',
                                'KMSKeyArn': 'string'
                            }
                        },
                        'Status': 'string',
                        'Message': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **ForecastExportJobs** *(list) --*

              An array of objects that summarize each export job's properties.

              - *(dict) --*

                Provides a summary of the forecast export job properties used in the
                ListForecastExportJobs operation. To get the complete set of properties, call the
                DescribeForecastExportJob operation, and provide the listed ``ForecastExportJobArn``
                .

                - **ForecastExportJobArn** *(string) --*

                  The Amazon Resource Name (ARN) of the forecast export job.

                - **ForecastExportJobName** *(string) --*

                  The name of the forecast export job.

                - **Destination** *(dict) --*

                  The path to the Amazon Simple Storage Service (Amazon S3) bucket where the
                  forecast is exported.

                  - **S3Config** *(dict) --*

                    The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the
                    credentials to access the bucket.

                    - **Path** *(string) --*

                      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in
                      an Amazon S3 bucket.

                    - **RoleArn** *(string) --*

                      The ARN of the AWS Identity and Access Management (IAM) role that Amazon
                      Forecast can assume to access the Amazon S3 bucket or files. If you provide a
                      value for the ``KMSKeyArn`` key, the role must allow access to the key.

                      Passing a role across AWS accounts is not allowed. If you pass a role that
                      isn't in your account, you get an ``InvalidInputException`` error.

                    - **KMSKeyArn** *(string) --*

                      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

                - **Status** *(string) --*

                  The status of the forecast export job. States include:

                  * ``ACTIVE``

                  * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

                  * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

                  .. note::

                    The ``Status`` of the forecast export job must be ``ACTIVE`` before you can
                    access the forecast in your S3 bucket.

                - **Message** *(string) --*

                  If an error occurred, an informational message about the error.

                - **CreationTime** *(datetime) --*

                  When the forecast export job was created.

                - **LastModificationTime** *(datetime) --*

                  When the last successful export job finished.

        """


class ListForecastsPaginator(Boto3Paginator):
    """
    Paginator for `list_forecasts`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        Filters: List[ListForecastsPaginateFiltersTypeDef] = None,
        PaginationConfig: ListForecastsPaginatePaginationConfigTypeDef = None,
    ) -> ListForecastsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_forecasts`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListForecasts>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type Filters: list
        :param Filters:

          An array of filters. For each filter, you provide a condition and a match statement. The
          condition is either ``IS`` or ``IS_NOT`` , which specifies whether to include or exclude
          the forecasts that match the statement from the list, respectively. The match statement
          consists of a key and a value.

           **Filter properties**

          * ``Condition`` - The condition to apply. Valid values are ``IS`` and ``IS_NOT`` . To
          include the forecasts that match the statement, specify ``IS`` . To exclude matching
          forecasts, specify ``IS_NOT`` .

          * ``Key`` - The name of the parameter to filter on. Valid values are ``DatasetGroupArn`` ,
          ``PredictorArn`` , and ``Status`` .

          * ``Value`` - The value to match.

          For example, to list all forecasts whose status is not ACTIVE, you would specify:

           ``"Filters": [ { "Condition": "IS_NOT", "Key": "Status", "Value": "ACTIVE" } ]``

          - *(dict) --*

            Describes a filter for choosing a subset of objects. Each filter consists of a condition
            and a match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies
            whether to include or exclude the objects that match the statement, respectively. The
            match statement consists of a key and a value.

            - **Key** *(string) --* **[REQUIRED]**

              The name of the parameter to filter on.

            - **Value** *(string) --* **[REQUIRED]**

              The value to match.

            - **Condition** *(string) --* **[REQUIRED]**

              The condition to apply. To include the objects that match the statement, specify
              ``IS`` . To exclude matching objects, specify ``IS_NOT`` .

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Forecasts': [
                    {
                        'ForecastArn': 'string',
                        'ForecastName': 'string',
                        'PredictorArn': 'string',
                        'DatasetGroupArn': 'string',
                        'Status': 'string',
                        'Message': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **Forecasts** *(list) --*

              An array of objects that summarize each forecast's properties.

              - *(dict) --*

                Provides a summary of the forecast properties used in the  ListForecasts operation.
                To get the complete set of properties, call the  DescribeForecast operation, and
                provide the ``ForecastArn`` that is listed in the summary.

                - **ForecastArn** *(string) --*

                  The ARN of the forecast.

                - **ForecastName** *(string) --*

                  The name of the forecast.

                - **PredictorArn** *(string) --*

                  The ARN of the predictor used to generate the forecast.

                - **DatasetGroupArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset group that provided the data used to
                  train the predictor.

                - **Status** *(string) --*

                  The status of the forecast. States include:

                  * ``ACTIVE``

                  * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

                  * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

                  .. note::

                    The ``Status`` of the forecast must be ``ACTIVE`` before you can query or export
                    the forecast.

                - **Message** *(string) --*

                  If an error occurred, an informational message about the error.

                - **CreationTime** *(datetime) --*

                  When the forecast creation task was created.

                - **LastModificationTime** *(datetime) --*

                  Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated
                  when inference (creating the forecast) starts (status changed to
                  ``CREATE_IN_PROGRESS`` ), and when inference is complete (status changed to
                  ``ACTIVE`` ) or fails (status changed to ``CREATE_FAILED`` ).

        """


class ListPredictorsPaginator(Boto3Paginator):
    """
    Paginator for `list_predictors`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        Filters: List[ListPredictorsPaginateFiltersTypeDef] = None,
        PaginationConfig: ListPredictorsPaginatePaginationConfigTypeDef = None,
    ) -> ListPredictorsPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ForecastService.Client.list_predictors`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListPredictors>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type Filters: list
        :param Filters:

          An array of filters. For each filter, you provide a condition and a match statement. The
          condition is either ``IS`` or ``IS_NOT`` , which specifies whether to include or exclude
          the predictors that match the statement from the list, respectively. The match statement
          consists of a key and a value.

           **Filter properties**

          * ``Condition`` - The condition to apply. Valid values are ``IS`` and ``IS_NOT`` . To
          include the predictors that match the statement, specify ``IS`` . To exclude matching
          predictors, specify ``IS_NOT`` .

          * ``Key`` - The name of the parameter to filter on. Valid values are ``DatasetGroupArn``
          and ``Status`` .

          * ``Value`` - The value to match.

          For example, to list all predictors whose status is ACTIVE, you would specify:

           ``"Filters": [ { "Condition": "IS", "Key": "Status", "Value": "ACTIVE" } ]``

          - *(dict) --*

            Describes a filter for choosing a subset of objects. Each filter consists of a condition
            and a match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies
            whether to include or exclude the objects that match the statement, respectively. The
            match statement consists of a key and a value.

            - **Key** *(string) --* **[REQUIRED]**

              The name of the parameter to filter on.

            - **Value** *(string) --* **[REQUIRED]**

              The value to match.

            - **Condition** *(string) --* **[REQUIRED]**

              The condition to apply. To include the objects that match the statement, specify
              ``IS`` . To exclude matching objects, specify ``IS_NOT`` .

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Predictors': [
                    {
                        'PredictorArn': 'string',
                        'PredictorName': 'string',
                        'DatasetGroupArn': 'string',
                        'Status': 'string',
                        'Message': 'string',
                        'CreationTime': datetime(2015, 1, 1),
                        'LastModificationTime': datetime(2015, 1, 1)
                    },
                ],

            }
          **Response Structure**

          - *(dict) --*

            - **Predictors** *(list) --*

              An array of objects that summarize each predictor's properties.

              - *(dict) --*

                Provides a summary of the predictor properties that are used in the  ListPredictors
                operation. To get the complete set of properties, call the  DescribePredictor
                operation, and provide the listed ``PredictorArn`` .

                - **PredictorArn** *(string) --*

                  The ARN of the predictor.

                - **PredictorName** *(string) --*

                  The name of the predictor.

                - **DatasetGroupArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset group that contains the data used to
                  train the predictor.

                - **Status** *(string) --*

                  The status of the predictor. States include:

                  * ``ACTIVE``

                  * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

                  * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

                  * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

                  .. note::

                    The ``Status`` of the predictor must be ``ACTIVE`` before you can use the
                    predictor to create a forecast.

                - **Message** *(string) --*

                  If an error occurred, an informational message about the error.

                - **CreationTime** *(datetime) --*

                  When the model training task was created.

                - **LastModificationTime** *(datetime) --*

                  Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated
                  when training starts (status changed to ``CREATE_IN_PROGRESS`` ), and when
                  training is complete (status changed to ``ACTIVE`` ) or fails (status changed to
                  ``CREATE_FAILED`` ).

        """
