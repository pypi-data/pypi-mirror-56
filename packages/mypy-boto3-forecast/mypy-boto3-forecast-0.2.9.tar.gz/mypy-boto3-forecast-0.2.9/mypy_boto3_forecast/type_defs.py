"Main interface for forecast type defs"
from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientCreateDatasetEncryptionConfigTypeDef",
    "ClientCreateDatasetGroupResponseTypeDef",
    "ClientCreateDatasetImportJobDataSourceS3ConfigTypeDef",
    "ClientCreateDatasetImportJobDataSourceTypeDef",
    "ClientCreateDatasetImportJobResponseTypeDef",
    "ClientCreateDatasetResponseTypeDef",
    "ClientCreateDatasetSchemaAttributesTypeDef",
    "ClientCreateDatasetSchemaTypeDef",
    "ClientCreateForecastExportJobDestinationS3ConfigTypeDef",
    "ClientCreateForecastExportJobDestinationTypeDef",
    "ClientCreateForecastExportJobResponseTypeDef",
    "ClientCreateForecastResponseTypeDef",
    "ClientCreatePredictorEncryptionConfigTypeDef",
    "ClientCreatePredictorEvaluationParametersTypeDef",
    "ClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef",
    "ClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef",
    "ClientCreatePredictorFeaturizationConfigTypeDef",
    "ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef",
    "ClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef",
    "ClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef",
    "ClientCreatePredictorHPOConfigParameterRangesTypeDef",
    "ClientCreatePredictorHPOConfigTypeDef",
    "ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef",
    "ClientCreatePredictorInputDataConfigTypeDef",
    "ClientCreatePredictorResponseTypeDef",
    "ClientDescribeDatasetGroupResponseTypeDef",
    "ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef",
    "ClientDescribeDatasetImportJobResponseDataSourceTypeDef",
    "ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef",
    "ClientDescribeDatasetImportJobResponseTypeDef",
    "ClientDescribeDatasetResponseEncryptionConfigTypeDef",
    "ClientDescribeDatasetResponseSchemaAttributesTypeDef",
    "ClientDescribeDatasetResponseSchemaTypeDef",
    "ClientDescribeDatasetResponseTypeDef",
    "ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef",
    "ClientDescribeForecastExportJobResponseDestinationTypeDef",
    "ClientDescribeForecastExportJobResponseTypeDef",
    "ClientDescribeForecastResponseTypeDef",
    "ClientDescribePredictorResponseEncryptionConfigTypeDef",
    "ClientDescribePredictorResponseEvaluationParametersTypeDef",
    "ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef",
    "ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef",
    "ClientDescribePredictorResponseFeaturizationConfigTypeDef",
    "ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef",
    "ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef",
    "ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef",
    "ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef",
    "ClientDescribePredictorResponseHPOConfigTypeDef",
    "ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef",
    "ClientDescribePredictorResponseInputDataConfigTypeDef",
    "ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef",
    "ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef",
    "ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef",
    "ClientDescribePredictorResponseTypeDef",
    "ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef",
    "ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef",
    "ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef",
    "ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef",
    "ClientGetAccuracyMetricsResponseTypeDef",
    "ClientListDatasetGroupsResponseDatasetGroupsTypeDef",
    "ClientListDatasetGroupsResponseTypeDef",
    "ClientListDatasetImportJobsFiltersTypeDef",
    "ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef",
    "ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef",
    "ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef",
    "ClientListDatasetImportJobsResponseTypeDef",
    "ClientListDatasetsResponseDatasetsTypeDef",
    "ClientListDatasetsResponseTypeDef",
    "ClientListForecastExportJobsFiltersTypeDef",
    "ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef",
    "ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef",
    "ClientListForecastExportJobsResponseForecastExportJobsTypeDef",
    "ClientListForecastExportJobsResponseTypeDef",
    "ClientListForecastsFiltersTypeDef",
    "ClientListForecastsResponseForecastsTypeDef",
    "ClientListForecastsResponseTypeDef",
    "ClientListPredictorsFiltersTypeDef",
    "ClientListPredictorsResponsePredictorsTypeDef",
    "ClientListPredictorsResponseTypeDef",
    "ListDatasetGroupsPaginatePaginationConfigTypeDef",
    "ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef",
    "ListDatasetGroupsPaginateResponseTypeDef",
    "ListDatasetImportJobsPaginateFiltersTypeDef",
    "ListDatasetImportJobsPaginatePaginationConfigTypeDef",
    "ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef",
    "ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef",
    "ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef",
    "ListDatasetImportJobsPaginateResponseTypeDef",
    "ListDatasetsPaginatePaginationConfigTypeDef",
    "ListDatasetsPaginateResponseDatasetsTypeDef",
    "ListDatasetsPaginateResponseTypeDef",
    "ListForecastExportJobsPaginateFiltersTypeDef",
    "ListForecastExportJobsPaginatePaginationConfigTypeDef",
    "ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef",
    "ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef",
    "ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef",
    "ListForecastExportJobsPaginateResponseTypeDef",
    "ListForecastsPaginateFiltersTypeDef",
    "ListForecastsPaginatePaginationConfigTypeDef",
    "ListForecastsPaginateResponseForecastsTypeDef",
    "ListForecastsPaginateResponseTypeDef",
    "ListPredictorsPaginateFiltersTypeDef",
    "ListPredictorsPaginatePaginationConfigTypeDef",
    "ListPredictorsPaginateResponsePredictorsTypeDef",
    "ListPredictorsPaginateResponseTypeDef",
)


_ClientCreateDatasetEncryptionConfigTypeDef = TypedDict(
    "_ClientCreateDatasetEncryptionConfigTypeDef", {"RoleArn": str, "KMSKeyArn": str}
)


class ClientCreateDatasetEncryptionConfigTypeDef(_ClientCreateDatasetEncryptionConfigTypeDef):
    """
    Type definition for `ClientCreateDataset` `EncryptionConfig`

    An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the key.

    - **RoleArn** *(string) --* **[REQUIRED]**

      The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --* **[REQUIRED]**

      The Amazon Resource Name (ARN) of the KMS key.
    """


_ClientCreateDatasetGroupResponseTypeDef = TypedDict(
    "_ClientCreateDatasetGroupResponseTypeDef", {"DatasetGroupArn": str}, total=False
)


class ClientCreateDatasetGroupResponseTypeDef(_ClientCreateDatasetGroupResponseTypeDef):
    """
    Type definition for `ClientCreateDatasetGroup` `Response`

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group.
    """


_RequiredClientCreateDatasetImportJobDataSourceS3ConfigTypeDef = TypedDict(
    "_RequiredClientCreateDatasetImportJobDataSourceS3ConfigTypeDef", {"Path": str, "RoleArn": str}
)
_OptionalClientCreateDatasetImportJobDataSourceS3ConfigTypeDef = TypedDict(
    "_OptionalClientCreateDatasetImportJobDataSourceS3ConfigTypeDef",
    {"KMSKeyArn": str},
    total=False,
)


class ClientCreateDatasetImportJobDataSourceS3ConfigTypeDef(
    _RequiredClientCreateDatasetImportJobDataSourceS3ConfigTypeDef,
    _OptionalClientCreateDatasetImportJobDataSourceS3ConfigTypeDef,
):
    """
    Type definition for `ClientCreateDatasetImportJobDataSource` `S3Config`

    The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
    along with the credentials to access the data.

    - **Path** *(string) --* **[REQUIRED]**

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --* **[REQUIRED]**

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientCreateDatasetImportJobDataSourceTypeDef = TypedDict(
    "_ClientCreateDatasetImportJobDataSourceTypeDef",
    {"S3Config": ClientCreateDatasetImportJobDataSourceS3ConfigTypeDef},
)


class ClientCreateDatasetImportJobDataSourceTypeDef(_ClientCreateDatasetImportJobDataSourceTypeDef):
    """
    Type definition for `ClientCreateDatasetImportJob` `DataSource`

    The location of the training data to import and an AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the data. The training data must be stored in an
    Amazon S3 bucket.

    If encryption is used, ``DataSource`` must include an AWS Key Management Service (KMS) key and
    the IAM role must allow Amazon Forecast permission to access the key. The KMS key and IAM role
    must match those specified in the ``EncryptionConfig`` parameter of the  CreateDataset
    operation.

    - **S3Config** *(dict) --* **[REQUIRED]**

      The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
      along with the credentials to access the data.

      - **Path** *(string) --* **[REQUIRED]**

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --* **[REQUIRED]**

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientCreateDatasetImportJobResponseTypeDef = TypedDict(
    "_ClientCreateDatasetImportJobResponseTypeDef", {"DatasetImportJobArn": str}, total=False
)


class ClientCreateDatasetImportJobResponseTypeDef(_ClientCreateDatasetImportJobResponseTypeDef):
    """
    Type definition for `ClientCreateDatasetImportJob` `Response`

    - **DatasetImportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset import job.
    """


_ClientCreateDatasetResponseTypeDef = TypedDict(
    "_ClientCreateDatasetResponseTypeDef", {"DatasetArn": str}, total=False
)


class ClientCreateDatasetResponseTypeDef(_ClientCreateDatasetResponseTypeDef):
    """
    Type definition for `ClientCreateDataset` `Response`

    - **DatasetArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset.
    """


_ClientCreateDatasetSchemaAttributesTypeDef = TypedDict(
    "_ClientCreateDatasetSchemaAttributesTypeDef",
    {"AttributeName": str, "AttributeType": str},
    total=False,
)


class ClientCreateDatasetSchemaAttributesTypeDef(_ClientCreateDatasetSchemaAttributesTypeDef):
    """
    Type definition for `ClientCreateDatasetSchema` `Attributes`

    An attribute of a schema, which defines a dataset field. A schema attribute is required for
    every field in a dataset. The  Schema object contains an array of ``SchemaAttribute`` objects.

    - **AttributeName** *(string) --*

      The name of the dataset field.

    - **AttributeType** *(string) --*

      The data type of the field.
    """


_ClientCreateDatasetSchemaTypeDef = TypedDict(
    "_ClientCreateDatasetSchemaTypeDef",
    {"Attributes": List[ClientCreateDatasetSchemaAttributesTypeDef]},
    total=False,
)


class ClientCreateDatasetSchemaTypeDef(_ClientCreateDatasetSchemaTypeDef):
    """
    Type definition for `ClientCreateDataset` `Schema`

    The schema for the dataset. The schema attributes and their order must match the fields in your
    data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required
    fields in your training data. For information about the required fields for a specific dataset
    domain and type, see  howitworks-domains-ds-types .

    - **Attributes** *(list) --*

      An array of attributes specifying the name and type of each field in a dataset.

      - *(dict) --*

        An attribute of a schema, which defines a dataset field. A schema attribute is required for
        every field in a dataset. The  Schema object contains an array of ``SchemaAttribute``
        objects.

        - **AttributeName** *(string) --*

          The name of the dataset field.

        - **AttributeType** *(string) --*

          The data type of the field.
    """


_RequiredClientCreateForecastExportJobDestinationS3ConfigTypeDef = TypedDict(
    "_RequiredClientCreateForecastExportJobDestinationS3ConfigTypeDef",
    {"Path": str, "RoleArn": str},
)
_OptionalClientCreateForecastExportJobDestinationS3ConfigTypeDef = TypedDict(
    "_OptionalClientCreateForecastExportJobDestinationS3ConfigTypeDef",
    {"KMSKeyArn": str},
    total=False,
)


class ClientCreateForecastExportJobDestinationS3ConfigTypeDef(
    _RequiredClientCreateForecastExportJobDestinationS3ConfigTypeDef,
    _OptionalClientCreateForecastExportJobDestinationS3ConfigTypeDef,
):
    """
    Type definition for `ClientCreateForecastExportJobDestination` `S3Config`

    The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
    access the bucket.

    - **Path** *(string) --* **[REQUIRED]**

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --* **[REQUIRED]**

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientCreateForecastExportJobDestinationTypeDef = TypedDict(
    "_ClientCreateForecastExportJobDestinationTypeDef",
    {"S3Config": ClientCreateForecastExportJobDestinationS3ConfigTypeDef},
)


class ClientCreateForecastExportJobDestinationTypeDef(
    _ClientCreateForecastExportJobDestinationTypeDef
):
    """
    Type definition for `ClientCreateForecastExportJob` `Destination`

    The location where you want to save the forecast and an AWS Identity and Access Management (IAM)
    role that Amazon Forecast can assume to access the location. The forecast must be exported to an
    Amazon S3 bucket.

    If encryption is used, ``Destination`` must include an AWS Key Management Service (KMS) key. The
    IAM role must allow Amazon Forecast permission to access the key.

    - **S3Config** *(dict) --* **[REQUIRED]**

      The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
      access the bucket.

      - **Path** *(string) --* **[REQUIRED]**

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --* **[REQUIRED]**

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientCreateForecastExportJobResponseTypeDef = TypedDict(
    "_ClientCreateForecastExportJobResponseTypeDef", {"ForecastExportJobArn": str}, total=False
)


class ClientCreateForecastExportJobResponseTypeDef(_ClientCreateForecastExportJobResponseTypeDef):
    """
    Type definition for `ClientCreateForecastExportJob` `Response`

    - **ForecastExportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the export job.
    """


_ClientCreateForecastResponseTypeDef = TypedDict(
    "_ClientCreateForecastResponseTypeDef", {"ForecastArn": str}, total=False
)


class ClientCreateForecastResponseTypeDef(_ClientCreateForecastResponseTypeDef):
    """
    Type definition for `ClientCreateForecast` `Response`

    - **ForecastArn** *(string) --*

      The Amazon Resource Name (ARN) of the forecast.
    """


_ClientCreatePredictorEncryptionConfigTypeDef = TypedDict(
    "_ClientCreatePredictorEncryptionConfigTypeDef", {"RoleArn": str, "KMSKeyArn": str}
)


class ClientCreatePredictorEncryptionConfigTypeDef(_ClientCreatePredictorEncryptionConfigTypeDef):
    """
    Type definition for `ClientCreatePredictor` `EncryptionConfig`

    An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the key.

    - **RoleArn** *(string) --* **[REQUIRED]**

      The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --* **[REQUIRED]**

      The Amazon Resource Name (ARN) of the KMS key.
    """


_ClientCreatePredictorEvaluationParametersTypeDef = TypedDict(
    "_ClientCreatePredictorEvaluationParametersTypeDef",
    {"NumberOfBacktestWindows": int, "BackTestWindowOffset": int},
    total=False,
)


class ClientCreatePredictorEvaluationParametersTypeDef(
    _ClientCreatePredictorEvaluationParametersTypeDef
):
    """
    Type definition for `ClientCreatePredictor` `EvaluationParameters`

    Used to override the default evaluation parameters of the specified algorithm. Amazon Forecast
    evaluates a predictor by splitting a dataset into training data and testing data. The evaluation
    parameters define how to perform the split and the number of iterations.

    - **NumberOfBacktestWindows** *(integer) --*

      The number of times to split the input data. The default is 1. Valid values are 1 through 5.

    - **BackTestWindowOffset** *(integer) --*

      The point from the end of the dataset where you want to split the data for model training and
      testing (evaluation). Specify the value as the number of data points. The default is the value
      of the forecast horizon. ``BackTestWindowOffset`` can be used to mimic a past virtual forecast
      start date. This value must be greater than or equal to the forecast horizon and less than
      half of the TARGET_TIME_SERIES dataset length.

       ``ForecastHorizon`` <= ``BackTestWindowOffset`` < 1/2 * TARGET_TIME_SERIES dataset length
    """


_RequiredClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef = TypedDict(
    "_RequiredClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef",
    {"FeaturizationMethodName": str},
)
_OptionalClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef = TypedDict(
    "_OptionalClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef",
    {"FeaturizationMethodParameters": Dict[str, str]},
    total=False,
)


class ClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef(
    _RequiredClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef,
    _OptionalClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef,
):
    """
    Type definition for `ClientCreatePredictorFeaturizationConfigFeaturizations`
    `FeaturizationPipeline`

    Provides information about the method that featurizes (transforms) a dataset field. The method
    is part of the ``FeaturizationPipeline`` of the  Featurization object. If you don't specify
    ``FeaturizationMethodParameters`` , Amazon Forecast uses default parameters.

    The following is an example of how you specify a ``FeaturizationMethod`` object.

     ``{``

     ``"FeaturizationMethodName": "filling",``

     ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

     ``}``

    - **FeaturizationMethodName** *(string) --* **[REQUIRED]**

      The name of the method. The "filling" method is the only supported method.

    - **FeaturizationMethodParameters** *(dict) --*

      The method parameters (key-value pairs). Specify these parameters to override the default
      values. The following list shows the parameters and their valid values. Bold signifies the
      default value.

      * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

      * ``frontfill`` : **none**

      * ``middlefill`` : **zero** , ``nan`` (not a number)

      * ``backfill`` : **zero** , ``nan``

      - *(string) --*

        - *(string) --*
    """


_RequiredClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef = TypedDict(
    "_RequiredClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef", {"AttributeName": str}
)
_OptionalClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef = TypedDict(
    "_OptionalClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef",
    {
        "FeaturizationPipeline": List[
            ClientCreatePredictorFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef
        ]
    },
    total=False,
)


class ClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef(
    _RequiredClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef,
    _OptionalClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef,
):
    """
    Type definition for `ClientCreatePredictorFeaturizationConfig` `Featurizations`

    Provides featurization (transformation) information for a dataset field. This object is part of
    the  FeaturizationConfig object.

    For example:

     ``{``

     ``"AttributeName": "demand",``

     ``FeaturizationPipeline [ {``

     ``"FeaturizationMethodName": "filling",``

     ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

     ``} ]``

     ``}``

    - **AttributeName** *(string) --* **[REQUIRED]**

      The name of the schema attribute that specifies the data field to be featurized. Only the
      ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported. For example, for the
      ``RETAIL`` domain, the target is ``demand`` , and for the ``CUSTOM`` domain, the target is
      ``target_value`` .

    - **FeaturizationPipeline** *(list) --*

      An array of one ``FeaturizationMethod`` object that specifies the feature transformation
      method.

      - *(dict) --*

        Provides information about the method that featurizes (transforms) a dataset field. The
        method is part of the ``FeaturizationPipeline`` of the  Featurization object. If you don't
        specify ``FeaturizationMethodParameters`` , Amazon Forecast uses default parameters.

        The following is an example of how you specify a ``FeaturizationMethod`` object.

         ``{``

         ``"FeaturizationMethodName": "filling",``

         ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

         ``}``

        - **FeaturizationMethodName** *(string) --* **[REQUIRED]**

          The name of the method. The "filling" method is the only supported method.

        - **FeaturizationMethodParameters** *(dict) --*

          The method parameters (key-value pairs). Specify these parameters to override the default
          values. The following list shows the parameters and their valid values. Bold signifies the
          default value.

          * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

          * ``frontfill`` : **none**

          * ``middlefill`` : **zero** , ``nan`` (not a number)

          * ``backfill`` : **zero** , ``nan``

          - *(string) --*

            - *(string) --*
    """


_RequiredClientCreatePredictorFeaturizationConfigTypeDef = TypedDict(
    "_RequiredClientCreatePredictorFeaturizationConfigTypeDef", {"ForecastFrequency": str}
)
_OptionalClientCreatePredictorFeaturizationConfigTypeDef = TypedDict(
    "_OptionalClientCreatePredictorFeaturizationConfigTypeDef",
    {
        "ForecastDimensions": List[str],
        "Featurizations": List[ClientCreatePredictorFeaturizationConfigFeaturizationsTypeDef],
    },
    total=False,
)


class ClientCreatePredictorFeaturizationConfigTypeDef(
    _RequiredClientCreatePredictorFeaturizationConfigTypeDef,
    _OptionalClientCreatePredictorFeaturizationConfigTypeDef,
):
    """
    Type definition for `ClientCreatePredictor` `FeaturizationConfig`

    The featurization configuration.

    - **ForecastFrequency** *(string) --* **[REQUIRED]**

      The frequency of predictions in a forecast.

      Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30 minutes),
      15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute). For example,
      "Y" indicates every year and "5min" indicates every five minutes.

      The frequency must be greater than or equal to the TARGET_TIME_SERIES dataset frequency.

      When a RELATED_TIME_SERIES dataset is provided, the frequency must be equal to the
      RELATED_TIME_SERIES dataset frequency.

    - **ForecastDimensions** *(list) --*

      An array of dimension (field) names that specify how to group the generated forecast.

      For example, suppose that you are generating a forecast for item sales across all of your
      stores, and your dataset contains a ``store_id`` field. If you want the sales forecast for
      each item by store, you would specify ``store_id`` as the dimension.

      All forecast dimensions specified in the ``TARGET_TIME_SERIES`` dataset don't need to be
      specified in the ``CreatePredictor`` request. All forecast dimensions specified in the
      ``RELATED_TIME_SERIES`` dataset must be specified in the ``CreatePredictor`` request.

      - *(string) --*

    - **Featurizations** *(list) --*

      An array of featurization (transformation) information for the fields of a dataset. Only a
      single featurization is supported.

      - *(dict) --*

        Provides featurization (transformation) information for a dataset field. This object is part
        of the  FeaturizationConfig object.

        For example:

         ``{``

         ``"AttributeName": "demand",``

         ``FeaturizationPipeline [ {``

         ``"FeaturizationMethodName": "filling",``

         ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

         ``} ]``

         ``}``

        - **AttributeName** *(string) --* **[REQUIRED]**

          The name of the schema attribute that specifies the data field to be featurized. Only the
          ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported. For example, for
          the ``RETAIL`` domain, the target is ``demand`` , and for the ``CUSTOM`` domain, the
          target is ``target_value`` .

        - **FeaturizationPipeline** *(list) --*

          An array of one ``FeaturizationMethod`` object that specifies the feature transformation
          method.

          - *(dict) --*

            Provides information about the method that featurizes (transforms) a dataset field. The
            method is part of the ``FeaturizationPipeline`` of the  Featurization object. If you
            don't specify ``FeaturizationMethodParameters`` , Amazon Forecast uses default
            parameters.

            The following is an example of how you specify a ``FeaturizationMethod`` object.

             ``{``

             ``"FeaturizationMethodName": "filling",``

             ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

             ``}``

            - **FeaturizationMethodName** *(string) --* **[REQUIRED]**

              The name of the method. The "filling" method is the only supported method.

            - **FeaturizationMethodParameters** *(dict) --*

              The method parameters (key-value pairs). Specify these parameters to override the
              default values. The following list shows the parameters and their valid values. Bold
              signifies the default value.

              * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

              * ``frontfill`` : **none**

              * ``middlefill`` : **zero** , ``nan`` (not a number)

              * ``backfill`` : **zero** , ``nan``

              - *(string) --*

                - *(string) --*
    """


_ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef = TypedDict(
    "_ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef",
    {"Name": str, "Values": List[str]},
)


class ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef(
    _ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef
):
    """
    Type definition for `ClientCreatePredictorHPOConfigParameterRanges` `CategoricalParameterRanges`

    Specifies a categorical hyperparameter and it's range of tunable values. This object is part of
    the  ParameterRanges object.

    - **Name** *(string) --* **[REQUIRED]**

      The name of the categorical hyperparameter to tune.

    - **Values** *(list) --* **[REQUIRED]**

      A list of the tunable categories for the hyperparameter.

      - *(string) --*
    """


_RequiredClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef = TypedDict(
    "_RequiredClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef",
    {"Name": str, "MaxValue": float, "MinValue": float},
)
_OptionalClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef = TypedDict(
    "_OptionalClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef",
    {"ScalingType": str},
    total=False,
)


class ClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef(
    _RequiredClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef,
    _OptionalClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef,
):
    """
    Type definition for `ClientCreatePredictorHPOConfigParameterRanges` `ContinuousParameterRanges`

    Specifies a continuous hyperparameter and it's range of tunable values. This object is part of
    the  ParameterRanges object.

    - **Name** *(string) --* **[REQUIRED]**

      The name of the hyperparameter to tune.

    - **MaxValue** *(float) --* **[REQUIRED]**

      The maximum tunable value of the hyperparameter.

    - **MinValue** *(float) --* **[REQUIRED]**

      The minimum tunable value of the hyperparameter.

    - **ScalingType** *(string) --*

      The scale that hyperparameter tuning uses to search the hyperparameter range. Valid values:

        Auto

      Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

        Linear

      Hyperparameter tuning searches the values in the hyperparameter range by using a linear scale.

        Logarithmic

      Hyperparameter tuning searches the values in the hyperparameter range by using a logarithmic
      scale.

      Logarithmic scaling works only for ranges that have values greater than 0.

        ReverseLogarithmic

      hyperparameter tuning searches the values in the hyperparameter range by using a reverse
      logarithmic scale.

      Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
           x <
      1.0.

      For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
      . One of the following values:
    """


_RequiredClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef = TypedDict(
    "_RequiredClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef",
    {"Name": str, "MaxValue": int, "MinValue": int},
)
_OptionalClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef = TypedDict(
    "_OptionalClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef",
    {"ScalingType": str},
    total=False,
)


class ClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef(
    _RequiredClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef,
    _OptionalClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef,
):
    """
    Type definition for `ClientCreatePredictorHPOConfigParameterRanges` `IntegerParameterRanges`

    Specifies an integer hyperparameter and it's range of tunable values. This object is part of the
    ParameterRanges object.

    - **Name** *(string) --* **[REQUIRED]**

      The name of the hyperparameter to tune.

    - **MaxValue** *(integer) --* **[REQUIRED]**

      The maximum tunable value of the hyperparameter.

    - **MinValue** *(integer) --* **[REQUIRED]**

      The minimum tunable value of the hyperparameter.

    - **ScalingType** *(string) --*

      The scale that hyperparameter tuning uses to search the hyperparameter range. Valid values:

        Auto

      Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

        Linear

      Hyperparameter tuning searches the values in the hyperparameter range by using a linear scale.

        Logarithmic

      Hyperparameter tuning searches the values in the hyperparameter range by using a logarithmic
      scale.

      Logarithmic scaling works only for ranges that have values greater than 0.

        ReverseLogarithmic

      Not supported for ``IntegerParameterRange`` .

      Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
           x <
      1.0.

      For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
      . One of the following values:
    """


_ClientCreatePredictorHPOConfigParameterRangesTypeDef = TypedDict(
    "_ClientCreatePredictorHPOConfigParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": List[
            ClientCreatePredictorHPOConfigParameterRangesCategoricalParameterRangesTypeDef
        ],
        "ContinuousParameterRanges": List[
            ClientCreatePredictorHPOConfigParameterRangesContinuousParameterRangesTypeDef
        ],
        "IntegerParameterRanges": List[
            ClientCreatePredictorHPOConfigParameterRangesIntegerParameterRangesTypeDef
        ],
    },
    total=False,
)


class ClientCreatePredictorHPOConfigParameterRangesTypeDef(
    _ClientCreatePredictorHPOConfigParameterRangesTypeDef
):
    """
    Type definition for `ClientCreatePredictorHPOConfig` `ParameterRanges`

    Specifies the ranges of valid values for the hyperparameters.

    - **CategoricalParameterRanges** *(list) --*

      Specifies the tunable range for each categorical hyperparameter.

      - *(dict) --*

        Specifies a categorical hyperparameter and it's range of tunable values. This object is part
        of the  ParameterRanges object.

        - **Name** *(string) --* **[REQUIRED]**

          The name of the categorical hyperparameter to tune.

        - **Values** *(list) --* **[REQUIRED]**

          A list of the tunable categories for the hyperparameter.

          - *(string) --*

    - **ContinuousParameterRanges** *(list) --*

      Specifies the tunable range for each continuous hyperparameter.

      - *(dict) --*

        Specifies a continuous hyperparameter and it's range of tunable values. This object is part
        of the  ParameterRanges object.

        - **Name** *(string) --* **[REQUIRED]**

          The name of the hyperparameter to tune.

        - **MaxValue** *(float) --* **[REQUIRED]**

          The maximum tunable value of the hyperparameter.

        - **MinValue** *(float) --* **[REQUIRED]**

          The minimum tunable value of the hyperparameter.

        - **ScalingType** *(string) --*

          The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
          values:

            Auto

          Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

            Linear

          Hyperparameter tuning searches the values in the hyperparameter range by using a linear
          scale.

            Logarithmic

          Hyperparameter tuning searches the values in the hyperparameter range by using a
          logarithmic scale.

          Logarithmic scaling works only for ranges that have values greater than 0.

            ReverseLogarithmic

          hyperparameter tuning searches the values in the hyperparameter range by using a reverse
          logarithmic scale.

          Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
          x < 1.0.

          For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
          <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
          . One of the following values:

    - **IntegerParameterRanges** *(list) --*

      Specifies the tunable range for each integer hyperparameter.

      - *(dict) --*

        Specifies an integer hyperparameter and it's range of tunable values. This object is part of
        the  ParameterRanges object.

        - **Name** *(string) --* **[REQUIRED]**

          The name of the hyperparameter to tune.

        - **MaxValue** *(integer) --* **[REQUIRED]**

          The maximum tunable value of the hyperparameter.

        - **MinValue** *(integer) --* **[REQUIRED]**

          The minimum tunable value of the hyperparameter.

        - **ScalingType** *(string) --*

          The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
          values:

            Auto

          Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

            Linear

          Hyperparameter tuning searches the values in the hyperparameter range by using a linear
          scale.

            Logarithmic

          Hyperparameter tuning searches the values in the hyperparameter range by using a
          logarithmic scale.

          Logarithmic scaling works only for ranges that have values greater than 0.

            ReverseLogarithmic

          Not supported for ``IntegerParameterRange`` .

          Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
          x < 1.0.

          For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
          <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
          . One of the following values:
    """


_ClientCreatePredictorHPOConfigTypeDef = TypedDict(
    "_ClientCreatePredictorHPOConfigTypeDef",
    {"ParameterRanges": ClientCreatePredictorHPOConfigParameterRangesTypeDef},
    total=False,
)


