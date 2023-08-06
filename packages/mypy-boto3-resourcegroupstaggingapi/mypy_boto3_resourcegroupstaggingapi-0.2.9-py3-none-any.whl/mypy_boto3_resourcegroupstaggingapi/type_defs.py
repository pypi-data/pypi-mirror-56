"Main interface for resourcegroupstaggingapi type defs"
from __future__ import annotations

from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientDescribeReportCreationResponseTypeDef",
    "ClientGetComplianceSummaryResponseSummaryListTypeDef",
    "ClientGetComplianceSummaryResponseTypeDef",
    "ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef",
    "ClientGetResourcesResponseResourceTagMappingListTagsTypeDef",
    "ClientGetResourcesResponseResourceTagMappingListTypeDef",
    "ClientGetResourcesResponseTypeDef",
    "ClientGetResourcesTagFiltersTypeDef",
    "ClientGetTagKeysResponseTypeDef",
    "ClientGetTagValuesResponseTypeDef",
    "ClientTagResourcesResponseFailedResourcesMapTypeDef",
    "ClientTagResourcesResponseTypeDef",
    "ClientUntagResourcesResponseFailedResourcesMapTypeDef",
    "ClientUntagResourcesResponseTypeDef",
    "GetComplianceSummaryPaginatePaginationConfigTypeDef",
    "GetComplianceSummaryPaginateResponseSummaryListTypeDef",
    "GetComplianceSummaryPaginateResponseTypeDef",
    "GetResourcesPaginatePaginationConfigTypeDef",
    "GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef",
    "GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef",
    "GetResourcesPaginateResponseResourceTagMappingListTypeDef",
    "GetResourcesPaginateResponseTypeDef",
    "GetResourcesPaginateTagFiltersTypeDef",
    "GetTagKeysPaginatePaginationConfigTypeDef",
    "GetTagKeysPaginateResponseTypeDef",
    "GetTagValuesPaginatePaginationConfigTypeDef",
    "GetTagValuesPaginateResponseTypeDef",
)


_ClientDescribeReportCreationResponseTypeDef = TypedDict(
    "_ClientDescribeReportCreationResponseTypeDef",
    {"Status": str, "S3Location": str, "ErrorMessage": str},
    total=False,
)


class ClientDescribeReportCreationResponseTypeDef(_ClientDescribeReportCreationResponseTypeDef):
    """
    Type definition for `ClientDescribeReportCreation` `Response`

    - **Status** *(string) --*

      Reports the status of the operation.

      The operation status can be one of the following:

      * ``RUNNING`` - Report creation is in progress.

      * ``SUCCEEDED`` - Report creation is complete. You can open the report from the Amazon S3
      bucket that you specified when you ran ``StartReportCreation`` .

      * ``FAILED`` - Report creation timed out or the Amazon S3 bucket is not accessible.

      * ``NO REPORT`` - No report was generated in the last 90 days.

    - **S3Location** *(string) --*

      The path to the Amazon S3 bucket where the report was stored on creation.

    - **ErrorMessage** *(string) --*

      Details of the common errors that all operations return.
    """


_ClientGetComplianceSummaryResponseSummaryListTypeDef = TypedDict(
    "_ClientGetComplianceSummaryResponseSummaryListTypeDef",
    {
        "LastUpdated": str,
        "TargetId": str,
        "TargetIdType": str,
        "Region": str,
        "ResourceType": str,
        "NonCompliantResources": int,
    },
    total=False,
)


class ClientGetComplianceSummaryResponseSummaryListTypeDef(
    _ClientGetComplianceSummaryResponseSummaryListTypeDef
):
    """
    Type definition for `ClientGetComplianceSummaryResponse` `SummaryList`

    A count of noncompliant resources.

    - **LastUpdated** *(string) --*

      The timestamp that shows when this summary was generated in this Region.

    - **TargetId** *(string) --*

      The account identifier or the root identifier of the organization. If you don't know the root
      ID, you can call the AWS Organizations `ListRoots
      <http://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`__ API.

    - **TargetIdType** *(string) --*

      Whether the target is an account, an OU, or the organization root.

    - **Region** *(string) --*

      The AWS Region that the summary applies to.

    - **ResourceType** *(string) --*

      The AWS resource type.

    - **NonCompliantResources** *(integer) --*

      The count of noncompliant resources.
    """


