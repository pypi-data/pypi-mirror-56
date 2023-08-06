"Main interface for application-insights type defs"
from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientCreateApplicationResponseApplicationInfoTypeDef",
    "ClientCreateApplicationResponseTypeDef",
    "ClientCreateApplicationTagsTypeDef",
    "ClientCreateLogPatternResponseLogPatternTypeDef",
    "ClientCreateLogPatternResponseTypeDef",
    "ClientDescribeApplicationResponseApplicationInfoTypeDef",
    "ClientDescribeApplicationResponseTypeDef",
    "ClientDescribeComponentConfigurationRecommendationResponseTypeDef",
    "ClientDescribeComponentConfigurationResponseTypeDef",
    "ClientDescribeComponentResponseApplicationComponentTypeDef",
    "ClientDescribeComponentResponseTypeDef",
    "ClientDescribeLogPatternResponseLogPatternTypeDef",
    "ClientDescribeLogPatternResponseTypeDef",
    "ClientDescribeObservationResponseObservationTypeDef",
    "ClientDescribeObservationResponseTypeDef",
    "ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef",
    "ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef",
    "ClientDescribeProblemObservationsResponseTypeDef",
    "ClientDescribeProblemResponseProblemTypeDef",
    "ClientDescribeProblemResponseTypeDef",
    "ClientListApplicationsResponseApplicationInfoListTypeDef",
    "ClientListApplicationsResponseTypeDef",
    "ClientListComponentsResponseApplicationComponentListTypeDef",
    "ClientListComponentsResponseTypeDef",
    "ClientListLogPatternSetsResponseTypeDef",
    "ClientListLogPatternsResponseLogPatternsTypeDef",
    "ClientListLogPatternsResponseTypeDef",
    "ClientListProblemsResponseProblemListTypeDef",
    "ClientListProblemsResponseTypeDef",
    "ClientListTagsForResourceResponseTagsTypeDef",
    "ClientListTagsForResourceResponseTypeDef",
    "ClientTagResourceTagsTypeDef",
    "ClientUpdateApplicationResponseApplicationInfoTypeDef",
    "ClientUpdateApplicationResponseTypeDef",
    "ClientUpdateLogPatternResponseLogPatternTypeDef",
    "ClientUpdateLogPatternResponseTypeDef",
)


_ClientCreateApplicationResponseApplicationInfoTypeDef = TypedDict(
    "_ClientCreateApplicationResponseApplicationInfoTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "Remarks": str,
    },
    total=False,
)


class ClientCreateApplicationResponseApplicationInfoTypeDef(
    _ClientCreateApplicationResponseApplicationInfoTypeDef
):
    """
    Type definition for `ClientCreateApplicationResponse` `ApplicationInfo`

    Information about the application.

    - **ResourceGroupName** *(string) --*

      The name of the resource group used for the application.

    - **LifeCycle** *(string) --*

      The lifecycle of the application.

    - **OpsItemSNSTopicArn** *(string) --*

      The SNS topic provided to Application Insights that is associated to the created opsItems to
      receive SNS notifications for opsItem updates.

    - **OpsCenterEnabled** *(boolean) --*

      Indicates whether Application Insights will create opsItems for any problem detected by
      Application Insights for an application.

    - **Remarks** *(string) --*

      The issues on the user side that block Application Insights from successfully monitoring an
      application.
    """


_ClientCreateApplicationResponseTypeDef = TypedDict(
    "_ClientCreateApplicationResponseTypeDef",
    {"ApplicationInfo": ClientCreateApplicationResponseApplicationInfoTypeDef},
    total=False,
)


class ClientCreateApplicationResponseTypeDef(_ClientCreateApplicationResponseTypeDef):
    """
    Type definition for `ClientCreateApplication` `Response`

    - **ApplicationInfo** *(dict) --*

      Information about the application.

      - **ResourceGroupName** *(string) --*

        The name of the resource group used for the application.

      - **LifeCycle** *(string) --*

        The lifecycle of the application.

      - **OpsItemSNSTopicArn** *(string) --*

        The SNS topic provided to Application Insights that is associated to the created opsItems to
        receive SNS notifications for opsItem updates.

      - **OpsCenterEnabled** *(boolean) --*

        Indicates whether Application Insights will create opsItems for any problem detected by
        Application Insights for an application.

      - **Remarks** *(string) --*

        The issues on the user side that block Application Insights from successfully monitoring an
        application.
    """


_ClientCreateApplicationTagsTypeDef = TypedDict(
    "_ClientCreateApplicationTagsTypeDef", {"Key": str, "Value": str}
)


class ClientCreateApplicationTagsTypeDef(_ClientCreateApplicationTagsTypeDef):
    """
    Type definition for `ClientCreateApplication` `Tags`

    An object that defines the tags associated with an application. A *tag* is a label that you
    optionally define and associate with an application. Tags can help you categorize and manage
    resources in different ways, such as by purpose, owner, environment, or other criteria.

    Each tag consists of a required *tag key* and an associated *tag value* , both of which you
    define. A tag key is a general label that acts as a category for a more specific tag value. A
    tag value acts as a descriptor within a tag key. A tag key can contain as many as 128
    characters. A tag value can contain as many as 256 characters. The characters can be Unicode
    letters, digits, white space, or one of the following symbols: _ . : / = + -. The following
    additional restrictions apply to tags:

    * Tag keys and values are case sensitive.

    * For each associated resource, each tag key must be unique and it can have only one value.

    * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or values
    that you define. In addition, you can't edit or remove tag keys or values that use this prefix.

    - **Key** *(string) --* **[REQUIRED]**

      One part of a key-value pair that defines a tag. The maximum length of a tag key is 128
      characters. The minimum length is 1 character.

    - **Value** *(string) --* **[REQUIRED]**

      The optional part of a key-value pair that defines a tag. The maximum length of a tag value is
      256 characters. The minimum length is 0 characters. If you don't want an application to have a
      specific tag value, don't specify a value for this parameter.
    """