class ClientCreatePredictorHPOConfigTypeDef(_ClientCreatePredictorHPOConfigTypeDef):
    """
    Type definition for `ClientCreatePredictor` `HPOConfig`

    Provides hyperparameter override values for the algorithm. If you don't provide this parameter,
    Amazon Forecast uses default values. The individual algorithms specify which hyperparameters
    support hyperparameter optimization (HPO). For more information, see
    aws-forecast-choosing-recipes .

    If you included the ``HPOConfig`` object, you must set ``PerformHPO`` to true.

    - **ParameterRanges** *(dict) --*

      Specifies the ranges of valid values for the hyperparameters.

      - **CategoricalParameterRanges** *(list) --*

        Specifies the tunable range for each categorical hyperparameter.

        - *(dict) --*

          Specifies a categorical hyperparameter and it's range of tunable values. This object is
          part of the  ParameterRanges object.

          - **Name** *(string) --* **[REQUIRED]**

            The name of the categorical hyperparameter to tune.

          - **Values** *(list) --* **[REQUIRED]**

            A list of the tunable categories for the hyperparameter.

            - *(string) --*

      - **ContinuousParameterRanges** *(list) --*

        Specifies the tunable range for each continuous hyperparameter.

        - *(dict) --*

          Specifies a continuous hyperparameter and it's range of tunable values. This object is
          part of the  ParameterRanges object.

          - **Name** *(string) --* **[REQUIRED]**

            The name of the hyperparameter to tune.

          - **MaxValue** *(float) --* **[REQUIRED]**

            The maximum tunable value of the hyperparameter.

          - **MinValue** *(float) --* **[REQUIRED]**

            The minimum tunable value of the hyperparameter.

          - **ScalingType** *(string) --*

            The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
            values:

              Auto

            Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

              Linear

            Hyperparameter tuning searches the values in the hyperparameter range by using a linear
            scale.

              Logarithmic

            Hyperparameter tuning searches the values in the hyperparameter range by using a
            logarithmic scale.

            Logarithmic scaling works only for ranges that have values greater than 0.

              ReverseLogarithmic

            hyperparameter tuning searches the values in the hyperparameter range by using a reverse
            logarithmic scale.

            Reverse logarithmic scaling works only for ranges that are entirely within the range 0
            <= x < 1.0.

            For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
            <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
            . One of the following values:

      - **IntegerParameterRanges** *(list) --*

        Specifies the tunable range for each integer hyperparameter.

        - *(dict) --*

          Specifies an integer hyperparameter and it's range of tunable values. This object is part
          of the  ParameterRanges object.

          - **Name** *(string) --* **[REQUIRED]**

            The name of the hyperparameter to tune.

          - **MaxValue** *(integer) --* **[REQUIRED]**

            The maximum tunable value of the hyperparameter.

          - **MinValue** *(integer) --* **[REQUIRED]**

            The minimum tunable value of the hyperparameter.

          - **ScalingType** *(string) --*

            The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
            values:

              Auto

            Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

              Linear

            Hyperparameter tuning searches the values in the hyperparameter range by using a linear
            scale.

              Logarithmic

            Hyperparameter tuning searches the values in the hyperparameter range by using a
            logarithmic scale.

            Logarithmic scaling works only for ranges that have values greater than 0.

              ReverseLogarithmic

            Not supported for ``IntegerParameterRange`` .

            Reverse logarithmic scaling works only for ranges that are entirely within the range 0
            <= x < 1.0.

            For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
            <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
            . One of the following values:
    """


_ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef = TypedDict(
    "_ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef", {"Name": str, "Value": str}
)


class ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef(
    _ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef
):
    """
    Type definition for `ClientCreatePredictorInputDataConfig` `SupplementaryFeatures`

    Describes a supplementary feature of a dataset group. This object is part of the
    InputDataConfig object.

    The only supported feature is a holiday calendar. If you use the calendar, all data in the
    datasets should belong to the same country as the calendar. For the holiday calendar data, see
    the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web site.

    - **Name** *(string) --* **[REQUIRED]**

      The name of the feature. This must be "holiday".

    - **Value** *(string) --* **[REQUIRED]**

      One of the following 2 letter country codes:

      * "AU" - AUSTRALIA

      * "DE" - GERMANY

      * "JP" - JAPAN

      * "US" - UNITED_STATES

      * "UK" - UNITED_KINGDOM
    """


_RequiredClientCreatePredictorInputDataConfigTypeDef = TypedDict(
    "_RequiredClientCreatePredictorInputDataConfigTypeDef", {"DatasetGroupArn": str}
)
_OptionalClientCreatePredictorInputDataConfigTypeDef = TypedDict(
    "_OptionalClientCreatePredictorInputDataConfigTypeDef",
    {
        "SupplementaryFeatures": List[
            ClientCreatePredictorInputDataConfigSupplementaryFeaturesTypeDef
        ]
    },
    total=False,
)


class ClientCreatePredictorInputDataConfigTypeDef(
    _RequiredClientCreatePredictorInputDataConfigTypeDef,
    _OptionalClientCreatePredictorInputDataConfigTypeDef,
):
    """
    Type definition for `ClientCreatePredictor` `InputDataConfig`

    Describes the dataset group that contains the data to use to train the predictor.

    - **DatasetGroupArn** *(string) --* **[REQUIRED]**

      The Amazon Resource Name (ARN) of the dataset group.

    - **SupplementaryFeatures** *(list) --*

      An array of supplementary features. The only supported feature is a holiday calendar.

      - *(dict) --*

        Describes a supplementary feature of a dataset group. This object is part of the
        InputDataConfig object.

        The only supported feature is a holiday calendar. If you use the calendar, all data in the
        datasets should belong to the same country as the calendar. For the holiday calendar data,
        see the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web site.

        - **Name** *(string) --* **[REQUIRED]**

          The name of the feature. This must be "holiday".

        - **Value** *(string) --* **[REQUIRED]**

          One of the following 2 letter country codes:

          * "AU" - AUSTRALIA

          * "DE" - GERMANY

          * "JP" - JAPAN

          * "US" - UNITED_STATES

          * "UK" - UNITED_KINGDOM
    """


_ClientCreatePredictorResponseTypeDef = TypedDict(
    "_ClientCreatePredictorResponseTypeDef", {"PredictorArn": str}, total=False
)


class ClientCreatePredictorResponseTypeDef(_ClientCreatePredictorResponseTypeDef):
    """
    Type definition for `ClientCreatePredictor` `Response`

    - **PredictorArn** *(string) --*

      The Amazon Resource Name (ARN) of the predictor.
    """