_ClientGetComplianceSummaryResponseTypeDef = TypedDict(
    "_ClientGetComplianceSummaryResponseTypeDef",
    {
        "SummaryList": List[ClientGetComplianceSummaryResponseSummaryListTypeDef],
        "PaginationToken": str,
    },
    total=False,
)


class ClientGetComplianceSummaryResponseTypeDef(_ClientGetComplianceSummaryResponseTypeDef):
    """
    Type definition for `ClientGetComplianceSummary` `Response`

    - **SummaryList** *(list) --*

      A table that shows counts of noncompliant resources.

      - *(dict) --*

        A count of noncompliant resources.

        - **LastUpdated** *(string) --*

          The timestamp that shows when this summary was generated in this Region.

        - **TargetId** *(string) --*

          The account identifier or the root identifier of the organization. If you don't know the
          root ID, you can call the AWS Organizations `ListRoots
          <http://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`__ API.

        - **TargetIdType** *(string) --*

          Whether the target is an account, an OU, or the organization root.

        - **Region** *(string) --*

          The AWS Region that the summary applies to.

        - **ResourceType** *(string) --*

          The AWS resource type.

        - **NonCompliantResources** *(integer) --*

          The count of noncompliant resources.

    - **PaginationToken** *(string) --*

      A string that indicates that the response contains more data than can be returned in a single
      response. To receive additional data, specify this string for the ``PaginationToken`` value in
      a subsequent request.
    """


_ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef = TypedDict(
    "_ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef",
    {
        "NoncompliantKeys": List[str],
        "KeysWithNoncompliantValues": List[str],
        "ComplianceStatus": bool,
    },
    total=False,
)


class ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef(
    _ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef
):
    """
    Type definition for `ClientGetResourcesResponseResourceTagMappingList` `ComplianceDetails`

    Information that shows whether a resource is compliant with the effective tag policy, including
    details on any noncompliant tag keys.

    - **NoncompliantKeys** *(list) --*

      The tag key is noncompliant with the effective tag policy.

      - *(string) --*

    - **KeysWithNoncompliantValues** *(list) --*

      The tag value is noncompliant with the effective tag policy.

      - *(string) --*

    - **ComplianceStatus** *(boolean) --*

      Whether a resource is compliant with the effective tag policy.
    """


_ClientGetResourcesResponseResourceTagMappingListTagsTypeDef = TypedDict(
    "_ClientGetResourcesResponseResourceTagMappingListTagsTypeDef",
    {"Key": str, "Value": str},
    total=False,
)


class ClientGetResourcesResponseResourceTagMappingListTagsTypeDef(
    _ClientGetResourcesResponseResourceTagMappingListTagsTypeDef
):
    """
    Type definition for `ClientGetResourcesResponseResourceTagMappingList` `Tags`

    The metadata that you apply to AWS resources to help you categorize and organize them. Each tag
    consists of a key and an optional value, both of which you define. For more information, see
    `Tagging AWS Resources <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the
    *AWS General Reference* .

    - **Key** *(string) --*

      One part of a key-value pair that makes up a tag. A key is a general label that acts like a
      category for more specific tag values.

    - **Value** *(string) --*

      The optional part of a key-value pair that make up a tag. A value acts as a descriptor within
      a tag category (key).
    """


_ClientGetResourcesResponseResourceTagMappingListTypeDef = TypedDict(
    "_ClientGetResourcesResponseResourceTagMappingListTypeDef",
    {
        "ResourceARN": str,
        "Tags": List[ClientGetResourcesResponseResourceTagMappingListTagsTypeDef],
        "ComplianceDetails": ClientGetResourcesResponseResourceTagMappingListComplianceDetailsTypeDef,
    },
    total=False,
)