_ClientCreateLogPatternResponseLogPatternTypeDef = TypedDict(
    "_ClientCreateLogPatternResponseLogPatternTypeDef",
    {"PatternSetName": str, "PatternName": str, "Pattern": str, "Rank": int},
    total=False,
)


class ClientCreateLogPatternResponseLogPatternTypeDef(
    _ClientCreateLogPatternResponseLogPatternTypeDef
):
    """
    Type definition for `ClientCreateLogPatternResponse` `LogPattern`

    The successfully created log pattern.

    - **PatternSetName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 30 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **PatternName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 50 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **Pattern** *(string) --*

      A regular expression that defines the log pattern. A log pattern can contains at many as 50
      characters, and it cannot be empty.

    - **Rank** *(integer) --*

      Rank of the log pattern.
    """


_ClientCreateLogPatternResponseTypeDef = TypedDict(
    "_ClientCreateLogPatternResponseTypeDef",
    {"LogPattern": ClientCreateLogPatternResponseLogPatternTypeDef, "ResourceGroupName": str},
    total=False,
)


class ClientCreateLogPatternResponseTypeDef(_ClientCreateLogPatternResponseTypeDef):
    """
    Type definition for `ClientCreateLogPattern` `Response`

    - **LogPattern** *(dict) --*

      The successfully created log pattern.

      - **PatternSetName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 30 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **PatternName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 50 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **Pattern** *(string) --*

        A regular expression that defines the log pattern. A log pattern can contains at many as 50
        characters, and it cannot be empty.

      - **Rank** *(integer) --*

        Rank of the log pattern.

    - **ResourceGroupName** *(string) --*

      The name of the resource group.
    """


_ClientDescribeApplicationResponseApplicationInfoTypeDef = TypedDict(
    "_ClientDescribeApplicationResponseApplicationInfoTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "Remarks": str,
    },
    total=False,
)


class ClientDescribeApplicationResponseApplicationInfoTypeDef(
    _ClientDescribeApplicationResponseApplicationInfoTypeDef
):
    """
    Type definition for `ClientDescribeApplicationResponse` `ApplicationInfo`

    Information about the application.

    - **ResourceGroupName** *(string) --*

      The name of the resource group used for the application.

    - **LifeCycle** *(string) --*

      The lifecycle of the application.

    - **OpsItemSNSTopicArn** *(string) --*

      The SNS topic provided to Application Insights that is associated to the created opsItems to
      receive SNS notifications for opsItem updates.

    - **OpsCenterEnabled** *(boolean) --*

      Indicates whether Application Insights will create opsItems for any problem detected by
      Application Insights for an application.

    - **Remarks** *(string) --*

      The issues on the user side that block Application Insights from successfully monitoring an
      application.
    """


_ClientDescribeApplicationResponseTypeDef = TypedDict(
    "_ClientDescribeApplicationResponseTypeDef",
    {"ApplicationInfo": ClientDescribeApplicationResponseApplicationInfoTypeDef},
    total=False,
)


class ClientDescribeApplicationResponseTypeDef(_ClientDescribeApplicationResponseTypeDef):
    """
    Type definition for `ClientDescribeApplication` `Response`

    - **ApplicationInfo** *(dict) --*

      Information about the application.

      - **ResourceGroupName** *(string) --*

        The name of the resource group used for the application.

      - **LifeCycle** *(string) --*

        The lifecycle of the application.

      - **OpsItemSNSTopicArn** *(string) --*

        The SNS topic provided to Application Insights that is associated to the created opsItems to
        receive SNS notifications for opsItem updates.

      - **OpsCenterEnabled** *(boolean) --*

        Indicates whether Application Insights will create opsItems for any problem detected by
        Application Insights for an application.

      - **Remarks** *(string) --*

        The issues on the user side that block Application Insights from successfully monitoring an
        application.
    """


_ClientDescribeComponentConfigurationRecommendationResponseTypeDef = TypedDict(
    "_ClientDescribeComponentConfigurationRecommendationResponseTypeDef",
    {"ComponentConfiguration": str},
    total=False,
)


class ClientDescribeComponentConfigurationRecommendationResponseTypeDef(
    _ClientDescribeComponentConfigurationRecommendationResponseTypeDef
):
    """
    Type definition for `ClientDescribeComponentConfigurationRecommendation` `Response`

    - **ComponentConfiguration** *(string) --*

      The recommended configuration settings of the component. The value is the escaped JSON of the
      configuration.
    """


_ClientDescribeComponentConfigurationResponseTypeDef = TypedDict(
    "_ClientDescribeComponentConfigurationResponseTypeDef",
    {"Monitor": bool, "Tier": str, "ComponentConfiguration": str},
    total=False,
)


class ClientDescribeComponentConfigurationResponseTypeDef(
    _ClientDescribeComponentConfigurationResponseTypeDef
):
    """
    Type definition for `ClientDescribeComponentConfiguration` `Response`

    - **Monitor** *(boolean) --*

      Indicates whether the application component is monitored.

    - **Tier** *(string) --*

      The tier of the application component. Supported tiers include ``DOT_NET_CORE`` ,
      ``DOT_NET_WORKER`` , ``DOT_NET_WEB`` , ``SQL_SERVER`` , and ``DEFAULT``

    - **ComponentConfiguration** *(string) --*

      The configuration settings of the component. The value is the escaped JSON of the
      configuration.
    """


