"Main interface for forecast Client"
from __future__ import annotations

from typing import Any, Dict, List
from typing_extensions import Literal, overload
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError
from botocore.paginate import Paginator as Boto3Paginator

# pylint: disable=import-self
import mypy_boto3_forecast.client as client_scope

# pylint: disable=import-self
import mypy_boto3_forecast.paginator as paginator_scope
from mypy_boto3_forecast.type_defs import (
    ClientCreateDatasetEncryptionConfigTypeDef,
    ClientCreateDatasetGroupResponseTypeDef,
    ClientCreateDatasetImportJobDataSourceTypeDef,
    ClientCreateDatasetImportJobResponseTypeDef,
    ClientCreateDatasetResponseTypeDef,
    ClientCreateDatasetSchemaTypeDef,
    ClientCreateForecastExportJobDestinationTypeDef,
    ClientCreateForecastExportJobResponseTypeDef,
    ClientCreateForecastResponseTypeDef,
    ClientCreatePredictorEncryptionConfigTypeDef,
    ClientCreatePredictorEvaluationParametersTypeDef,
    ClientCreatePredictorFeaturizationConfigTypeDef,
    ClientCreatePredictorHPOConfigTypeDef,
    ClientCreatePredictorInputDataConfigTypeDef,
    ClientCreatePredictorResponseTypeDef,
    ClientDescribeDatasetGroupResponseTypeDef,
    ClientDescribeDatasetImportJobResponseTypeDef,
    ClientDescribeDatasetResponseTypeDef,
    ClientDescribeForecastExportJobResponseTypeDef,
    ClientDescribeForecastResponseTypeDef,
    ClientDescribePredictorResponseTypeDef,
    ClientGetAccuracyMetricsResponseTypeDef,
    ClientListDatasetGroupsResponseTypeDef,
    ClientListDatasetImportJobsFiltersTypeDef,
    ClientListDatasetImportJobsResponseTypeDef,
    ClientListDatasetsResponseTypeDef,
    ClientListForecastExportJobsFiltersTypeDef,
    ClientListForecastExportJobsResponseTypeDef,
    ClientListForecastsFiltersTypeDef,
    ClientListForecastsResponseTypeDef,
    ClientListPredictorsFiltersTypeDef,
    ClientListPredictorsResponseTypeDef,
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
    def create_dataset(
        self,
        DatasetName: str,
        Domain: str,
        DatasetType: str,
        Schema: ClientCreateDatasetSchemaTypeDef,
        DataFrequency: str = None,
        EncryptionConfig: ClientCreateDatasetEncryptionConfigTypeDef = None,
    ) -> ClientCreateDatasetResponseTypeDef:
        """
        Creates an Amazon Forecast dataset. The information about the dataset that you provide helps
        Forecast understand how to consume the data for model training. This includes the following:

        * *``DataFrequency`` * - How frequently your historical time-series data is collected.

        * *``Domain`` * and * ``DatasetType`` * - Each dataset has an associated dataset domain and
        a type within the domain. Amazon Forecast provides a list of predefined domains and types
        within each domain. For each unique dataset domain and type within the domain, Amazon
        Forecast requires your data to include a minimum set of predefined fields.

        * *``Schema`` * - A schema specifies the fields in the dataset, including the field name and
        data type.

        After creating a dataset, you import your training data into it and add the dataset to a
        dataset group. You use the dataset group to create a predictor. For more information, see
        howitworks-datasets-groups .

        To get a list of all your datasets, use the  ListDatasets operation.

        For example Forecast datasets, see the `Amazon Forecast Sample GitHub repository
        <https://github.com/aws-samples/amazon-forecast-samples/tree/master/data>`__ .

        .. note::

          The ``Status`` of a dataset must be ``ACTIVE`` before you can import training data. Use
          the  DescribeDataset operation to get the status.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreateDataset>`_

        **Request Syntax**
        ::

          response = client.create_dataset(
              DatasetName='string',
              Domain=
                  'RETAIL'|'CUSTOM'|'INVENTORY_PLANNING'|'EC2_CAPACITY'|'WORK_FORCE'|'WEB_TRAFFIC'
                  |'METRICS',
              DatasetType='TARGET_TIME_SERIES'|'RELATED_TIME_SERIES'|'ITEM_METADATA',
              DataFrequency='string',
              Schema={
                  'Attributes': [
                      {
                          'AttributeName': 'string',
                          'AttributeType': 'string'|'integer'|'float'|'timestamp'
                      },
                  ]
              },
              EncryptionConfig={
                  'RoleArn': 'string',
                  'KMSKeyArn': 'string'
              }
          )
        :type DatasetName: string
        :param DatasetName: **[REQUIRED]**

          A name for the dataset.

        :type Domain: string
        :param Domain: **[REQUIRED]**

          The domain associated with the dataset. When you add a dataset to a dataset group, this
          value and the value specified for the ``Domain`` parameter of the  CreateDatasetGroup
          operation must match.

          The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be
          present in the training data that you import to the dataset. For example, if you choose
          the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast
          requires ``item_id`` , ``timestamp`` , and ``demand`` fields to be present in your data.
          For more information, see  howitworks-datasets-groups .

        :type DatasetType: string
        :param DatasetType: **[REQUIRED]**

          The dataset type. Valid values depend on the chosen ``Domain`` .

        :type DataFrequency: string
        :param DataFrequency:

          The frequency of data collection. This parameter is required for RELATED_TIME_SERIES
          datasets.

          Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30 minutes),
          15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute). For
          example, "D" indicates every day and "15min" indicates every 15 minutes.

        :type Schema: dict
        :param Schema: **[REQUIRED]**

          The schema for the dataset. The schema attributes and their order must match the fields in
          your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the
          minimum required fields in your training data. For information about the required fields
          for a specific dataset domain and type, see  howitworks-domains-ds-types .

          - **Attributes** *(list) --*

            An array of attributes specifying the name and type of each field in a dataset.

            - *(dict) --*

              An attribute of a schema, which defines a dataset field. A schema attribute is
              required for every field in a dataset. The  Schema object contains an array of
              ``SchemaAttribute`` objects.

              - **AttributeName** *(string) --*

                The name of the dataset field.

              - **AttributeType** *(string) --*

                The data type of the field.

        :type EncryptionConfig: dict
        :param EncryptionConfig:

          An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM)
          role that Amazon Forecast can assume to access the key.

          - **RoleArn** *(string) --* **[REQUIRED]**

            The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

            Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
            account, you get an ``InvalidInputException`` error.

          - **KMSKeyArn** *(string) --* **[REQUIRED]**

            The Amazon Resource Name (ARN) of the KMS key.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetArn** *(string) --*

              The Amazon Resource Name (ARN) of the dataset.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_dataset_group(
        self, DatasetGroupName: str, Domain: str, DatasetArns: List[str] = None
    ) -> ClientCreateDatasetGroupResponseTypeDef:
        """
        Creates a dataset group, which holds a collection of related datasets. You can add datasets
        to the dataset group when you create the dataset group, or later by using the
        UpdateDatasetGroup operation.

        After creating a dataset group and adding datasets, you use the dataset group when you
        create a predictor. For more information, see  howitworks-datasets-groups .

        To get a list of all your datasets groups, use the  ListDatasetGroups operation.

        .. note::

          The ``Status`` of a dataset group must be ``ACTIVE`` before you can create use the dataset
          group to create a predictor. To get the status, use the  DescribeDatasetGroup operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreateDatasetGroup>`_

        **Request Syntax**
        ::

          response = client.create_dataset_group(
              DatasetGroupName='string',
              Domain=
                  'RETAIL'|'CUSTOM'|'INVENTORY_PLANNING'|'EC2_CAPACITY'|'WORK_FORCE'|'WEB_TRAFFIC'
                  |'METRICS',
              DatasetArns=[
                  'string',
              ]
          )
        :type DatasetGroupName: string
        :param DatasetGroupName: **[REQUIRED]**

          A name for the dataset group.

        :type Domain: string
        :param Domain: **[REQUIRED]**

          The domain associated with the dataset group. When you add a dataset to a dataset group,
          this value and the value specified for the ``Domain`` parameter of the  CreateDataset
          operation must match.

          The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be
          present in training data that you import to a dataset. For example, if you choose the
          ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast
          requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your
          data. For more information, see  howitworks-datasets-groups .

        :type DatasetArns: list
        :param DatasetArns:

          An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the
          dataset group.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetGroupArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetGroupArn** *(string) --*

              The Amazon Resource Name (ARN) of the dataset group.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_dataset_import_job(
        self,
        DatasetImportJobName: str,
        DatasetArn: str,
        DataSource: ClientCreateDatasetImportJobDataSourceTypeDef,
        TimestampFormat: str = None,
    ) -> ClientCreateDatasetImportJobResponseTypeDef:
        """
        Imports your training data to an Amazon Forecast dataset. You provide the location of your
        training data in an Amazon Simple Storage Service (Amazon S3) bucket and the Amazon Resource
        Name (ARN) of the dataset that you want to import the data to.

        You must specify a  DataSource object that includes an AWS Identity and Access Management
        (IAM) role that Amazon Forecast can assume to access the data. For more information, see
        aws-forecast-iam-roles .

        The training data must be in CSV format. The delimiter must be a comma (,).

        You can specify the path to a specific CSV file, the S3 bucket, or to a folder in the S3
        bucket. For the latter two cases, Amazon Forecast imports all files up to the limit of
        10,000 files.

        To get a list of all your dataset import jobs, filtered by specified criteria, use the
        ListDatasetImportJobs operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreateDatasetImportJob>`_

        **Request Syntax**
        ::

          response = client.create_dataset_import_job(
              DatasetImportJobName='string',
              DatasetArn='string',
              DataSource={
                  'S3Config': {
                      'Path': 'string',
                      'RoleArn': 'string',
                      'KMSKeyArn': 'string'
                  }
              },
              TimestampFormat='string'
          )
        :type DatasetImportJobName: string
        :param DatasetImportJobName: **[REQUIRED]**

          The name for the dataset import job. We recommend including the current timestamp in the
          name, for example, ``20190721DatasetImport`` . This can help you avoid getting a
          ``ResourceAlreadyExistsException`` exception.

        :type DatasetArn: string
        :param DatasetArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the Amazon Forecast dataset that you want to import data
          to.

        :type DataSource: dict
        :param DataSource: **[REQUIRED]**

          The location of the training data to import and an AWS Identity and Access Management
          (IAM) role that Amazon Forecast can assume to access the data. The training data must be
          stored in an Amazon S3 bucket.

          If encryption is used, ``DataSource`` must include an AWS Key Management Service (KMS) key
          and the IAM role must allow Amazon Forecast permission to access the key. The KMS key and
          IAM role must match those specified in the ``EncryptionConfig`` parameter of the
          CreateDataset operation.

          - **S3Config** *(dict) --* **[REQUIRED]**

            The path to the training data stored in an Amazon Simple Storage Service (Amazon S3)
            bucket along with the credentials to access the data.

            - **Path** *(string) --* **[REQUIRED]**

              The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
              Amazon S3 bucket.

            - **RoleArn** *(string) --* **[REQUIRED]**

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        :type TimestampFormat: string
        :param TimestampFormat:

          The format of timestamps in the dataset. The format that you specify depends on the
          ``DataFrequency`` specified when the dataset was created. The following formats are
          supported

          * "yyyy-MM-dd" For the following data frequencies: Y, M, W, and D

          * "yyyy-MM-dd HH:mm:ss" For the following data frequencies: H, 30min, 15min, and 1min; and
          optionally, for: Y, M, W, and D

          If the format isn't specified, Amazon Forecast expects the format to be "yyyy-MM-dd
          HH:mm:ss".

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetImportJobArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetImportJobArn** *(string) --*

              The Amazon Resource Name (ARN) of the dataset import job.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_forecast(
        self, ForecastName: str, PredictorArn: str, ForecastTypes: List[str] = None
    ) -> ClientCreateForecastResponseTypeDef:
        """
        Creates a forecast for each item in the ``TARGET_TIME_SERIES`` dataset that was used to
        train the predictor. This is known as inference. To retrieve the forecast for a single item
        at low latency, use the operation. To export the complete forecast into your Amazon Simple
        Storage Service (Amazon S3) bucket, use the  CreateForecastExportJob operation.

        The range of the forecast is determined by the ``ForecastHorizon`` value, which you specify
        in the  CreatePredictor request, multiplied by the ``DataFrequency`` value, which you
        specify in the  CreateDataset request. When you query a forecast, you can request a specific
        date range within the forecast.

        To get a list of all your forecasts, use the  ListForecasts operation.

        .. note::

          The forecasts generated by Amazon Forecast are in the same time zone as the dataset that
          was used to create the predictor.

        For more information, see  howitworks-forecast .

        .. note::

          The ``Status`` of the forecast must be ``ACTIVE`` before you can query or export the
          forecast. Use the  DescribeForecast operation to get the status.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreateForecast>`_

        **Request Syntax**
        ::

          response = client.create_forecast(
              ForecastName='string',
              PredictorArn='string',
              ForecastTypes=[
                  'string',
              ]
          )
        :type ForecastName: string
        :param ForecastName: **[REQUIRED]**

          A name for the forecast.

        :type PredictorArn: string
        :param PredictorArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the predictor to use to generate the forecast.

        :type ForecastTypes: list
        :param ForecastTypes:

          The quantiles at which probabilistic forecasts are generated. You can specify up to 5
          quantiles per forecast. Accepted values include ``0.01 to 0.99`` (increments of .01 only)
          and ``mean`` . The mean forecast is different from the median (0.50) when the distribution
          is not symmetric (e.g. Beta, Negative Binomial). The default value is ``["0.1", "0.5",
          "0.9"]`` .

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ForecastArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ForecastArn** *(string) --*

              The Amazon Resource Name (ARN) of the forecast.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_forecast_export_job(
        self,
        ForecastExportJobName: str,
        ForecastArn: str,
        Destination: ClientCreateForecastExportJobDestinationTypeDef,
    ) -> ClientCreateForecastExportJobResponseTypeDef:
        """
        Exports a forecast created by the  CreateForecast operation to your Amazon Simple Storage
        Service (Amazon S3) bucket. The forecast file name will match the following conventions:

        <ForecastExportJobName>_<ExportTimestamp>_<PageNumber>

        where the <ExportTimestamp> component is in Java SimpleDateFormat (yyyy-MM-ddTHH-mm-ssZ).

        You must specify a  DataDestination object that includes an AWS Identity and Access
        Management (IAM) role that Amazon Forecast can assume to access the Amazon S3 bucket. For
        more information, see  aws-forecast-iam-roles .

        For more information, see  howitworks-forecast .

        To get a list of all your forecast export jobs, use the  ListForecastExportJobs operation.

        .. note::

          The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
          forecast in your Amazon S3 bucket. To get the status, use the  DescribeForecastExportJob
          operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreateForecastExportJob>`_

        **Request Syntax**
        ::

          response = client.create_forecast_export_job(
              ForecastExportJobName='string',
              ForecastArn='string',
              Destination={
                  'S3Config': {
                      'Path': 'string',
                      'RoleArn': 'string',
                      'KMSKeyArn': 'string'
                  }
              }
          )
        :type ForecastExportJobName: string
        :param ForecastExportJobName: **[REQUIRED]**

          The name for the forecast export job.

        :type ForecastArn: string
        :param ForecastArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the forecast that you want to export.

        :type Destination: dict
        :param Destination: **[REQUIRED]**

          The location where you want to save the forecast and an AWS Identity and Access Management
          (IAM) role that Amazon Forecast can assume to access the location. The forecast must be
          exported to an Amazon S3 bucket.

          If encryption is used, ``Destination`` must include an AWS Key Management Service (KMS)
          key. The IAM role must allow Amazon Forecast permission to access the key.

          - **S3Config** *(dict) --* **[REQUIRED]**

            The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the
            credentials to access the bucket.

            - **Path** *(string) --* **[REQUIRED]**

              The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
              Amazon S3 bucket.

            - **RoleArn** *(string) --* **[REQUIRED]**

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ForecastExportJobArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ForecastExportJobArn** *(string) --*

              The Amazon Resource Name (ARN) of the export job.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_predictor(
        self,
        PredictorName: str,
        ForecastHorizon: int,
        InputDataConfig: ClientCreatePredictorInputDataConfigTypeDef,
        FeaturizationConfig: ClientCreatePredictorFeaturizationConfigTypeDef,
        AlgorithmArn: str = None,
        PerformAutoML: bool = None,
        PerformHPO: bool = None,
        TrainingParameters: Dict[str, str] = None,
        EvaluationParameters: ClientCreatePredictorEvaluationParametersTypeDef = None,
        HPOConfig: ClientCreatePredictorHPOConfigTypeDef = None,
        EncryptionConfig: ClientCreatePredictorEncryptionConfigTypeDef = None,
    ) -> ClientCreatePredictorResponseTypeDef:
        """
        Creates an Amazon Forecast predictor.

        In the request, you provide a dataset group and either specify an algorithm or let Amazon
        Forecast choose the algorithm for you using AutoML. If you specify an algorithm, you also
        can override algorithm-specific hyperparameters.

        Amazon Forecast uses the chosen algorithm to train a model using the latest version of the
        datasets in the specified dataset group. The result is called a predictor. You then generate
        a forecast using the  CreateForecast operation.

        After training a model, the ``CreatePredictor`` operation also evaluates it. To see the
        evaluation metrics, use the  GetAccuracyMetrics operation. Always review the evaluation
        metrics before deciding to use the predictor to generate a forecast.

        Optionally, you can specify a featurization configuration to fill and aggregate the data
        fields in the ``TARGET_TIME_SERIES`` dataset to improve model training. For more
        information, see  FeaturizationConfig .

        For RELATED_TIME_SERIES datasets, ``CreatePredictor`` verifies that the ``DataFrequency``
        specified when the dataset was created matches the ``ForecastFrequency`` .
        TARGET_TIME_SERIES datasets don't have this restriction. Amazon Forecast also verifies the
        delimiter and timestamp format. For more information, see  howitworks-datasets-groups .

         **AutoML**

        If you want Amazon Forecast to evaluate each algorithm and choose the one that minimizes the
        ``objective function`` , set ``PerformAutoML`` to ``true`` . The ``objective function`` is
        defined as the mean of the weighted p10, p50, and p90 quantile losses. For more information,
        see  EvaluationResult .

        When AutoML is enabled, the following properties are disallowed:

        * ``AlgorithmArn``

        * ``HPOConfig``

        * ``PerformHPO``

        * ``TrainingParameters``

        To get a list of all of your predictors, use the  ListPredictors operation.

        .. note::

          Before you can use the predictor to create a forecast, the ``Status`` of the predictor
          must be ``ACTIVE`` , signifying that training has completed. To get the status, use the
          DescribePredictor operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/CreatePredictor>`_

        **Request Syntax**
        ::

          response = client.create_predictor(
              PredictorName='string',
              AlgorithmArn='string',
              ForecastHorizon=123,
              PerformAutoML=True|False,
              PerformHPO=True|False,
              TrainingParameters={
                  'string': 'string'
              },
              EvaluationParameters={
                  'NumberOfBacktestWindows': 123,
                  'BackTestWindowOffset': 123
              },
              HPOConfig={
                  'ParameterRanges': {
                      'CategoricalParameterRanges': [
                          {
                              'Name': 'string',
                              'Values': [
                                  'string',
                              ]
                          },
                      ],
                      'ContinuousParameterRanges': [
                          {
                              'Name': 'string',
                              'MaxValue': 123.0,
                              'MinValue': 123.0,
                              'ScalingType': 'Auto'|'Linear'|'Logarithmic'|'ReverseLogarithmic'
                          },
                      ],
                      'IntegerParameterRanges': [
                          {
                              'Name': 'string',
                              'MaxValue': 123,
                              'MinValue': 123,
                              'ScalingType': 'Auto'|'Linear'|'Logarithmic'|'ReverseLogarithmic'
                          },
                      ]
                  }
              },
              InputDataConfig={
                  'DatasetGroupArn': 'string',
                  'SupplementaryFeatures': [
                      {
                          'Name': 'string',
                          'Value': 'string'
                      },
                  ]
              },
              FeaturizationConfig={
                  'ForecastFrequency': 'string',
                  'ForecastDimensions': [
                      'string',
                  ],
                  'Featurizations': [
                      {
                          'AttributeName': 'string',
                          'FeaturizationPipeline': [
                              {
                                  'FeaturizationMethodName': 'filling',
                                  'FeaturizationMethodParameters': {
                                      'string': 'string'
                                  }
                              },
                          ]
                      },
                  ]
              },
              EncryptionConfig={
                  'RoleArn': 'string',
                  'KMSKeyArn': 'string'
              }
          )
        :type PredictorName: string
        :param PredictorName: **[REQUIRED]**

          A name for the predictor.

        :type AlgorithmArn: string
        :param AlgorithmArn:

          The Amazon Resource Name (ARN) of the algorithm to use for model training. Required if
          ``PerformAutoML`` is not set to ``true`` .

           **Supported algorithms:**

          * ``arn:aws:forecast:::algorithm/ARIMA``

          * ``arn:aws:forecast:::algorithm/Deep_AR_Plus``   Supports hyperparameter optimization
          (HPO)

          * ``arn:aws:forecast:::algorithm/ETS``

          * ``arn:aws:forecast:::algorithm/NPTS``

          * ``arn:aws:forecast:::algorithm/Prophet``

        :type ForecastHorizon: integer
        :param ForecastHorizon: **[REQUIRED]**

          Specifies the number of time-steps that the model is trained to predict. The forecast
          horizon is also called the prediction length.

          For example, if you configure a dataset for daily data collection (using the
          ``DataFrequency`` parameter of the  CreateDataset operation) and set the forecast horizon
          to 10, the model returns predictions for 10 days.

          The maximum forecast horizon is the lesser of 500 time-steps or 1/3 of the
          TARGET_TIME_SERIES dataset length.

        :type PerformAutoML: boolean
        :param PerformAutoML:

          Whether to perform AutoML. When Amazon Forecast performs AutoML, it evaluates the
          algorithms it provides and chooses the best algorithm and configuration for your training
          dataset.

          The default value is ``false`` . In this case, you are required to specify an algorithm.

          Set ``PerformAutoML`` to ``true`` to have Amazon Forecast perform AutoML. This is a good
          option if you aren't sure which algorithm is suitable for your training data. In this
          case, ``PerformHPO`` must be false.

        :type PerformHPO: boolean
        :param PerformHPO:

          Whether to perform hyperparameter optimization (HPO). HPO finds optimal hyperparameter
          values for your training data. The process of performing HPO is known as running a
          hyperparameter tuning job.

          The default value is ``false`` . In this case, Amazon Forecast uses default hyperparameter
          values from the chosen algorithm.

          To override the default values, set ``PerformHPO`` to ``true`` and, optionally, supply the
          HyperParameterTuningJobConfig object. The tuning job specifies a metric to optimize, which
          hyperparameters participate in tuning, and the valid range for each tunable
          hyperparameter. In this case, you are required to specify an algorithm and
          ``PerformAutoML`` must be false.

          The following algorithm supports HPO:

          * DeepAR+

        :type TrainingParameters: dict
        :param TrainingParameters:

          The hyperparameters to override for model training. The hyperparameters that you can
          override are listed in the individual algorithms. For the list of supported algorithms,
          see  aws-forecast-choosing-recipes .

          - *(string) --*

            - *(string) --*

        :type EvaluationParameters: dict
        :param EvaluationParameters:

          Used to override the default evaluation parameters of the specified algorithm. Amazon
          Forecast evaluates a predictor by splitting a dataset into training data and testing data.
          The evaluation parameters define how to perform the split and the number of iterations.

          - **NumberOfBacktestWindows** *(integer) --*

            The number of times to split the input data. The default is 1. Valid values are 1
            through 5.

          - **BackTestWindowOffset** *(integer) --*

            The point from the end of the dataset where you want to split the data for model
            training and testing (evaluation). Specify the value as the number of data points. The
            default is the value of the forecast horizon. ``BackTestWindowOffset`` can be used to
            mimic a past virtual forecast start date. This value must be greater than or equal to
            the forecast horizon and less than half of the TARGET_TIME_SERIES dataset length.

             ``ForecastHorizon`` <= ``BackTestWindowOffset`` < 1/2 * TARGET_TIME_SERIES dataset
             length

        :type HPOConfig: dict
        :param HPOConfig:

          Provides hyperparameter override values for the algorithm. If you don't provide this
          parameter, Amazon Forecast uses default values. The individual algorithms specify which
          hyperparameters support hyperparameter optimization (HPO). For more information, see
          aws-forecast-choosing-recipes .

          If you included the ``HPOConfig`` object, you must set ``PerformHPO`` to true.

          - **ParameterRanges** *(dict) --*

            Specifies the ranges of valid values for the hyperparameters.

            - **CategoricalParameterRanges** *(list) --*

              Specifies the tunable range for each categorical hyperparameter.

              - *(dict) --*

                Specifies a categorical hyperparameter and it's range of tunable values. This object
                is part of the  ParameterRanges object.

                - **Name** *(string) --* **[REQUIRED]**

                  The name of the categorical hyperparameter to tune.

                - **Values** *(list) --* **[REQUIRED]**

                  A list of the tunable categories for the hyperparameter.

                  - *(string) --*

            - **ContinuousParameterRanges** *(list) --*

              Specifies the tunable range for each continuous hyperparameter.

              - *(dict) --*

                Specifies a continuous hyperparameter and it's range of tunable values. This object
                is part of the  ParameterRanges object.

                - **Name** *(string) --* **[REQUIRED]**

                  The name of the hyperparameter to tune.

                - **MaxValue** *(float) --* **[REQUIRED]**

                  The maximum tunable value of the hyperparameter.

                - **MinValue** *(float) --* **[REQUIRED]**

                  The minimum tunable value of the hyperparameter.

                - **ScalingType** *(string) --*

                  The scale that hyperparameter tuning uses to search the hyperparameter range.
                  Valid values:

                    Auto

                  Amazon Forecast hyperparameter tuning chooses the best scale for the
                  hyperparameter.

                    Linear

                  Hyperparameter tuning searches the values in the hyperparameter range by using a
                  linear scale.

                    Logarithmic

                  Hyperparameter tuning searches the values in the hyperparameter range by using a
                  logarithmic scale.

                  Logarithmic scaling works only for ranges that have values greater than 0.

                    ReverseLogarithmic

                  hyperparameter tuning searches the values in the hyperparameter range by using a
                  reverse logarithmic scale.

                  Reverse logarithmic scaling works only for ranges that are entirely within the
                  range 0 <= x < 1.0.

                  For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
                  <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
                  . One of the following values:

            - **IntegerParameterRanges** *(list) --*

              Specifies the tunable range for each integer hyperparameter.

              - *(dict) --*

                Specifies an integer hyperparameter and it's range of tunable values. This object is
                part of the  ParameterRanges object.

                - **Name** *(string) --* **[REQUIRED]**

                  The name of the hyperparameter to tune.

                - **MaxValue** *(integer) --* **[REQUIRED]**

                  The maximum tunable value of the hyperparameter.

                - **MinValue** *(integer) --* **[REQUIRED]**

                  The minimum tunable value of the hyperparameter.

                - **ScalingType** *(string) --*

                  The scale that hyperparameter tuning uses to search the hyperparameter range.
                  Valid values:

                    Auto

                  Amazon Forecast hyperparameter tuning chooses the best scale for the
                  hyperparameter.

                    Linear

                  Hyperparameter tuning searches the values in the hyperparameter range by using a
                  linear scale.

                    Logarithmic

                  Hyperparameter tuning searches the values in the hyperparameter range by using a
                  logarithmic scale.

                  Logarithmic scaling works only for ranges that have values greater than 0.

                    ReverseLogarithmic

                  Not supported for ``IntegerParameterRange`` .

                  Reverse logarithmic scaling works only for ranges that are entirely within the
                  range 0 <= x < 1.0.

                  For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
                  <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
                  . One of the following values:

        :type InputDataConfig: dict
        :param InputDataConfig: **[REQUIRED]**

          Describes the dataset group that contains the data to use to train the predictor.

          - **DatasetGroupArn** *(string) --* **[REQUIRED]**

            The Amazon Resource Name (ARN) of the dataset group.

          - **SupplementaryFeatures** *(list) --*

            An array of supplementary features. The only supported feature is a holiday calendar.

            - *(dict) --*

              Describes a supplementary feature of a dataset group. This object is part of the
              InputDataConfig object.

              The only supported feature is a holiday calendar. If you use the calendar, all data in
              the datasets should belong to the same country as the calendar. For the holiday
              calendar data, see the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web
              site.

              - **Name** *(string) --* **[REQUIRED]**

                The name of the feature. This must be "holiday".

              - **Value** *(string) --* **[REQUIRED]**

                One of the following 2 letter country codes:

                * "AU" - AUSTRALIA

                * "DE" - GERMANY

                * "JP" - JAPAN

                * "US" - UNITED_STATES

                * "UK" - UNITED_KINGDOM

        :type FeaturizationConfig: dict
        :param FeaturizationConfig: **[REQUIRED]**

          The featurization configuration.

          - **ForecastFrequency** *(string) --* **[REQUIRED]**

            The frequency of predictions in a forecast.

            Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30
            minutes), 15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute).
            For example, "Y" indicates every year and "5min" indicates every five minutes.

            The frequency must be greater than or equal to the TARGET_TIME_SERIES dataset frequency.

            When a RELATED_TIME_SERIES dataset is provided, the frequency must be equal to the
            RELATED_TIME_SERIES dataset frequency.

          - **ForecastDimensions** *(list) --*

            An array of dimension (field) names that specify how to group the generated forecast.

            For example, suppose that you are generating a forecast for item sales across all of
            your stores, and your dataset contains a ``store_id`` field. If you want the sales
            forecast for each item by store, you would specify ``store_id`` as the dimension.

            All forecast dimensions specified in the ``TARGET_TIME_SERIES`` dataset don't need to be
            specified in the ``CreatePredictor`` request. All forecast dimensions specified in the
            ``RELATED_TIME_SERIES`` dataset must be specified in the ``CreatePredictor`` request.

            - *(string) --*

          - **Featurizations** *(list) --*

            An array of featurization (transformation) information for the fields of a dataset. Only
            a single featurization is supported.

            - *(dict) --*

              Provides featurization (transformation) information for a dataset field. This object
              is part of the  FeaturizationConfig object.

              For example:

               ``{``

               ``"AttributeName": "demand",``

               ``FeaturizationPipeline [ {``

               ``"FeaturizationMethodName": "filling",``

               ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

               ``} ]``

               ``}``

              - **AttributeName** *(string) --* **[REQUIRED]**

                The name of the schema attribute that specifies the data field to be featurized.
                Only the ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported.
                For example, for the ``RETAIL`` domain, the target is ``demand`` , and for the
                ``CUSTOM`` domain, the target is ``target_value`` .

              - **FeaturizationPipeline** *(list) --*

                An array of one ``FeaturizationMethod`` object that specifies the feature
                transformation method.

                - *(dict) --*

                  Provides information about the method that featurizes (transforms) a dataset
                  field. The method is part of the ``FeaturizationPipeline`` of the  Featurization
                  object. If you don't specify ``FeaturizationMethodParameters`` , Amazon Forecast
                  uses default parameters.

                  The following is an example of how you specify a ``FeaturizationMethod`` object.

                   ``{``

                   ``"FeaturizationMethodName": "filling",``

                   ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

                   ``}``

                  - **FeaturizationMethodName** *(string) --* **[REQUIRED]**

                    The name of the method. The "filling" method is the only supported method.

                  - **FeaturizationMethodParameters** *(dict) --*

                    The method parameters (key-value pairs). Specify these parameters to override
                    the default values. The following list shows the parameters and their valid
                    values. Bold signifies the default value.

                    * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

                    * ``frontfill`` : **none**

                    * ``middlefill`` : **zero** , ``nan`` (not a number)

                    * ``backfill`` : **zero** , ``nan``

                    - *(string) --*

                      - *(string) --*

        :type EncryptionConfig: dict
        :param EncryptionConfig:

          An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM)
          role that Amazon Forecast can assume to access the key.

          - **RoleArn** *(string) --* **[REQUIRED]**

            The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

            Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
            account, you get an ``InvalidInputException`` error.

          - **KMSKeyArn** *(string) --* **[REQUIRED]**

            The Amazon Resource Name (ARN) of the KMS key.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'PredictorArn': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **PredictorArn** *(string) --*

              The Amazon Resource Name (ARN) of the predictor.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_dataset(self, DatasetArn: str) -> None:
        """
        Deletes an Amazon Forecast dataset that was created using the  CreateDataset operation. You
        can only delete datasets that have a status of ``ACTIVE`` or ``CREATE_FAILED`` . To get the
        status use the  DescribeDataset operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeleteDataset>`_

        **Request Syntax**
        ::

          response = client.delete_dataset(
              DatasetArn='string'
          )
        :type DatasetArn: string
        :param DatasetArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_dataset_group(self, DatasetGroupArn: str) -> None:
        """
        Deletes a dataset group created using the  CreateDatasetGroup operation. You can only delete
        dataset groups that have a status of ``ACTIVE`` , ``CREATE_FAILED`` , or ``UPDATE_FAILED`` .
        To get the status, use the  DescribeDatasetGroup operation.

        This operation deletes only the dataset group, not the datasets in the group.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeleteDatasetGroup>`_

        **Request Syntax**
        ::

          response = client.delete_dataset_group(
              DatasetGroupArn='string'
          )
        :type DatasetGroupArn: string
        :param DatasetGroupArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset group to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_dataset_import_job(self, DatasetImportJobArn: str) -> None:
        """
        Deletes a dataset import job created using the  CreateDatasetImportJob operation. You can
        delete only dataset import jobs that have a status of ``ACTIVE`` or ``CREATE_FAILED`` . To
        get the status, use the  DescribeDatasetImportJob operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeleteDatasetImportJob>`_

        **Request Syntax**
        ::

          response = client.delete_dataset_import_job(
              DatasetImportJobArn='string'
          )
        :type DatasetImportJobArn: string
        :param DatasetImportJobArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset import job to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_forecast(self, ForecastArn: str) -> None:
        """
        Deletes a forecast created using the  CreateForecast operation. You can delete only
        forecasts that have a status of ``ACTIVE`` or ``CREATE_FAILED`` . To get the status, use the
        DescribeForecast operation.

        You can't delete a forecast while it is being exported. After a forecast is deleted, you can
        no longer query the forecast.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeleteForecast>`_

        **Request Syntax**
        ::

          response = client.delete_forecast(
              ForecastArn='string'
          )
        :type ForecastArn: string
        :param ForecastArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the forecast to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_forecast_export_job(self, ForecastExportJobArn: str) -> None:
        """
        Deletes a forecast export job created using the  CreateForecastExportJob operation. You can
        delete only export jobs that have a status of ``ACTIVE`` or ``CREATE_FAILED`` . To get the
        status, use the  DescribeForecastExportJob operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeleteForecastExportJob>`_

        **Request Syntax**
        ::

          response = client.delete_forecast_export_job(
              ForecastExportJobArn='string'
          )
        :type ForecastExportJobArn: string
        :param ForecastExportJobArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the forecast export job to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_predictor(self, PredictorArn: str) -> None:
        """
        Deletes a predictor created using the  CreatePredictor operation. You can delete only
        predictor that have a status of ``ACTIVE`` or ``CREATE_FAILED`` . To get the status, use the
        DescribePredictor operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DeletePredictor>`_

        **Request Syntax**
        ::

          response = client.delete_predictor(
              PredictorArn='string'
          )
        :type PredictorArn: string
        :param PredictorArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the predictor to delete.

        :returns: None
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_dataset(self, DatasetArn: str) -> ClientDescribeDatasetResponseTypeDef:
        """
        Describes an Amazon Forecast dataset created using the  CreateDataset operation.

        In addition to listing the parameters specified in the ``CreateDataset`` request, this
        operation includes the following dataset properties:

        * ``CreationTime``

        * ``LastModificationTime``

        * ``Status``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribeDataset>`_

        **Request Syntax**
        ::

          response = client.describe_dataset(
              DatasetArn='string'
          )
        :type DatasetArn: string
        :param DatasetArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetArn': 'string',
                'DatasetName': 'string',
                'Domain':
                'RETAIL'|'CUSTOM'|'INVENTORY_PLANNING'|'EC2_CAPACITY'|'WORK_FORCE'
                |'WEB_TRAFFIC'|'METRICS',
                'DatasetType': 'TARGET_TIME_SERIES'|'RELATED_TIME_SERIES'|'ITEM_METADATA',
                'DataFrequency': 'string',
                'Schema': {
                    'Attributes': [
                        {
                            'AttributeName': 'string',
                            'AttributeType': 'string'|'integer'|'float'|'timestamp'
                        },
                    ]
                },
                'EncryptionConfig': {
                    'RoleArn': 'string',
                    'KMSKeyArn': 'string'
                },
                'Status': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetArn** *(string) --*

              The Amazon Resource Name (ARN) of the dataset.

            - **DatasetName** *(string) --*

              The name of the dataset.

            - **Domain** *(string) --*

              The domain associated with the dataset.

            - **DatasetType** *(string) --*

              The dataset type.

            - **DataFrequency** *(string) --*

              The frequency of data collection.

              Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30
              minutes), 15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1
              minute). For example, "M" indicates every month and "30min" indicates every 30
              minutes.

            - **Schema** *(dict) --*

              An array of ``SchemaAttribute`` objects that specify the dataset fields. Each
              ``SchemaAttribute`` specifies the name and data type of a field.

              - **Attributes** *(list) --*

                An array of attributes specifying the name and type of each field in a dataset.

                - *(dict) --*

                  An attribute of a schema, which defines a dataset field. A schema attribute is
                  required for every field in a dataset. The  Schema object contains an array of
                  ``SchemaAttribute`` objects.

                  - **AttributeName** *(string) --*

                    The name of the dataset field.

                  - **AttributeType** *(string) --*

                    The data type of the field.

            - **EncryptionConfig** *(dict) --*

              The AWS Key Management Service (KMS) key and the AWS Identity and Access Management
              (IAM) role that Amazon Forecast can assume to access the key.

              - **RoleArn** *(string) --*

                The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

                Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
                your account, you get an ``InvalidInputException`` error.

              - **KMSKeyArn** *(string) --*

                The Amazon Resource Name (ARN) of the KMS key.

            - **Status** *(string) --*

              The status of the dataset. States include:

              * ``ACTIVE``

              * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

              * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

              * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

              The ``UPDATE`` states apply while data is imported to the dataset from a call to the
              CreateDatasetImportJob operation and reflect the status of the dataset import job. For
              example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of the
              dataset is ``UPDATE_IN_PROGRESS`` .

              .. note::

                The ``Status`` of the dataset must be ``ACTIVE`` before you can import training
                data.

            - **CreationTime** *(datetime) --*

              When the dataset was created.

            - **LastModificationTime** *(datetime) --*

              When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` .
              While data is being imported to the dataset, ``LastModificationTime`` is the current
              time of the ``DescribeDataset`` call. After a  CreateDatasetImportJob operation has
              finished, ``LastModificationTime`` is when the import job completed or failed.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_dataset_group(
        self, DatasetGroupArn: str
    ) -> ClientDescribeDatasetGroupResponseTypeDef:
        """
        Describes a dataset group created using the  CreateDatasetGroup operation.

        In addition to listing the parameters provided in the ``CreateDatasetGroup`` request, this
        operation includes the following properties:

        * ``DatasetArns`` - The datasets belonging to the group.

        * ``CreationTime``

        * ``LastModificationTime``

        * ``Status``

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribeDatasetGroup>`_

        **Request Syntax**
        ::

          response = client.describe_dataset_group(
              DatasetGroupArn='string'
          )
        :type DatasetGroupArn: string
        :param DatasetGroupArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset group.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetGroupName': 'string',
                'DatasetGroupArn': 'string',
                'DatasetArns': [
                    'string',
                ],
                'Domain':
                'RETAIL'|'CUSTOM'|'INVENTORY_PLANNING'|'EC2_CAPACITY'|'WORK_FORCE'
                |'WEB_TRAFFIC'|'METRICS',
                'Status': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetGroupName** *(string) --*

              The name of the dataset group.

            - **DatasetGroupArn** *(string) --*

              The ARN of the dataset group.

            - **DatasetArns** *(list) --*

              An array of Amazon Resource Names (ARNs) of the datasets contained in the dataset
              group.

              - *(string) --*

            - **Domain** *(string) --*

              The domain associated with the dataset group.

            - **Status** *(string) --*

              The status of the dataset group. States include:

              * ``ACTIVE``

              * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

              * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

              * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

              The ``UPDATE`` states apply when you call the  UpdateDatasetGroup operation.

              .. note::

                The ``Status`` of the dataset group must be ``ACTIVE`` before you can use the
                dataset group to create a predictor.

            - **CreationTime** *(datetime) --*

              When the dataset group was created.

            - **LastModificationTime** *(datetime) --*

              When the dataset group was created or last updated from a call to the
              UpdateDatasetGroup operation. While the dataset group is being updated,
              ``LastModificationTime`` is the current time of the ``DescribeDatasetGroup`` call.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_dataset_import_job(
        self, DatasetImportJobArn: str
    ) -> ClientDescribeDatasetImportJobResponseTypeDef:
        """
        Describes a dataset import job created using the  CreateDatasetImportJob operation.

        In addition to listing the parameters provided in the ``CreateDatasetImportJob`` request,
        this operation includes the following properties:

        * ``CreationTime``

        * ``LastModificationTime``

        * ``DataSize``

        * ``FieldStatistics``

        * ``Status``

        * ``Message`` - If an error occurred, information about the error.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribeDatasetImportJob>`_

        **Request Syntax**
        ::

          response = client.describe_dataset_import_job(
              DatasetImportJobArn='string'
          )
        :type DatasetImportJobArn: string
        :param DatasetImportJobArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the dataset import job.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DatasetImportJobName': 'string',
                'DatasetImportJobArn': 'string',
                'DatasetArn': 'string',
                'TimestampFormat': 'string',
                'DataSource': {
                    'S3Config': {
                        'Path': 'string',
                        'RoleArn': 'string',
                        'KMSKeyArn': 'string'
                    }
                },
                'FieldStatistics': {
                    'string': {
                        'Count': 123,
                        'CountDistinct': 123,
                        'CountNull': 123,
                        'CountNan': 123,
                        'Min': 'string',
                        'Max': 'string',
                        'Avg': 123.0,
                        'Stddev': 123.0
                    }
                },
                'DataSize': 123.0,
                'Status': 'string',
                'Message': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **DatasetImportJobName** *(string) --*

              The name of the dataset import job.

            - **DatasetImportJobArn** *(string) --*

              The ARN of the dataset import job.

            - **DatasetArn** *(string) --*

              The Amazon Resource Name (ARN) of the dataset that the training data was imported to.

            - **TimestampFormat** *(string) --*

              The format of timestamps in the dataset. The format that you specify depends on the
              ``DataFrequency`` specified when the dataset was created. The following formats are
              supported

              * "yyyy-MM-dd" For the following data frequencies: Y, M, W, and D

              * "yyyy-MM-dd HH:mm:ss" For the following data frequencies: H, 30min, 15min, and 1min;
              and optionally, for: Y, M, W, and D

            - **DataSource** *(dict) --*

              The location of the training data to import and an AWS Identity and Access Management
              (IAM) role that Amazon Forecast can assume to access the data.

              If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS)
              key.

              - **S3Config** *(dict) --*

                The path to the training data stored in an Amazon Simple Storage Service (Amazon S3)
                bucket along with the credentials to access the data.

                - **Path** *(string) --*

                  The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
                  Amazon S3 bucket.

                - **RoleArn** *(string) --*

                  The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast
                  can assume to access the Amazon S3 bucket or files. If you provide a value for the
                  ``KMSKeyArn`` key, the role must allow access to the key.

                  Passing a role across AWS accounts is not allowed. If you pass a role that isn't
                  in your account, you get an ``InvalidInputException`` error.

                - **KMSKeyArn** *(string) --*

                  The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

            - **FieldStatistics** *(dict) --*

              Statistical information about each field in the input data.

              - *(string) --*

                - *(dict) --*

                  Provides statistics for each data field imported into to an Amazon Forecast
                  dataset with the  CreateDatasetImportJob operation.

                  - **Count** *(integer) --*

                    The number of values in the field.

                  - **CountDistinct** *(integer) --*

                    The number of distinct values in the field.

                  - **CountNull** *(integer) --*

                    The number of null values in the field.

                  - **CountNan** *(integer) --*

                    The number of NAN (not a number) values in the field.

                  - **Min** *(string) --*

                    For a numeric field, the minimum value in the field.

                  - **Max** *(string) --*

                    For a numeric field, the maximum value in the field.

                  - **Avg** *(float) --*

                    For a numeric field, the average value in the field.

                  - **Stddev** *(float) --*

                    For a numeric field, the standard deviation.

            - **DataSize** *(float) --*

              The size of the dataset in gigabytes (GB) after the import job has finished.

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_forecast(self, ForecastArn: str) -> ClientDescribeForecastResponseTypeDef:
        """
        Describes a forecast created using the  CreateForecast operation.

        In addition to listing the properties provided in the ``CreateForecast`` request, this
        operation lists the following properties:

        * ``DatasetGroupArn`` - The dataset group that provided the training data.

        * ``CreationTime``

        * ``LastModificationTime``

        * ``Status``

        * ``Message`` - If an error occurred, information about the error.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribeForecast>`_

        **Request Syntax**
        ::

          response = client.describe_forecast(
              ForecastArn='string'
          )
        :type ForecastArn: string
        :param ForecastArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the forecast.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ForecastArn': 'string',
                'ForecastName': 'string',
                'ForecastTypes': [
                    'string',
                ],
                'PredictorArn': 'string',
                'DatasetGroupArn': 'string',
                'Status': 'string',
                'Message': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **ForecastArn** *(string) --*

              The forecast ARN as specified in the request.

            - **ForecastName** *(string) --*

              The name of the forecast.

            - **ForecastTypes** *(list) --*

              The quantiles at which proababilistic forecasts were generated.

              - *(string) --*

            - **PredictorArn** *(string) --*

              The ARN of the predictor used to generate the forecast.

            - **DatasetGroupArn** *(string) --*

              The ARN of the dataset group that provided the data used to train the predictor.

            - **Status** *(string) --*

              The status of the forecast. States include:

              * ``ACTIVE``

              * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

              * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

              .. note::

                The ``Status`` of the forecast must be ``ACTIVE`` before you can query or export the
                forecast.

            - **Message** *(string) --*

              If an error occurred, an informational message about the error.

            - **CreationTime** *(datetime) --*

              When the forecast creation task was created.

            - **LastModificationTime** *(datetime) --*

              Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated when
              inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ),
              and when inference is complete (status changed to ``ACTIVE`` ) or fails (status
              changed to ``CREATE_FAILED`` ).

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_forecast_export_job(
        self, ForecastExportJobArn: str
    ) -> ClientDescribeForecastExportJobResponseTypeDef:
        """
        Describes a forecast export job created using the  CreateForecastExportJob operation.

        In addition to listing the properties provided by the user in the
        ``CreateForecastExportJob`` request, this operation lists the following properties:

        * ``CreationTime``

        * ``LastModificationTime``

        * ``Status``

        * ``Message`` - If an error occurred, information about the error.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribeForecastExportJob>`_

        **Request Syntax**
        ::

          response = client.describe_forecast_export_job(
              ForecastExportJobArn='string'
          )
        :type ForecastExportJobArn: string
        :param ForecastExportJobArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the forecast export job.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ForecastExportJobArn': 'string',
                'ForecastExportJobName': 'string',
                'ForecastArn': 'string',
                'Destination': {
                    'S3Config': {
                        'Path': 'string',
                        'RoleArn': 'string',
                        'KMSKeyArn': 'string'
                    }
                },
                'Message': 'string',
                'Status': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **ForecastExportJobArn** *(string) --*

              The ARN of the forecast export job.

            - **ForecastExportJobName** *(string) --*

              The name of the forecast export job.

            - **ForecastArn** *(string) --*

              The Amazon Resource Name (ARN) of the exported forecast.

            - **Destination** *(dict) --*

              The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is
              exported.

              - **S3Config** *(dict) --*

                The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the
                credentials to access the bucket.

                - **Path** *(string) --*

                  The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
                  Amazon S3 bucket.

                - **RoleArn** *(string) --*

                  The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast
                  can assume to access the Amazon S3 bucket or files. If you provide a value for the
                  ``KMSKeyArn`` key, the role must allow access to the key.

                  Passing a role across AWS accounts is not allowed. If you pass a role that isn't
                  in your account, you get an ``InvalidInputException`` error.

                - **KMSKeyArn** *(string) --*

                  The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

            - **Message** *(string) --*

              If an error occurred, an informational message about the error.

            - **Status** *(string) --*

              The status of the forecast export job. States include:

              * ``ACTIVE``

              * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

              * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

              .. note::

                The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access
                the forecast in your S3 bucket.

            - **CreationTime** *(datetime) --*

              When the forecast export job was created.

            - **LastModificationTime** *(datetime) --*

              When the last successful export job finished.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_predictor(self, PredictorArn: str) -> ClientDescribePredictorResponseTypeDef:
        """
        Describes a predictor created using the  CreatePredictor operation.

        In addition to listing the properties provided in the ``CreatePredictor`` request, this
        operation lists the following properties:

        * ``DatasetImportJobArns`` - The dataset import jobs used to import training data.

        * ``AutoMLAlgorithmArns`` - If AutoML is performed, the algorithms that were evaluated.

        * ``CreationTime``

        * ``LastModificationTime``

        * ``Status``

        * ``Message`` - If an error occurred, information about the error.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/DescribePredictor>`_

        **Request Syntax**
        ::

          response = client.describe_predictor(
              PredictorArn='string'
          )
        :type PredictorArn: string
        :param PredictorArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the predictor that you want information about.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'PredictorArn': 'string',
                'PredictorName': 'string',
                'AlgorithmArn': 'string',
                'ForecastHorizon': 123,
                'PerformAutoML': True|False,
                'PerformHPO': True|False,
                'TrainingParameters': {
                    'string': 'string'
                },
                'EvaluationParameters': {
                    'NumberOfBacktestWindows': 123,
                    'BackTestWindowOffset': 123
                },
                'HPOConfig': {
                    'ParameterRanges': {
                        'CategoricalParameterRanges': [
                            {
                                'Name': 'string',
                                'Values': [
                                    'string',
                                ]
                            },
                        ],
                        'ContinuousParameterRanges': [
                            {
                                'Name': 'string',
                                'MaxValue': 123.0,
                                'MinValue': 123.0,
                                'ScalingType': 'Auto'|'Linear'|'Logarithmic'|'ReverseLogarithmic'
                            },
                        ],
                        'IntegerParameterRanges': [
                            {
                                'Name': 'string',
                                'MaxValue': 123,
                                'MinValue': 123,
                                'ScalingType': 'Auto'|'Linear'|'Logarithmic'|'ReverseLogarithmic'
                            },
                        ]
                    }
                },
                'InputDataConfig': {
                    'DatasetGroupArn': 'string',
                    'SupplementaryFeatures': [
                        {
                            'Name': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                'FeaturizationConfig': {
                    'ForecastFrequency': 'string',
                    'ForecastDimensions': [
                        'string',
                    ],
                    'Featurizations': [
                        {
                            'AttributeName': 'string',
                            'FeaturizationPipeline': [
                                {
                                    'FeaturizationMethodName': 'filling',
                                    'FeaturizationMethodParameters': {
                                        'string': 'string'
                                    }
                                },
                            ]
                        },
                    ]
                },
                'EncryptionConfig': {
                    'RoleArn': 'string',
                    'KMSKeyArn': 'string'
                },
                'PredictorExecutionDetails': {
                    'PredictorExecutions': [
                        {
                            'AlgorithmArn': 'string',
                            'TestWindows': [
                                {
                                    'TestWindowStart': datetime(2015, 1, 1),
                                    'TestWindowEnd': datetime(2015, 1, 1),
                                    'Status': 'string',
                                    'Message': 'string'
                                },
                            ]
                        },
                    ]
                },
                'DatasetImportJobArns': [
                    'string',
                ],
                'AutoMLAlgorithmArns': [
                    'string',
                ],
                'Status': 'string',
                'Message': 'string',
                'CreationTime': datetime(2015, 1, 1),
                'LastModificationTime': datetime(2015, 1, 1)
            }
          **Response Structure**

          - *(dict) --*

            - **PredictorArn** *(string) --*

              The ARN of the predictor.

            - **PredictorName** *(string) --*

              The name of the predictor.

            - **AlgorithmArn** *(string) --*

              The Amazon Resource Name (ARN) of the algorithm used for model training.

            - **ForecastHorizon** *(integer) --*

              The number of time-steps of the forecast. The forecast horizon is also called the
              prediction length.

            - **PerformAutoML** *(boolean) --*

              Whether the predictor is set to perform AutoML.

            - **PerformHPO** *(boolean) --*

              Whether the predictor is set to perform hyperparameter optimization (HPO).

            - **TrainingParameters** *(dict) --*

              The default training parameters or overrides selected during model training. If using
              the AutoML algorithm or if HPO is turned on while using the DeepAR+ algorithms, the
              optimized values for the chosen hyperparameters are returned. For more information,
              see  aws-forecast-choosing-recipes .

              - *(string) --*

                - *(string) --*

            - **EvaluationParameters** *(dict) --*

              Used to override the default evaluation parameters of the specified algorithm. Amazon
              Forecast evaluates a predictor by splitting a dataset into training data and testing
              data. The evaluation parameters define how to perform the split and the number of
              iterations.

              - **NumberOfBacktestWindows** *(integer) --*

                The number of times to split the input data. The default is 1. Valid values are 1
                through 5.

              - **BackTestWindowOffset** *(integer) --*

                The point from the end of the dataset where you want to split the data for model
                training and testing (evaluation). Specify the value as the number of data points.
                The default is the value of the forecast horizon. ``BackTestWindowOffset`` can be
                used to mimic a past virtual forecast start date. This value must be greater than or
                equal to the forecast horizon and less than half of the TARGET_TIME_SERIES dataset
                length.

                 ``ForecastHorizon`` <=
                      ``BackTestWindowOffset`` < 1/2 * TARGET_TIME_SERIES dataset
                 length

            - **HPOConfig** *(dict) --*

              The hyperparameter override values for the algorithm.

              - **ParameterRanges** *(dict) --*

                Specifies the ranges of valid values for the hyperparameters.

                - **CategoricalParameterRanges** *(list) --*

                  Specifies the tunable range for each categorical hyperparameter.

                  - *(dict) --*

                    Specifies a categorical hyperparameter and it's range of tunable values. This
                    object is part of the  ParameterRanges object.

                    - **Name** *(string) --*

                      The name of the categorical hyperparameter to tune.

                    - **Values** *(list) --*

                      A list of the tunable categories for the hyperparameter.

                      - *(string) --*

                - **ContinuousParameterRanges** *(list) --*

                  Specifies the tunable range for each continuous hyperparameter.

                  - *(dict) --*

                    Specifies a continuous hyperparameter and it's range of tunable values. This
                    object is part of the  ParameterRanges object.

                    - **Name** *(string) --*

                      The name of the hyperparameter to tune.

                    - **MaxValue** *(float) --*

                      The maximum tunable value of the hyperparameter.

                    - **MinValue** *(float) --*

                      The minimum tunable value of the hyperparameter.

                    - **ScalingType** *(string) --*

                      The scale that hyperparameter tuning uses to search the hyperparameter range.
                      Valid values:

                        Auto

                      Amazon Forecast hyperparameter tuning chooses the best scale for the
                      hyperparameter.

                        Linear

                      Hyperparameter tuning searches the values in the hyperparameter range by using
                      a linear scale.

                        Logarithmic

                      Hyperparameter tuning searches the values in the hyperparameter range by using
                      a logarithmic scale.

                      Logarithmic scaling works only for ranges that have values greater than 0.

                        ReverseLogarithmic

                      hyperparameter tuning searches the values in the hyperparameter range by using
                      a reverse logarithmic scale.

                      Reverse logarithmic scaling works only for ranges that are entirely within the
                      range 0 <= x < 1.0.

                      For information about choosing a hyperparameter scale, see `Hyperparameter
                      Scaling
                      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
                      . One of the following values:

                - **IntegerParameterRanges** *(list) --*

                  Specifies the tunable range for each integer hyperparameter.

                  - *(dict) --*

                    Specifies an integer hyperparameter and it's range of tunable values. This
                    object is part of the  ParameterRanges object.

                    - **Name** *(string) --*

                      The name of the hyperparameter to tune.

                    - **MaxValue** *(integer) --*

                      The maximum tunable value of the hyperparameter.

                    - **MinValue** *(integer) --*

                      The minimum tunable value of the hyperparameter.

                    - **ScalingType** *(string) --*

                      The scale that hyperparameter tuning uses to search the hyperparameter range.
                      Valid values:

                        Auto

                      Amazon Forecast hyperparameter tuning chooses the best scale for the
                      hyperparameter.

                        Linear

                      Hyperparameter tuning searches the values in the hyperparameter range by using
                      a linear scale.

                        Logarithmic

                      Hyperparameter tuning searches the values in the hyperparameter range by using
                      a logarithmic scale.

                      Logarithmic scaling works only for ranges that have values greater than 0.

                        ReverseLogarithmic

                      Not supported for ``IntegerParameterRange`` .

                      Reverse logarithmic scaling works only for ranges that are entirely within the
                      range 0 <= x < 1.0.

                      For information about choosing a hyperparameter scale, see `Hyperparameter
                      Scaling
                      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
                      . One of the following values:

            - **InputDataConfig** *(dict) --*

              Describes the dataset group that contains the data to use to train the predictor.

              - **DatasetGroupArn** *(string) --*

                The Amazon Resource Name (ARN) of the dataset group.

              - **SupplementaryFeatures** *(list) --*

                An array of supplementary features. The only supported feature is a holiday
                calendar.

                - *(dict) --*

                  Describes a supplementary feature of a dataset group. This object is part of the
                  InputDataConfig object.

                  The only supported feature is a holiday calendar. If you use the calendar, all
                  data in the datasets should belong to the same country as the calendar. For the
                  holiday calendar data, see the `Jollyday
                  <http://jollyday.sourceforge.net/data.html>`__ web site.

                  - **Name** *(string) --*

                    The name of the feature. This must be "holiday".

                  - **Value** *(string) --*

                    One of the following 2 letter country codes:

                    * "AU" - AUSTRALIA

                    * "DE" - GERMANY

                    * "JP" - JAPAN

                    * "US" - UNITED_STATES

                    * "UK" - UNITED_KINGDOM

            - **FeaturizationConfig** *(dict) --*

              The featurization configuration.

              - **ForecastFrequency** *(string) --*

                The frequency of predictions in a forecast.

                Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30
                minutes), 15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1
                minute). For example, "Y" indicates every year and "5min" indicates every five
                minutes.

                The frequency must be greater than or equal to the TARGET_TIME_SERIES dataset
                frequency.

                When a RELATED_TIME_SERIES dataset is provided, the frequency must be equal to the
                RELATED_TIME_SERIES dataset frequency.

              - **ForecastDimensions** *(list) --*

                An array of dimension (field) names that specify how to group the generated
                forecast.

                For example, suppose that you are generating a forecast for item sales across all of
                your stores, and your dataset contains a ``store_id`` field. If you want the sales
                forecast for each item by store, you would specify ``store_id`` as the dimension.

                All forecast dimensions specified in the ``TARGET_TIME_SERIES`` dataset don't need
                to be specified in the ``CreatePredictor`` request. All forecast dimensions
                specified in the ``RELATED_TIME_SERIES`` dataset must be specified in the
                ``CreatePredictor`` request.

                - *(string) --*

              - **Featurizations** *(list) --*

                An array of featurization (transformation) information for the fields of a dataset.
                Only a single featurization is supported.

                - *(dict) --*

                  Provides featurization (transformation) information for a dataset field. This
                  object is part of the  FeaturizationConfig object.

                  For example:

                   ``{``

                   ``"AttributeName": "demand",``

                   ``FeaturizationPipeline [ {``

                   ``"FeaturizationMethodName": "filling",``

                   ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

                   ``} ]``

                   ``}``

                  - **AttributeName** *(string) --*

                    The name of the schema attribute that specifies the data field to be featurized.
                    Only the ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is
                    supported. For example, for the ``RETAIL`` domain, the target is ``demand`` ,
                    and for the ``CUSTOM`` domain, the target is ``target_value`` .

                  - **FeaturizationPipeline** *(list) --*

                    An array of one ``FeaturizationMethod`` object that specifies the feature
                    transformation method.

                    - *(dict) --*

                      Provides information about the method that featurizes (transforms) a dataset
                      field. The method is part of the ``FeaturizationPipeline`` of the
                      Featurization object. If you don't specify ``FeaturizationMethodParameters`` ,
                      Amazon Forecast uses default parameters.

                      The following is an example of how you specify a ``FeaturizationMethod``
                      object.

                       ``{``

                       ``"FeaturizationMethodName": "filling",``

                       ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill":
                       "nan"}``

                       ``}``

                      - **FeaturizationMethodName** *(string) --*

                        The name of the method. The "filling" method is the only supported method.

                      - **FeaturizationMethodParameters** *(dict) --*

                        The method parameters (key-value pairs). Specify these parameters to
                        override the default values. The following list shows the parameters and
                        their valid values. Bold signifies the default value.

                        * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

                        * ``frontfill`` : **none**

                        * ``middlefill`` : **zero** , ``nan`` (not a number)

                        * ``backfill`` : **zero** , ``nan``

                        - *(string) --*

                          - *(string) --*

            - **EncryptionConfig** *(dict) --*

              An AWS Key Management Service (KMS) key and the AWS Identity and Access Management
              (IAM) role that Amazon Forecast can assume to access the key.

              - **RoleArn** *(string) --*

                The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

                Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
                your account, you get an ``InvalidInputException`` error.

              - **KMSKeyArn** *(string) --*

                The Amazon Resource Name (ARN) of the KMS key.

            - **PredictorExecutionDetails** *(dict) --*

              Details on the the status and results of the backtests performed to evaluate the
              accuracy of the predictor. You specify the number of backtests to perform when you
              call the operation.

              - **PredictorExecutions** *(list) --*

                An array of the backtests performed to evaluate the accuracy of the predictor
                against a particular algorithm. The ``NumberOfBacktestWindows`` from the object
                determines the number of windows in the array.

                - *(dict) --*

                  The algorithm used to perform a backtest and the status of those tests.

                  - **AlgorithmArn** *(string) --*

                    The ARN of the algorithm used to test the predictor.

                  - **TestWindows** *(list) --*

                    An array of test windows used to evaluate the algorithm. The
                    ``NumberOfBacktestWindows`` from the object determines the number of windows in
                    the array.

                    - *(dict) --*

                      The status, start time, and end time of a backtest, as well as a failure
                      reason if applicable.

                      - **TestWindowStart** *(datetime) --*

                        The time at which the test began.

                      - **TestWindowEnd** *(datetime) --*

                        The time at which the test ended.

                      - **Status** *(string) --*

                        The status of the test. Possible status values are:

                        * ``ACTIVE``

                        * ``CREATE_IN_PROGRESS``

                        * ``CREATE_FAILED``

                      - **Message** *(string) --*

                        If the test failed, the reason why it failed.

            - **DatasetImportJobArns** *(list) --*

              An array of the ARNs of the dataset import jobs used to import training data for the
              predictor.

              - *(string) --*

            - **AutoMLAlgorithmArns** *(list) --*

              When ``PerformAutoML`` is specified, the ARN of the chosen algorithm.

              - *(string) --*

            - **Status** *(string) --*

              The status of the predictor. States include:

              * ``ACTIVE``

              * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

              * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

              * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

              .. note::

                The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor
                to create a forecast.

            - **Message** *(string) --*

              If an error occurred, an informational message about the error.

            - **CreationTime** *(datetime) --*

              When the model training task was created.

            - **LastModificationTime** *(datetime) --*

              Initially, the same as ``CreationTime`` (when the status is ``CREATE_PENDING`` ). This
              value is updated when training starts (when the status changes to
              ``CREATE_IN_PROGRESS`` ), and when training has completed (when the status changes to
              ``ACTIVE`` ) or fails (when the status changes to ``CREATE_FAILED`` ).

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
    def get_accuracy_metrics(self, PredictorArn: str) -> ClientGetAccuracyMetricsResponseTypeDef:
        """
        Provides metrics on the accuracy of the models that were trained by the  CreatePredictor
        operation. Use metrics to see how well the model performed and to decide whether to use the
        predictor to generate a forecast. For more information, see  metrics .

        This operation generates metrics for each backtest window that was evaluated. The number of
        backtest windows (``NumberOfBacktestWindows`` ) is specified using the  EvaluationParameters
        object, which is optionally included in the ``CreatePredictor`` request. If
        ``NumberOfBacktestWindows`` isn't specified, the number defaults to one.

        The parameters of the ``filling`` method determine which items contribute to the metrics. If
        you want all items to contribute, specify ``zero`` . If you want only those items that have
        complete data in the range being evaluated to contribute, specify ``nan`` . For more
        information, see  FeaturizationMethod .

        .. note::

          Before you can get accuracy metrics, the ``Status`` of the predictor must be ``ACTIVE`` ,
          signifying that training has completed. To get the status, use the  DescribePredictor
          operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/GetAccuracyMetrics>`_

        **Request Syntax**
        ::

          response = client.get_accuracy_metrics(
              PredictorArn='string'
          )
        :type PredictorArn: string
        :param PredictorArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the predictor to get metrics for.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'PredictorEvaluationResults': [
                    {
                        'AlgorithmArn': 'string',
                        'TestWindows': [
                            {
                                'TestWindowStart': datetime(2015, 1, 1),
                                'TestWindowEnd': datetime(2015, 1, 1),
                                'ItemCount': 123,
                                'EvaluationType': 'SUMMARY'|'COMPUTED',
                                'Metrics': {
                                    'RMSE': 123.0,
                                    'WeightedQuantileLosses': [
                                        {
                                            'Quantile': 123.0,
                                            'LossValue': 123.0
                                        },
                                    ]
                                }
                            },
                        ]
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **PredictorEvaluationResults** *(list) --*

              An array of results from evaluating the predictor.

              - *(dict) --*

                The results of evaluating an algorithm. Returned as part of the  GetAccuracyMetrics
                response.

                - **AlgorithmArn** *(string) --*

                  The Amazon Resource Name (ARN) of the algorithm that was evaluated.

                - **TestWindows** *(list) --*

                  The array of test windows used for evaluating the algorithm. The
                  ``NumberOfBacktestWindows`` from the  EvaluationParameters object determines the
                  number of windows in the array.

                  - *(dict) --*

                    The metrics for a time range within the evaluation portion of a dataset. This
                    object is part of the  EvaluationResult object.

                    The ``TestWindowStart`` and ``TestWindowEnd`` parameters are determined by the
                    ``BackTestWindowOffset`` parameter of the  EvaluationParameters object.

                    - **TestWindowStart** *(datetime) --*

                      The timestamp that defines the start of the window.

                    - **TestWindowEnd** *(datetime) --*

                      The timestamp that defines the end of the window.

                    - **ItemCount** *(integer) --*

                      The number of data points within the window.

                    - **EvaluationType** *(string) --*

                      The type of evaluation.

                      * ``SUMMARY`` - The average metrics across all windows.

                      * ``COMPUTED`` - The metrics for the specified window.

                    - **Metrics** *(dict) --*

                      Provides metrics used to evaluate the performance of a predictor.

                      - **RMSE** *(float) --*

                        The root mean square error (RMSE).

                      - **WeightedQuantileLosses** *(list) --*

                        An array of weighted quantile losses. Quantiles divide a probability
                        distribution into regions of equal probability. The distribution in this
                        case is the loss function.

                        - *(dict) --*

                          The weighted loss value for a quantile. This object is part of the
                          Metrics object.

                          - **Quantile** *(float) --*

                            The quantile. Quantiles divide a probability distribution into regions
                            of equal probability. For example, if the distribution was divided into
                            5 regions of equal probability, the quantiles would be 0.2, 0.4, 0.6,
                            and 0.8.

                          - **LossValue** *(float) --*

                            The difference between the predicted value and the actual value over the
                            quantile, weighted (normalized) by dividing by the sum over all
                            quantiles.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_dataset_groups(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDatasetGroupsResponseTypeDef:
        """
        Returns a list of dataset groups created using the  CreateDatasetGroup operation. For each
        dataset group, this operation returns a summary of its properties, including its Amazon
        Resource Name (ARN). You can retrieve the complete set of properties by using the dataset
        group ARN with the  DescribeDatasetGroup operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasetGroups>`_

        **Request Syntax**
        ::

          response = client.list_dataset_groups(
              NextToken='string',
              MaxResults=123
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_dataset_import_jobs(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[ClientListDatasetImportJobsFiltersTypeDef] = None,
    ) -> ClientListDatasetImportJobsResponseTypeDef:
        """
        Returns a list of dataset import jobs created using the  CreateDatasetImportJob operation.
        For each import job, this operation returns a summary of its properties, including its
        Amazon Resource Name (ARN). You can retrieve the complete set of properties by using the ARN
        with the  DescribeDatasetImportJob operation. You can filter the list by providing an array
        of  Filter objects.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasetImportJobs>`_

        **Request Syntax**
        ::

          response = client.list_dataset_import_jobs(
              NextToken='string',
              MaxResults=123,
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ]
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_datasets(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ClientListDatasetsResponseTypeDef:
        """
        Returns a list of datasets created using the  CreateDataset operation. For each dataset, a
        summary of its properties, including its Amazon Resource Name (ARN), is returned. To
        retrieve the complete set of properties, use the ARN with the  DescribeDataset operation.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListDatasets>`_

        **Request Syntax**
        ::

          response = client.list_datasets(
              NextToken='string',
              MaxResults=123
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_forecast_export_jobs(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[ClientListForecastExportJobsFiltersTypeDef] = None,
    ) -> ClientListForecastExportJobsResponseTypeDef:
        """
        Returns a list of forecast export jobs created using the  CreateForecastExportJob operation.
        For each forecast export job, this operation returns a summary of its properties, including
        its Amazon Resource Name (ARN). To retrieve the complete set of properties, use the ARN with
        the  DescribeForecastExportJob operation. You can filter the list using an array of  Filter
        objects.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListForecastExportJobs>`_

        **Request Syntax**
        ::

          response = client.list_forecast_export_jobs(
              NextToken='string',
              MaxResults=123,
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ]
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_forecasts(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[ClientListForecastsFiltersTypeDef] = None,
    ) -> ClientListForecastsResponseTypeDef:
        """
        Returns a list of forecasts created using the  CreateForecast operation. For each forecast,
        this operation returns a summary of its properties, including its Amazon Resource Name
        (ARN). To retrieve the complete set of properties, specify the ARN with the
        DescribeForecast operation. You can filter the list using an array of  Filter objects.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListForecasts>`_

        **Request Syntax**
        ::

          response = client.list_forecasts(
              NextToken='string',
              MaxResults=123,
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ]
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_predictors(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[ClientListPredictorsFiltersTypeDef] = None,
    ) -> ClientListPredictorsResponseTypeDef:
        """
        Returns a list of predictors created using the  CreatePredictor operation. For each
        predictor, this operation returns a summary of its properties, including its Amazon Resource
        Name (ARN). You can retrieve the complete set of properties by using the ARN with the
        DescribePredictor operation. You can filter the list using an array of  Filter objects.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/ListPredictors>`_

        **Request Syntax**
        ::

          response = client.list_predictors(
              NextToken='string',
              MaxResults=123,
              Filters=[
                  {
                      'Key': 'string',
                      'Value': 'string',
                      'Condition': 'IS'|'IS_NOT'
                  },
              ]
          )
        :type NextToken: string
        :param NextToken:

          If the result of the previous request was truncated, the response includes a ``NextToken``
          . To retrieve the next set of results, use the token in the next request. Tokens expire
          after 24 hours.

        :type MaxResults: integer
        :param MaxResults:

          The number of items to return in the response.

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
                'NextToken': 'string'
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

            - **NextToken** *(string) --*

              If the response is truncated, Amazon Forecast returns this token. To retrieve the next
              set of results, use the token in the next request.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_dataset_group(self, DatasetGroupArn: str, DatasetArns: List[str]) -> Dict[str, Any]:
        """
        Replaces the datasets in a dataset group with the specified datasets.

        .. note::

          The ``Status`` of the dataset group must be ``ACTIVE`` before you can use the dataset
          group to create a predictor. Use the  DescribeDatasetGroup operation to get the status.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/forecast-2018-06-26/UpdateDatasetGroup>`_

        **Request Syntax**
        ::

          response = client.update_dataset_group(
              DatasetGroupArn='string',
              DatasetArns=[
                  'string',
              ]
          )
        :type DatasetGroupArn: string
        :param DatasetGroupArn: **[REQUIRED]**

          The ARN of the dataset group.

        :type DatasetArns: list
        :param DatasetArns: **[REQUIRED]**

          An array of the Amazon Resource Names (ARNs) of the datasets to add to the dataset group.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_dataset_groups"]
    ) -> paginator_scope.ListDatasetGroupsPaginator:
        """
        Get Paginator for `list_dataset_groups` operation.
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_dataset_import_jobs"]
    ) -> paginator_scope.ListDatasetImportJobsPaginator:
        """
        Get Paginator for `list_dataset_import_jobs` operation.
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_datasets"]
    ) -> paginator_scope.ListDatasetsPaginator:
        """
        Get Paginator for `list_datasets` operation.
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_forecast_export_jobs"]
    ) -> paginator_scope.ListForecastExportJobsPaginator:
        """
        Get Paginator for `list_forecast_export_jobs` operation.
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_forecasts"]
    ) -> paginator_scope.ListForecastsPaginator:
        """
        Get Paginator for `list_forecasts` operation.
        """

    @overload
    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(
        self, operation_name: Literal["list_predictors"]
    ) -> paginator_scope.ListPredictorsPaginator:
        """
        Get Paginator for `list_predictors` operation.
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def get_paginator(self, operation_name: str) -> Boto3Paginator:
        """
        Create a paginator for an operation.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :raise OperationNotPageableError: Raised if the operation is not
            pageable.  You can use the ``client.can_paginate`` method to
            check if an operation is pageable.

        :rtype: L{botocore.paginate.Paginator}
        :return: A paginator object.
        """


class Exceptions:
    ClientError: Boto3ClientError
    InvalidInputException: Boto3ClientError
    InvalidNextTokenException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    ResourceAlreadyExistsException: Boto3ClientError
    ResourceInUseException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