class ClientGetResourcesResponseResourceTagMappingListTypeDef(
    _ClientGetResourcesResponseResourceTagMappingListTypeDef
):
    """
    Type definition for `ClientGetResourcesResponse` `ResourceTagMappingList`

    A list of resource ARNs and the tags (keys and values) that are associated with each.

    - **ResourceARN** *(string) --*

      The ARN of the resource.

    - **Tags** *(list) --*

      The tags that have been applied to one or more AWS resources.

      - *(dict) --*

        The metadata that you apply to AWS resources to help you categorize and organize them. Each
        tag consists of a key and an optional value, both of which you define. For more information,
        see `Tagging AWS Resources
        <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the *AWS General
        Reference* .

        - **Key** *(string) --*

          One part of a key-value pair that makes up a tag. A key is a general label that acts like
          a category for more specific tag values.

        - **Value** *(string) --*

          The optional part of a key-value pair that make up a tag. A value acts as a descriptor
          within a tag category (key).

    - **ComplianceDetails** *(dict) --*

      Information that shows whether a resource is compliant with the effective tag policy,
      including details on any noncompliant tag keys.

      - **NoncompliantKeys** *(list) --*

        The tag key is noncompliant with the effective tag policy.

        - *(string) --*

      - **KeysWithNoncompliantValues** *(list) --*

        The tag value is noncompliant with the effective tag policy.

        - *(string) --*

      - **ComplianceStatus** *(boolean) --*

        Whether a resource is compliant with the effective tag policy.
    """


_ClientGetResourcesResponseTypeDef = TypedDict(
    "_ClientGetResourcesResponseTypeDef",
    {
        "PaginationToken": str,
        "ResourceTagMappingList": List[ClientGetResourcesResponseResourceTagMappingListTypeDef],
    },
    total=False,
)


class ClientGetResourcesResponseTypeDef(_ClientGetResourcesResponseTypeDef):
    """
    Type definition for `ClientGetResources` `Response`

    - **PaginationToken** *(string) --*

      A string that indicates that the response contains more data than can be returned in a single
      response. To receive additional data, specify this string for the ``PaginationToken`` value in
      a subsequent request.

    - **ResourceTagMappingList** *(list) --*

      A list of resource ARNs and the tags (keys and values) associated with each.

      - *(dict) --*

        A list of resource ARNs and the tags (keys and values) that are associated with each.

        - **ResourceARN** *(string) --*

          The ARN of the resource.

        - **Tags** *(list) --*

          The tags that have been applied to one or more AWS resources.

          - *(dict) --*

            The metadata that you apply to AWS resources to help you categorize and organize them.
            Each tag consists of a key and an optional value, both of which you define. For more
            information, see `Tagging AWS Resources
            <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the *AWS General
            Reference* .

            - **Key** *(string) --*

              One part of a key-value pair that makes up a tag. A key is a general label that acts
              like a category for more specific tag values.

            - **Value** *(string) --*

              The optional part of a key-value pair that make up a tag. A value acts as a descriptor
              within a tag category (key).

        - **ComplianceDetails** *(dict) --*

          Information that shows whether a resource is compliant with the effective tag policy,
          including details on any noncompliant tag keys.

          - **NoncompliantKeys** *(list) --*

            The tag key is noncompliant with the effective tag policy.

            - *(string) --*

          - **KeysWithNoncompliantValues** *(list) --*

            The tag value is noncompliant with the effective tag policy.

            - *(string) --*

          - **ComplianceStatus** *(boolean) --*

            Whether a resource is compliant with the effective tag policy.
    """


_ClientGetResourcesTagFiltersTypeDef = TypedDict(
    "_ClientGetResourcesTagFiltersTypeDef", {"Key": str, "Values": List[str]}, total=False
)