_ClientDescribeComponentResponseApplicationComponentTypeDef = TypedDict(
    "_ClientDescribeComponentResponseApplicationComponentTypeDef",
    {"ComponentName": str, "ResourceType": str, "Tier": str, "Monitor": bool},
    total=False,
)


class ClientDescribeComponentResponseApplicationComponentTypeDef(
    _ClientDescribeComponentResponseApplicationComponentTypeDef
):
    """
    Type definition for `ClientDescribeComponentResponse` `ApplicationComponent`

    Describes a standalone resource or similarly grouped resources that the application is made up
    of.

    - **ComponentName** *(string) --*

      The name of the component.

    - **ResourceType** *(string) --*

      The resource type. Supported resource types include EC2 instances, Auto Scaling group, Classic
      ELB, Application ELB, and SQS Queue.

    - **Tier** *(string) --*

      The stack tier of the application component.

    - **Monitor** *(boolean) --*

      Indicates whether the application component is monitored.
    """


_ClientDescribeComponentResponseTypeDef = TypedDict(
    "_ClientDescribeComponentResponseTypeDef",
    {
        "ApplicationComponent": ClientDescribeComponentResponseApplicationComponentTypeDef,
        "ResourceList": List[str],
    },
    total=False,
)


class ClientDescribeComponentResponseTypeDef(_ClientDescribeComponentResponseTypeDef):
    """
    Type definition for `ClientDescribeComponent` `Response`

    - **ApplicationComponent** *(dict) --*

      Describes a standalone resource or similarly grouped resources that the application is made up
      of.

      - **ComponentName** *(string) --*

        The name of the component.

      - **ResourceType** *(string) --*

        The resource type. Supported resource types include EC2 instances, Auto Scaling group,
        Classic ELB, Application ELB, and SQS Queue.

      - **Tier** *(string) --*

        The stack tier of the application component.

      - **Monitor** *(boolean) --*

        Indicates whether the application component is monitored.

    - **ResourceList** *(list) --*

      The list of resource ARNs that belong to the component.

      - *(string) --*
    """


_ClientDescribeLogPatternResponseLogPatternTypeDef = TypedDict(
    "_ClientDescribeLogPatternResponseLogPatternTypeDef",
    {"PatternSetName": str, "PatternName": str, "Pattern": str, "Rank": int},
    total=False,
)


class ClientDescribeLogPatternResponseLogPatternTypeDef(
    _ClientDescribeLogPatternResponseLogPatternTypeDef
):
    """
    Type definition for `ClientDescribeLogPatternResponse` `LogPattern`

    The successfully created log pattern.

    - **PatternSetName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 30 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **PatternName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 50 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **Pattern** *(string) --*

      A regular expression that defines the log pattern. A log pattern can contains at many as 50
      characters, and it cannot be empty.

    - **Rank** *(integer) --*

      Rank of the log pattern.
    """


_ClientDescribeLogPatternResponseTypeDef = TypedDict(
    "_ClientDescribeLogPatternResponseTypeDef",
    {"ResourceGroupName": str, "LogPattern": ClientDescribeLogPatternResponseLogPatternTypeDef},
    total=False,
)


class ClientDescribeLogPatternResponseTypeDef(_ClientDescribeLogPatternResponseTypeDef):
    """
    Type definition for `ClientDescribeLogPattern` `Response`

    - **ResourceGroupName** *(string) --*

      The name of the resource group.

    - **LogPattern** *(dict) --*

      The successfully created log pattern.

      - **PatternSetName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 30 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **PatternName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 50 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **Pattern** *(string) --*

        A regular expression that defines the log pattern. A log pattern can contains at many as 50
        characters, and it cannot be empty.

      - **Rank** *(integer) --*

        Rank of the log pattern.
    """


_ClientDescribeObservationResponseObservationTypeDef = TypedDict(
    "_ClientDescribeObservationResponseObservationTypeDef",
    {
        "Id": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SourceType": str,
        "SourceARN": str,
        "LogGroup": str,
        "LineTime": datetime,
        "LogText": str,
        "LogFilter": str,
        "MetricNamespace": str,
        "MetricName": str,
        "Unit": str,
        "Value": float,
    },
    total=False,
)


class ClientDescribeObservationResponseObservationTypeDef(
    _ClientDescribeObservationResponseObservationTypeDef
):
    """
    Type definition for `ClientDescribeObservationResponse` `Observation`

    Information about the observation.

    - **Id** *(string) --*

      The ID of the observation type.

    - **StartTime** *(datetime) --*

      The time when the observation was first detected, in epoch seconds.

    - **EndTime** *(datetime) --*

      The time when the observation ended, in epoch seconds.

    - **SourceType** *(string) --*

      The source type of the observation.

    - **SourceARN** *(string) --*

      The source resource ARN of the observation.

    - **LogGroup** *(string) --*

      The log group name.

    - **LineTime** *(datetime) --*

      The timestamp in the CloudWatch Logs that specifies when the matched line occurred.

    - **LogText** *(string) --*

      The log text of the observation.

    - **LogFilter** *(string) --*

      The log filter of the observation.

    - **MetricNamespace** *(string) --*

      The namespace of the observation metric.

    - **MetricName** *(string) --*

      The name of the observation metric.

    - **Unit** *(string) --*

      The unit of the source observation metric.

    - **Value** *(float) --*

      The value of the source observation metric.
    """


