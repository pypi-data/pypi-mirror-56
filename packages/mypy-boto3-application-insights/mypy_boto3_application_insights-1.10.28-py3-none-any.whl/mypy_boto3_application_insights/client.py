"Main interface for application-insights Client"
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError

# pylint: disable=import-self
import mypy_boto3_application_insights.client as client_scope
from mypy_boto3_application_insights.type_defs import (
    ClientCreateApplicationResponseTypeDef,
    ClientCreateApplicationTagsTypeDef,
    ClientCreateLogPatternResponseTypeDef,
    ClientDescribeApplicationResponseTypeDef,
    ClientDescribeComponentConfigurationRecommendationResponseTypeDef,
    ClientDescribeComponentConfigurationResponseTypeDef,
    ClientDescribeComponentResponseTypeDef,
    ClientDescribeLogPatternResponseTypeDef,
    ClientDescribeObservationResponseTypeDef,
    ClientDescribeProblemObservationsResponseTypeDef,
    ClientDescribeProblemResponseTypeDef,
    ClientListApplicationsResponseTypeDef,
    ClientListComponentsResponseTypeDef,
    ClientListLogPatternSetsResponseTypeDef,
    ClientListLogPatternsResponseTypeDef,
    ClientListProblemsResponseTypeDef,
    ClientListTagsForResourceResponseTypeDef,
    ClientTagResourceTagsTypeDef,
    ClientUpdateApplicationResponseTypeDef,
    ClientUpdateLogPatternResponseTypeDef,
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
    def create_application(
        self,
        ResourceGroupName: str,
        OpsCenterEnabled: bool = None,
        OpsItemSNSTopicArn: str = None,
        Tags: List[ClientCreateApplicationTagsTypeDef] = None,
    ) -> ClientCreateApplicationResponseTypeDef:
        """
        Adds an application that is created from a resource group.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/CreateApplication>`_

        **Request Syntax**
        ::

          response = client.create_application(
              ResourceGroupName='string',
              OpsCenterEnabled=True|False,
              OpsItemSNSTopicArn='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type OpsCenterEnabled: boolean
        :param OpsCenterEnabled:

          When set to ``true`` , creates opsItems for any problems detected on an application.

        :type OpsItemSNSTopicArn: string
        :param OpsItemSNSTopicArn:

          The SNS topic provided to Application Insights that is associated to the created opsItem.
          Allows you to receive notifications for updates to the opsItem.

        :type Tags: list
        :param Tags:

          List of tags to add to the application. tag key (``Key`` ) and an associated tag value
          (``Value`` ). The maximum length of a tag key is 128 characters. The maximum length of a
          tag value is 256 characters.

          - *(dict) --*

            An object that defines the tags associated with an application. A *tag* is a label that
            you optionally define and associate with an application. Tags can help you categorize
            and manage resources in different ways, such as by purpose, owner, environment, or other
            criteria.

            Each tag consists of a required *tag key* and an associated *tag value* , both of which
            you define. A tag key is a general label that acts as a category for a more specific tag
            value. A tag value acts as a descriptor within a tag key. A tag key can contain as many
            as 128 characters. A tag value can contain as many as 256 characters. The characters can
            be Unicode letters, digits, white space, or one of the following symbols: _ . : / =
                 + -.
            The following additional restrictions apply to tags:

            * Tag keys and values are case sensitive.

            * For each associated resource, each tag key must be unique and it can have only one
            value.

            * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or
            values that you define. In addition, you can't edit or remove tag keys or values that
            use this prefix.

            - **Key** *(string) --* **[REQUIRED]**

              One part of a key-value pair that defines a tag. The maximum length of a tag key is
              128 characters. The minimum length is 1 character.

            - **Value** *(string) --* **[REQUIRED]**

              The optional part of a key-value pair that defines a tag. The maximum length of a tag
              value is 256 characters. The minimum length is 0 characters. If you don't want an
              application to have a specific tag value, don't specify a value for this parameter.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationInfo': {
                    'ResourceGroupName': 'string',
                    'LifeCycle': 'string',
                    'OpsItemSNSTopicArn': 'string',
                    'OpsCenterEnabled': True|False,
                    'Remarks': 'string'
                }
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationInfo** *(dict) --*

              Information about the application.

              - **ResourceGroupName** *(string) --*

                The name of the resource group used for the application.

              - **LifeCycle** *(string) --*

                The lifecycle of the application.

              - **OpsItemSNSTopicArn** *(string) --*

                The SNS topic provided to Application Insights that is associated to the created
                opsItems to receive SNS notifications for opsItem updates.

              - **OpsCenterEnabled** *(boolean) --*

                Indicates whether Application Insights will create opsItems for any problem detected
                by Application Insights for an application.

              - **Remarks** *(string) --*

                The issues on the user side that block Application Insights from successfully
                monitoring an application.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_component(
        self, ResourceGroupName: str, ComponentName: str, ResourceList: List[str]
    ) -> Dict[str, Any]:
        """
        Creates a custom component by grouping similar standalone instances to monitor.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/CreateComponent>`_

        **Request Syntax**
        ::

          response = client.create_component(
              ResourceGroupName='string',
              ComponentName='string',
              ResourceList=[
                  'string',
              ]
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :type ResourceList: list
        :param ResourceList: **[REQUIRED]**

          The list of resource ARNs that belong to the component.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def create_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str, Pattern: str, Rank: int
    ) -> ClientCreateLogPatternResponseTypeDef:
        """
        Adds an log pattern to a ``LogPatternSet`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/CreateLogPattern>`_

        **Request Syntax**
        ::

          response = client.create_log_pattern(
              ResourceGroupName='string',
              PatternSetName='string',
              PatternName='string',
              Pattern='string',
              Rank=123
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type PatternSetName: string
        :param PatternSetName: **[REQUIRED]**

          The name of the log pattern set.

        :type PatternName: string
        :param PatternName: **[REQUIRED]**

          The name of the log pattern.

        :type Pattern: string
        :param Pattern: **[REQUIRED]**

          The log pattern.

        :type Rank: integer
        :param Rank: **[REQUIRED]**

          Rank of the log pattern.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'LogPattern': {
                    'PatternSetName': 'string',
                    'PatternName': 'string',
                    'Pattern': 'string',
                    'Rank': 123
                },
                'ResourceGroupName': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **LogPattern** *(dict) --*

              The successfully created log pattern.

              - **PatternSetName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 30
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **PatternName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 50
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **Pattern** *(string) --*

                A regular expression that defines the log pattern. A log pattern can contains at
                many as 50 characters, and it cannot be empty.

              - **Rank** *(integer) --*

                Rank of the log pattern.

            - **ResourceGroupName** *(string) --*

              The name of the resource group.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_application(self, ResourceGroupName: str) -> Dict[str, Any]:
        """
        Removes the specified application from monitoring. Does not delete the application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DeleteApplication>`_

        **Request Syntax**
        ::

          response = client.delete_application(
              ResourceGroupName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_component(self, ResourceGroupName: str, ComponentName: str) -> Dict[str, Any]:
        """
        Ungroups a custom component. When you ungroup custom components, all applicable monitors
        that are set up for the component are removed and the instances revert to their standalone
        status.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DeleteComponent>`_

        **Request Syntax**
        ::

          response = client.delete_component(
              ResourceGroupName='string',
              ComponentName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def delete_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> Dict[str, Any]:
        """
        Removes the specified log pattern from a ``LogPatternSet`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DeleteLogPattern>`_

        **Request Syntax**
        ::

          response = client.delete_log_pattern(
              ResourceGroupName='string',
              PatternSetName='string',
              PatternName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type PatternSetName: string
        :param PatternSetName: **[REQUIRED]**

          The name of the log pattern set.

        :type PatternName: string
        :param PatternName: **[REQUIRED]**

          The name of the log pattern.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_application(
        self, ResourceGroupName: str
    ) -> ClientDescribeApplicationResponseTypeDef:
        """
        Describes the application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeApplication>`_

        **Request Syntax**
        ::

          response = client.describe_application(
              ResourceGroupName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationInfo': {
                    'ResourceGroupName': 'string',
                    'LifeCycle': 'string',
                    'OpsItemSNSTopicArn': 'string',
                    'OpsCenterEnabled': True|False,
                    'Remarks': 'string'
                }
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationInfo** *(dict) --*

              Information about the application.

              - **ResourceGroupName** *(string) --*

                The name of the resource group used for the application.

              - **LifeCycle** *(string) --*

                The lifecycle of the application.

              - **OpsItemSNSTopicArn** *(string) --*

                The SNS topic provided to Application Insights that is associated to the created
                opsItems to receive SNS notifications for opsItem updates.

              - **OpsCenterEnabled** *(boolean) --*

                Indicates whether Application Insights will create opsItems for any problem detected
                by Application Insights for an application.

              - **Remarks** *(string) --*

                The issues on the user side that block Application Insights from successfully
                monitoring an application.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_component(
        self, ResourceGroupName: str, ComponentName: str
    ) -> ClientDescribeComponentResponseTypeDef:
        """
        Describes a component and lists the resources that are grouped together in a component.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeComponent>`_

        **Request Syntax**
        ::

          response = client.describe_component(
              ResourceGroupName='string',
              ComponentName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationComponent': {
                    'ComponentName': 'string',
                    'ResourceType': 'string',
                    'Tier': 'DEFAULT'|'DOT_NET_CORE'|'DOT_NET_WORKER'|'DOT_NET_WEB'|'SQL_SERVER',
                    'Monitor': True|False
                },
                'ResourceList': [
                    'string',
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationComponent** *(dict) --*

              Describes a standalone resource or similarly grouped resources that the application is
              made up of.

              - **ComponentName** *(string) --*

                The name of the component.

              - **ResourceType** *(string) --*

                The resource type. Supported resource types include EC2 instances, Auto Scaling
                group, Classic ELB, Application ELB, and SQS Queue.

              - **Tier** *(string) --*

                The stack tier of the application component.

              - **Monitor** *(boolean) --*

                Indicates whether the application component is monitored.

            - **ResourceList** *(list) --*

              The list of resource ARNs that belong to the component.

              - *(string) --*

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_component_configuration(
        self, ResourceGroupName: str, ComponentName: str
    ) -> ClientDescribeComponentConfigurationResponseTypeDef:
        """
        Describes the monitoring configuration of the component.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeComponentConfiguration>`_

        **Request Syntax**
        ::

          response = client.describe_component_configuration(
              ResourceGroupName='string',
              ComponentName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Monitor': True|False,
                'Tier': 'DEFAULT'|'DOT_NET_CORE'|'DOT_NET_WORKER'|'DOT_NET_WEB'|'SQL_SERVER',
                'ComponentConfiguration': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **Monitor** *(boolean) --*

              Indicates whether the application component is monitored.

            - **Tier** *(string) --*

              The tier of the application component. Supported tiers include ``DOT_NET_CORE`` ,
              ``DOT_NET_WORKER`` , ``DOT_NET_WEB`` , ``SQL_SERVER`` , and ``DEFAULT``

            - **ComponentConfiguration** *(string) --*

              The configuration settings of the component. The value is the escaped JSON of the
              configuration.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_component_configuration_recommendation(
        self, ResourceGroupName: str, ComponentName: str, Tier: str
    ) -> ClientDescribeComponentConfigurationRecommendationResponseTypeDef:
        """
        Describes the recommended monitoring configuration of the component.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeComponentConfigurationRecommendation>`_

        **Request Syntax**
        ::

          response = client.describe_component_configuration_recommendation(
              ResourceGroupName='string',
              ComponentName='string',
              Tier='DEFAULT'|'DOT_NET_CORE'|'DOT_NET_WORKER'|'DOT_NET_WEB'|'SQL_SERVER'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :type Tier: string
        :param Tier: **[REQUIRED]**

          The tier of the application component. Supported tiers include ``DOT_NET_CORE`` ,
          ``DOT_NET_WORKER`` , ``DOT_NET_WEB`` , ``SQL_SERVER`` , and ``DEFAULT`` .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ComponentConfiguration': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ComponentConfiguration** *(string) --*

              The recommended configuration settings of the component. The value is the escaped JSON
              of the configuration.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> ClientDescribeLogPatternResponseTypeDef:
        """
        Describe a specific log pattern from a ``LogPatternSet`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeLogPattern>`_

        **Request Syntax**
        ::

          response = client.describe_log_pattern(
              ResourceGroupName='string',
              PatternSetName='string',
              PatternName='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type PatternSetName: string
        :param PatternSetName: **[REQUIRED]**

          The name of the log pattern set.

        :type PatternName: string
        :param PatternName: **[REQUIRED]**

          The name of the log pattern.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ResourceGroupName': 'string',
                'LogPattern': {
                    'PatternSetName': 'string',
                    'PatternName': 'string',
                    'Pattern': 'string',
                    'Rank': 123
                }
            }
          **Response Structure**

          - *(dict) --*

            - **ResourceGroupName** *(string) --*

              The name of the resource group.

            - **LogPattern** *(dict) --*

              The successfully created log pattern.

              - **PatternSetName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 30
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **PatternName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 50
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **Pattern** *(string) --*

                A regular expression that defines the log pattern. A log pattern can contains at
                many as 50 characters, and it cannot be empty.

              - **Rank** *(integer) --*

                Rank of the log pattern.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_observation(self, ObservationId: str) -> ClientDescribeObservationResponseTypeDef:
        """
        Describes an anomaly or error with the application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeObservation>`_

        **Request Syntax**
        ::

          response = client.describe_observation(
              ObservationId='string'
          )
        :type ObservationId: string
        :param ObservationId: **[REQUIRED]**

          The ID of the observation.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Observation': {
                    'Id': 'string',
                    'StartTime': datetime(2015, 1, 1),
                    'EndTime': datetime(2015, 1, 1),
                    'SourceType': 'string',
                    'SourceARN': 'string',
                    'LogGroup': 'string',
                    'LineTime': datetime(2015, 1, 1),
                    'LogText': 'string',
                    'LogFilter': 'ERROR'|'WARN'|'INFO',
                    'MetricNamespace': 'string',
                    'MetricName': 'string',
                    'Unit': 'string',
                    'Value': 123.0
                }
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_problem(self, ProblemId: str) -> ClientDescribeProblemResponseTypeDef:
        """
        Describes an application problem.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeProblem>`_

        **Request Syntax**
        ::

          response = client.describe_problem(
              ProblemId='string'
          )
        :type ProblemId: string
        :param ProblemId: **[REQUIRED]**

          The ID of the problem.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Problem': {
                    'Id': 'string',
                    'Title': 'string',
                    'Insights': 'string',
                    'Status': 'IGNORE'|'RESOLVED'|'PENDING',
                    'AffectedResource': 'string',
                    'StartTime': datetime(2015, 1, 1),
                    'EndTime': datetime(2015, 1, 1),
                    'SeverityLevel': 'Low'|'Medium'|'High',
                    'ResourceGroupName': 'string',
                    'Feedback': {
                        'string': 'NOT_SPECIFIED'|'USEFUL'|'NOT_USEFUL'
                    }
                }
            }
          **Response Structure**

          - *(dict) --*

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

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def describe_problem_observations(
        self, ProblemId: str
    ) -> ClientDescribeProblemObservationsResponseTypeDef:
        """
        Describes the anomalies or errors associated with the problem.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/DescribeProblemObservations>`_

        **Request Syntax**
        ::

          response = client.describe_problem_observations(
              ProblemId='string'
          )
        :type ProblemId: string
        :param ProblemId: **[REQUIRED]**

          The ID of the problem.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'RelatedObservations': {
                    'ObservationList': [
                        {
                            'Id': 'string',
                            'StartTime': datetime(2015, 1, 1),
                            'EndTime': datetime(2015, 1, 1),
                            'SourceType': 'string',
                            'SourceARN': 'string',
                            'LogGroup': 'string',
                            'LineTime': datetime(2015, 1, 1),
                            'LogText': 'string',
                            'LogFilter': 'ERROR'|'WARN'|'INFO',
                            'MetricNamespace': 'string',
                            'MetricName': 'string',
                            'Unit': 'string',
                            'Value': 123.0
                        },
                    ]
                }
            }
          **Response Structure**

          - *(dict) --*

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

                    The timestamp in the CloudWatch Logs that specifies when the matched line
                    occurred.

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
    def list_applications(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ClientListApplicationsResponseTypeDef:
        """
        Lists the IDs of the applications that you are monitoring.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListApplications>`_

        **Request Syntax**
        ::

          response = client.list_applications(
              MaxResults=123,
              NextToken='string'
          )
        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return in a single call. To retrieve the remaining
          results, make another call with the returned ``NextToken`` value.

        :type NextToken: string
        :param NextToken:

          The token to request the next page of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationInfoList': [
                    {
                        'ResourceGroupName': 'string',
                        'LifeCycle': 'string',
                        'OpsItemSNSTopicArn': 'string',
                        'OpsCenterEnabled': True|False,
                        'Remarks': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationInfoList** *(list) --*

              The list of applications.

              - *(dict) --*

                Describes the status of the application.

                - **ResourceGroupName** *(string) --*

                  The name of the resource group used for the application.

                - **LifeCycle** *(string) --*

                  The lifecycle of the application.

                - **OpsItemSNSTopicArn** *(string) --*

                  The SNS topic provided to Application Insights that is associated to the created
                  opsItems to receive SNS notifications for opsItem updates.

                - **OpsCenterEnabled** *(boolean) --*

                  Indicates whether Application Insights will create opsItems for any problem
                  detected by Application Insights for an application.

                - **Remarks** *(string) --*

                  The issues on the user side that block Application Insights from successfully
                  monitoring an application.

            - **NextToken** *(string) --*

              The token used to retrieve the next page of results. This value is ``null`` when there
              are no more results to return.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_components(
        self, ResourceGroupName: str, MaxResults: int = None, NextToken: str = None
    ) -> ClientListComponentsResponseTypeDef:
        """
        Lists the auto-grouped, standalone, and custom components of the application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListComponents>`_

        **Request Syntax**
        ::

          response = client.list_components(
              ResourceGroupName='string',
              MaxResults=123,
              NextToken='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return in a single call. To retrieve the remaining
          results, make another call with the returned ``NextToken`` value.

        :type NextToken: string
        :param NextToken:

          The token to request the next page of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationComponentList': [
                    {
                        'ComponentName': 'string',
                        'ResourceType': 'string',
                        'Tier':
                        'DEFAULT'|'DOT_NET_CORE'|'DOT_NET_WORKER'|'DOT_NET_WEB'
                        |'SQL_SERVER',
                        'Monitor': True|False
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationComponentList** *(list) --*

              The list of application components.

              - *(dict) --*

                Describes a standalone resource or similarly grouped resources that the application
                is made up of.

                - **ComponentName** *(string) --*

                  The name of the component.

                - **ResourceType** *(string) --*

                  The resource type. Supported resource types include EC2 instances, Auto Scaling
                  group, Classic ELB, Application ELB, and SQS Queue.

                - **Tier** *(string) --*

                  The stack tier of the application component.

                - **Monitor** *(boolean) --*

                  Indicates whether the application component is monitored.

            - **NextToken** *(string) --*

              The token to request the next page of results.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_log_pattern_sets(
        self, ResourceGroupName: str, MaxResults: int = None, NextToken: str = None
    ) -> ClientListLogPatternSetsResponseTypeDef:
        """
        Lists the log pattern sets in the specific application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListLogPatternSets>`_

        **Request Syntax**
        ::

          response = client.list_log_pattern_sets(
              ResourceGroupName='string',
              MaxResults=123,
              NextToken='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return in a single call. To retrieve the remaining
          results, make another call with the returned ``NextToken`` value.

        :type NextToken: string
        :param NextToken:

          The token to request the next page of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ResourceGroupName': 'string',
                'LogPatternSets': [
                    'string',
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ResourceGroupName** *(string) --*

              The name of the resource group.

            - **LogPatternSets** *(list) --*

              The list of log pattern sets.

              - *(string) --*

            - **NextToken** *(string) --*

              The token used to retrieve the next page of results. This value is ``null`` when there
              are no more results to return.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_log_patterns(
        self,
        ResourceGroupName: str,
        PatternSetName: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ClientListLogPatternsResponseTypeDef:
        """
        Lists the log patterns in the specific log ``LogPatternSet`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListLogPatterns>`_

        **Request Syntax**
        ::

          response = client.list_log_patterns(
              ResourceGroupName='string',
              PatternSetName='string',
              MaxResults=123,
              NextToken='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type PatternSetName: string
        :param PatternSetName:

          The name of the log pattern set.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return in a single call. To retrieve the remaining
          results, make another call with the returned ``NextToken`` value.

        :type NextToken: string
        :param NextToken:

          The token to request the next page of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ResourceGroupName': 'string',
                'LogPatterns': [
                    {
                        'PatternSetName': 'string',
                        'PatternName': 'string',
                        'Pattern': 'string',
                        'Rank': 123
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ResourceGroupName** *(string) --*

              The name of the resource group.

            - **LogPatterns** *(list) --*

              The list of log patterns.

              - *(dict) --*

                An object that defines the log patterns that belongs to a ``LogPatternSet`` .

                - **PatternSetName** *(string) --*

                  The name of the log pattern. A log pattern name can contains at many as 30
                  characters, and it cannot be empty. The characters can be Unicode letters, digits
                  or one of the following symbols: period, dash, underscore.

                - **PatternName** *(string) --*

                  The name of the log pattern. A log pattern name can contains at many as 50
                  characters, and it cannot be empty. The characters can be Unicode letters, digits
                  or one of the following symbols: period, dash, underscore.

                - **Pattern** *(string) --*

                  A regular expression that defines the log pattern. A log pattern can contains at
                  many as 50 characters, and it cannot be empty.

                - **Rank** *(integer) --*

                  Rank of the log pattern.

            - **NextToken** *(string) --*

              The token used to retrieve the next page of results. This value is ``null`` when there
              are no more results to return.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_problems(
        self,
        ResourceGroupName: str = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ClientListProblemsResponseTypeDef:
        """
        Lists the problems with your application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListProblems>`_

        **Request Syntax**
        ::

          response = client.list_problems(
              ResourceGroupName='string',
              StartTime=datetime(2015, 1, 1),
              EndTime=datetime(2015, 1, 1),
              MaxResults=123,
              NextToken='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName:

          The name of the resource group.

        :type StartTime: datetime
        :param StartTime:

          The time when the problem was detected, in epoch seconds. If you don't specify a time
          frame for the request, problems within the past seven days are returned.

        :type EndTime: datetime
        :param EndTime:

          The time when the problem ended, in epoch seconds. If not specified, problems within the
          past seven days are returned.

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return in a single call. To retrieve the remaining
          results, make another call with the returned ``NextToken`` value.

        :type NextToken: string
        :param NextToken:

          The token to request the next page of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ProblemList': [
                    {
                        'Id': 'string',
                        'Title': 'string',
                        'Insights': 'string',
                        'Status': 'IGNORE'|'RESOLVED'|'PENDING',
                        'AffectedResource': 'string',
                        'StartTime': datetime(2015, 1, 1),
                        'EndTime': datetime(2015, 1, 1),
                        'SeverityLevel': 'Low'|'Medium'|'High',
                        'ResourceGroupName': 'string',
                        'Feedback': {
                            'string': 'NOT_SPECIFIED'|'USEFUL'|'NOT_USEFUL'
                        }
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

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

              The token used to retrieve the next page of results. This value is ``null`` when there
              are no more results to return.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def list_tags_for_resource(self, ResourceARN: str) -> ClientListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a specified
        application. A *tag* is a label that you optionally define and associate with an
        application. Each tag consists of a required *tag key* and an optional associated *tag
        value* . A tag key is a general label that acts as a category for more specific tag values.
        A tag value acts as a descriptor within a tag key.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/ListTagsForResource>`_

        **Request Syntax**
        ::

          response = client.list_tags_for_resource(
              ResourceARN='string'
          )
        :type ResourceARN: string
        :param ResourceARN: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the application that you want to retrieve tag
          information for.

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
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **Tags** *(list) --*

              An array that lists all the tags that are associated with the application. Each tag
              consists of a required tag key (``Key`` ) and an associated tag value (``Value`` ).

              - *(dict) --*

                An object that defines the tags associated with an application. A *tag* is a label
                that you optionally define and associate with an application. Tags can help you
                categorize and manage resources in different ways, such as by purpose, owner,
                environment, or other criteria.

                Each tag consists of a required *tag key* and an associated *tag value* , both of
                which you define. A tag key is a general label that acts as a category for a more
                specific tag value. A tag value acts as a descriptor within a tag key. A tag key can
                contain as many as 128 characters. A tag value can contain as many as 256
                characters. The characters can be Unicode letters, digits, white space, or one of
                the following symbols: _ . : / =
                     + -. The following additional restrictions apply to
                tags:

                * Tag keys and values are case sensitive.

                * For each associated resource, each tag key must be unique and it can have only one
                value.

                * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys
                or values that you define. In addition, you can't edit or remove tag keys or values
                that use this prefix.

                - **Key** *(string) --*

                  One part of a key-value pair that defines a tag. The maximum length of a tag key
                  is 128 characters. The minimum length is 1 character.

                - **Value** *(string) --*

                  The optional part of a key-value pair that defines a tag. The maximum length of a
                  tag value is 256 characters. The minimum length is 0 characters. If you don't want
                  an application to have a specific tag value, don't specify a value for this
                  parameter.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def tag_resource(
        self, ResourceARN: str, Tags: List[ClientTagResourceTagsTypeDef]
    ) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified application. A *tag* is a label that
        you optionally define and associate with an application. Tags can help you categorize and
        manage application in different ways, such as by purpose, owner, environment, or other
        criteria.

        Each tag consists of a required *tag key* and an associated *tag value* , both of which you
        define. A tag key is a general label that acts as a category for more specific tag values. A
        tag value acts as a descriptor within a tag key.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/TagResource>`_

        **Request Syntax**
        ::

          response = client.tag_resource(
              ResourceARN='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type ResourceARN: string
        :param ResourceARN: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the application that you want to add one or more tags
          to.

        :type Tags: list
        :param Tags: **[REQUIRED]**

          A list of tags that to add to the application. A tag consists of a required tag key
          (``Key`` ) and an associated tag value (``Value`` ). The maximum length of a tag key is
          128 characters. The maximum length of a tag value is 256 characters.

          - *(dict) --*

            An object that defines the tags associated with an application. A *tag* is a label that
            you optionally define and associate with an application. Tags can help you categorize
            and manage resources in different ways, such as by purpose, owner, environment, or other
            criteria.

            Each tag consists of a required *tag key* and an associated *tag value* , both of which
            you define. A tag key is a general label that acts as a category for a more specific tag
            value. A tag value acts as a descriptor within a tag key. A tag key can contain as many
            as 128 characters. A tag value can contain as many as 256 characters. The characters can
            be Unicode letters, digits, white space, or one of the following symbols: _ . : / =
                 + -.
            The following additional restrictions apply to tags:

            * Tag keys and values are case sensitive.

            * For each associated resource, each tag key must be unique and it can have only one
            value.

            * The ``aws:`` prefix is reserved for use by AWS; you can’t use it in any tag keys or
            values that you define. In addition, you can't edit or remove tag keys or values that
            use this prefix.

            - **Key** *(string) --* **[REQUIRED]**

              One part of a key-value pair that defines a tag. The maximum length of a tag key is
              128 characters. The minimum length is 1 character.

            - **Value** *(string) --* **[REQUIRED]**

              The optional part of a key-value pair that defines a tag. The maximum length of a tag
              value is 256 characters. The minimum length is 0 characters. If you don't want an
              application to have a specific tag value, don't specify a value for this parameter.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def untag_resource(self, ResourceARN: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/UntagResource>`_

        **Request Syntax**
        ::

          response = client.untag_resource(
              ResourceARN='string',
              TagKeys=[
                  'string',
              ]
          )
        :type ResourceARN: string
        :param ResourceARN: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the application that you want to remove one or more tags
          from.

        :type TagKeys: list
        :param TagKeys: **[REQUIRED]**

          The tags (tag keys) that you want to remove from the resource. When you specify a tag key,
          the action removes both that key and its associated tag value.

          To remove more than one tag from the application, append the ``TagKeys`` parameter and
          argument for each additional tag to remove, separated by an ampersand.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_application(
        self,
        ResourceGroupName: str,
        OpsCenterEnabled: bool = None,
        OpsItemSNSTopicArn: str = None,
        RemoveSNSTopic: bool = None,
    ) -> ClientUpdateApplicationResponseTypeDef:
        """
        Updates the application.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/UpdateApplication>`_

        **Request Syntax**
        ::

          response = client.update_application(
              ResourceGroupName='string',
              OpsCenterEnabled=True|False,
              OpsItemSNSTopicArn='string',
              RemoveSNSTopic=True|False
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type OpsCenterEnabled: boolean
        :param OpsCenterEnabled:

          When set to ``true`` , creates opsItems for any problems detected on an application.

        :type OpsItemSNSTopicArn: string
        :param OpsItemSNSTopicArn:

          The SNS topic provided to Application Insights that is associated to the created opsItem.
          Allows you to receive notifications for updates to the opsItem.

        :type RemoveSNSTopic: boolean
        :param RemoveSNSTopic:

          Disassociates the SNS topic from the opsItem created for detected problems.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ApplicationInfo': {
                    'ResourceGroupName': 'string',
                    'LifeCycle': 'string',
                    'OpsItemSNSTopicArn': 'string',
                    'OpsCenterEnabled': True|False,
                    'Remarks': 'string'
                }
            }
          **Response Structure**

          - *(dict) --*

            - **ApplicationInfo** *(dict) --*

              Information about the application.

              - **ResourceGroupName** *(string) --*

                The name of the resource group used for the application.

              - **LifeCycle** *(string) --*

                The lifecycle of the application.

              - **OpsItemSNSTopicArn** *(string) --*

                The SNS topic provided to Application Insights that is associated to the created
                opsItems to receive SNS notifications for opsItem updates.

              - **OpsCenterEnabled** *(boolean) --*

                Indicates whether Application Insights will create opsItems for any problem detected
                by Application Insights for an application.

              - **Remarks** *(string) --*

                The issues on the user side that block Application Insights from successfully
                monitoring an application.

        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_component(
        self,
        ResourceGroupName: str,
        ComponentName: str,
        NewComponentName: str = None,
        ResourceList: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Updates the custom component name and/or the list of resources that make up the component.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/UpdateComponent>`_

        **Request Syntax**
        ::

          response = client.update_component(
              ResourceGroupName='string',
              ComponentName='string',
              NewComponentName='string',
              ResourceList=[
                  'string',
              ]
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :type NewComponentName: string
        :param NewComponentName:

          The new name of the component.

        :type ResourceList: list
        :param ResourceList:

          The list of resource ARNs that belong to the component.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_component_configuration(
        self,
        ResourceGroupName: str,
        ComponentName: str,
        Monitor: bool = None,
        Tier: str = None,
        ComponentConfiguration: str = None,
    ) -> Dict[str, Any]:
        """
        Updates the monitoring configurations for the component. The configuration input parameter
        is an escaped JSON of the configuration and should match the schema of what is returned by
        ``DescribeComponentConfigurationRecommendation`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/UpdateComponentConfiguration>`_

        **Request Syntax**
        ::

          response = client.update_component_configuration(
              ResourceGroupName='string',
              ComponentName='string',
              Monitor=True|False,
              Tier='DEFAULT'|'DOT_NET_CORE'|'DOT_NET_WORKER'|'DOT_NET_WEB'|'SQL_SERVER',
              ComponentConfiguration='string'
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type ComponentName: string
        :param ComponentName: **[REQUIRED]**

          The name of the component.

        :type Monitor: boolean
        :param Monitor:

          Indicates whether the application component is monitored.

        :type Tier: string
        :param Tier:

          The tier of the application component. Supported tiers include ``DOT_NET_WORKER`` ,
          ``DOT_NET_WEB`` , ``DOT_NET_CORE`` , ``SQL_SERVER`` , and ``DEFAULT`` .

        :type ComponentConfiguration: string
        :param ComponentConfiguration:

          The configuration settings of the component. The value is the escaped JSON of the
          configuration. For more information about the JSON format, see `Working with JSON
          <https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/working-with-json.html>`__
          . You can send a request to ``DescribeComponentConfigurationRecommendation`` to see the
          recommended configuration for a component. For the complete format of the component
          configuration file, see `Component Configuration
          <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/component-config.html>`__
          .

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def update_log_pattern(
        self,
        ResourceGroupName: str,
        PatternSetName: str,
        PatternName: str,
        Pattern: str = None,
        Rank: int = None,
    ) -> ClientUpdateLogPatternResponseTypeDef:
        """
        Adds a log pattern to a ``LogPatternSet`` .

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/application-insights-2018-11-25/UpdateLogPattern>`_

        **Request Syntax**
        ::

          response = client.update_log_pattern(
              ResourceGroupName='string',
              PatternSetName='string',
              PatternName='string',
              Pattern='string',
              Rank=123
          )
        :type ResourceGroupName: string
        :param ResourceGroupName: **[REQUIRED]**

          The name of the resource group.

        :type PatternSetName: string
        :param PatternSetName: **[REQUIRED]**

          The name of the log pattern set.

        :type PatternName: string
        :param PatternName: **[REQUIRED]**

          The name of the log pattern.

        :type Pattern: string
        :param Pattern:

          The log pattern.

        :type Rank: integer
        :param Rank:

          Rank of the log pattern.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ResourceGroupName': 'string',
                'LogPattern': {
                    'PatternSetName': 'string',
                    'PatternName': 'string',
                    'Pattern': 'string',
                    'Rank': 123
                }
            }
          **Response Structure**

          - *(dict) --*

            - **ResourceGroupName** *(string) --*

              The name of the resource group.

            - **LogPattern** *(dict) --*

              The successfully created log pattern.

              - **PatternSetName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 30
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **PatternName** *(string) --*

                The name of the log pattern. A log pattern name can contains at many as 50
                characters, and it cannot be empty. The characters can be Unicode letters, digits or
                one of the following symbols: period, dash, underscore.

              - **Pattern** *(string) --*

                A regular expression that defines the log pattern. A log pattern can contains at
                many as 50 characters, and it cannot be empty.

              - **Rank** *(integer) --*

                Rank of the log pattern.

        """


class Exceptions:
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    InternalServerException: Boto3ClientError
    ResourceInUseException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    TagsAlreadyExistException: Boto3ClientError
    TooManyTagsException: Boto3ClientError
    ValidationException: Boto3ClientError