class ClientGetResourcesTagFiltersTypeDef(_ClientGetResourcesTagFiltersTypeDef):
    """
    Type definition for `ClientGetResources` `TagFilters`

    A list of tags (keys and values) that are used to specify the associated resources.

    - **Key** *(string) --*

      One part of a key-value pair that makes up a tag. A key is a general label that acts like a
      category for more specific tag values.

    - **Values** *(list) --*

      The optional part of a key-value pair that make up a tag. A value acts as a descriptor within
      a tag category (key).

      - *(string) --*
    """


_ClientGetTagKeysResponseTypeDef = TypedDict(
    "_ClientGetTagKeysResponseTypeDef", {"PaginationToken": str, "TagKeys": List[str]}, total=False
)


class ClientGetTagKeysResponseTypeDef(_ClientGetTagKeysResponseTypeDef):
    """
    Type definition for `ClientGetTagKeys` `Response`

    - **PaginationToken** *(string) --*

      A string that indicates that the response contains more data than can be returned in a single
      response. To receive additional data, specify this string for the ``PaginationToken`` value in
      a subsequent request.

    - **TagKeys** *(list) --*

      A list of all tag keys in the AWS account.

      - *(string) --*
    """


_ClientGetTagValuesResponseTypeDef = TypedDict(
    "_ClientGetTagValuesResponseTypeDef",
    {"PaginationToken": str, "TagValues": List[str]},
    total=False,
)


class ClientGetTagValuesResponseTypeDef(_ClientGetTagValuesResponseTypeDef):
    """
    Type definition for `ClientGetTagValues` `Response`

    - **PaginationToken** *(string) --*

      A string that indicates that the response contains more data than can be returned in a single
      response. To receive additional data, specify this string for the ``PaginationToken`` value in
      a subsequent request.

    - **TagValues** *(list) --*

      A list of all tag values for the specified key in the AWS account.

      - *(string) --*
    """