_ClientDescribeObservationResponseTypeDef = TypedDict(
    "_ClientDescribeObservationResponseTypeDef",
    {"Observation": ClientDescribeObservationResponseObservationTypeDef},
    total=False,
)


class ClientDescribeObservationResponseTypeDef(_ClientDescribeObservationResponseTypeDef):
    """
    Type definition for `ClientDescribeObservation` `Response`

    - **Observation** *(dict) --*

      Information about the observation.

      - **Id** *(string) --*

        The ID of the observation type.

      - **StartTime** *(datetime) --*

        The time when the observation was first detected, in epoch seconds.

      - **EndTime** *(datetime) --*

        The time when the observation ended, in epoch seconds.

      - **SourceType** *(string) --*

        The source type of the observation.

      - **SourceARN** *(string) --*

        The source resource ARN of the observation.

      - **LogGroup** *(string) --*

        The log group name.

      - **LineTime** *(datetime) --*

        The timestamp in the CloudWatch Logs that specifies when the matched line occurred.

      - **LogText** *(string) --*

        The log text of the observation.

      - **LogFilter** *(string) --*

        The log filter of the observation.

      - **MetricNamespace** *(string) --*

        The namespace of the observation metric.

      - **MetricName** *(string) --*

        The name of the observation metric.

      - **Unit** *(string) --*

        The unit of the source observation metric.

      - **Value** *(float) --*

        The value of the source observation metric.
    """


_ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef = TypedDict(
    "_ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef",
    {
        "Id": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SourceType": str,
        "SourceARN": str,
        "LogGroup": str,
        "LineTime": datetime,
        "LogText": str,
        "LogFilter": str,
        "MetricNamespace": str,
        "MetricName": str,
        "Unit": str,
        "Value": float,
    },
    total=False,
)


class ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef(
    _ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef
):
    """
    Type definition for `ClientDescribeProblemObservationsResponseRelatedObservations`
    `ObservationList`

    Describes an anomaly or error with the application.

    - **Id** *(string) --*

      The ID of the observation type.

    - **StartTime** *(datetime) --*

      The time when the observation was first detected, in epoch seconds.

    - **EndTime** *(datetime) --*

      The time when the observation ended, in epoch seconds.

    - **SourceType** *(string) --*

      The source type of the observation.

    - **SourceARN** *(string) --*

      The source resource ARN of the observation.

    - **LogGroup** *(string) --*

      The log group name.

    - **LineTime** *(datetime) --*

      The timestamp in the CloudWatch Logs that specifies when the matched line occurred.

    - **LogText** *(string) --*

      The log text of the observation.

    - **LogFilter** *(string) --*

      The log filter of the observation.

    - **MetricNamespace** *(string) --*

      The namespace of the observation metric.

    - **MetricName** *(string) --*

      The name of the observation metric.

    - **Unit** *(string) --*

      The unit of the source observation metric.

    - **Value** *(float) --*

      The value of the source observation metric.
    """


_ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef = TypedDict(
    "_ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef",
    {
        "ObservationList": List[
            ClientDescribeProblemObservationsResponseRelatedObservationsObservationListTypeDef
        ]
    },
    total=False,
)


class ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef(
    _ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef
):
    """
    Type definition for `ClientDescribeProblemObservationsResponse` `RelatedObservations`

    Observations related to the problem.

    - **ObservationList** *(list) --*

      The list of observations related to the problem.

      - *(dict) --*

        Describes an anomaly or error with the application.

        - **Id** *(string) --*

          The ID of the observation type.

        - **StartTime** *(datetime) --*

          The time when the observation was first detected, in epoch seconds.

        - **EndTime** *(datetime) --*

          The time when the observation ended, in epoch seconds.

        - **SourceType** *(string) --*

          The source type of the observation.

        - **SourceARN** *(string) --*

          The source resource ARN of the observation.

        - **LogGroup** *(string) --*

          The log group name.

        - **LineTime** *(datetime) --*

          The timestamp in the CloudWatch Logs that specifies when the matched line occurred.

        - **LogText** *(string) --*

          The log text of the observation.

        - **LogFilter** *(string) --*

          The log filter of the observation.

        - **MetricNamespace** *(string) --*

          The namespace of the observation metric.

        - **MetricName** *(string) --*

          The name of the observation metric.

        - **Unit** *(string) --*

          The unit of the source observation metric.

        - **Value** *(float) --*

          The value of the source observation metric.
    """


_ClientDescribeProblemObservationsResponseTypeDef = TypedDict(
    "_ClientDescribeProblemObservationsResponseTypeDef",
    {"RelatedObservations": ClientDescribeProblemObservationsResponseRelatedObservationsTypeDef},
    total=False,
)


class ClientDescribeProblemObservationsResponseTypeDef(
    _ClientDescribeProblemObservationsResponseTypeDef
):
    """
    Type definition for `ClientDescribeProblemObservations` `Response`

    - **RelatedObservations** *(dict) --*

      Observations related to the problem.

      - **ObservationList** *(list) --*

        The list of observations related to the problem.

        - *(dict) --*

          Describes an anomaly or error with the application.

          - **Id** *(string) --*

            The ID of the observation type.

          - **StartTime** *(datetime) --*

            The time when the observation was first detected, in epoch seconds.

          - **EndTime** *(datetime) --*

            The time when the observation ended, in epoch seconds.

          - **SourceType** *(string) --*

            The source type of the observation.

          - **SourceARN** *(string) --*

            The source resource ARN of the observation.

          - **LogGroup** *(string) --*

            The log group name.

          - **LineTime** *(datetime) --*

            The timestamp in the CloudWatch Logs that specifies when the matched line occurred.

          - **LogText** *(string) --*

            The log text of the observation.

          - **LogFilter** *(string) --*

            The log filter of the observation.

          - **MetricNamespace** *(string) --*

            The namespace of the observation metric.

          - **MetricName** *(string) --*

            The name of the observation metric.

          - **Unit** *(string) --*

            The unit of the source observation metric.

          - **Value** *(float) --*

            The value of the source observation metric.
    """