_ClientDescribeDatasetGroupResponseTypeDef = TypedDict(
    "_ClientDescribeDatasetGroupResponseTypeDef",
    {
        "DatasetGroupName": str,
        "DatasetGroupArn": str,
        "DatasetArns": List[str],
        "Domain": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribeDatasetGroupResponseTypeDef(_ClientDescribeDatasetGroupResponseTypeDef):
    """
    Type definition for `ClientDescribeDatasetGroup` `Response`

    - **DatasetGroupName** *(string) --*

      The name of the dataset group.

    - **DatasetGroupArn** *(string) --*

      The ARN of the dataset group.

    - **DatasetArns** *(list) --*

      An array of Amazon Resource Names (ARNs) of the datasets contained in the dataset group.

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

        The ``Status`` of the dataset group must be ``ACTIVE`` before you can use the dataset group
        to create a predictor.

    - **CreationTime** *(datetime) --*

      When the dataset group was created.

    - **LastModificationTime** *(datetime) --*

      When the dataset group was created or last updated from a call to the  UpdateDatasetGroup
      operation. While the dataset group is being updated, ``LastModificationTime`` is the current
      time of the ``DescribeDatasetGroup`` call.
    """


_ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef = TypedDict(
    "_ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef(
    _ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef
):
    """
    Type definition for `ClientDescribeDatasetImportJobResponseDataSource` `S3Config`

    The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
    along with the credentials to access the data.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientDescribeDatasetImportJobResponseDataSourceTypeDef = TypedDict(
    "_ClientDescribeDatasetImportJobResponseDataSourceTypeDef",
    {"S3Config": ClientDescribeDatasetImportJobResponseDataSourceS3ConfigTypeDef},
    total=False,
)


class ClientDescribeDatasetImportJobResponseDataSourceTypeDef(
    _ClientDescribeDatasetImportJobResponseDataSourceTypeDef
):
    """
    Type definition for `ClientDescribeDatasetImportJobResponse` `DataSource`

    The location of the training data to import and an AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the data.

    If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

    - **S3Config** *(dict) --*

      The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
      along with the credentials to access the data.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef = TypedDict(
    "_ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef",
    {
        "Count": int,
        "CountDistinct": int,
        "CountNull": int,
        "CountNan": int,
        "Min": str,
        "Max": str,
        "Avg": float,
        "Stddev": float,
    },
    total=False,
)


class ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef(
    _ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef
):
    """
    Type definition for `ClientDescribeDatasetImportJobResponse` `FieldStatistics`

    Provides statistics for each data field imported into to an Amazon Forecast dataset with the
    CreateDatasetImportJob operation.

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
    """


_ClientDescribeDatasetImportJobResponseTypeDef = TypedDict(
    "_ClientDescribeDatasetImportJobResponseTypeDef",
    {
        "DatasetImportJobName": str,
        "DatasetImportJobArn": str,
        "DatasetArn": str,
        "TimestampFormat": str,
        "DataSource": ClientDescribeDatasetImportJobResponseDataSourceTypeDef,
        "FieldStatistics": Dict[str, ClientDescribeDatasetImportJobResponseFieldStatisticsTypeDef],
        "DataSize": float,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribeDatasetImportJobResponseTypeDef(_ClientDescribeDatasetImportJobResponseTypeDef):
    """
    Type definition for `ClientDescribeDatasetImportJob` `Response`

    - **DatasetImportJobName** *(string) --*

      The name of the dataset import job.

    - **DatasetImportJobArn** *(string) --*

      The ARN of the dataset import job.

    - **DatasetArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset that the training data was imported to.

    - **TimestampFormat** *(string) --*

      The format of timestamps in the dataset. The format that you specify depends on the
      ``DataFrequency`` specified when the dataset was created. The following formats are supported

      * "yyyy-MM-dd" For the following data frequencies: Y, M, W, and D

      * "yyyy-MM-dd HH:mm:ss" For the following data frequencies: H, 30min, 15min, and 1min; and
      optionally, for: Y, M, W, and D

    - **DataSource** *(dict) --*

      The location of the training data to import and an AWS Identity and Access Management (IAM)
      role that Amazon Forecast can assume to access the data.

      If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

      - **S3Config** *(dict) --*

        The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
        along with the credentials to access the data.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

        - **KMSKeyArn** *(string) --*

          The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

    - **FieldStatistics** *(dict) --*

      Statistical information about each field in the input data.

      - *(string) --*

        - *(dict) --*

          Provides statistics for each data field imported into to an Amazon Forecast dataset with
          the  CreateDatasetImportJob operation.

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

      The status of the dataset import job. The status is reflected in the status of the dataset.
      For example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of the dataset
      is ``UPDATE_IN_PROGRESS`` . States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the dataset import job was created.

    - **LastModificationTime** *(datetime) --*

      The last time that the dataset was modified. The time depends on the status of the job, as
      follows:

      * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

      * ``CREATE_IN_PROGRESS`` - The current timestamp.

      * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.
    """


_ClientDescribeDatasetResponseEncryptionConfigTypeDef = TypedDict(
    "_ClientDescribeDatasetResponseEncryptionConfigTypeDef",
    {"RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientDescribeDatasetResponseEncryptionConfigTypeDef(
    _ClientDescribeDatasetResponseEncryptionConfigTypeDef
):
    """
    Type definition for `ClientDescribeDatasetResponse` `EncryptionConfig`

    The AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the key.

    - **RoleArn** *(string) --*

      The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of the KMS key.
    """


_ClientDescribeDatasetResponseSchemaAttributesTypeDef = TypedDict(
    "_ClientDescribeDatasetResponseSchemaAttributesTypeDef",
    {"AttributeName": str, "AttributeType": str},
    total=False,
)


class ClientDescribeDatasetResponseSchemaAttributesTypeDef(
    _ClientDescribeDatasetResponseSchemaAttributesTypeDef
):
    """
    Type definition for `ClientDescribeDatasetResponseSchema` `Attributes`

    An attribute of a schema, which defines a dataset field. A schema attribute is required for
    every field in a dataset. The  Schema object contains an array of ``SchemaAttribute`` objects.

    - **AttributeName** *(string) --*

      The name of the dataset field.

    - **AttributeType** *(string) --*

      The data type of the field.
    """


_ClientDescribeDatasetResponseSchemaTypeDef = TypedDict(
    "_ClientDescribeDatasetResponseSchemaTypeDef",
    {"Attributes": List[ClientDescribeDatasetResponseSchemaAttributesTypeDef]},
    total=False,
)


class ClientDescribeDatasetResponseSchemaTypeDef(_ClientDescribeDatasetResponseSchemaTypeDef):
    """
    Type definition for `ClientDescribeDatasetResponse` `Schema`

    An array of ``SchemaAttribute`` objects that specify the dataset fields. Each
    ``SchemaAttribute`` specifies the name and data type of a field.

    - **Attributes** *(list) --*

      An array of attributes specifying the name and type of each field in a dataset.

      - *(dict) --*

        An attribute of a schema, which defines a dataset field. A schema attribute is required for
        every field in a dataset. The  Schema object contains an array of ``SchemaAttribute``
        objects.

        - **AttributeName** *(string) --*

          The name of the dataset field.

        - **AttributeType** *(string) --*

          The data type of the field.
    """


_ClientDescribeDatasetResponseTypeDef = TypedDict(
    "_ClientDescribeDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "Domain": str,
        "DatasetType": str,
        "DataFrequency": str,
        "Schema": ClientDescribeDatasetResponseSchemaTypeDef,
        "EncryptionConfig": ClientDescribeDatasetResponseEncryptionConfigTypeDef,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribeDatasetResponseTypeDef(_ClientDescribeDatasetResponseTypeDef):
    """
    Type definition for `ClientDescribeDataset` `Response`

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

      Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30 minutes),
      15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute). For example,
      "M" indicates every month and "30min" indicates every 30 minutes.

    - **Schema** *(dict) --*

      An array of ``SchemaAttribute`` objects that specify the dataset fields. Each
      ``SchemaAttribute`` specifies the name and data type of a field.

      - **Attributes** *(list) --*

        An array of attributes specifying the name and type of each field in a dataset.

        - *(dict) --*

          An attribute of a schema, which defines a dataset field. A schema attribute is required
          for every field in a dataset. The  Schema object contains an array of ``SchemaAttribute``
          objects.

          - **AttributeName** *(string) --*

            The name of the dataset field.

          - **AttributeType** *(string) --*

            The data type of the field.

    - **EncryptionConfig** *(dict) --*

      The AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
      that Amazon Forecast can assume to access the key.

      - **RoleArn** *(string) --*

        The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

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
      example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of the dataset is
      ``UPDATE_IN_PROGRESS`` .

      .. note::

        The ``Status`` of the dataset must be ``ACTIVE`` before you can import training data.

    - **CreationTime** *(datetime) --*

      When the dataset was created.

    - **LastModificationTime** *(datetime) --*

      When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` . While
      data is being imported to the dataset, ``LastModificationTime`` is the current time of the
      ``DescribeDataset`` call. After a  CreateDatasetImportJob operation has finished,
      ``LastModificationTime`` is when the import job completed or failed.
    """


_ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef = TypedDict(
    "_ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef(
    _ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef
):
    """
    Type definition for `ClientDescribeForecastExportJobResponseDestination` `S3Config`

    The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
    access the bucket.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientDescribeForecastExportJobResponseDestinationTypeDef = TypedDict(
    "_ClientDescribeForecastExportJobResponseDestinationTypeDef",
    {"S3Config": ClientDescribeForecastExportJobResponseDestinationS3ConfigTypeDef},
    total=False,
)


class ClientDescribeForecastExportJobResponseDestinationTypeDef(
    _ClientDescribeForecastExportJobResponseDestinationTypeDef
):
    """
    Type definition for `ClientDescribeForecastExportJobResponse` `Destination`

    The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is exported.

    - **S3Config** *(dict) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
      access the bucket.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientDescribeForecastExportJobResponseTypeDef = TypedDict(
    "_ClientDescribeForecastExportJobResponseTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "ForecastArn": str,
        "Destination": ClientDescribeForecastExportJobResponseDestinationTypeDef,
        "Message": str,
        "Status": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribeForecastExportJobResponseTypeDef(
    _ClientDescribeForecastExportJobResponseTypeDef
):
    """
    Type definition for `ClientDescribeForecastExportJob` `Response`

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

        The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials
        to access the bucket.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

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

        The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
        forecast in your S3 bucket.

    - **CreationTime** *(datetime) --*

      When the forecast export job was created.

    - **LastModificationTime** *(datetime) --*

      When the last successful export job finished.
    """


_ClientDescribeForecastResponseTypeDef = TypedDict(
    "_ClientDescribeForecastResponseTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "ForecastTypes": List[str],
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribeForecastResponseTypeDef(_ClientDescribeForecastResponseTypeDef):
    """
    Type definition for `ClientDescribeForecast` `Response`

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
      inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ), and when
      inference is complete (status changed to ``ACTIVE`` ) or fails (status changed to
      ``CREATE_FAILED`` ).
    """


_ClientDescribePredictorResponseEncryptionConfigTypeDef = TypedDict(
    "_ClientDescribePredictorResponseEncryptionConfigTypeDef",
    {"RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientDescribePredictorResponseEncryptionConfigTypeDef(
    _ClientDescribePredictorResponseEncryptionConfigTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `EncryptionConfig`

    An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the key.

    - **RoleArn** *(string) --*

      The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of the KMS key.
    """


_ClientDescribePredictorResponseEvaluationParametersTypeDef = TypedDict(
    "_ClientDescribePredictorResponseEvaluationParametersTypeDef",
    {"NumberOfBacktestWindows": int, "BackTestWindowOffset": int},
    total=False,
)


class ClientDescribePredictorResponseEvaluationParametersTypeDef(
    _ClientDescribePredictorResponseEvaluationParametersTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `EvaluationParameters`

    Used to override the default evaluation parameters of the specified algorithm. Amazon Forecast
    evaluates a predictor by splitting a dataset into training data and testing data. The evaluation
    parameters define how to perform the split and the number of iterations.

    - **NumberOfBacktestWindows** *(integer) --*

      The number of times to split the input data. The default is 1. Valid values are 1 through 5.

    - **BackTestWindowOffset** *(integer) --*

      The point from the end of the dataset where you want to split the data for model training and
      testing (evaluation). Specify the value as the number of data points. The default is the value
      of the forecast horizon. ``BackTestWindowOffset`` can be used to mimic a past virtual forecast
      start date. This value must be greater than or equal to the forecast horizon and less than
      half of the TARGET_TIME_SERIES dataset length.

       ``ForecastHorizon`` <= ``BackTestWindowOffset`` < 1/2 * TARGET_TIME_SERIES dataset length
    """


_ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef = TypedDict(
    "_ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef",
    {"FeaturizationMethodName": str, "FeaturizationMethodParameters": Dict[str, str]},
    total=False,
)


class ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef(
    _ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseFeaturizationConfigFeaturizations`
    `FeaturizationPipeline`

    Provides information about the method that featurizes (transforms) a dataset field. The method
    is part of the ``FeaturizationPipeline`` of the  Featurization object. If you don't specify
    ``FeaturizationMethodParameters`` , Amazon Forecast uses default parameters.

    The following is an example of how you specify a ``FeaturizationMethod`` object.

     ``{``

     ``"FeaturizationMethodName": "filling",``

     ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

     ``}``

    - **FeaturizationMethodName** *(string) --*

      The name of the method. The "filling" method is the only supported method.

    - **FeaturizationMethodParameters** *(dict) --*

      The method parameters (key-value pairs). Specify these parameters to override the default
      values. The following list shows the parameters and their valid values. Bold signifies the
      default value.

      * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

      * ``frontfill`` : **none**

      * ``middlefill`` : **zero** , ``nan`` (not a number)

      * ``backfill`` : **zero** , ``nan``

      - *(string) --*

        - *(string) --*
    """


_ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef = TypedDict(
    "_ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef",
    {
        "AttributeName": str,
        "FeaturizationPipeline": List[
            ClientDescribePredictorResponseFeaturizationConfigFeaturizationsFeaturizationPipelineTypeDef
        ],
    },
    total=False,
)


class ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef(
    _ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseFeaturizationConfig` `Featurizations`

    Provides featurization (transformation) information for a dataset field. This object is part of
    the  FeaturizationConfig object.

    For example:

     ``{``

     ``"AttributeName": "demand",``

     ``FeaturizationPipeline [ {``

     ``"FeaturizationMethodName": "filling",``

     ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

     ``} ]``

     ``}``

    - **AttributeName** *(string) --*

      The name of the schema attribute that specifies the data field to be featurized. Only the
      ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported. For example, for the
      ``RETAIL`` domain, the target is ``demand`` , and for the ``CUSTOM`` domain, the target is
      ``target_value`` .

    - **FeaturizationPipeline** *(list) --*

      An array of one ``FeaturizationMethod`` object that specifies the feature transformation
      method.

      - *(dict) --*

        Provides information about the method that featurizes (transforms) a dataset field. The
        method is part of the ``FeaturizationPipeline`` of the  Featurization object. If you don't
        specify ``FeaturizationMethodParameters`` , Amazon Forecast uses default parameters.

        The following is an example of how you specify a ``FeaturizationMethod`` object.

         ``{``

         ``"FeaturizationMethodName": "filling",``

         ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

         ``}``

        - **FeaturizationMethodName** *(string) --*

          The name of the method. The "filling" method is the only supported method.

        - **FeaturizationMethodParameters** *(dict) --*

          The method parameters (key-value pairs). Specify these parameters to override the default
          values. The following list shows the parameters and their valid values. Bold signifies the
          default value.

          * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

          * ``frontfill`` : **none**

          * ``middlefill`` : **zero** , ``nan`` (not a number)

          * ``backfill`` : **zero** , ``nan``

          - *(string) --*

            - *(string) --*
    """


_ClientDescribePredictorResponseFeaturizationConfigTypeDef = TypedDict(
    "_ClientDescribePredictorResponseFeaturizationConfigTypeDef",
    {
        "ForecastFrequency": str,
        "ForecastDimensions": List[str],
        "Featurizations": List[
            ClientDescribePredictorResponseFeaturizationConfigFeaturizationsTypeDef
        ],
    },
    total=False,
)


class ClientDescribePredictorResponseFeaturizationConfigTypeDef(
    _ClientDescribePredictorResponseFeaturizationConfigTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `FeaturizationConfig`

    The featurization configuration.

    - **ForecastFrequency** *(string) --*

      The frequency of predictions in a forecast.

      Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30 minutes),
      15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute). For example,
      "Y" indicates every year and "5min" indicates every five minutes.

      The frequency must be greater than or equal to the TARGET_TIME_SERIES dataset frequency.

      When a RELATED_TIME_SERIES dataset is provided, the frequency must be equal to the
      RELATED_TIME_SERIES dataset frequency.

    - **ForecastDimensions** *(list) --*

      An array of dimension (field) names that specify how to group the generated forecast.

      For example, suppose that you are generating a forecast for item sales across all of your
      stores, and your dataset contains a ``store_id`` field. If you want the sales forecast for
      each item by store, you would specify ``store_id`` as the dimension.

      All forecast dimensions specified in the ``TARGET_TIME_SERIES`` dataset don't need to be
      specified in the ``CreatePredictor`` request. All forecast dimensions specified in the
      ``RELATED_TIME_SERIES`` dataset must be specified in the ``CreatePredictor`` request.

      - *(string) --*

    - **Featurizations** *(list) --*

      An array of featurization (transformation) information for the fields of a dataset. Only a
      single featurization is supported.

      - *(dict) --*

        Provides featurization (transformation) information for a dataset field. This object is part
        of the  FeaturizationConfig object.

        For example:

         ``{``

         ``"AttributeName": "demand",``

         ``FeaturizationPipeline [ {``

         ``"FeaturizationMethodName": "filling",``

         ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

         ``} ]``

         ``}``

        - **AttributeName** *(string) --*

          The name of the schema attribute that specifies the data field to be featurized. Only the
          ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported. For example, for
          the ``RETAIL`` domain, the target is ``demand`` , and for the ``CUSTOM`` domain, the
          target is ``target_value`` .

        - **FeaturizationPipeline** *(list) --*

          An array of one ``FeaturizationMethod`` object that specifies the feature transformation
          method.

          - *(dict) --*

            Provides information about the method that featurizes (transforms) a dataset field. The
            method is part of the ``FeaturizationPipeline`` of the  Featurization object. If you
            don't specify ``FeaturizationMethodParameters`` , Amazon Forecast uses default
            parameters.

            The following is an example of how you specify a ``FeaturizationMethod`` object.

             ``{``

             ``"FeaturizationMethodName": "filling",``

             ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

             ``}``

            - **FeaturizationMethodName** *(string) --*

              The name of the method. The "filling" method is the only supported method.

            - **FeaturizationMethodParameters** *(dict) --*

              The method parameters (key-value pairs). Specify these parameters to override the
              default values. The following list shows the parameters and their valid values. Bold
              signifies the default value.

              * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

              * ``frontfill`` : **none**

              * ``middlefill`` : **zero** , ``nan`` (not a number)

              * ``backfill`` : **zero** , ``nan``

              - *(string) --*

                - *(string) --*
    """


_ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef = TypedDict(
    "_ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef",
    {"Name": str, "Values": List[str]},
    total=False,
)


class ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef(
    _ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseHPOConfigParameterRanges`
    `CategoricalParameterRanges`

    Specifies a categorical hyperparameter and it's range of tunable values. This object is part of
    the  ParameterRanges object.

    - **Name** *(string) --*

      The name of the categorical hyperparameter to tune.

    - **Values** *(list) --*

      A list of the tunable categories for the hyperparameter.

      - *(string) --*
    """


_ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef = TypedDict(
    "_ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef",
    {"Name": str, "MaxValue": float, "MinValue": float, "ScalingType": str},
    total=False,
)


class ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef(
    _ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseHPOConfigParameterRanges`
    `ContinuousParameterRanges`

    Specifies a continuous hyperparameter and it's range of tunable values. This object is part of
    the  ParameterRanges object.

    - **Name** *(string) --*

      The name of the hyperparameter to tune.

    - **MaxValue** *(float) --*

      The maximum tunable value of the hyperparameter.

    - **MinValue** *(float) --*

      The minimum tunable value of the hyperparameter.

    - **ScalingType** *(string) --*

      The scale that hyperparameter tuning uses to search the hyperparameter range. Valid values:

        Auto

      Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

        Linear

      Hyperparameter tuning searches the values in the hyperparameter range by using a linear scale.

        Logarithmic

      Hyperparameter tuning searches the values in the hyperparameter range by using a logarithmic
      scale.

      Logarithmic scaling works only for ranges that have values greater than 0.

        ReverseLogarithmic

      hyperparameter tuning searches the values in the hyperparameter range by using a reverse
      logarithmic scale.

      Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
           x <
      1.0.

      For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
      . One of the following values:
    """


_ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef = TypedDict(
    "_ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef",
    {"Name": str, "MaxValue": int, "MinValue": int, "ScalingType": str},
    total=False,
)


class ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef(
    _ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseHPOConfigParameterRanges`
    `IntegerParameterRanges`

    Specifies an integer hyperparameter and it's range of tunable values. This object is part of the
    ParameterRanges object.

    - **Name** *(string) --*

      The name of the hyperparameter to tune.

    - **MaxValue** *(integer) --*

      The maximum tunable value of the hyperparameter.

    - **MinValue** *(integer) --*

      The minimum tunable value of the hyperparameter.

    - **ScalingType** *(string) --*

      The scale that hyperparameter tuning uses to search the hyperparameter range. Valid values:

        Auto

      Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

        Linear

      Hyperparameter tuning searches the values in the hyperparameter range by using a linear scale.

        Logarithmic

      Hyperparameter tuning searches the values in the hyperparameter range by using a logarithmic
      scale.

      Logarithmic scaling works only for ranges that have values greater than 0.

        ReverseLogarithmic

      Not supported for ``IntegerParameterRange`` .

      Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
           x <
      1.0.

      For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
      <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
      . One of the following values:
    """


_ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef = TypedDict(
    "_ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef",
    {
        "CategoricalParameterRanges": List[
            ClientDescribePredictorResponseHPOConfigParameterRangesCategoricalParameterRangesTypeDef
        ],
        "ContinuousParameterRanges": List[
            ClientDescribePredictorResponseHPOConfigParameterRangesContinuousParameterRangesTypeDef
        ],
        "IntegerParameterRanges": List[
            ClientDescribePredictorResponseHPOConfigParameterRangesIntegerParameterRangesTypeDef
        ],
    },
    total=False,
)


class ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef(
    _ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseHPOConfig` `ParameterRanges`

    Specifies the ranges of valid values for the hyperparameters.

    - **CategoricalParameterRanges** *(list) --*

      Specifies the tunable range for each categorical hyperparameter.

      - *(dict) --*

        Specifies a categorical hyperparameter and it's range of tunable values. This object is part
        of the  ParameterRanges object.

        - **Name** *(string) --*

          The name of the categorical hyperparameter to tune.

        - **Values** *(list) --*

          A list of the tunable categories for the hyperparameter.

          - *(string) --*

    - **ContinuousParameterRanges** *(list) --*

      Specifies the tunable range for each continuous hyperparameter.

      - *(dict) --*

        Specifies a continuous hyperparameter and it's range of tunable values. This object is part
        of the  ParameterRanges object.

        - **Name** *(string) --*

          The name of the hyperparameter to tune.

        - **MaxValue** *(float) --*

          The maximum tunable value of the hyperparameter.

        - **MinValue** *(float) --*

          The minimum tunable value of the hyperparameter.

        - **ScalingType** *(string) --*

          The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
          values:

            Auto

          Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

            Linear

          Hyperparameter tuning searches the values in the hyperparameter range by using a linear
          scale.

            Logarithmic

          Hyperparameter tuning searches the values in the hyperparameter range by using a
          logarithmic scale.

          Logarithmic scaling works only for ranges that have values greater than 0.

            ReverseLogarithmic

          hyperparameter tuning searches the values in the hyperparameter range by using a reverse
          logarithmic scale.

          Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
          x < 1.0.

          For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
          <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
          . One of the following values:

    - **IntegerParameterRanges** *(list) --*

      Specifies the tunable range for each integer hyperparameter.

      - *(dict) --*

        Specifies an integer hyperparameter and it's range of tunable values. This object is part of
        the  ParameterRanges object.

        - **Name** *(string) --*

          The name of the hyperparameter to tune.

        - **MaxValue** *(integer) --*

          The maximum tunable value of the hyperparameter.

        - **MinValue** *(integer) --*

          The minimum tunable value of the hyperparameter.

        - **ScalingType** *(string) --*

          The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
          values:

            Auto

          Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

            Linear

          Hyperparameter tuning searches the values in the hyperparameter range by using a linear
          scale.

            Logarithmic

          Hyperparameter tuning searches the values in the hyperparameter range by using a
          logarithmic scale.

          Logarithmic scaling works only for ranges that have values greater than 0.

            ReverseLogarithmic

          Not supported for ``IntegerParameterRange`` .

          Reverse logarithmic scaling works only for ranges that are entirely within the range 0 <=
          x < 1.0.

          For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
          <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
          . One of the following values:
    """


_ClientDescribePredictorResponseHPOConfigTypeDef = TypedDict(
    "_ClientDescribePredictorResponseHPOConfigTypeDef",
    {"ParameterRanges": ClientDescribePredictorResponseHPOConfigParameterRangesTypeDef},
    total=False,
)


class ClientDescribePredictorResponseHPOConfigTypeDef(
    _ClientDescribePredictorResponseHPOConfigTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `HPOConfig`

    The hyperparameter override values for the algorithm.

    - **ParameterRanges** *(dict) --*

      Specifies the ranges of valid values for the hyperparameters.

      - **CategoricalParameterRanges** *(list) --*

        Specifies the tunable range for each categorical hyperparameter.

        - *(dict) --*

          Specifies a categorical hyperparameter and it's range of tunable values. This object is
          part of the  ParameterRanges object.

          - **Name** *(string) --*

            The name of the categorical hyperparameter to tune.

          - **Values** *(list) --*

            A list of the tunable categories for the hyperparameter.

            - *(string) --*

      - **ContinuousParameterRanges** *(list) --*

        Specifies the tunable range for each continuous hyperparameter.

        - *(dict) --*

          Specifies a continuous hyperparameter and it's range of tunable values. This object is
          part of the  ParameterRanges object.

          - **Name** *(string) --*

            The name of the hyperparameter to tune.

          - **MaxValue** *(float) --*

            The maximum tunable value of the hyperparameter.

          - **MinValue** *(float) --*

            The minimum tunable value of the hyperparameter.

          - **ScalingType** *(string) --*

            The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
            values:

              Auto

            Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

              Linear

            Hyperparameter tuning searches the values in the hyperparameter range by using a linear
            scale.

              Logarithmic

            Hyperparameter tuning searches the values in the hyperparameter range by using a
            logarithmic scale.

            Logarithmic scaling works only for ranges that have values greater than 0.

              ReverseLogarithmic

            hyperparameter tuning searches the values in the hyperparameter range by using a reverse
            logarithmic scale.

            Reverse logarithmic scaling works only for ranges that are entirely within the range 0
            <= x < 1.0.

            For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
            <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
            . One of the following values:

      - **IntegerParameterRanges** *(list) --*

        Specifies the tunable range for each integer hyperparameter.

        - *(dict) --*

          Specifies an integer hyperparameter and it's range of tunable values. This object is part
          of the  ParameterRanges object.

          - **Name** *(string) --*

            The name of the hyperparameter to tune.

          - **MaxValue** *(integer) --*

            The maximum tunable value of the hyperparameter.

          - **MinValue** *(integer) --*

            The minimum tunable value of the hyperparameter.

          - **ScalingType** *(string) --*

            The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
            values:

              Auto

            Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

              Linear

            Hyperparameter tuning searches the values in the hyperparameter range by using a linear
            scale.

              Logarithmic

            Hyperparameter tuning searches the values in the hyperparameter range by using a
            logarithmic scale.

            Logarithmic scaling works only for ranges that have values greater than 0.

              ReverseLogarithmic

            Not supported for ``IntegerParameterRange`` .

            Reverse logarithmic scaling works only for ranges that are entirely within the range 0
            <= x < 1.0.

            For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
            <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
            . One of the following values:
    """


_ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef = TypedDict(
    "_ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef",
    {"Name": str, "Value": str},
    total=False,
)


class ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef(
    _ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponseInputDataConfig` `SupplementaryFeatures`

    Describes a supplementary feature of a dataset group. This object is part of the
    InputDataConfig object.

    The only supported feature is a holiday calendar. If you use the calendar, all data in the
    datasets should belong to the same country as the calendar. For the holiday calendar data, see
    the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web site.

    - **Name** *(string) --*

      The name of the feature. This must be "holiday".

    - **Value** *(string) --*

      One of the following 2 letter country codes:

      * "AU" - AUSTRALIA

      * "DE" - GERMANY

      * "JP" - JAPAN

      * "US" - UNITED_STATES

      * "UK" - UNITED_KINGDOM
    """


_ClientDescribePredictorResponseInputDataConfigTypeDef = TypedDict(
    "_ClientDescribePredictorResponseInputDataConfigTypeDef",
    {
        "DatasetGroupArn": str,
        "SupplementaryFeatures": List[
            ClientDescribePredictorResponseInputDataConfigSupplementaryFeaturesTypeDef
        ],
    },
    total=False,
)


class ClientDescribePredictorResponseInputDataConfigTypeDef(
    _ClientDescribePredictorResponseInputDataConfigTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `InputDataConfig`

    Describes the dataset group that contains the data to use to train the predictor.

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group.

    - **SupplementaryFeatures** *(list) --*

      An array of supplementary features. The only supported feature is a holiday calendar.

      - *(dict) --*

        Describes a supplementary feature of a dataset group. This object is part of the
        InputDataConfig object.

        The only supported feature is a holiday calendar. If you use the calendar, all data in the
        datasets should belong to the same country as the calendar. For the holiday calendar data,
        see the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web site.

        - **Name** *(string) --*

          The name of the feature. This must be "holiday".

        - **Value** *(string) --*

          One of the following 2 letter country codes:

          * "AU" - AUSTRALIA

          * "DE" - GERMANY

          * "JP" - JAPAN

          * "US" - UNITED_STATES

          * "UK" - UNITED_KINGDOM
    """


_ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef = TypedDict(
    "_ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef",
    {"TestWindowStart": datetime, "TestWindowEnd": datetime, "Status": str, "Message": str},
    total=False,
)


class ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef(
    _ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef
):
    """
    Type definition for
    `ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutions` `TestWindows`

    The status, start time, and end time of a backtest, as well as a failure reason if applicable.

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
    """


_ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef = TypedDict(
    "_ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef",
    {
        "AlgorithmArn": str,
        "TestWindows": List[
            ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTestWindowsTypeDef
        ],
    },
    total=False,
)


class ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef(
    _ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponsePredictorExecutionDetails`
    `PredictorExecutions`

    The algorithm used to perform a backtest and the status of those tests.

    - **AlgorithmArn** *(string) --*

      The ARN of the algorithm used to test the predictor.

    - **TestWindows** *(list) --*

      An array of test windows used to evaluate the algorithm. The ``NumberOfBacktestWindows`` from
      the object determines the number of windows in the array.

      - *(dict) --*

        The status, start time, and end time of a backtest, as well as a failure reason if
        applicable.

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
    """


_ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef = TypedDict(
    "_ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef",
    {
        "PredictorExecutions": List[
            ClientDescribePredictorResponsePredictorExecutionDetailsPredictorExecutionsTypeDef
        ]
    },
    total=False,
)


class ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef(
    _ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef
):
    """
    Type definition for `ClientDescribePredictorResponse` `PredictorExecutionDetails`

    Details on the the status and results of the backtests performed to evaluate the accuracy of the
    predictor. You specify the number of backtests to perform when you call the operation.

    - **PredictorExecutions** *(list) --*

      An array of the backtests performed to evaluate the accuracy of the predictor against a
      particular algorithm. The ``NumberOfBacktestWindows`` from the object determines the number of
      windows in the array.

      - *(dict) --*

        The algorithm used to perform a backtest and the status of those tests.

        - **AlgorithmArn** *(string) --*

          The ARN of the algorithm used to test the predictor.

        - **TestWindows** *(list) --*

          An array of test windows used to evaluate the algorithm. The ``NumberOfBacktestWindows``
          from the object determines the number of windows in the array.

          - *(dict) --*

            The status, start time, and end time of a backtest, as well as a failure reason if
            applicable.

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
    """


_ClientDescribePredictorResponseTypeDef = TypedDict(
    "_ClientDescribePredictorResponseTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "AlgorithmArn": str,
        "ForecastHorizon": int,
        "PerformAutoML": bool,
        "PerformHPO": bool,
        "TrainingParameters": Dict[str, str],
        "EvaluationParameters": ClientDescribePredictorResponseEvaluationParametersTypeDef,
        "HPOConfig": ClientDescribePredictorResponseHPOConfigTypeDef,
        "InputDataConfig": ClientDescribePredictorResponseInputDataConfigTypeDef,
        "FeaturizationConfig": ClientDescribePredictorResponseFeaturizationConfigTypeDef,
        "EncryptionConfig": ClientDescribePredictorResponseEncryptionConfigTypeDef,
        "PredictorExecutionDetails": ClientDescribePredictorResponsePredictorExecutionDetailsTypeDef,
        "DatasetImportJobArns": List[str],
        "AutoMLAlgorithmArns": List[str],
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientDescribePredictorResponseTypeDef(_ClientDescribePredictorResponseTypeDef):
    """
    Type definition for `ClientDescribePredictor` `Response`

    - **PredictorArn** *(string) --*

      The ARN of the predictor.

    - **PredictorName** *(string) --*

      The name of the predictor.

    - **AlgorithmArn** *(string) --*

      The Amazon Resource Name (ARN) of the algorithm used for model training.

    - **ForecastHorizon** *(integer) --*

      The number of time-steps of the forecast. The forecast horizon is also called the prediction
      length.

    - **PerformAutoML** *(boolean) --*

      Whether the predictor is set to perform AutoML.

    - **PerformHPO** *(boolean) --*

      Whether the predictor is set to perform hyperparameter optimization (HPO).

    - **TrainingParameters** *(dict) --*

      The default training parameters or overrides selected during model training. If using the
      AutoML algorithm or if HPO is turned on while using the DeepAR+ algorithms, the optimized
      values for the chosen hyperparameters are returned. For more information, see
      aws-forecast-choosing-recipes .

      - *(string) --*

        - *(string) --*

    - **EvaluationParameters** *(dict) --*

      Used to override the default evaluation parameters of the specified algorithm. Amazon Forecast
      evaluates a predictor by splitting a dataset into training data and testing data. The
      evaluation parameters define how to perform the split and the number of iterations.

      - **NumberOfBacktestWindows** *(integer) --*

        The number of times to split the input data. The default is 1. Valid values are 1 through 5.

      - **BackTestWindowOffset** *(integer) --*

        The point from the end of the dataset where you want to split the data for model training
        and testing (evaluation). Specify the value as the number of data points. The default is the
        value of the forecast horizon. ``BackTestWindowOffset`` can be used to mimic a past virtual
        forecast start date. This value must be greater than or equal to the forecast horizon and
        less than half of the TARGET_TIME_SERIES dataset length.

         ``ForecastHorizon`` <= ``BackTestWindowOffset`` < 1/2 * TARGET_TIME_SERIES dataset length

    - **HPOConfig** *(dict) --*

      The hyperparameter override values for the algorithm.

      - **ParameterRanges** *(dict) --*

        Specifies the ranges of valid values for the hyperparameters.

        - **CategoricalParameterRanges** *(list) --*

          Specifies the tunable range for each categorical hyperparameter.

          - *(dict) --*

            Specifies a categorical hyperparameter and it's range of tunable values. This object is
            part of the  ParameterRanges object.

            - **Name** *(string) --*

              The name of the categorical hyperparameter to tune.

            - **Values** *(list) --*

              A list of the tunable categories for the hyperparameter.

              - *(string) --*

        - **ContinuousParameterRanges** *(list) --*

          Specifies the tunable range for each continuous hyperparameter.

          - *(dict) --*

            Specifies a continuous hyperparameter and it's range of tunable values. This object is
            part of the  ParameterRanges object.

            - **Name** *(string) --*

              The name of the hyperparameter to tune.

            - **MaxValue** *(float) --*

              The maximum tunable value of the hyperparameter.

            - **MinValue** *(float) --*

              The minimum tunable value of the hyperparameter.

            - **ScalingType** *(string) --*

              The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
              values:

                Auto

              Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

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

              Reverse logarithmic scaling works only for ranges that are entirely within the range 0
              <= x < 1.0.

              For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
              <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
              . One of the following values:

        - **IntegerParameterRanges** *(list) --*

          Specifies the tunable range for each integer hyperparameter.

          - *(dict) --*

            Specifies an integer hyperparameter and it's range of tunable values. This object is
            part of the  ParameterRanges object.

            - **Name** *(string) --*

              The name of the hyperparameter to tune.

            - **MaxValue** *(integer) --*

              The maximum tunable value of the hyperparameter.

            - **MinValue** *(integer) --*

              The minimum tunable value of the hyperparameter.

            - **ScalingType** *(string) --*

              The scale that hyperparameter tuning uses to search the hyperparameter range. Valid
              values:

                Auto

              Amazon Forecast hyperparameter tuning chooses the best scale for the hyperparameter.

                Linear

              Hyperparameter tuning searches the values in the hyperparameter range by using a
              linear scale.

                Logarithmic

              Hyperparameter tuning searches the values in the hyperparameter range by using a
              logarithmic scale.

              Logarithmic scaling works only for ranges that have values greater than 0.

                ReverseLogarithmic

              Not supported for ``IntegerParameterRange`` .

              Reverse logarithmic scaling works only for ranges that are entirely within the range 0
              <= x < 1.0.

              For information about choosing a hyperparameter scale, see `Hyperparameter Scaling
              <http://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html#scaling-type>`__
              . One of the following values:

    - **InputDataConfig** *(dict) --*

      Describes the dataset group that contains the data to use to train the predictor.

      - **DatasetGroupArn** *(string) --*

        The Amazon Resource Name (ARN) of the dataset group.

      - **SupplementaryFeatures** *(list) --*

        An array of supplementary features. The only supported feature is a holiday calendar.

        - *(dict) --*

          Describes a supplementary feature of a dataset group. This object is part of the
          InputDataConfig object.

          The only supported feature is a holiday calendar. If you use the calendar, all data in the
          datasets should belong to the same country as the calendar. For the holiday calendar data,
          see the `Jollyday <http://jollyday.sourceforge.net/data.html>`__ web site.

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

        Valid intervals are Y (Year), M (Month), W (Week), D (Day), H (Hour), 30min (30 minutes),
        15min (15 minutes), 10min (10 minutes), 5min (5 minutes), and 1min (1 minute). For example,
        "Y" indicates every year and "5min" indicates every five minutes.

        The frequency must be greater than or equal to the TARGET_TIME_SERIES dataset frequency.

        When a RELATED_TIME_SERIES dataset is provided, the frequency must be equal to the
        RELATED_TIME_SERIES dataset frequency.

      - **ForecastDimensions** *(list) --*

        An array of dimension (field) names that specify how to group the generated forecast.

        For example, suppose that you are generating a forecast for item sales across all of your
        stores, and your dataset contains a ``store_id`` field. If you want the sales forecast for
        each item by store, you would specify ``store_id`` as the dimension.

        All forecast dimensions specified in the ``TARGET_TIME_SERIES`` dataset don't need to be
        specified in the ``CreatePredictor`` request. All forecast dimensions specified in the
        ``RELATED_TIME_SERIES`` dataset must be specified in the ``CreatePredictor`` request.

        - *(string) --*

      - **Featurizations** *(list) --*

        An array of featurization (transformation) information for the fields of a dataset. Only a
        single featurization is supported.

        - *(dict) --*

          Provides featurization (transformation) information for a dataset field. This object is
          part of the  FeaturizationConfig object.

          For example:

           ``{``

           ``"AttributeName": "demand",``

           ``FeaturizationPipeline [ {``

           ``"FeaturizationMethodName": "filling",``

           ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

           ``} ]``

           ``}``

          - **AttributeName** *(string) --*

            The name of the schema attribute that specifies the data field to be featurized. Only
            the ``target`` field of the ``TARGET_TIME_SERIES`` dataset type is supported. For
            example, for the ``RETAIL`` domain, the target is ``demand`` , and for the ``CUSTOM``
            domain, the target is ``target_value`` .

          - **FeaturizationPipeline** *(list) --*

            An array of one ``FeaturizationMethod`` object that specifies the feature transformation
            method.

            - *(dict) --*

              Provides information about the method that featurizes (transforms) a dataset field.
              The method is part of the ``FeaturizationPipeline`` of the  Featurization object. If
              you don't specify ``FeaturizationMethodParameters`` , Amazon Forecast uses default
              parameters.

              The following is an example of how you specify a ``FeaturizationMethod`` object.

               ``{``

               ``"FeaturizationMethodName": "filling",``

               ``"FeaturizationMethodParameters": {"aggregation": "avg", "backfill": "nan"}``

               ``}``

              - **FeaturizationMethodName** *(string) --*

                The name of the method. The "filling" method is the only supported method.

              - **FeaturizationMethodParameters** *(dict) --*

                The method parameters (key-value pairs). Specify these parameters to override the
                default values. The following list shows the parameters and their valid values. Bold
                signifies the default value.

                * ``aggregation`` : **sum** , ``avg`` , ``first`` , ``min`` , ``max``

                * ``frontfill`` : **none**

                * ``middlefill`` : **zero** , ``nan`` (not a number)

                * ``backfill`` : **zero** , ``nan``

                - *(string) --*

                  - *(string) --*

    - **EncryptionConfig** *(dict) --*

      An AWS Key Management Service (KMS) key and the AWS Identity and Access Management (IAM) role
      that Amazon Forecast can assume to access the key.

      - **RoleArn** *(string) --*

        The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of the KMS key.

    - **PredictorExecutionDetails** *(dict) --*

      Details on the the status and results of the backtests performed to evaluate the accuracy of
      the predictor. You specify the number of backtests to perform when you call the operation.

      - **PredictorExecutions** *(list) --*

        An array of the backtests performed to evaluate the accuracy of the predictor against a
        particular algorithm. The ``NumberOfBacktestWindows`` from the object determines the number
        of windows in the array.

        - *(dict) --*

          The algorithm used to perform a backtest and the status of those tests.

          - **AlgorithmArn** *(string) --*

            The ARN of the algorithm used to test the predictor.

          - **TestWindows** *(list) --*

            An array of test windows used to evaluate the algorithm. The ``NumberOfBacktestWindows``
            from the object determines the number of windows in the array.

            - *(dict) --*

              The status, start time, and end time of a backtest, as well as a failure reason if
              applicable.

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

        The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor to
        create a forecast.

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the model training task was created.

    - **LastModificationTime** *(datetime) --*

      Initially, the same as ``CreationTime`` (when the status is ``CREATE_PENDING`` ). This value
      is updated when training starts (when the status changes to ``CREATE_IN_PROGRESS`` ), and when
      training has completed (when the status changes to ``ACTIVE`` ) or fails (when the status
      changes to ``CREATE_FAILED`` ).
    """


_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef = TypedDict(
    "_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef",
    {"Quantile": float, "LossValue": float},
    total=False,
)


class ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef(
    _ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef
):
    """
    Type definition for
    `ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetrics`
    `WeightedQuantileLosses`

    The weighted loss value for a quantile. This object is part of the  Metrics object.

    - **Quantile** *(float) --*

      The quantile. Quantiles divide a probability distribution into regions of equal probability.
      For example, if the distribution was divided into 5 regions of equal probability, the
      quantiles would be 0.2, 0.4, 0.6, and 0.8.

    - **LossValue** *(float) --*

      The difference between the predicted value and the actual value over the quantile, weighted
      (normalized) by dividing by the sum over all quantiles.
    """


_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef = TypedDict(
    "_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef",
    {
        "RMSE": float,
        "WeightedQuantileLosses": List[
            ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsWeightedQuantileLossesTypeDef
        ],
    },
    total=False,
)


class ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef(
    _ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef
):
    """
    Type definition for `ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindows`
    `Metrics`

    Provides metrics used to evaluate the performance of a predictor.

    - **RMSE** *(float) --*

      The root mean square error (RMSE).

    - **WeightedQuantileLosses** *(list) --*

      An array of weighted quantile losses. Quantiles divide a probability distribution into regions
      of equal probability. The distribution in this case is the loss function.

      - *(dict) --*

        The weighted loss value for a quantile. This object is part of the  Metrics object.

        - **Quantile** *(float) --*

          The quantile. Quantiles divide a probability distribution into regions of equal
          probability. For example, if the distribution was divided into 5 regions of equal
          probability, the quantiles would be 0.2, 0.4, 0.6, and 0.8.

        - **LossValue** *(float) --*

          The difference between the predicted value and the actual value over the quantile,
          weighted (normalized) by dividing by the sum over all quantiles.
    """


_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef = TypedDict(
    "_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef",
    {
        "TestWindowStart": datetime,
        "TestWindowEnd": datetime,
        "ItemCount": int,
        "EvaluationType": str,
        "Metrics": ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsMetricsTypeDef,
    },
    total=False,
)


class ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef(
    _ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef
):
    """
    Type definition for `ClientGetAccuracyMetricsResponsePredictorEvaluationResults` `TestWindows`

    The metrics for a time range within the evaluation portion of a dataset. This object is part of
    the  EvaluationResult object.

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

        An array of weighted quantile losses. Quantiles divide a probability distribution into
        regions of equal probability. The distribution in this case is the loss function.

        - *(dict) --*

          The weighted loss value for a quantile. This object is part of the  Metrics object.

          - **Quantile** *(float) --*

            The quantile. Quantiles divide a probability distribution into regions of equal
            probability. For example, if the distribution was divided into 5 regions of equal
            probability, the quantiles would be 0.2, 0.4, 0.6, and 0.8.

          - **LossValue** *(float) --*

            The difference between the predicted value and the actual value over the quantile,
            weighted (normalized) by dividing by the sum over all quantiles.
    """


_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef = TypedDict(
    "_ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef",
    {
        "AlgorithmArn": str,
        "TestWindows": List[
            ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTestWindowsTypeDef
        ],
    },
    total=False,
)


class ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef(
    _ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef
):
    """
    Type definition for `ClientGetAccuracyMetricsResponse` `PredictorEvaluationResults`

    The results of evaluating an algorithm. Returned as part of the  GetAccuracyMetrics response.

    - **AlgorithmArn** *(string) --*

      The Amazon Resource Name (ARN) of the algorithm that was evaluated.

    - **TestWindows** *(list) --*

      The array of test windows used for evaluating the algorithm. The ``NumberOfBacktestWindows``
      from the  EvaluationParameters object determines the number of windows in the array.

      - *(dict) --*

        The metrics for a time range within the evaluation portion of a dataset. This object is part
        of the  EvaluationResult object.

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

            An array of weighted quantile losses. Quantiles divide a probability distribution into
            regions of equal probability. The distribution in this case is the loss function.

            - *(dict) --*

              The weighted loss value for a quantile. This object is part of the  Metrics object.

              - **Quantile** *(float) --*

                The quantile. Quantiles divide a probability distribution into regions of equal
                probability. For example, if the distribution was divided into 5 regions of equal
                probability, the quantiles would be 0.2, 0.4, 0.6, and 0.8.

              - **LossValue** *(float) --*

                The difference between the predicted value and the actual value over the quantile,
                weighted (normalized) by dividing by the sum over all quantiles.
    """


_ClientGetAccuracyMetricsResponseTypeDef = TypedDict(
    "_ClientGetAccuracyMetricsResponseTypeDef",
    {
        "PredictorEvaluationResults": List[
            ClientGetAccuracyMetricsResponsePredictorEvaluationResultsTypeDef
        ]
    },
    total=False,
)


class ClientGetAccuracyMetricsResponseTypeDef(_ClientGetAccuracyMetricsResponseTypeDef):
    """
    Type definition for `ClientGetAccuracyMetrics` `Response`

    - **PredictorEvaluationResults** *(list) --*

      An array of results from evaluating the predictor.

      - *(dict) --*

        The results of evaluating an algorithm. Returned as part of the  GetAccuracyMetrics
        response.

        - **AlgorithmArn** *(string) --*

          The Amazon Resource Name (ARN) of the algorithm that was evaluated.

        - **TestWindows** *(list) --*

          The array of test windows used for evaluating the algorithm. The
          ``NumberOfBacktestWindows`` from the  EvaluationParameters object determines the number of
          windows in the array.

          - *(dict) --*

            The metrics for a time range within the evaluation portion of a dataset. This object is
            part of the  EvaluationResult object.

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

                An array of weighted quantile losses. Quantiles divide a probability distribution
                into regions of equal probability. The distribution in this case is the loss
                function.

                - *(dict) --*

                  The weighted loss value for a quantile. This object is part of the  Metrics
                  object.

                  - **Quantile** *(float) --*

                    The quantile. Quantiles divide a probability distribution into regions of equal
                    probability. For example, if the distribution was divided into 5 regions of
                    equal probability, the quantiles would be 0.2, 0.4, 0.6, and 0.8.

                  - **LossValue** *(float) --*

                    The difference between the predicted value and the actual value over the
                    quantile, weighted (normalized) by dividing by the sum over all quantiles.
    """


_ClientListDatasetGroupsResponseDatasetGroupsTypeDef = TypedDict(
    "_ClientListDatasetGroupsResponseDatasetGroupsTypeDef",
    {
        "DatasetGroupArn": str,
        "DatasetGroupName": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListDatasetGroupsResponseDatasetGroupsTypeDef(
    _ClientListDatasetGroupsResponseDatasetGroupsTypeDef
):
    """
    Type definition for `ClientListDatasetGroupsResponse` `DatasetGroups`

    Provides a summary of the dataset group properties used in the  ListDatasetGroups operation. To
    get the complete set of properties, call the  DescribeDatasetGroup operation, and provide the
    ``DatasetGroupArn`` .

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group.

    - **DatasetGroupName** *(string) --*

      The name of the dataset group.

    - **CreationTime** *(datetime) --*

      When the dataset group was created.

    - **LastModificationTime** *(datetime) --*

      When the dataset group was created or last updated from a call to the  UpdateDatasetGroup
      operation. While the dataset group is being updated, ``LastModificationTime`` is the current
      time of the ``ListDatasetGroups`` call.
    """


_ClientListDatasetGroupsResponseTypeDef = TypedDict(
    "_ClientListDatasetGroupsResponseTypeDef",
    {"DatasetGroups": List[ClientListDatasetGroupsResponseDatasetGroupsTypeDef], "NextToken": str},
    total=False,
)


class ClientListDatasetGroupsResponseTypeDef(_ClientListDatasetGroupsResponseTypeDef):
    """
    Type definition for `ClientListDatasetGroups` `Response`

    - **DatasetGroups** *(list) --*

      An array of objects that summarize each dataset group's properties.

      - *(dict) --*

        Provides a summary of the dataset group properties used in the  ListDatasetGroups operation.
        To get the complete set of properties, call the  DescribeDatasetGroup operation, and provide
        the ``DatasetGroupArn`` .

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group.

        - **DatasetGroupName** *(string) --*

          The name of the dataset group.

        - **CreationTime** *(datetime) --*

          When the dataset group was created.

        - **LastModificationTime** *(datetime) --*

          When the dataset group was created or last updated from a call to the  UpdateDatasetGroup
          operation. While the dataset group is being updated, ``LastModificationTime`` is the
          current time of the ``ListDatasetGroups`` call.

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ClientListDatasetImportJobsFiltersTypeDef = TypedDict(
    "_ClientListDatasetImportJobsFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ClientListDatasetImportJobsFiltersTypeDef(_ClientListDatasetImportJobsFiltersTypeDef):
    """
    Type definition for `ClientListDatasetImportJobs` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef = TypedDict(
    "_ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef(
    _ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef
):
    """
    Type definition for `ClientListDatasetImportJobsResponseDatasetImportJobsDataSource` `S3Config`

    The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
    along with the credentials to access the data.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef = TypedDict(
    "_ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef",
    {"S3Config": ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceS3ConfigTypeDef},
    total=False,
)


class ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef(
    _ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef
):
    """
    Type definition for `ClientListDatasetImportJobsResponseDatasetImportJobs` `DataSource`

    The location of the training data to import and an AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the data. The training data must be stored in an
    Amazon S3 bucket.

    If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

    - **S3Config** *(dict) --*

      The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
      along with the credentials to access the data.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef = TypedDict(
    "_ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef",
    {
        "DatasetImportJobArn": str,
        "DatasetImportJobName": str,
        "DataSource": ClientListDatasetImportJobsResponseDatasetImportJobsDataSourceTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef(
    _ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef
):
    """
    Type definition for `ClientListDatasetImportJobsResponse` `DatasetImportJobs`

    Provides a summary of the dataset import job properties used in the  ListDatasetImportJobs
    operation. To get the complete set of properties, call the  DescribeDatasetImportJob operation,
    and provide the ``DatasetImportJobArn`` .

    - **DatasetImportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset import job.

    - **DatasetImportJobName** *(string) --*

      The name of the dataset import job.

    - **DataSource** *(dict) --*

      The location of the training data to import and an AWS Identity and Access Management (IAM)
      role that Amazon Forecast can assume to access the data. The training data must be stored in
      an Amazon S3 bucket.

      If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

      - **S3Config** *(dict) --*

        The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
        along with the credentials to access the data.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

        - **KMSKeyArn** *(string) --*

          The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

    - **Status** *(string) --*

      The status of the dataset import job. The status is reflected in the status of the dataset.
      For example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of the dataset
      is ``UPDATE_IN_PROGRESS`` . States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the dataset import job was created.

    - **LastModificationTime** *(datetime) --*

      The last time that the dataset was modified. The time depends on the status of the job, as
      follows:

      * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

      * ``CREATE_IN_PROGRESS`` - The current timestamp.

      * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.
    """


_ClientListDatasetImportJobsResponseTypeDef = TypedDict(
    "_ClientListDatasetImportJobsResponseTypeDef",
    {
        "DatasetImportJobs": List[ClientListDatasetImportJobsResponseDatasetImportJobsTypeDef],
        "NextToken": str,
    },
    total=False,
)


class ClientListDatasetImportJobsResponseTypeDef(_ClientListDatasetImportJobsResponseTypeDef):
    """
    Type definition for `ClientListDatasetImportJobs` `Response`

    - **DatasetImportJobs** *(list) --*

      An array of objects that summarize each dataset import job's properties.

      - *(dict) --*

        Provides a summary of the dataset import job properties used in the  ListDatasetImportJobs
        operation. To get the complete set of properties, call the  DescribeDatasetImportJob
        operation, and provide the ``DatasetImportJobArn`` .

        - **DatasetImportJobArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset import job.

        - **DatasetImportJobName** *(string) --*

          The name of the dataset import job.

        - **DataSource** *(dict) --*

          The location of the training data to import and an AWS Identity and Access Management
          (IAM) role that Amazon Forecast can assume to access the data. The training data must be
          stored in an Amazon S3 bucket.

          If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

          - **S3Config** *(dict) --*

            The path to the training data stored in an Amazon Simple Storage Service (Amazon S3)
            bucket along with the credentials to access the data.

            - **Path** *(string) --*

              The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
              Amazon S3 bucket.

            - **RoleArn** *(string) --*

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        - **Status** *(string) --*

          The status of the dataset import job. The status is reflected in the status of the
          dataset. For example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of
          the dataset is ``UPDATE_IN_PROGRESS`` . States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the dataset import job was created.

        - **LastModificationTime** *(datetime) --*

          The last time that the dataset was modified. The time depends on the status of the job, as
          follows:

          * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

          * ``CREATE_IN_PROGRESS`` - The current timestamp.

          * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ClientListDatasetsResponseDatasetsTypeDef = TypedDict(
    "_ClientListDatasetsResponseDatasetsTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "DatasetType": str,
        "Domain": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListDatasetsResponseDatasetsTypeDef(_ClientListDatasetsResponseDatasetsTypeDef):
    """
    Type definition for `ClientListDatasetsResponse` `Datasets`

    Provides a summary of the dataset properties used in the  ListDatasets operation. To get the
    complete set of properties, call the  DescribeDataset operation, and provide the ``DatasetArn``
    .

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

      When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` . While
      data is being imported to the dataset, ``LastModificationTime`` is the current time of the
      ``ListDatasets`` call. After a  CreateDatasetImportJob operation has finished,
      ``LastModificationTime`` is when the import job completed or failed.
    """


_ClientListDatasetsResponseTypeDef = TypedDict(
    "_ClientListDatasetsResponseTypeDef",
    {"Datasets": List[ClientListDatasetsResponseDatasetsTypeDef], "NextToken": str},
    total=False,
)


class ClientListDatasetsResponseTypeDef(_ClientListDatasetsResponseTypeDef):
    """
    Type definition for `ClientListDatasets` `Response`

    - **Datasets** *(list) --*

      An array of objects that summarize each dataset's properties.

      - *(dict) --*

        Provides a summary of the dataset properties used in the  ListDatasets operation. To get the
        complete set of properties, call the  DescribeDataset operation, and provide the
        ``DatasetArn`` .

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

          When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` .
          While data is being imported to the dataset, ``LastModificationTime`` is the current time
          of the ``ListDatasets`` call. After a  CreateDatasetImportJob operation has finished,
          ``LastModificationTime`` is when the import job completed or failed.

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ClientListForecastExportJobsFiltersTypeDef = TypedDict(
    "_ClientListForecastExportJobsFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ClientListForecastExportJobsFiltersTypeDef(_ClientListForecastExportJobsFiltersTypeDef):
    """
    Type definition for `ClientListForecastExportJobs` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef = TypedDict(
    "_ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef(
    _ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef
):
    """
    Type definition for `ClientListForecastExportJobsResponseForecastExportJobsDestination`
    `S3Config`

    The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
    access the bucket.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef = TypedDict(
    "_ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef",
    {"S3Config": ClientListForecastExportJobsResponseForecastExportJobsDestinationS3ConfigTypeDef},
    total=False,
)


class ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef(
    _ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef
):
    """
    Type definition for `ClientListForecastExportJobsResponseForecastExportJobs` `Destination`

    The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is exported.

    - **S3Config** *(dict) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
      access the bucket.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ClientListForecastExportJobsResponseForecastExportJobsTypeDef = TypedDict(
    "_ClientListForecastExportJobsResponseForecastExportJobsTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "Destination": ClientListForecastExportJobsResponseForecastExportJobsDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListForecastExportJobsResponseForecastExportJobsTypeDef(
    _ClientListForecastExportJobsResponseForecastExportJobsTypeDef
):
    """
    Type definition for `ClientListForecastExportJobsResponse` `ForecastExportJobs`

    Provides a summary of the forecast export job properties used in the  ListForecastExportJobs
    operation. To get the complete set of properties, call the  DescribeForecastExportJob operation,
    and provide the listed ``ForecastExportJobArn`` .

    - **ForecastExportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the forecast export job.

    - **ForecastExportJobName** *(string) --*

      The name of the forecast export job.

    - **Destination** *(dict) --*

      The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is
      exported.

      - **S3Config** *(dict) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials
        to access the bucket.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

        - **KMSKeyArn** *(string) --*

          The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

    - **Status** *(string) --*

      The status of the forecast export job. States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

      .. note::

        The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
        forecast in your S3 bucket.

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the forecast export job was created.

    - **LastModificationTime** *(datetime) --*

      When the last successful export job finished.
    """


_ClientListForecastExportJobsResponseTypeDef = TypedDict(
    "_ClientListForecastExportJobsResponseTypeDef",
    {
        "ForecastExportJobs": List[ClientListForecastExportJobsResponseForecastExportJobsTypeDef],
        "NextToken": str,
    },
    total=False,
)


class ClientListForecastExportJobsResponseTypeDef(_ClientListForecastExportJobsResponseTypeDef):
    """
    Type definition for `ClientListForecastExportJobs` `Response`

    - **ForecastExportJobs** *(list) --*

      An array of objects that summarize each export job's properties.

      - *(dict) --*

        Provides a summary of the forecast export job properties used in the  ListForecastExportJobs
        operation. To get the complete set of properties, call the  DescribeForecastExportJob
        operation, and provide the listed ``ForecastExportJobArn`` .

        - **ForecastExportJobArn** *(string) --*

          The Amazon Resource Name (ARN) of the forecast export job.

        - **ForecastExportJobName** *(string) --*

          The name of the forecast export job.

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

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        - **Status** *(string) --*

          The status of the forecast export job. States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

          .. note::

            The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
            forecast in your S3 bucket.

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the forecast export job was created.

        - **LastModificationTime** *(datetime) --*

          When the last successful export job finished.

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ClientListForecastsFiltersTypeDef = TypedDict(
    "_ClientListForecastsFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ClientListForecastsFiltersTypeDef(_ClientListForecastsFiltersTypeDef):
    """
    Type definition for `ClientListForecasts` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ClientListForecastsResponseForecastsTypeDef = TypedDict(
    "_ClientListForecastsResponseForecastsTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListForecastsResponseForecastsTypeDef(_ClientListForecastsResponseForecastsTypeDef):
    """
    Type definition for `ClientListForecastsResponse` `Forecasts`

    Provides a summary of the forecast properties used in the  ListForecasts operation. To get the
    complete set of properties, call the  DescribeForecast operation, and provide the
    ``ForecastArn`` that is listed in the summary.

    - **ForecastArn** *(string) --*

      The ARN of the forecast.

    - **ForecastName** *(string) --*

      The name of the forecast.

    - **PredictorArn** *(string) --*

      The ARN of the predictor used to generate the forecast.

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group that provided the data used to train the
      predictor.

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
      inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ), and when
      inference is complete (status changed to ``ACTIVE`` ) or fails (status changed to
      ``CREATE_FAILED`` ).
    """


_ClientListForecastsResponseTypeDef = TypedDict(
    "_ClientListForecastsResponseTypeDef",
    {"Forecasts": List[ClientListForecastsResponseForecastsTypeDef], "NextToken": str},
    total=False,
)


class ClientListForecastsResponseTypeDef(_ClientListForecastsResponseTypeDef):
    """
    Type definition for `ClientListForecasts` `Response`

    - **Forecasts** *(list) --*

      An array of objects that summarize each forecast's properties.

      - *(dict) --*

        Provides a summary of the forecast properties used in the  ListForecasts operation. To get
        the complete set of properties, call the  DescribeForecast operation, and provide the
        ``ForecastArn`` that is listed in the summary.

        - **ForecastArn** *(string) --*

          The ARN of the forecast.

        - **ForecastName** *(string) --*

          The name of the forecast.

        - **PredictorArn** *(string) --*

          The ARN of the predictor used to generate the forecast.

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group that provided the data used to train
          the predictor.

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
          inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ), and
          when inference is complete (status changed to ``ACTIVE`` ) or fails (status changed to
          ``CREATE_FAILED`` ).

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ClientListPredictorsFiltersTypeDef = TypedDict(
    "_ClientListPredictorsFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ClientListPredictorsFiltersTypeDef(_ClientListPredictorsFiltersTypeDef):
    """
    Type definition for `ClientListPredictors` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ClientListPredictorsResponsePredictorsTypeDef = TypedDict(
    "_ClientListPredictorsResponsePredictorsTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ClientListPredictorsResponsePredictorsTypeDef(_ClientListPredictorsResponsePredictorsTypeDef):
    """
    Type definition for `ClientListPredictorsResponse` `Predictors`

    Provides a summary of the predictor properties that are used in the  ListPredictors operation.
    To get the complete set of properties, call the  DescribePredictor operation, and provide the
    listed ``PredictorArn`` .

    - **PredictorArn** *(string) --*

      The ARN of the predictor.

    - **PredictorName** *(string) --*

      The name of the predictor.

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group that contains the data used to train the
      predictor.

    - **Status** *(string) --*

      The status of the predictor. States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

      * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

      .. note::

        The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor to
        create a forecast.

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the model training task was created.

    - **LastModificationTime** *(datetime) --*

      Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated when training
      starts (status changed to ``CREATE_IN_PROGRESS`` ), and when training is complete (status
      changed to ``ACTIVE`` ) or fails (status changed to ``CREATE_FAILED`` ).
    """


_ClientListPredictorsResponseTypeDef = TypedDict(
    "_ClientListPredictorsResponseTypeDef",
    {"Predictors": List[ClientListPredictorsResponsePredictorsTypeDef], "NextToken": str},
    total=False,
)


class ClientListPredictorsResponseTypeDef(_ClientListPredictorsResponseTypeDef):
    """
    Type definition for `ClientListPredictors` `Response`

    - **Predictors** *(list) --*

      An array of objects that summarize each predictor's properties.

      - *(dict) --*

        Provides a summary of the predictor properties that are used in the  ListPredictors
        operation. To get the complete set of properties, call the  DescribePredictor operation, and
        provide the listed ``PredictorArn`` .

        - **PredictorArn** *(string) --*

          The ARN of the predictor.

        - **PredictorName** *(string) --*

          The name of the predictor.

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group that contains the data used to train
          the predictor.

        - **Status** *(string) --*

          The status of the predictor. States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

          * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

          .. note::

            The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor to
            create a forecast.

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the model training task was created.

        - **LastModificationTime** *(datetime) --*

          Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated when
          training starts (status changed to ``CREATE_IN_PROGRESS`` ), and when training is complete
          (status changed to ``ACTIVE`` ) or fails (status changed to ``CREATE_FAILED`` ).

    - **NextToken** *(string) --*

      If the response is truncated, Amazon Forecast returns this token. To retrieve the next set of
      results, use the token in the next request.
    """


_ListDatasetGroupsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListDatasetGroupsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListDatasetGroupsPaginatePaginationConfigTypeDef(
    _ListDatasetGroupsPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListDatasetGroupsPaginate` `PaginationConfig`

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


_ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef = TypedDict(
    "_ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef",
    {
        "DatasetGroupArn": str,
        "DatasetGroupName": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef(
    _ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef
):
    """
    Type definition for `ListDatasetGroupsPaginateResponse` `DatasetGroups`

    Provides a summary of the dataset group properties used in the  ListDatasetGroups operation. To
    get the complete set of properties, call the  DescribeDatasetGroup operation, and provide the
    ``DatasetGroupArn`` .

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group.

    - **DatasetGroupName** *(string) --*

      The name of the dataset group.

    - **CreationTime** *(datetime) --*

      When the dataset group was created.

    - **LastModificationTime** *(datetime) --*

      When the dataset group was created or last updated from a call to the  UpdateDatasetGroup
      operation. While the dataset group is being updated, ``LastModificationTime`` is the current
      time of the ``ListDatasetGroups`` call.
    """


_ListDatasetGroupsPaginateResponseTypeDef = TypedDict(
    "_ListDatasetGroupsPaginateResponseTypeDef",
    {"DatasetGroups": List[ListDatasetGroupsPaginateResponseDatasetGroupsTypeDef]},
    total=False,
)


class ListDatasetGroupsPaginateResponseTypeDef(_ListDatasetGroupsPaginateResponseTypeDef):
    """
    Type definition for `ListDatasetGroupsPaginate` `Response`

    - **DatasetGroups** *(list) --*

      An array of objects that summarize each dataset group's properties.

      - *(dict) --*

        Provides a summary of the dataset group properties used in the  ListDatasetGroups operation.
        To get the complete set of properties, call the  DescribeDatasetGroup operation, and provide
        the ``DatasetGroupArn`` .

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group.

        - **DatasetGroupName** *(string) --*

          The name of the dataset group.

        - **CreationTime** *(datetime) --*

          When the dataset group was created.

        - **LastModificationTime** *(datetime) --*

          When the dataset group was created or last updated from a call to the  UpdateDatasetGroup
          operation. While the dataset group is being updated, ``LastModificationTime`` is the
          current time of the ``ListDatasetGroups`` call.
    """


_ListDatasetImportJobsPaginateFiltersTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginateFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ListDatasetImportJobsPaginateFiltersTypeDef(_ListDatasetImportJobsPaginateFiltersTypeDef):
    """
    Type definition for `ListDatasetImportJobsPaginate` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ListDatasetImportJobsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListDatasetImportJobsPaginatePaginationConfigTypeDef(
    _ListDatasetImportJobsPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListDatasetImportJobsPaginate` `PaginationConfig`

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


_ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef(
    _ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef
):
    """
    Type definition for `ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSource`
    `S3Config`

    The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
    along with the credentials to access the data.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef",
    {"S3Config": ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceS3ConfigTypeDef},
    total=False,
)


class ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef(
    _ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef
):
    """
    Type definition for `ListDatasetImportJobsPaginateResponseDatasetImportJobs` `DataSource`

    The location of the training data to import and an AWS Identity and Access Management (IAM) role
    that Amazon Forecast can assume to access the data. The training data must be stored in an
    Amazon S3 bucket.

    If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

    - **S3Config** *(dict) --*

      The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
      along with the credentials to access the data.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef",
    {
        "DatasetImportJobArn": str,
        "DatasetImportJobName": str,
        "DataSource": ListDatasetImportJobsPaginateResponseDatasetImportJobsDataSourceTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef(
    _ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef
):
    """
    Type definition for `ListDatasetImportJobsPaginateResponse` `DatasetImportJobs`

    Provides a summary of the dataset import job properties used in the  ListDatasetImportJobs
    operation. To get the complete set of properties, call the  DescribeDatasetImportJob operation,
    and provide the ``DatasetImportJobArn`` .

    - **DatasetImportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset import job.

    - **DatasetImportJobName** *(string) --*

      The name of the dataset import job.

    - **DataSource** *(dict) --*

      The location of the training data to import and an AWS Identity and Access Management (IAM)
      role that Amazon Forecast can assume to access the data. The training data must be stored in
      an Amazon S3 bucket.

      If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

      - **S3Config** *(dict) --*

        The path to the training data stored in an Amazon Simple Storage Service (Amazon S3) bucket
        along with the credentials to access the data.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

        - **KMSKeyArn** *(string) --*

          The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

    - **Status** *(string) --*

      The status of the dataset import job. The status is reflected in the status of the dataset.
      For example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of the dataset
      is ``UPDATE_IN_PROGRESS`` . States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the dataset import job was created.

    - **LastModificationTime** *(datetime) --*

      The last time that the dataset was modified. The time depends on the status of the job, as
      follows:

      * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

      * ``CREATE_IN_PROGRESS`` - The current timestamp.

      * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.
    """


_ListDatasetImportJobsPaginateResponseTypeDef = TypedDict(
    "_ListDatasetImportJobsPaginateResponseTypeDef",
    {"DatasetImportJobs": List[ListDatasetImportJobsPaginateResponseDatasetImportJobsTypeDef]},
    total=False,
)


class ListDatasetImportJobsPaginateResponseTypeDef(_ListDatasetImportJobsPaginateResponseTypeDef):
    """
    Type definition for `ListDatasetImportJobsPaginate` `Response`

    - **DatasetImportJobs** *(list) --*

      An array of objects that summarize each dataset import job's properties.

      - *(dict) --*

        Provides a summary of the dataset import job properties used in the  ListDatasetImportJobs
        operation. To get the complete set of properties, call the  DescribeDatasetImportJob
        operation, and provide the ``DatasetImportJobArn`` .

        - **DatasetImportJobArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset import job.

        - **DatasetImportJobName** *(string) --*

          The name of the dataset import job.

        - **DataSource** *(dict) --*

          The location of the training data to import and an AWS Identity and Access Management
          (IAM) role that Amazon Forecast can assume to access the data. The training data must be
          stored in an Amazon S3 bucket.

          If encryption is used, ``DataSource`` includes an AWS Key Management Service (KMS) key.

          - **S3Config** *(dict) --*

            The path to the training data stored in an Amazon Simple Storage Service (Amazon S3)
            bucket along with the credentials to access the data.

            - **Path** *(string) --*

              The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an
              Amazon S3 bucket.

            - **RoleArn** *(string) --*

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        - **Status** *(string) --*

          The status of the dataset import job. The status is reflected in the status of the
          dataset. For example, when the import job status is ``CREATE_IN_PROGRESS`` , the status of
          the dataset is ``UPDATE_IN_PROGRESS`` . States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the dataset import job was created.

        - **LastModificationTime** *(datetime) --*

          The last time that the dataset was modified. The time depends on the status of the job, as
          follows:

          * ``CREATE_PENDING`` - The same time as ``CreationTime`` .

          * ``CREATE_IN_PROGRESS`` - The current timestamp.

          * ``ACTIVE`` or ``CREATE_FAILED`` - When the job finished or failed.
    """


_ListDatasetsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListDatasetsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListDatasetsPaginatePaginationConfigTypeDef(_ListDatasetsPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListDatasetsPaginate` `PaginationConfig`

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


_ListDatasetsPaginateResponseDatasetsTypeDef = TypedDict(
    "_ListDatasetsPaginateResponseDatasetsTypeDef",
    {
        "DatasetArn": str,
        "DatasetName": str,
        "DatasetType": str,
        "Domain": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListDatasetsPaginateResponseDatasetsTypeDef(_ListDatasetsPaginateResponseDatasetsTypeDef):
    """
    Type definition for `ListDatasetsPaginateResponse` `Datasets`

    Provides a summary of the dataset properties used in the  ListDatasets operation. To get the
    complete set of properties, call the  DescribeDataset operation, and provide the ``DatasetArn``
    .

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

      When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` . While
      data is being imported to the dataset, ``LastModificationTime`` is the current time of the
      ``ListDatasets`` call. After a  CreateDatasetImportJob operation has finished,
      ``LastModificationTime`` is when the import job completed or failed.
    """


_ListDatasetsPaginateResponseTypeDef = TypedDict(
    "_ListDatasetsPaginateResponseTypeDef",
    {"Datasets": List[ListDatasetsPaginateResponseDatasetsTypeDef]},
    total=False,
)


class ListDatasetsPaginateResponseTypeDef(_ListDatasetsPaginateResponseTypeDef):
    """
    Type definition for `ListDatasetsPaginate` `Response`

    - **Datasets** *(list) --*

      An array of objects that summarize each dataset's properties.

      - *(dict) --*

        Provides a summary of the dataset properties used in the  ListDatasets operation. To get the
        complete set of properties, call the  DescribeDataset operation, and provide the
        ``DatasetArn`` .

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

          When you create a dataset, ``LastModificationTime`` is the same as ``CreationTime`` .
          While data is being imported to the dataset, ``LastModificationTime`` is the current time
          of the ``ListDatasets`` call. After a  CreateDatasetImportJob operation has finished,
          ``LastModificationTime`` is when the import job completed or failed.
    """


_ListForecastExportJobsPaginateFiltersTypeDef = TypedDict(
    "_ListForecastExportJobsPaginateFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ListForecastExportJobsPaginateFiltersTypeDef(_ListForecastExportJobsPaginateFiltersTypeDef):
    """
    Type definition for `ListForecastExportJobsPaginate` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ListForecastExportJobsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListForecastExportJobsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListForecastExportJobsPaginatePaginationConfigTypeDef(
    _ListForecastExportJobsPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListForecastExportJobsPaginate` `PaginationConfig`

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


_ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef = TypedDict(
    "_ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef",
    {"Path": str, "RoleArn": str, "KMSKeyArn": str},
    total=False,
)


class ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef(
    _ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef
):
    """
    Type definition for `ListForecastExportJobsPaginateResponseForecastExportJobsDestination`
    `S3Config`

    The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
    access the bucket.

    - **Path** *(string) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
      bucket.

    - **RoleArn** *(string) --*

      The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
      to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key, the
      role must allow access to the key.

      Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
      account, you get an ``InvalidInputException`` error.

    - **KMSKeyArn** *(string) --*

      The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef = TypedDict(
    "_ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef",
    {
        "S3Config": ListForecastExportJobsPaginateResponseForecastExportJobsDestinationS3ConfigTypeDef
    },
    total=False,
)


class ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef(
    _ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef
):
    """
    Type definition for `ListForecastExportJobsPaginateResponseForecastExportJobs` `Destination`

    The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is exported.

    - **S3Config** *(dict) --*

      The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials to
      access the bucket.

      - **Path** *(string) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
        bucket.

      - **RoleArn** *(string) --*

        The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can assume
        to access the Amazon S3 bucket or files. If you provide a value for the ``KMSKeyArn`` key,
        the role must allow access to the key.

        Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
        account, you get an ``InvalidInputException`` error.

      - **KMSKeyArn** *(string) --*

        The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.
    """


_ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef = TypedDict(
    "_ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef",
    {
        "ForecastExportJobArn": str,
        "ForecastExportJobName": str,
        "Destination": ListForecastExportJobsPaginateResponseForecastExportJobsDestinationTypeDef,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef(
    _ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef
):
    """
    Type definition for `ListForecastExportJobsPaginateResponse` `ForecastExportJobs`

    Provides a summary of the forecast export job properties used in the  ListForecastExportJobs
    operation. To get the complete set of properties, call the  DescribeForecastExportJob operation,
    and provide the listed ``ForecastExportJobArn`` .

    - **ForecastExportJobArn** *(string) --*

      The Amazon Resource Name (ARN) of the forecast export job.

    - **ForecastExportJobName** *(string) --*

      The name of the forecast export job.

    - **Destination** *(dict) --*

      The path to the Amazon Simple Storage Service (Amazon S3) bucket where the forecast is
      exported.

      - **S3Config** *(dict) --*

        The path to an Amazon Simple Storage Service (Amazon S3) bucket along with the credentials
        to access the bucket.

        - **Path** *(string) --*

          The path to an Amazon Simple Storage Service (Amazon S3) bucket or file(s) in an Amazon S3
          bucket.

        - **RoleArn** *(string) --*

          The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
          assume to access the Amazon S3 bucket or files. If you provide a value for the
          ``KMSKeyArn`` key, the role must allow access to the key.

          Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your
          account, you get an ``InvalidInputException`` error.

        - **KMSKeyArn** *(string) --*

          The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

    - **Status** *(string) --*

      The status of the forecast export job. States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

      .. note::

        The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
        forecast in your S3 bucket.

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the forecast export job was created.

    - **LastModificationTime** *(datetime) --*

      When the last successful export job finished.
    """


_ListForecastExportJobsPaginateResponseTypeDef = TypedDict(
    "_ListForecastExportJobsPaginateResponseTypeDef",
    {"ForecastExportJobs": List[ListForecastExportJobsPaginateResponseForecastExportJobsTypeDef]},
    total=False,
)


class ListForecastExportJobsPaginateResponseTypeDef(_ListForecastExportJobsPaginateResponseTypeDef):
    """
    Type definition for `ListForecastExportJobsPaginate` `Response`

    - **ForecastExportJobs** *(list) --*

      An array of objects that summarize each export job's properties.

      - *(dict) --*

        Provides a summary of the forecast export job properties used in the  ListForecastExportJobs
        operation. To get the complete set of properties, call the  DescribeForecastExportJob
        operation, and provide the listed ``ForecastExportJobArn`` .

        - **ForecastExportJobArn** *(string) --*

          The Amazon Resource Name (ARN) of the forecast export job.

        - **ForecastExportJobName** *(string) --*

          The name of the forecast export job.

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

              The ARN of the AWS Identity and Access Management (IAM) role that Amazon Forecast can
              assume to access the Amazon S3 bucket or files. If you provide a value for the
              ``KMSKeyArn`` key, the role must allow access to the key.

              Passing a role across AWS accounts is not allowed. If you pass a role that isn't in
              your account, you get an ``InvalidInputException`` error.

            - **KMSKeyArn** *(string) --*

              The Amazon Resource Name (ARN) of an AWS Key Management Service (KMS) key.

        - **Status** *(string) --*

          The status of the forecast export job. States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

          .. note::

            The ``Status`` of the forecast export job must be ``ACTIVE`` before you can access the
            forecast in your S3 bucket.

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the forecast export job was created.

        - **LastModificationTime** *(datetime) --*

          When the last successful export job finished.
    """


_ListForecastsPaginateFiltersTypeDef = TypedDict(
    "_ListForecastsPaginateFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ListForecastsPaginateFiltersTypeDef(_ListForecastsPaginateFiltersTypeDef):
    """
    Type definition for `ListForecastsPaginate` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ListForecastsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListForecastsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListForecastsPaginatePaginationConfigTypeDef(_ListForecastsPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListForecastsPaginate` `PaginationConfig`

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


_ListForecastsPaginateResponseForecastsTypeDef = TypedDict(
    "_ListForecastsPaginateResponseForecastsTypeDef",
    {
        "ForecastArn": str,
        "ForecastName": str,
        "PredictorArn": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListForecastsPaginateResponseForecastsTypeDef(_ListForecastsPaginateResponseForecastsTypeDef):
    """
    Type definition for `ListForecastsPaginateResponse` `Forecasts`

    Provides a summary of the forecast properties used in the  ListForecasts operation. To get the
    complete set of properties, call the  DescribeForecast operation, and provide the
    ``ForecastArn`` that is listed in the summary.

    - **ForecastArn** *(string) --*

      The ARN of the forecast.

    - **ForecastName** *(string) --*

      The name of the forecast.

    - **PredictorArn** *(string) --*

      The ARN of the predictor used to generate the forecast.

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group that provided the data used to train the
      predictor.

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
      inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ), and when
      inference is complete (status changed to ``ACTIVE`` ) or fails (status changed to
      ``CREATE_FAILED`` ).
    """


_ListForecastsPaginateResponseTypeDef = TypedDict(
    "_ListForecastsPaginateResponseTypeDef",
    {"Forecasts": List[ListForecastsPaginateResponseForecastsTypeDef]},
    total=False,
)


class ListForecastsPaginateResponseTypeDef(_ListForecastsPaginateResponseTypeDef):
    """
    Type definition for `ListForecastsPaginate` `Response`

    - **Forecasts** *(list) --*

      An array of objects that summarize each forecast's properties.

      - *(dict) --*

        Provides a summary of the forecast properties used in the  ListForecasts operation. To get
        the complete set of properties, call the  DescribeForecast operation, and provide the
        ``ForecastArn`` that is listed in the summary.

        - **ForecastArn** *(string) --*

          The ARN of the forecast.

        - **ForecastName** *(string) --*

          The name of the forecast.

        - **PredictorArn** *(string) --*

          The ARN of the predictor used to generate the forecast.

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group that provided the data used to train
          the predictor.

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
          inference (creating the forecast) starts (status changed to ``CREATE_IN_PROGRESS`` ), and
          when inference is complete (status changed to ``ACTIVE`` ) or fails (status changed to
          ``CREATE_FAILED`` ).
    """


_ListPredictorsPaginateFiltersTypeDef = TypedDict(
    "_ListPredictorsPaginateFiltersTypeDef", {"Key": str, "Value": str, "Condition": str}
)


class ListPredictorsPaginateFiltersTypeDef(_ListPredictorsPaginateFiltersTypeDef):
    """
    Type definition for `ListPredictorsPaginate` `Filters`

    Describes a filter for choosing a subset of objects. Each filter consists of a condition and a
    match statement. The condition is either ``IS`` or ``IS_NOT`` , which specifies whether to
    include or exclude the objects that match the statement, respectively. The match statement
    consists of a key and a value.

    - **Key** *(string) --* **[REQUIRED]**

      The name of the parameter to filter on.

    - **Value** *(string) --* **[REQUIRED]**

      The value to match.

    - **Condition** *(string) --* **[REQUIRED]**

      The condition to apply. To include the objects that match the statement, specify ``IS`` . To
      exclude matching objects, specify ``IS_NOT`` .
    """


_ListPredictorsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListPredictorsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListPredictorsPaginatePaginationConfigTypeDef(_ListPredictorsPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListPredictorsPaginate` `PaginationConfig`

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


_ListPredictorsPaginateResponsePredictorsTypeDef = TypedDict(
    "_ListPredictorsPaginateResponsePredictorsTypeDef",
    {
        "PredictorArn": str,
        "PredictorName": str,
        "DatasetGroupArn": str,
        "Status": str,
        "Message": str,
        "CreationTime": datetime,
        "LastModificationTime": datetime,
    },
    total=False,
)


class ListPredictorsPaginateResponsePredictorsTypeDef(
    _ListPredictorsPaginateResponsePredictorsTypeDef
):
    """
    Type definition for `ListPredictorsPaginateResponse` `Predictors`

    Provides a summary of the predictor properties that are used in the  ListPredictors operation.
    To get the complete set of properties, call the  DescribePredictor operation, and provide the
    listed ``PredictorArn`` .

    - **PredictorArn** *(string) --*

      The ARN of the predictor.

    - **PredictorName** *(string) --*

      The name of the predictor.

    - **DatasetGroupArn** *(string) --*

      The Amazon Resource Name (ARN) of the dataset group that contains the data used to train the
      predictor.

    - **Status** *(string) --*

      The status of the predictor. States include:

      * ``ACTIVE``

      * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

      * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

      * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

      .. note::

        The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor to
        create a forecast.

    - **Message** *(string) --*

      If an error occurred, an informational message about the error.

    - **CreationTime** *(datetime) --*

      When the model training task was created.

    - **LastModificationTime** *(datetime) --*

      Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated when training
      starts (status changed to ``CREATE_IN_PROGRESS`` ), and when training is complete (status
      changed to ``ACTIVE`` ) or fails (status changed to ``CREATE_FAILED`` ).
    """


_ListPredictorsPaginateResponseTypeDef = TypedDict(
    "_ListPredictorsPaginateResponseTypeDef",
    {"Predictors": List[ListPredictorsPaginateResponsePredictorsTypeDef]},
    total=False,
)


class ListPredictorsPaginateResponseTypeDef(_ListPredictorsPaginateResponseTypeDef):
    """
    Type definition for `ListPredictorsPaginate` `Response`

    - **Predictors** *(list) --*

      An array of objects that summarize each predictor's properties.

      - *(dict) --*

        Provides a summary of the predictor properties that are used in the  ListPredictors
        operation. To get the complete set of properties, call the  DescribePredictor operation, and
        provide the listed ``PredictorArn`` .

        - **PredictorArn** *(string) --*

          The ARN of the predictor.

        - **PredictorName** *(string) --*

          The name of the predictor.

        - **DatasetGroupArn** *(string) --*

          The Amazon Resource Name (ARN) of the dataset group that contains the data used to train
          the predictor.

        - **Status** *(string) --*

          The status of the predictor. States include:

          * ``ACTIVE``

          * ``CREATE_PENDING`` , ``CREATE_IN_PROGRESS`` , ``CREATE_FAILED``

          * ``DELETE_PENDING`` , ``DELETE_IN_PROGRESS`` , ``DELETE_FAILED``

          * ``UPDATE_PENDING`` , ``UPDATE_IN_PROGRESS`` , ``UPDATE_FAILED``

          .. note::

            The ``Status`` of the predictor must be ``ACTIVE`` before you can use the predictor to
            create a forecast.

        - **Message** *(string) --*

          If an error occurred, an informational message about the error.

        - **CreationTime** *(datetime) --*

          When the model training task was created.

        - **LastModificationTime** *(datetime) --*

          Initially, the same as ``CreationTime`` (status is ``CREATE_PENDING`` ). Updated when
          training starts (status changed to ``CREATE_IN_PROGRESS`` ), and when training is complete
          (status changed to ``ACTIVE`` ) or fails (status changed to ``CREATE_FAILED`` ).
    """
