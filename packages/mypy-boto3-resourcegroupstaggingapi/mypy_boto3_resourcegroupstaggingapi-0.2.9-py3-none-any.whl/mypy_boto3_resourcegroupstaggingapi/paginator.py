"Main interface for resourcegroupstaggingapi Paginators"
from __future__ import annotations

from typing import List
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_resourcegroupstaggingapi.type_defs import (
    GetComplianceSummaryPaginatePaginationConfigTypeDef,
    GetComplianceSummaryPaginateResponseTypeDef,
    GetResourcesPaginatePaginationConfigTypeDef,
    GetResourcesPaginateResponseTypeDef,
    GetResourcesPaginateTagFiltersTypeDef,
    GetTagKeysPaginatePaginationConfigTypeDef,
    GetTagKeysPaginateResponseTypeDef,
    GetTagValuesPaginatePaginationConfigTypeDef,
    GetTagValuesPaginateResponseTypeDef,
)


__all__ = (
    "GetComplianceSummaryPaginator",
    "GetResourcesPaginator",
    "GetTagKeysPaginator",
    "GetTagValuesPaginator",
)


class GetComplianceSummaryPaginator(Boto3Paginator):
    """
    Paginator for `get_compliance_summary`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        TargetIdFilters: List[str] = None,
        RegionFilters: List[str] = None,
        ResourceTypeFilters: List[str] = None,
        TagKeyFilters: List[str] = None,
        GroupBy: List[str] = None,
        PaginationConfig: GetComplianceSummaryPaginatePaginationConfigTypeDef = None,
    ) -> GetComplianceSummaryPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ResourceGroupsTaggingAPI.Client.get_compliance_summary`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/resourcegroupstaggingapi-2017-01-26/GetComplianceSummary>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              TargetIdFilters=[
                  'string',
              ],
              RegionFilters=[
                  'string',
              ],
              ResourceTypeFilters=[
                  'string',
              ],
              TagKeyFilters=[
                  'string',
              ],
              GroupBy=[
                  'TARGET_ID'|'REGION'|'RESOURCE_TYPE',
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type TargetIdFilters: list
        :param TargetIdFilters:

          The target identifiers (usually, specific account IDs) to limit the output by. If you use
          this parameter, the count of returned noncompliant resources includes only resources with
          the specified target IDs.

          - *(string) --*

        :type RegionFilters: list
        :param RegionFilters:

          A list of Regions to limit the output by. If you use this parameter, the count of returned
          noncompliant resources includes only resources in the specified Regions.

          - *(string) --*

        :type ResourceTypeFilters: list
        :param ResourceTypeFilters:

          The constraints on the resources that you want returned. The format of each resource type
          is ``service[:resourceType]`` . For example, specifying a resource type of ``ec2`` returns
          all Amazon EC2 resources (which includes EC2 instances). Specifying a resource type of
          ``ec2:instance`` returns only EC2 instances.

          The string for each service name and resource type is the same as that embedded in a
          resource's Amazon Resource Name (ARN). Consult the *AWS General Reference* for the
          following:

          * For a list of service name strings, see `AWS Service Namespaces
          <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__
          .

          * For resource type strings, see `Example ARNs
          <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arns-syntax>`__
          .

          * For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service
          Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__
          .

          You can specify multiple resource types by using an array. The array can include up to 100
          items. Note that the length constraint requirement applies to each resource type filter.

          - *(string) --*

        :type TagKeyFilters: list
        :param TagKeyFilters:

          A list of tag keys to limit the output by. If you use this parameter, the count of
          returned noncompliant resources includes only resources that have the specified tag keys.

          - *(string) --*

        :type GroupBy: list
        :param GroupBy:

          A list of attributes to group the counts of noncompliant resources by. If supplied, the
          counts are sorted by those attributes.

          - *(string) --*

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
                'SummaryList': [
                    {
                        'LastUpdated': 'string',
                        'TargetId': 'string',
                        'TargetIdType': 'ACCOUNT'|'OU'|'ROOT',
                        'Region': 'string',
                        'ResourceType': 'string',
                        'NonCompliantResources': 123
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **SummaryList** *(list) --*

              A table that shows counts of noncompliant resources.

              - *(dict) --*

                A count of noncompliant resources.

                - **LastUpdated** *(string) --*

                  The timestamp that shows when this summary was generated in this Region.

                - **TargetId** *(string) --*

                  The account identifier or the root identifier of the organization. If you don't
                  know the root ID, you can call the AWS Organizations `ListRoots
                  <http://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`__
                  API.

                - **TargetIdType** *(string) --*

                  Whether the target is an account, an OU, or the organization root.

                - **Region** *(string) --*

                  The AWS Region that the summary applies to.

                - **ResourceType** *(string) --*

                  The AWS resource type.

                - **NonCompliantResources** *(integer) --*

                  The count of noncompliant resources.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """


class GetResourcesPaginator(Boto3Paginator):
    """
    Paginator for `get_resources`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self,
        TagFilters: List[GetResourcesPaginateTagFiltersTypeDef] = None,
        TagsPerPage: int = None,
        ResourceTypeFilters: List[str] = None,
        IncludeComplianceDetails: bool = None,
        ExcludeCompliantResources: bool = None,
        PaginationConfig: GetResourcesPaginatePaginationConfigTypeDef = None,
    ) -> GetResourcesPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ResourceGroupsTaggingAPI.Client.get_resources`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/resourcegroupstaggingapi-2017-01-26/GetResources>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              TagFilters=[
                  {
                      'Key': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              TagsPerPage=123,
              ResourceTypeFilters=[
                  'string',
              ],
              IncludeComplianceDetails=True|False,
              ExcludeCompliantResources=True|False,
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type TagFilters: list
        :param TagFilters:

          A list of TagFilters (keys and values). Each TagFilter specified must contain a key with
          values as optional. A request can include up to 50 keys, and each key can include up to 20
          values.

          Note the following when deciding how to use TagFilters:

          * If you *do* specify a TagFilter, the response returns only those resources that are
          currently associated with the specified tag.

          * If you *don't* specify a TagFilter, the response includes all resources that were ever
          associated with tags. Resources that currently don't have associated tags are shown with
          an empty tag set, like this: ``"Tags": []`` .

          * If you specify more than one filter in a single request, the response returns only those
          resources that satisfy all specified filters.

          * If you specify a filter that contains more than one value for a key, the response
          returns resources that match any of the specified values for that key.

          * If you don't specify any values for a key, the response returns resources that are
          tagged with that key irrespective of the value. For example, for filters: filter1 =
               {key1,
          {value1}}, filter2 = {key2, {value2,value3,value4}} , filter3 = {key3}:

            * GetResources( {filter1} ) returns resources tagged with key1=value1

            * GetResources( {filter2} ) returns resources tagged with key2=value2 or key2=
                value3 or
            key2=value4

            * GetResources( {filter3} ) returns resources tagged with any tag containing key3 as its
            tag key, irrespective of its value

            * GetResources( {filter1,filter2,filter3} ) returns resources tagged with ( key1=
                value1)
            and ( key2=value2 or key2=value3 or key2=
                value4) and (key3, irrespective of the value)

          - *(dict) --*

            A list of tags (keys and values) that are used to specify the associated resources.

            - **Key** *(string) --*

              One part of a key-value pair that makes up a tag. A key is a general label that acts
              like a category for more specific tag values.

            - **Values** *(list) --*

              The optional part of a key-value pair that make up a tag. A value acts as a descriptor
              within a tag category (key).

              - *(string) --*

        :type TagsPerPage: integer
        :param TagsPerPage:

          AWS recommends using ``ResourcesPerPage`` instead of this parameter.

          A limit that restricts the number of tags (key and value pairs) returned by GetResources
          in paginated output. A resource with no tags is counted as having one tag (one key and
          value pair).

           ``GetResources`` does not split a resource and its associated tags across pages. If the
           specified ``TagsPerPage`` would cause such a break, a ``PaginationToken`` is returned in
           place of the affected resource and its tags. Use that token in another request to get the
           remaining data. For example, if you specify a ``TagsPerPage`` of ``100`` and the account
           has 22 resources with 10 tags each (meaning that each resource has 10 key and value
           pairs), the output will consist of three pages. The first page displays the first 10
           resources, each with its 10 tags. The second page displays the next 10 resources, each
           with its 10 tags. The third page displays the remaining 2 resources, each with its 10
           tags.

          You can set ``TagsPerPage`` to a minimum of 100 items and the maximum of 500 items.

        :type ResourceTypeFilters: list
        :param ResourceTypeFilters:

          The constraints on the resources that you want returned. The format of each resource type
          is ``service[:resourceType]`` . For example, specifying a resource type of ``ec2`` returns
          all Amazon EC2 resources (which includes EC2 instances). Specifying a resource type of
          ``ec2:instance`` returns only EC2 instances.

          The string for each service name and resource type is the same as that embedded in a
          resource's Amazon Resource Name (ARN). Consult the *AWS General Reference* for the
          following:

          * For a list of service name strings, see `AWS Service Namespaces
          <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__
          .

          * For resource type strings, see `Example ARNs
          <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arns-syntax>`__
          .

          * For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service
          Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__
          .

          You can specify multiple resource types by using an array. The array can include up to 100
          items. Note that the length constraint requirement applies to each resource type filter.

          - *(string) --*

        :type IncludeComplianceDetails: boolean
        :param IncludeComplianceDetails:

          Specifies whether to include details regarding the compliance with the effective tag
          policy. Set this to ``true`` to determine whether resources are compliant with the tag
          policy and to get details.

        :type ExcludeCompliantResources: boolean
        :param ExcludeCompliantResources:

          Specifies whether to exclude resources that are compliant with the tag policy. Set this to
          ``true`` if you are interested in retrieving information on noncompliant resources only.

          You can use this parameter only if the ``IncludeComplianceDetails`` parameter is also set
          to ``true`` .

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
                'ResourceTagMappingList': [
                    {
                        'ResourceARN': 'string',
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ],
                        'ComplianceDetails': {
                            'NoncompliantKeys': [
                                'string',
                            ],
                            'KeysWithNoncompliantValues': [
                                'string',
                            ],
                            'ComplianceStatus': True|False
                        }
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **ResourceTagMappingList** *(list) --*

              A list of resource ARNs and the tags (keys and values) associated with each.

              - *(dict) --*

                A list of resource ARNs and the tags (keys and values) that are associated with
                each.

                - **ResourceARN** *(string) --*

                  The ARN of the resource.

                - **Tags** *(list) --*

                  The tags that have been applied to one or more AWS resources.

                  - *(dict) --*

                    The metadata that you apply to AWS resources to help you categorize and organize
                    them. Each tag consists of a key and an optional value, both of which you
                    define. For more information, see `Tagging AWS Resources
                    <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the *AWS
                    General Reference* .

                    - **Key** *(string) --*

                      One part of a key-value pair that makes up a tag. A key is a general label
                      that acts like a category for more specific tag values.

                    - **Value** *(string) --*

                      The optional part of a key-value pair that make up a tag. A value acts as a
                      descriptor within a tag category (key).

                - **ComplianceDetails** *(dict) --*

                  Information that shows whether a resource is compliant with the effective tag
                  policy, including details on any noncompliant tag keys.

                  - **NoncompliantKeys** *(list) --*

                    The tag key is noncompliant with the effective tag policy.

                    - *(string) --*

                  - **KeysWithNoncompliantValues** *(list) --*

                    The tag value is noncompliant with the effective tag policy.

                    - *(string) --*

                  - **ComplianceStatus** *(boolean) --*

                    Whether a resource is compliant with the effective tag policy.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """


class GetTagKeysPaginator(Boto3Paginator):
    """
    Paginator for `get_tag_keys`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self, PaginationConfig: GetTagKeysPaginatePaginationConfigTypeDef = None
    ) -> GetTagKeysPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ResourceGroupsTaggingAPI.Client.get_tag_keys`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/resourcegroupstaggingapi-2017-01-26/GetTagKeys>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              PaginationConfig={
                  'MaxItems': 123,
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

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TagKeys': [
                    'string',
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **TagKeys** *(list) --*

              A list of all tag keys in the AWS account.

              - *(string) --*

            - **NextToken** *(string) --*

              A token to resume pagination.

        """


class GetTagValuesPaginator(Boto3Paginator):
    """
    Paginator for `get_tag_values`
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def paginate(
        self, Key: str, PaginationConfig: GetTagValuesPaginatePaginationConfigTypeDef = None
    ) -> GetTagValuesPaginateResponseTypeDef:
        """
        Creates an iterator that will paginate through responses from
        :py:meth:`ResourceGroupsTaggingAPI.Client.get_tag_values`.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/resourcegroupstaggingapi-2017-01-26/GetTagValues>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              Key='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'StartingToken': 'string'
              }
          )
        :type Key: string
        :param Key: **[REQUIRED]**

          The key for which you want to list all existing values in the specified Region for the AWS
          account.

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than
            the value specified in max-items then a ``NextToken`` will be provided in the output
            that you can use to resume pagination.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous
            response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'TagValues': [
                    'string',
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **TagValues** *(list) --*

              A list of all tag values for the specified key in the AWS account.

              - *(string) --*

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