_ClientDescribeProblemResponseProblemTypeDef = TypedDict(
    "_ClientDescribeProblemResponseProblemTypeDef",
    {
        "Id": str,
        "Title": str,
        "Insights": str,
        "Status": str,
        "AffectedResource": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SeverityLevel": str,
        "ResourceGroupName": str,
        "Feedback": Dict[str, str],
    },
    total=False,
)


class ClientDescribeProblemResponseProblemTypeDef(_ClientDescribeProblemResponseProblemTypeDef):
    """
    Type definition for `ClientDescribeProblemResponse` `Problem`

    Information about the problem.

    - **Id** *(string) --*

      The ID of the problem.

    - **Title** *(string) --*

      The name of the problem.

    - **Insights** *(string) --*

      A detailed analysis of the problem using machine learning.

    - **Status** *(string) --*

      The status of the problem.

    - **AffectedResource** *(string) --*

      The resource affected by the problem.

    - **StartTime** *(datetime) --*

      The time when the problem started, in epoch seconds.

    - **EndTime** *(datetime) --*

      The time when the problem ended, in epoch seconds.

    - **SeverityLevel** *(string) --*

      A measure of the level of impact of the problem.

    - **ResourceGroupName** *(string) --*

      The name of the resource group affected by the problem.

    - **Feedback** *(dict) --*

      Feedback provided by the user about the problem.

      - *(string) --*

        - *(string) --*
    """


_ClientDescribeProblemResponseTypeDef = TypedDict(
    "_ClientDescribeProblemResponseTypeDef",
    {"Problem": ClientDescribeProblemResponseProblemTypeDef},
    total=False,
)


class ClientDescribeProblemResponseTypeDef(_ClientDescribeProblemResponseTypeDef):
    """
    Type definition for `ClientDescribeProblem` `Response`

    - **Problem** *(dict) --*

      Information about the problem.

      - **Id** *(string) --*

        The ID of the problem.

      - **Title** *(string) --*

        The name of the problem.

      - **Insights** *(string) --*

        A detailed analysis of the problem using machine learning.

      - **Status** *(string) --*

        The status of the problem.

      - **AffectedResource** *(string) --*

        The resource affected by the problem.

      - **StartTime** *(datetime) --*

        The time when the problem started, in epoch seconds.

      - **EndTime** *(datetime) --*

        The time when the problem ended, in epoch seconds.

      - **SeverityLevel** *(string) --*

        A measure of the level of impact of the problem.

      - **ResourceGroupName** *(string) --*

        The name of the resource group affected by the problem.

      - **Feedback** *(dict) --*

        Feedback provided by the user about the problem.

        - *(string) --*

          - *(string) --*
    """


_ClientListApplicationsResponseApplicationInfoListTypeDef = TypedDict(
    "_ClientListApplicationsResponseApplicationInfoListTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "Remarks": str,
    },
    total=False,
)


class ClientListApplicationsResponseApplicationInfoListTypeDef(
    _ClientListApplicationsResponseApplicationInfoListTypeDef
):
    """
    Type definition for `ClientListApplicationsResponse` `ApplicationInfoList`

    Describes the status of the application.

    - **ResourceGroupName** *(string) --*

      The name of the resource group used for the application.

    - **LifeCycle** *(string) --*

      The lifecycle of the application.

    - **OpsItemSNSTopicArn** *(string) --*

      The SNS topic provided to Application Insights that is associated to the created opsItems to
      receive SNS notifications for opsItem updates.

    - **OpsCenterEnabled** *(boolean) --*

      Indicates whether Application Insights will create opsItems for any problem detected by
      Application Insights for an application.

    - **Remarks** *(string) --*

      The issues on the user side that block Application Insights from successfully monitoring an
      application.
    """


_ClientListApplicationsResponseTypeDef = TypedDict(
    "_ClientListApplicationsResponseTypeDef",
    {
        "ApplicationInfoList": List[ClientListApplicationsResponseApplicationInfoListTypeDef],
        "NextToken": str,
    },
    total=False,
)


class ClientListApplicationsResponseTypeDef(_ClientListApplicationsResponseTypeDef):
    """
    Type definition for `ClientListApplications` `Response`

    - **ApplicationInfoList** *(list) --*

      The list of applications.

      - *(dict) --*

        Describes the status of the application.

        - **ResourceGroupName** *(string) --*

          The name of the resource group used for the application.

        - **LifeCycle** *(string) --*

          The lifecycle of the application.

        - **OpsItemSNSTopicArn** *(string) --*

          The SNS topic provided to Application Insights that is associated to the created opsItems
          to receive SNS notifications for opsItem updates.

        - **OpsCenterEnabled** *(boolean) --*

          Indicates whether Application Insights will create opsItems for any problem detected by
          Application Insights for an application.

        - **Remarks** *(string) --*

          The issues on the user side that block Application Insights from successfully monitoring
          an application.

    - **NextToken** *(string) --*

      The token used to retrieve the next page of results. This value is ``null`` when there are no
      more results to return.
    """


_ClientListComponentsResponseApplicationComponentListTypeDef = TypedDict(
    "_ClientListComponentsResponseApplicationComponentListTypeDef",
    {"ComponentName": str, "ResourceType": str, "Tier": str, "Monitor": bool},
    total=False,
)