_ClientTagResourcesResponseFailedResourcesMapTypeDef = TypedDict(
    "_ClientTagResourcesResponseFailedResourcesMapTypeDef",
    {"StatusCode": int, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)


class ClientTagResourcesResponseFailedResourcesMapTypeDef(
    _ClientTagResourcesResponseFailedResourcesMapTypeDef
):
    """
    Type definition for `ClientTagResourcesResponse` `FailedResourcesMap`

    Details of the common errors that all actions return.

    - **StatusCode** *(integer) --*

      The HTTP status code of the common error.

    - **ErrorCode** *(string) --*

      The code of the common error. Valid values include ``InternalServiceException`` ,
      ``InvalidParameterException`` , and any valid error code returned by the AWS service that
      hosts the resource that you want to tag.

    - **ErrorMessage** *(string) --*

      The message of the common error.
    """


_ClientTagResourcesResponseTypeDef = TypedDict(
    "_ClientTagResourcesResponseTypeDef",
    {"FailedResourcesMap": Dict[str, ClientTagResourcesResponseFailedResourcesMapTypeDef]},
    total=False,
)


class ClientTagResourcesResponseTypeDef(_ClientTagResourcesResponseTypeDef):
    """
    Type definition for `ClientTagResources` `Response`

    - **FailedResourcesMap** *(dict) --*

      Details of resources that could not be tagged. An error code, status code, and error message
      are returned for each failed item.

      - *(string) --*

        - *(dict) --*

          Details of the common errors that all actions return.

          - **StatusCode** *(integer) --*

            The HTTP status code of the common error.

          - **ErrorCode** *(string) --*

            The code of the common error. Valid values include ``InternalServiceException`` ,
            ``InvalidParameterException`` , and any valid error code returned by the AWS service
            that hosts the resource that you want to tag.

          - **ErrorMessage** *(string) --*

            The message of the common error.
    """


_ClientUntagResourcesResponseFailedResourcesMapTypeDef = TypedDict(
    "_ClientUntagResourcesResponseFailedResourcesMapTypeDef",
    {"StatusCode": int, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)


class ClientUntagResourcesResponseFailedResourcesMapTypeDef(
    _ClientUntagResourcesResponseFailedResourcesMapTypeDef
):
    """
    Type definition for `ClientUntagResourcesResponse` `FailedResourcesMap`

    Details of the common errors that all actions return.

    - **StatusCode** *(integer) --*

      The HTTP status code of the common error.

    - **ErrorCode** *(string) --*

      The code of the common error. Valid values include ``InternalServiceException`` ,
      ``InvalidParameterException`` , and any valid error code returned by the AWS service that
      hosts the resource that you want to tag.

    - **ErrorMessage** *(string) --*

      The message of the common error.
    """


_ClientUntagResourcesResponseTypeDef = TypedDict(
    "_ClientUntagResourcesResponseTypeDef",
    {"FailedResourcesMap": Dict[str, ClientUntagResourcesResponseFailedResourcesMapTypeDef]},
    total=False,
)


class ClientUntagResourcesResponseTypeDef(_ClientUntagResourcesResponseTypeDef):
    """
    Type definition for `ClientUntagResources` `Response`

    - **FailedResourcesMap** *(dict) --*

      Details of resources that could not be untagged. An error code, status code, and error message
      are returned for each failed item.

      - *(string) --*

        - *(dict) --*

          Details of the common errors that all actions return.

          - **StatusCode** *(integer) --*

            The HTTP status code of the common error.

          - **ErrorCode** *(string) --*

            The code of the common error. Valid values include ``InternalServiceException`` ,
            ``InvalidParameterException`` , and any valid error code returned by the AWS service
            that hosts the resource that you want to tag.

          - **ErrorMessage** *(string) --*

            The message of the common error.
    """


_GetComplianceSummaryPaginatePaginationConfigTypeDef = TypedDict(
    "_GetComplianceSummaryPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class GetComplianceSummaryPaginatePaginationConfigTypeDef(
    _GetComplianceSummaryPaginatePaginationConfigTypeDef
):
    """
    Type definition for `GetComplianceSummaryPaginate` `PaginationConfig`

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


_GetComplianceSummaryPaginateResponseSummaryListTypeDef = TypedDict(
    "_GetComplianceSummaryPaginateResponseSummaryListTypeDef",
    {
        "LastUpdated": str,
        "TargetId": str,
        "TargetIdType": str,
        "Region": str,
        "ResourceType": str,
        "NonCompliantResources": int,
    },
    total=False,
)


class GetComplianceSummaryPaginateResponseSummaryListTypeDef(
    _GetComplianceSummaryPaginateResponseSummaryListTypeDef
):
    """
    Type definition for `GetComplianceSummaryPaginateResponse` `SummaryList`

    A count of noncompliant resources.

    - **LastUpdated** *(string) --*

      The timestamp that shows when this summary was generated in this Region.

    - **TargetId** *(string) --*

      The account identifier or the root identifier of the organization. If you don't know the root
      ID, you can call the AWS Organizations `ListRoots
      <http://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`__ API.

    - **TargetIdType** *(string) --*

      Whether the target is an account, an OU, or the organization root.

    - **Region** *(string) --*

      The AWS Region that the summary applies to.

    - **ResourceType** *(string) --*

      The AWS resource type.

    - **NonCompliantResources** *(integer) --*

      The count of noncompliant resources.
    """


_GetComplianceSummaryPaginateResponseTypeDef = TypedDict(
    "_GetComplianceSummaryPaginateResponseTypeDef",
    {"SummaryList": List[GetComplianceSummaryPaginateResponseSummaryListTypeDef], "NextToken": str},
    total=False,
)


class GetComplianceSummaryPaginateResponseTypeDef(_GetComplianceSummaryPaginateResponseTypeDef):
    """
    Type definition for `GetComplianceSummaryPaginate` `Response`

    - **SummaryList** *(list) --*

      A table that shows counts of noncompliant resources.

      - *(dict) --*

        A count of noncompliant resources.

        - **LastUpdated** *(string) --*

          The timestamp that shows when this summary was generated in this Region.

        - **TargetId** *(string) --*

          The account identifier or the root identifier of the organization. If you don't know the
          root ID, you can call the AWS Organizations `ListRoots
          <http://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`__ API.

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


_GetResourcesPaginatePaginationConfigTypeDef = TypedDict(
    "_GetResourcesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class GetResourcesPaginatePaginationConfigTypeDef(_GetResourcesPaginatePaginationConfigTypeDef):
    """
    Type definition for `GetResourcesPaginate` `PaginationConfig`

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


_GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef = TypedDict(
    "_GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef",
    {
        "NoncompliantKeys": List[str],
        "KeysWithNoncompliantValues": List[str],
        "ComplianceStatus": bool,
    },
    total=False,
)


class GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef(
    _GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef
):
    """
    Type definition for `GetResourcesPaginateResponseResourceTagMappingList` `ComplianceDetails`

    Information that shows whether a resource is compliant with the effective tag policy, including
    details on any noncompliant tag keys.

    - **NoncompliantKeys** *(list) --*

      The tag key is noncompliant with the effective tag policy.

      - *(string) --*

    - **KeysWithNoncompliantValues** *(list) --*

      The tag value is noncompliant with the effective tag policy.

      - *(string) --*

    - **ComplianceStatus** *(boolean) --*

      Whether a resource is compliant with the effective tag policy.
    """


_GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef = TypedDict(
    "_GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef",
    {"Key": str, "Value": str},
    total=False,
)


class GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef(
    _GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef
):
    """
    Type definition for `GetResourcesPaginateResponseResourceTagMappingList` `Tags`

    The metadata that you apply to AWS resources to help you categorize and organize them. Each tag
    consists of a key and an optional value, both of which you define. For more information, see
    `Tagging AWS Resources <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the
    *AWS General Reference* .

    - **Key** *(string) --*

      One part of a key-value pair that makes up a tag. A key is a general label that acts like a
      category for more specific tag values.

    - **Value** *(string) --*

      The optional part of a key-value pair that make up a tag. A value acts as a descriptor within
      a tag category (key).
    """


_GetResourcesPaginateResponseResourceTagMappingListTypeDef = TypedDict(
    "_GetResourcesPaginateResponseResourceTagMappingListTypeDef",
    {
        "ResourceARN": str,
        "Tags": List[GetResourcesPaginateResponseResourceTagMappingListTagsTypeDef],
        "ComplianceDetails": GetResourcesPaginateResponseResourceTagMappingListComplianceDetailsTypeDef,
    },
    total=False,
)


class GetResourcesPaginateResponseResourceTagMappingListTypeDef(
    _GetResourcesPaginateResponseResourceTagMappingListTypeDef
):
    """
    Type definition for `GetResourcesPaginateResponse` `ResourceTagMappingList`

    A list of resource ARNs and the tags (keys and values) that are associated with each.

    - **ResourceARN** *(string) --*

      The ARN of the resource.

    - **Tags** *(list) --*

      The tags that have been applied to one or more AWS resources.

      - *(dict) --*

        The metadata that you apply to AWS resources to help you categorize and organize them. Each
        tag consists of a key and an optional value, both of which you define. For more information,
        see `Tagging AWS Resources
        <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the *AWS General
        Reference* .

        - **Key** *(string) --*

          One part of a key-value pair that makes up a tag. A key is a general label that acts like
          a category for more specific tag values.

        - **Value** *(string) --*

          The optional part of a key-value pair that make up a tag. A value acts as a descriptor
          within a tag category (key).

    - **ComplianceDetails** *(dict) --*

      Information that shows whether a resource is compliant with the effective tag policy,
      including details on any noncompliant tag keys.

      - **NoncompliantKeys** *(list) --*

        The tag key is noncompliant with the effective tag policy.

        - *(string) --*

      - **KeysWithNoncompliantValues** *(list) --*

        The tag value is noncompliant with the effective tag policy.

        - *(string) --*

      - **ComplianceStatus** *(boolean) --*

        Whether a resource is compliant with the effective tag policy.
    """


_GetResourcesPaginateResponseTypeDef = TypedDict(
    "_GetResourcesPaginateResponseTypeDef",
    {
        "ResourceTagMappingList": List[GetResourcesPaginateResponseResourceTagMappingListTypeDef],
        "NextToken": str,
    },
    total=False,
)


class GetResourcesPaginateResponseTypeDef(_GetResourcesPaginateResponseTypeDef):
    """
    Type definition for `GetResourcesPaginate` `Response`

    - **ResourceTagMappingList** *(list) --*

      A list of resource ARNs and the tags (keys and values) associated with each.

      - *(dict) --*

        A list of resource ARNs and the tags (keys and values) that are associated with each.

        - **ResourceARN** *(string) --*

          The ARN of the resource.

        - **Tags** *(list) --*

          The tags that have been applied to one or more AWS resources.

          - *(dict) --*

            The metadata that you apply to AWS resources to help you categorize and organize them.
            Each tag consists of a key and an optional value, both of which you define. For more
            information, see `Tagging AWS Resources
            <http://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__ in the *AWS General
            Reference* .

            - **Key** *(string) --*

              One part of a key-value pair that makes up a tag. A key is a general label that acts
              like a category for more specific tag values.

            - **Value** *(string) --*

              The optional part of a key-value pair that make up a tag. A value acts as a descriptor
              within a tag category (key).

        - **ComplianceDetails** *(dict) --*

          Information that shows whether a resource is compliant with the effective tag policy,
          including details on any noncompliant tag keys.

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


_GetResourcesPaginateTagFiltersTypeDef = TypedDict(
    "_GetResourcesPaginateTagFiltersTypeDef", {"Key": str, "Values": List[str]}, total=False
)


class GetResourcesPaginateTagFiltersTypeDef(_GetResourcesPaginateTagFiltersTypeDef):
    """
    Type definition for `GetResourcesPaginate` `TagFilters`

    A list of tags (keys and values) that are used to specify the associated resources.

    - **Key** *(string) --*

      One part of a key-value pair that makes up a tag. A key is a general label that acts like a
      category for more specific tag values.

    - **Values** *(list) --*

      The optional part of a key-value pair that make up a tag. A value acts as a descriptor within
      a tag category (key).

      - *(string) --*
    """


_GetTagKeysPaginatePaginationConfigTypeDef = TypedDict(
    "_GetTagKeysPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "StartingToken": str},
    total=False,
)


class GetTagKeysPaginatePaginationConfigTypeDef(_GetTagKeysPaginatePaginationConfigTypeDef):
    """
    Type definition for `GetTagKeysPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_GetTagKeysPaginateResponseTypeDef = TypedDict(
    "_GetTagKeysPaginateResponseTypeDef", {"TagKeys": List[str], "NextToken": str}, total=False
)


class GetTagKeysPaginateResponseTypeDef(_GetTagKeysPaginateResponseTypeDef):
    """
    Type definition for `GetTagKeysPaginate` `Response`

    - **TagKeys** *(list) --*

      A list of all tag keys in the AWS account.

      - *(string) --*

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_GetTagValuesPaginatePaginationConfigTypeDef = TypedDict(
    "_GetTagValuesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "StartingToken": str},
    total=False,
)


class GetTagValuesPaginatePaginationConfigTypeDef(_GetTagValuesPaginatePaginationConfigTypeDef):
    """
    Type definition for `GetTagValuesPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_GetTagValuesPaginateResponseTypeDef = TypedDict(
    "_GetTagValuesPaginateResponseTypeDef", {"TagValues": List[str], "NextToken": str}, total=False
)


class GetTagValuesPaginateResponseTypeDef(_GetTagValuesPaginateResponseTypeDef):
    """
    Type definition for `GetTagValuesPaginate` `Response`

    - **TagValues** *(list) --*

      A list of all tag values for the specified key in the AWS account.

      - *(string) --*

    - **NextToken** *(string) --*

      A token to resume pagination.
    """