class ClientListComponentsResponseApplicationComponentListTypeDef(
    _ClientListComponentsResponseApplicationComponentListTypeDef
):
    """
    Type definition for `ClientListComponentsResponse` `ApplicationComponentList`

    Describes a standalone resource or similarly grouped resources that the application is made up
    of.

    - **ComponentName** *(string) --*

      The name of the component.

    - **ResourceType** *(string) --*

      The resource type. Supported resource types include EC2 instances, Auto Scaling group, Classic
      ELB, Application ELB, and SQS Queue.

    - **Tier** *(string) --*

      The stack tier of the application component.

    - **Monitor** *(boolean) --*

      Indicates whether the application component is monitored.
    """


_ClientListComponentsResponseTypeDef = TypedDict(
    "_ClientListComponentsResponseTypeDef",
    {
        "ApplicationComponentList": List[
            ClientListComponentsResponseApplicationComponentListTypeDef
        ],
        "NextToken": str,
    },
    total=False,
)


class ClientListComponentsResponseTypeDef(_ClientListComponentsResponseTypeDef):
    """
    Type definition for `ClientListComponents` `Response`

    - **ApplicationComponentList** *(list) --*

      The list of application components.

      - *(dict) --*

        Describes a standalone resource or similarly grouped resources that the application is made
        up of.

        - **ComponentName** *(string) --*

          The name of the component.

        - **ResourceType** *(string) --*

          The resource type. Supported resource types include EC2 instances, Auto Scaling group,
          Classic ELB, Application ELB, and SQS Queue.

        - **Tier** *(string) --*

          The stack tier of the application component.

        - **Monitor** *(boolean) --*

          Indicates whether the application component is monitored.

    - **NextToken** *(string) --*

      The token to request the next page of results.
    """


_ClientListLogPatternSetsResponseTypeDef = TypedDict(
    "_ClientListLogPatternSetsResponseTypeDef",
    {"ResourceGroupName": str, "LogPatternSets": List[str], "NextToken": str},
    total=False,
)


class ClientListLogPatternSetsResponseTypeDef(_ClientListLogPatternSetsResponseTypeDef):
    """
    Type definition for `ClientListLogPatternSets` `Response`

    - **ResourceGroupName** *(string) --*

      The name of the resource group.

    - **LogPatternSets** *(list) --*

      The list of log pattern sets.

      - *(string) --*

    - **NextToken** *(string) --*

      The token used to retrieve the next page of results. This value is ``null`` when there are no
      more results to return.
    """


_ClientListLogPatternsResponseLogPatternsTypeDef = TypedDict(
    "_ClientListLogPatternsResponseLogPatternsTypeDef",
    {"PatternSetName": str, "PatternName": str, "Pattern": str, "Rank": int},
    total=False,
)


class ClientListLogPatternsResponseLogPatternsTypeDef(
    _ClientListLogPatternsResponseLogPatternsTypeDef
):
    """
    Type definition for `ClientListLogPatternsResponse` `LogPatterns`

    An object that defines the log patterns that belongs to a ``LogPatternSet`` .

    - **PatternSetName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 30 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **PatternName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 50 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **Pattern** *(string) --*

      A regular expression that defines the log pattern. A log pattern can contains at many as 50
      characters, and it cannot be empty.

    - **Rank** *(integer) --*

      Rank of the log pattern.
    """


_ClientListLogPatternsResponseTypeDef = TypedDict(
    "_ClientListLogPatternsResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPatterns": List[ClientListLogPatternsResponseLogPatternsTypeDef],
        "NextToken": str,
    },
    total=False,
)


class ClientListLogPatternsResponseTypeDef(_ClientListLogPatternsResponseTypeDef):
    """
    Type definition for `ClientListLogPatterns` `Response`

    - **ResourceGroupName** *(string) --*

      The name of the resource group.

    - **LogPatterns** *(list) --*

      The list of log patterns.

      - *(dict) --*

        An object that defines the log patterns that belongs to a ``LogPatternSet`` .

        - **PatternSetName** *(string) --*

          The name of the log pattern. A log pattern name can contains at many as 30 characters, and
          it cannot be empty. The characters can be Unicode letters, digits or one of the following
          symbols: period, dash, underscore.

        - **PatternName** *(string) --*

          The name of the log pattern. A log pattern name can contains at many as 50 characters, and
          it cannot be empty. The characters can be Unicode letters, digits or one of the following
          symbols: period, dash, underscore.

        - **Pattern** *(string) --*

          A regular expression that defines the log pattern. A log pattern can contains at many as
          50 characters, and it cannot be empty.

        - **Rank** *(integer) --*

          Rank of the log pattern.

    - **NextToken** *(string) --*

      The token used to retrieve the next page of results. This value is ``null`` when there are no
      more results to return.
    """


_ClientListProblemsResponseProblemListTypeDef = TypedDict(
    "_ClientListProblemsResponseProblemListTypeDef",
    {
        "Id": str,
        "Title": str,
        "Insights": str,
        "Status": str,
        "AffectedResource": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SeverityLevel": str,
        "ResourceGroupName": str,
        "Feedback": Dict[str, str],
    },
    total=False,
)


class ClientListProblemsResponseProblemListTypeDef(_ClientListProblemsResponseProblemListTypeDef):
    """
    Type definition for `ClientListProblemsResponse` `ProblemList`

    Describes a problem that is detected by correlating observations.

    - **Id** *(string) --*

      The ID of the problem.

    - **Title** *(string) --*

      The name of the problem.

    - **Insights** *(string) --*

      A detailed analysis of the problem using machine learning.

    - **Status** *(string) --*

      The status of the problem.

    - **AffectedResource** *(string) --*

      The resource affected by the problem.

    - **StartTime** *(datetime) --*

      The time when the problem started, in epoch seconds.

    - **EndTime** *(datetime) --*

      The time when the problem ended, in epoch seconds.

    - **SeverityLevel** *(string) --*

      A measure of the level of impact of the problem.

    - **ResourceGroupName** *(string) --*

      The name of the resource group affected by the problem.

    - **Feedback** *(dict) --*

      Feedback provided by the user about the problem.

      - *(string) --*

        - *(string) --*
    """


_ClientListProblemsResponseTypeDef = TypedDict(
    "_ClientListProblemsResponseTypeDef",
    {"ProblemList": List[ClientListProblemsResponseProblemListTypeDef], "NextToken": str},
    total=False,
)


class ClientListProblemsResponseTypeDef(_ClientListProblemsResponseTypeDef):
    """
    Type definition for `ClientListProblems` `Response`

    - **ProblemList** *(list) --*

      The list of problems.

      - *(dict) --*

        Describes a problem that is detected by correlating observations.

        - **Id** *(string) --*

          The ID of the problem.

        - **Title** *(string) --*

          The name of the problem.

        - **Insights** *(string) --*

          A detailed analysis of the problem using machine learning.

        - **Status** *(string) --*

          The status of the problem.

        - **AffectedResource** *(string) --*

          The resource affected by the problem.

        - **StartTime** *(datetime) --*

          The time when the problem started, in epoch seconds.

        - **EndTime** *(datetime) --*

          The time when the problem ended, in epoch seconds.

        - **SeverityLevel** *(string) --*

          A measure of the level of impact of the problem.

        - **ResourceGroupName** *(string) --*

          The name of the resource group affected by the problem.

        - **Feedback** *(dict) --*

          Feedback provided by the user about the problem.

          - *(string) --*

            - *(string) --*

    - **NextToken** *(string) --*

      The token used to retrieve the next page of results. This value is ``null`` when there are no
      more results to return.
    """


_ClientListTagsForResourceResponseTagsTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTagsTypeDef", {"Key": str, "Value": str}, total=False
)


class ClientListTagsForResourceResponseTagsTypeDef(_ClientListTagsForResourceResponseTagsTypeDef):
    """
    Type definition for `ClientListTagsForResourceResponse` `Tags`

    An object that defines the tags associated with an application. A *tag* is a label that you
    optionally define and associate with an application. Tags can help you categorize and manage
    resources in different ways, such as by purpose, owner, environment, or other criteria.

    Each tag consists of a required *tag key* and an associated *tag value* , both of which you
    define. A tag key is a general label that acts as a category for a more specific tag value. A
    tag value acts as a descriptor within a tag key. A tag key can contain as many as 128
    characters. A tag value can contain as many as 256 characters. The characters can be Unicode
    letters, digits, white space, or one of the following symbols: _ . : / = + -. The following
    additional restrictions apply to tags:

    * Tag keys and values are case sensitive.

    * For each associated resource, each tag key must be unique and it can have only one value.

    * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or values
    that you define. In addition, you can't edit or remove tag keys or values that use this prefix.

    - **Key** *(string) --*

      One part of a key-value pair that defines a tag. The maximum length of a tag key is 128
      characters. The minimum length is 1 character.

    - **Value** *(string) --*

      The optional part of a key-value pair that defines a tag. The maximum length of a tag value is
      256 characters. The minimum length is 0 characters. If you don't want an application to have a
      specific tag value, don't specify a value for this parameter.
    """


_ClientListTagsForResourceResponseTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTypeDef",
    {"Tags": List[ClientListTagsForResourceResponseTagsTypeDef]},
    total=False,
)


class ClientListTagsForResourceResponseTypeDef(_ClientListTagsForResourceResponseTypeDef):
    """
    Type definition for `ClientListTagsForResource` `Response`

    - **Tags** *(list) --*

      An array that lists all the tags that are associated with the application. Each tag consists
      of a required tag key (``Key`` ) and an associated tag value (``Value`` ).

      - *(dict) --*

        An object that defines the tags associated with an application. A *tag* is a label that you
        optionally define and associate with an application. Tags can help you categorize and manage
        resources in different ways, such as by purpose, owner, environment, or other criteria.

        Each tag consists of a required *tag key* and an associated *tag value* , both of which you
        define. A tag key is a general label that acts as a category for a more specific tag value.
        A tag value acts as a descriptor within a tag key. A tag key can contain as many as 128
        characters. A tag value can contain as many as 256 characters. The characters can be Unicode
        letters, digits, white space, or one of the following symbols: _ . : / =
             + -. The following
        additional restrictions apply to tags:

        * Tag keys and values are case sensitive.

        * For each associated resource, each tag key must be unique and it can have only one value.

        * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or values
        that you define. In addition, you can't edit or remove tag keys or values that use this
        prefix.

        - **Key** *(string) --*

          One part of a key-value pair that defines a tag. The maximum length of a tag key is 128
          characters. The minimum length is 1 character.

        - **Value** *(string) --*

          The optional part of a key-value pair that defines a tag. The maximum length of a tag
          value is 256 characters. The minimum length is 0 characters. If you don't want an
          application to have a specific tag value, don't specify a value for this parameter.
    """


_ClientTagResourceTagsTypeDef = TypedDict(
    "_ClientTagResourceTagsTypeDef", {"Key": str, "Value": str}
)


class ClientTagResourceTagsTypeDef(_ClientTagResourceTagsTypeDef):
    """
    Type definition for `ClientTagResource` `Tags`

    An object that defines the tags associated with an application. A *tag* is a label that you
    optionally define and associate with an application. Tags can help you categorize and manage
    resources in different ways, such as by purpose, owner, environment, or other criteria.

    Each tag consists of a required *tag key* and an associated *tag value* , both of which you
    define. A tag key is a general label that acts as a category for a more specific tag value. A
    tag value acts as a descriptor within a tag key. A tag key can contain as many as 128
    characters. A tag value can contain as many as 256 characters. The characters can be Unicode
    letters, digits, white space, or one of the following symbols: _ . : / = + -. The following
    additional restrictions apply to tags:

    * Tag keys and values are case sensitive.

    * For each associated resource, each tag key must be unique and it can have only one value.

    * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or values
    that you define. In addition, you can't edit or remove tag keys or values that use this prefix.

    - **Key** *(string) --* **[REQUIRED]**

      One part of a key-value pair that defines a tag. The maximum length of a tag key is 128
      characters. The minimum length is 1 character.

    - **Value** *(string) --* **[REQUIRED]**

      The optional part of a key-value pair that defines a tag. The maximum length of a tag value is
      256 characters. The minimum length is 0 characters. If you don't want an application to have a
      specific tag value, don't specify a value for this parameter.
    """


_ClientUpdateApplicationResponseApplicationInfoTypeDef = TypedDict(
    "_ClientUpdateApplicationResponseApplicationInfoTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "Remarks": str,
    },
    total=False,
)


class ClientUpdateApplicationResponseApplicationInfoTypeDef(
    _ClientUpdateApplicationResponseApplicationInfoTypeDef
):
    """
    Type definition for `ClientUpdateApplicationResponse` `ApplicationInfo`

    Information about the application.

    - **ResourceGroupName** *(string) --*

      The name of the resource group used for the application.

    - **LifeCycle** *(string) --*

      The lifecycle of the application.

    - **OpsItemSNSTopicArn** *(string) --*

      The SNS topic provided to Application Insights that is associated to the created opsItems to
      receive SNS notifications for opsItem updates.

    - **OpsCenterEnabled** *(boolean) --*

      Indicates whether Application Insights will create opsItems for any problem detected by
      Application Insights for an application.

    - **Remarks** *(string) --*

      The issues on the user side that block Application Insights from successfully monitoring an
      application.
    """


_ClientUpdateApplicationResponseTypeDef = TypedDict(
    "_ClientUpdateApplicationResponseTypeDef",
    {"ApplicationInfo": ClientUpdateApplicationResponseApplicationInfoTypeDef},
    total=False,
)


class ClientUpdateApplicationResponseTypeDef(_ClientUpdateApplicationResponseTypeDef):
    """
    Type definition for `ClientUpdateApplication` `Response`

    - **ApplicationInfo** *(dict) --*

      Information about the application.

      - **ResourceGroupName** *(string) --*

        The name of the resource group used for the application.

      - **LifeCycle** *(string) --*

        The lifecycle of the application.

      - **OpsItemSNSTopicArn** *(string) --*

        The SNS topic provided to Application Insights that is associated to the created opsItems to
        receive SNS notifications for opsItem updates.

      - **OpsCenterEnabled** *(boolean) --*

        Indicates whether Application Insights will create opsItems for any problem detected by
        Application Insights for an application.

      - **Remarks** *(string) --*

        The issues on the user side that block Application Insights from successfully monitoring an
        application.
    """


_ClientUpdateLogPatternResponseLogPatternTypeDef = TypedDict(
    "_ClientUpdateLogPatternResponseLogPatternTypeDef",
    {"PatternSetName": str, "PatternName": str, "Pattern": str, "Rank": int},
    total=False,
)


class ClientUpdateLogPatternResponseLogPatternTypeDef(
    _ClientUpdateLogPatternResponseLogPatternTypeDef
):
    """
    Type definition for `ClientUpdateLogPatternResponse` `LogPattern`

    The successfully created log pattern.

    - **PatternSetName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 30 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **PatternName** *(string) --*

      The name of the log pattern. A log pattern name can contains at many as 50 characters, and it
      cannot be empty. The characters can be Unicode letters, digits or one of the following
      symbols: period, dash, underscore.

    - **Pattern** *(string) --*

      A regular expression that defines the log pattern. A log pattern can contains at many as 50
      characters, and it cannot be empty.

    - **Rank** *(integer) --*

      Rank of the log pattern.
    """


_ClientUpdateLogPatternResponseTypeDef = TypedDict(
    "_ClientUpdateLogPatternResponseTypeDef",
    {"ResourceGroupName": str, "LogPattern": ClientUpdateLogPatternResponseLogPatternTypeDef},
    total=False,
)


class ClientUpdateLogPatternResponseTypeDef(_ClientUpdateLogPatternResponseTypeDef):
    """
    Type definition for `ClientUpdateLogPattern` `Response`

    - **ResourceGroupName** *(string) --*

      The name of the resource group.

    - **LogPattern** *(dict) --*

      The successfully created log pattern.

      - **PatternSetName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 30 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **PatternName** *(string) --*

        The name of the log pattern. A log pattern name can contains at many as 50 characters, and
        it cannot be empty. The characters can be Unicode letters, digits or one of the following
        symbols: period, dash, underscore.

      - **Pattern** *(string) --*

        A regular expression that defines the log pattern. A log pattern can contains at many as 50
        characters, and it cannot be empty.

      - **Rank** *(integer) --*

        Rank of the log pattern.
    """
