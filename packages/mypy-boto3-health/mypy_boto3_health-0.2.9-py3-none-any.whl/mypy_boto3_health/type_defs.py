"Main interface for health type defs"
from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientDescribeAffectedEntitiesResponseentitiesTypeDef",
    "ClientDescribeAffectedEntitiesResponseTypeDef",
    "ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef",
    "ClientDescribeAffectedEntitiesfilterTypeDef",
    "ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef",
    "ClientDescribeEntityAggregatesResponseTypeDef",
    "ClientDescribeEventAggregatesResponseeventAggregatesTypeDef",
    "ClientDescribeEventAggregatesResponseTypeDef",
    "ClientDescribeEventAggregatesfilterendTimesTypeDef",
    "ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef",
    "ClientDescribeEventAggregatesfilterstartTimesTypeDef",
    "ClientDescribeEventAggregatesfilterTypeDef",
    "ClientDescribeEventDetailsResponsefailedSetTypeDef",
    "ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef",
    "ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef",
    "ClientDescribeEventDetailsResponsesuccessfulSetTypeDef",
    "ClientDescribeEventDetailsResponseTypeDef",
    "ClientDescribeEventTypesResponseeventTypesTypeDef",
    "ClientDescribeEventTypesResponseTypeDef",
    "ClientDescribeEventTypesfilterTypeDef",
    "ClientDescribeEventsResponseeventsTypeDef",
    "ClientDescribeEventsResponseTypeDef",
    "ClientDescribeEventsfilterendTimesTypeDef",
    "ClientDescribeEventsfilterlastUpdatedTimesTypeDef",
    "ClientDescribeEventsfilterstartTimesTypeDef",
    "ClientDescribeEventsfilterTypeDef",
    "DescribeAffectedEntitiesPaginatePaginationConfigTypeDef",
    "DescribeAffectedEntitiesPaginateResponseentitiesTypeDef",
    "DescribeAffectedEntitiesPaginateResponseTypeDef",
    "DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef",
    "DescribeAffectedEntitiesPaginatefilterTypeDef",
    "DescribeEventAggregatesPaginatePaginationConfigTypeDef",
    "DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef",
    "DescribeEventAggregatesPaginateResponseTypeDef",
    "DescribeEventAggregatesPaginatefilterendTimesTypeDef",
    "DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef",
    "DescribeEventAggregatesPaginatefilterstartTimesTypeDef",
    "DescribeEventAggregatesPaginatefilterTypeDef",
    "DescribeEventTypesPaginatePaginationConfigTypeDef",
    "DescribeEventTypesPaginateResponseeventTypesTypeDef",
    "DescribeEventTypesPaginateResponseTypeDef",
    "DescribeEventTypesPaginatefilterTypeDef",
    "DescribeEventsPaginatePaginationConfigTypeDef",
    "DescribeEventsPaginateResponseeventsTypeDef",
    "DescribeEventsPaginateResponseTypeDef",
    "DescribeEventsPaginatefilterendTimesTypeDef",
    "DescribeEventsPaginatefilterlastUpdatedTimesTypeDef",
    "DescribeEventsPaginatefilterstartTimesTypeDef",
    "DescribeEventsPaginatefilterTypeDef",
)


_ClientDescribeAffectedEntitiesResponseentitiesTypeDef = TypedDict(
    "_ClientDescribeAffectedEntitiesResponseentitiesTypeDef",
    {
        "entityArn": str,
        "eventArn": str,
        "entityValue": str,
        "entityUrl": str,
        "awsAccountId": str,
        "lastUpdatedTime": datetime,
        "statusCode": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ClientDescribeAffectedEntitiesResponseentitiesTypeDef(
    _ClientDescribeAffectedEntitiesResponseentitiesTypeDef
):
    """
    Type definition for `ClientDescribeAffectedEntitiesResponse` `entities`

    Information about an entity that is affected by a Health event.

    - **entityArn** *(string) --*

      The unique identifier for the entity. Format: ``arn:aws:health:*entity-region* :*aws-account*
      :entity/*entity-id* `` . Example:
      ``arn:aws:health:us-east-1:111222333444:entity/AVh5GGT7ul1arKr1sE1K``

    - **eventArn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **entityValue** *(string) --*

      The ID of the affected entity.

    - **entityUrl** *(string) --*

    - **awsAccountId** *(string) --*

      The 12-digit AWS account number that contains the affected entity.

    - **lastUpdatedTime** *(datetime) --*

      The most recent time that the entity was updated.

    - **statusCode** *(string) --*

      The most recent status of the entity affected by the event. The possible values are
      ``IMPAIRED`` , ``UNIMPAIRED`` , and ``UNKNOWN`` .

    - **tags** *(dict) --*

      A map of entity tags attached to the affected entity.

      - *(string) --*

        - *(string) --*
    """


_ClientDescribeAffectedEntitiesResponseTypeDef = TypedDict(
    "_ClientDescribeAffectedEntitiesResponseTypeDef",
    {"entities": List[ClientDescribeAffectedEntitiesResponseentitiesTypeDef], "nextToken": str},
    total=False,
)


class ClientDescribeAffectedEntitiesResponseTypeDef(_ClientDescribeAffectedEntitiesResponseTypeDef):
    """
    Type definition for `ClientDescribeAffectedEntities` `Response`

    - **entities** *(list) --*

      The entities that match the filter criteria.

      - *(dict) --*

        Information about an entity that is affected by a Health event.

        - **entityArn** *(string) --*

          The unique identifier for the entity. Format: ``arn:aws:health:*entity-region*
          :*aws-account* :entity/*entity-id* `` . Example:
          ``arn:aws:health:us-east-1:111222333444:entity/AVh5GGT7ul1arKr1sE1K``

        - **eventArn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **entityValue** *(string) --*

          The ID of the affected entity.

        - **entityUrl** *(string) --*

        - **awsAccountId** *(string) --*

          The 12-digit AWS account number that contains the affected entity.

        - **lastUpdatedTime** *(datetime) --*

          The most recent time that the entity was updated.

        - **statusCode** *(string) --*

          The most recent status of the entity affected by the event. The possible values are
          ``IMPAIRED`` , ``UNIMPAIRED`` , and ``UNKNOWN`` .

        - **tags** *(dict) --*

          A map of entity tags attached to the affected entity.

          - *(string) --*

            - *(string) --*

    - **nextToken** *(string) --*

      If the results of a search are large, only a portion of the results are returned, and a
      ``nextToken`` pagination token is returned in the response. To retrieve the next batch of
      results, reissue the search request and include the returned token. When all results have been
      returned, the response does not contain a pagination token value.
    """


_ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef = TypedDict(
    "_ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef(
    _ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `ClientDescribeAffectedEntitiesfilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_RequiredClientDescribeAffectedEntitiesfilterTypeDef = TypedDict(
    "_RequiredClientDescribeAffectedEntitiesfilterTypeDef", {"eventArns": List[str]}
)
_OptionalClientDescribeAffectedEntitiesfilterTypeDef = TypedDict(
    "_OptionalClientDescribeAffectedEntitiesfilterTypeDef",
    {
        "entityArns": List[str],
        "entityValues": List[str],
        "lastUpdatedTimes": List[ClientDescribeAffectedEntitiesfilterlastUpdatedTimesTypeDef],
        "tags": List[Dict[str, str]],
        "statusCodes": List[str],
    },
    total=False,
)


class ClientDescribeAffectedEntitiesfilterTypeDef(
    _RequiredClientDescribeAffectedEntitiesfilterTypeDef,
    _OptionalClientDescribeAffectedEntitiesfilterTypeDef,
):
    """
    Type definition for `ClientDescribeAffectedEntities` `filter`

    Values to narrow the results returned. At least one event ARN is required.

    - **eventArns** *(list) --* **[REQUIRED]**

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of IDs for affected entities.

      - *(string) --*

    - **lastUpdatedTimes** *(list) --*

      A list of the most recent dates and times that the entity was updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **statusCodes** *(list) --*

      A list of entity status codes (``IMPAIRED`` , ``UNIMPAIRED`` , or ``UNKNOWN`` ).

      - *(string) --*
    """


_ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef = TypedDict(
    "_ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef",
    {"eventArn": str, "count": int},
    total=False,
)


class ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef(
    _ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef
):
    """
    Type definition for `ClientDescribeEntityAggregatesResponse` `entityAggregates`

    The number of entities that are affected by one or more events. Returned by the
    DescribeEntityAggregates operation.

    - **eventArn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **count** *(integer) --*

      The number entities that match the criteria for the specified events.
    """


_ClientDescribeEntityAggregatesResponseTypeDef = TypedDict(
    "_ClientDescribeEntityAggregatesResponseTypeDef",
    {"entityAggregates": List[ClientDescribeEntityAggregatesResponseentityAggregatesTypeDef]},
    total=False,
)


class ClientDescribeEntityAggregatesResponseTypeDef(_ClientDescribeEntityAggregatesResponseTypeDef):
    """
    Type definition for `ClientDescribeEntityAggregates` `Response`

    - **entityAggregates** *(list) --*

      The number of entities that are affected by each of the specified events.

      - *(dict) --*

        The number of entities that are affected by one or more events. Returned by the
        DescribeEntityAggregates operation.

        - **eventArn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **count** *(integer) --*

          The number entities that match the criteria for the specified events.
    """


_ClientDescribeEventAggregatesResponseeventAggregatesTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesResponseeventAggregatesTypeDef",
    {"aggregateValue": str, "count": int},
    total=False,
)


class ClientDescribeEventAggregatesResponseeventAggregatesTypeDef(
    _ClientDescribeEventAggregatesResponseeventAggregatesTypeDef
):
    """
    Type definition for `ClientDescribeEventAggregatesResponse` `eventAggregates`

    The number of events of each issue type. Returned by the  DescribeEventAggregates operation.

    - **aggregateValue** *(string) --*

      The issue type for the associated count.

    - **count** *(integer) --*

      The number of events of the associated issue type.
    """


_ClientDescribeEventAggregatesResponseTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesResponseTypeDef",
    {
        "eventAggregates": List[ClientDescribeEventAggregatesResponseeventAggregatesTypeDef],
        "nextToken": str,
    },
    total=False,
)


class ClientDescribeEventAggregatesResponseTypeDef(_ClientDescribeEventAggregatesResponseTypeDef):
    """
    Type definition for `ClientDescribeEventAggregates` `Response`

    - **eventAggregates** *(list) --*

      The number of events in each category that meet the optional filter criteria.

      - *(dict) --*

        The number of events of each issue type. Returned by the  DescribeEventAggregates operation.

        - **aggregateValue** *(string) --*

          The issue type for the associated count.

        - **count** *(integer) --*

          The number of events of the associated issue type.

    - **nextToken** *(string) --*

      If the results of a search are large, only a portion of the results are returned, and a
      ``nextToken`` pagination token is returned in the response. To retrieve the next batch of
      results, reissue the search request and include the returned token. When all results have been
      returned, the response does not contain a pagination token value.
    """


_ClientDescribeEventAggregatesfilterendTimesTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesfilterendTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class ClientDescribeEventAggregatesfilterendTimesTypeDef(
    _ClientDescribeEventAggregatesfilterendTimesTypeDef
):
    """
    Type definition for `ClientDescribeEventAggregatesfilter` `endTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef(
    _ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `ClientDescribeEventAggregatesfilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventAggregatesfilterstartTimesTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesfilterstartTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class ClientDescribeEventAggregatesfilterstartTimesTypeDef(
    _ClientDescribeEventAggregatesfilterstartTimesTypeDef
):
    """
    Type definition for `ClientDescribeEventAggregatesfilter` `startTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventAggregatesfilterTypeDef = TypedDict(
    "_ClientDescribeEventAggregatesfilterTypeDef",
    {
        "eventArns": List[str],
        "eventTypeCodes": List[str],
        "services": List[str],
        "regions": List[str],
        "availabilityZones": List[str],
        "startTimes": List[ClientDescribeEventAggregatesfilterstartTimesTypeDef],
        "endTimes": List[ClientDescribeEventAggregatesfilterendTimesTypeDef],
        "lastUpdatedTimes": List[ClientDescribeEventAggregatesfilterlastUpdatedTimesTypeDef],
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[str],
        "tags": List[Dict[str, str]],
        "eventStatusCodes": List[str],
    },
    total=False,
)


class ClientDescribeEventAggregatesfilterTypeDef(_ClientDescribeEventAggregatesfilterTypeDef):
    """
    Type definition for `ClientDescribeEventAggregates` `filter`

    Values to narrow the results returned.

    - **eventArns** *(list) --*

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **eventTypeCodes** *(list) --*

      A list of unique identifiers for event types. For example,
      ``"AWS_EC2_SYSTEM_MAINTENANCE_EVENT","AWS_RDS_MAINTENANCE_SCHEDULED"``

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **regions** *(list) --*

      A list of AWS regions.

      - *(string) --*

    - **availabilityZones** *(list) --*

      A list of AWS availability zones.

      - *(string) --*

    - **startTimes** *(list) --*

      A list of dates and times that the event began.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **endTimes** *(list) --*

      A list of dates and times that the event ended.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **lastUpdatedTimes** *(list) --*

      A list of dates and times that the event was last updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of entity identifiers, such as EC2 instance IDs (``i-34ab692e`` ) or EBS volumes
      (``vol-426ab23e`` ).

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **eventStatusCodes** *(list) --*

      A list of event status codes.

      - *(string) --*
    """


_ClientDescribeEventDetailsResponsefailedSetTypeDef = TypedDict(
    "_ClientDescribeEventDetailsResponsefailedSetTypeDef",
    {"eventArn": str, "errorName": str, "errorMessage": str},
    total=False,
)


class ClientDescribeEventDetailsResponsefailedSetTypeDef(
    _ClientDescribeEventDetailsResponsefailedSetTypeDef
):
    """
    Type definition for `ClientDescribeEventDetailsResponse` `failedSet`

    Error information returned when a  DescribeEventDetails operation cannot find a specified event.

    - **eventArn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **errorName** *(string) --*

      The name of the error.

    - **errorMessage** *(string) --*

      A message that describes the error.
    """


_ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef = TypedDict(
    "_ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef",
    {"latestDescription": str},
    total=False,
)


class ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef(
    _ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef
):
    """
    Type definition for `ClientDescribeEventDetailsResponsesuccessfulSet` `eventDescription`

    The most recent description of the event.

    - **latestDescription** *(string) --*

      The most recent description of the event.
    """


_ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef = TypedDict(
    "_ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": str,
        "region": str,
        "availabilityZone": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": str,
    },
    total=False,
)


class ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef(
    _ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef
):
    """
    Type definition for `ClientDescribeEventDetailsResponsesuccessfulSet` `event`

    Summary information about the event.

    - **arn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **service** *(string) --*

      The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

    - **eventTypeCode** *(string) --*

      The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
      for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

    - **eventTypeCategory** *(string) --*

      The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
      ``accountNotification`` .

    - **region** *(string) --*

      The AWS region name of the event.

    - **availabilityZone** *(string) --*

      The AWS Availability Zone of the event. For example, us-east-1a.

    - **startTime** *(datetime) --*

      The date and time that the event began.

    - **endTime** *(datetime) --*

      The date and time that the event ended.

    - **lastUpdatedTime** *(datetime) --*

      The most recent date and time that the event was updated.

    - **statusCode** *(string) --*

      The most recent status of the event. Possible values are ``open`` , ``closed`` , and
      ``upcoming`` .
    """


_ClientDescribeEventDetailsResponsesuccessfulSetTypeDef = TypedDict(
    "_ClientDescribeEventDetailsResponsesuccessfulSetTypeDef",
    {
        "event": ClientDescribeEventDetailsResponsesuccessfulSeteventTypeDef,
        "eventDescription": ClientDescribeEventDetailsResponsesuccessfulSeteventDescriptionTypeDef,
        "eventMetadata": Dict[str, str],
    },
    total=False,
)


class ClientDescribeEventDetailsResponsesuccessfulSetTypeDef(
    _ClientDescribeEventDetailsResponsesuccessfulSetTypeDef
):
    """
    Type definition for `ClientDescribeEventDetailsResponse` `successfulSet`

    Detailed information about an event. A combination of an  Event object, an  EventDescription
    object, and additional metadata about the event. Returned by the  DescribeEventDetails
    operation.

    - **event** *(dict) --*

      Summary information about the event.

      - **arn** *(string) --*

        The unique identifier for the event. Format: ``arn:aws:health:*event-region*
        ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
        arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

      - **service** *(string) --*

        The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

      - **eventTypeCode** *(string) --*

        The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
        for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

      - **eventTypeCategory** *(string) --*

        The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
        ``accountNotification`` .

      - **region** *(string) --*

        The AWS region name of the event.

      - **availabilityZone** *(string) --*

        The AWS Availability Zone of the event. For example, us-east-1a.

      - **startTime** *(datetime) --*

        The date and time that the event began.

      - **endTime** *(datetime) --*

        The date and time that the event ended.

      - **lastUpdatedTime** *(datetime) --*

        The most recent date and time that the event was updated.

      - **statusCode** *(string) --*

        The most recent status of the event. Possible values are ``open`` , ``closed`` , and
        ``upcoming`` .

    - **eventDescription** *(dict) --*

      The most recent description of the event.

      - **latestDescription** *(string) --*

        The most recent description of the event.

    - **eventMetadata** *(dict) --*

      Additional metadata about the event.

      - *(string) --*

        - *(string) --*
    """


_ClientDescribeEventDetailsResponseTypeDef = TypedDict(
    "_ClientDescribeEventDetailsResponseTypeDef",
    {
        "successfulSet": List[ClientDescribeEventDetailsResponsesuccessfulSetTypeDef],
        "failedSet": List[ClientDescribeEventDetailsResponsefailedSetTypeDef],
    },
    total=False,
)


class ClientDescribeEventDetailsResponseTypeDef(_ClientDescribeEventDetailsResponseTypeDef):
    """
    Type definition for `ClientDescribeEventDetails` `Response`

    - **successfulSet** *(list) --*

      Information about the events that could be retrieved.

      - *(dict) --*

        Detailed information about an event. A combination of an  Event object, an  EventDescription
        object, and additional metadata about the event. Returned by the  DescribeEventDetails
        operation.

        - **event** *(dict) --*

          Summary information about the event.

          - **arn** *(string) --*

            The unique identifier for the event. Format: ``arn:aws:health:*event-region*
            ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
            arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

          - **service** *(string) --*

            The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

          - **eventTypeCode** *(string) --*

            The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION*
            `` ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

          - **eventTypeCategory** *(string) --*

            The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
            ``accountNotification`` .

          - **region** *(string) --*

            The AWS region name of the event.

          - **availabilityZone** *(string) --*

            The AWS Availability Zone of the event. For example, us-east-1a.

          - **startTime** *(datetime) --*

            The date and time that the event began.

          - **endTime** *(datetime) --*

            The date and time that the event ended.

          - **lastUpdatedTime** *(datetime) --*

            The most recent date and time that the event was updated.

          - **statusCode** *(string) --*

            The most recent status of the event. Possible values are ``open`` , ``closed`` , and
            ``upcoming`` .

        - **eventDescription** *(dict) --*

          The most recent description of the event.

          - **latestDescription** *(string) --*

            The most recent description of the event.

        - **eventMetadata** *(dict) --*

          Additional metadata about the event.

          - *(string) --*

            - *(string) --*

    - **failedSet** *(list) --*

      Error messages for any events that could not be retrieved.

      - *(dict) --*

        Error information returned when a  DescribeEventDetails operation cannot find a specified
        event.

        - **eventArn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **errorName** *(string) --*

          The name of the error.

        - **errorMessage** *(string) --*

          A message that describes the error.
    """


_ClientDescribeEventTypesResponseeventTypesTypeDef = TypedDict(
    "_ClientDescribeEventTypesResponseeventTypesTypeDef",
    {"service": str, "code": str, "category": str},
    total=False,
)


class ClientDescribeEventTypesResponseeventTypesTypeDef(
    _ClientDescribeEventTypesResponseeventTypesTypeDef
):
    """
    Type definition for `ClientDescribeEventTypesResponse` `eventTypes`

    Metadata about a type of event that is reported by AWS Health. Data consists of the category
    (for example, ``issue`` ), the service (for example, ``EC2`` ), and the event type code (for
    example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

    - **service** *(string) --*

      The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

    - **code** *(string) --*

      The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
      for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

    - **category** *(string) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).
    """


_ClientDescribeEventTypesResponseTypeDef = TypedDict(
    "_ClientDescribeEventTypesResponseTypeDef",
    {"eventTypes": List[ClientDescribeEventTypesResponseeventTypesTypeDef], "nextToken": str},
    total=False,
)


class ClientDescribeEventTypesResponseTypeDef(_ClientDescribeEventTypesResponseTypeDef):
    """
    Type definition for `ClientDescribeEventTypes` `Response`

    - **eventTypes** *(list) --*

      A list of event types that match the filter criteria. Event types have a category (``issue`` ,
      ``accountNotification`` , or ``scheduledChange`` ), a service (for example, ``EC2`` , ``RDS``
      , ``DATAPIPELINE`` , ``BILLING`` ), and a code (in the format ``AWS_*SERVICE* _*DESCRIPTION*
      `` ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

      - *(dict) --*

        Metadata about a type of event that is reported by AWS Health. Data consists of the category
        (for example, ``issue`` ), the service (for example, ``EC2`` ), and the event type code (for
        example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

        - **service** *(string) --*

          The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

        - **code** *(string) --*

          The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* ``
          ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

        - **category** *(string) --*

          A list of event type category codes (``issue`` , ``scheduledChange`` , or
          ``accountNotification`` ).

    - **nextToken** *(string) --*

      If the results of a search are large, only a portion of the results are returned, and a
      ``nextToken`` pagination token is returned in the response. To retrieve the next batch of
      results, reissue the search request and include the returned token. When all results have been
      returned, the response does not contain a pagination token value.
    """


_ClientDescribeEventTypesfilterTypeDef = TypedDict(
    "_ClientDescribeEventTypesfilterTypeDef",
    {"eventTypeCodes": List[str], "services": List[str], "eventTypeCategories": List[str]},
    total=False,
)


class ClientDescribeEventTypesfilterTypeDef(_ClientDescribeEventTypesfilterTypeDef):
    """
    Type definition for `ClientDescribeEventTypes` `filter`

    Values to narrow the results returned.

    - **eventTypeCodes** *(list) --*

      A list of event type codes.

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*
    """


_ClientDescribeEventsResponseeventsTypeDef = TypedDict(
    "_ClientDescribeEventsResponseeventsTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": str,
        "region": str,
        "availabilityZone": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": str,
    },
    total=False,
)


class ClientDescribeEventsResponseeventsTypeDef(_ClientDescribeEventsResponseeventsTypeDef):
    """
    Type definition for `ClientDescribeEventsResponse` `events`

    Summary information about an event, returned by the  DescribeEvents operation. The
    DescribeEventDetails operation also returns this information, as well as the  EventDescription
    and additional event metadata.

    - **arn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **service** *(string) --*

      The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

    - **eventTypeCode** *(string) --*

      The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
      for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

    - **eventTypeCategory** *(string) --*

      The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
      ``accountNotification`` .

    - **region** *(string) --*

      The AWS region name of the event.

    - **availabilityZone** *(string) --*

      The AWS Availability Zone of the event. For example, us-east-1a.

    - **startTime** *(datetime) --*

      The date and time that the event began.

    - **endTime** *(datetime) --*

      The date and time that the event ended.

    - **lastUpdatedTime** *(datetime) --*

      The most recent date and time that the event was updated.

    - **statusCode** *(string) --*

      The most recent status of the event. Possible values are ``open`` , ``closed`` , and
      ``upcoming`` .
    """


_ClientDescribeEventsResponseTypeDef = TypedDict(
    "_ClientDescribeEventsResponseTypeDef",
    {"events": List[ClientDescribeEventsResponseeventsTypeDef], "nextToken": str},
    total=False,
)


class ClientDescribeEventsResponseTypeDef(_ClientDescribeEventsResponseTypeDef):
    """
    Type definition for `ClientDescribeEvents` `Response`

    - **events** *(list) --*

      The events that match the specified filter criteria.

      - *(dict) --*

        Summary information about an event, returned by the  DescribeEvents operation. The
        DescribeEventDetails operation also returns this information, as well as the
        EventDescription and additional event metadata.

        - **arn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **service** *(string) --*

          The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

        - **eventTypeCode** *(string) --*

          The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* ``
          ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

        - **eventTypeCategory** *(string) --*

          The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
          ``accountNotification`` .

        - **region** *(string) --*

          The AWS region name of the event.

        - **availabilityZone** *(string) --*

          The AWS Availability Zone of the event. For example, us-east-1a.

        - **startTime** *(datetime) --*

          The date and time that the event began.

        - **endTime** *(datetime) --*

          The date and time that the event ended.

        - **lastUpdatedTime** *(datetime) --*

          The most recent date and time that the event was updated.

        - **statusCode** *(string) --*

          The most recent status of the event. Possible values are ``open`` , ``closed`` , and
          ``upcoming`` .

    - **nextToken** *(string) --*

      If the results of a search are large, only a portion of the results are returned, and a
      ``nextToken`` pagination token is returned in the response. To retrieve the next batch of
      results, reissue the search request and include the returned token. When all results have been
      returned, the response does not contain a pagination token value.
    """


_ClientDescribeEventsfilterendTimesTypeDef = TypedDict(
    "_ClientDescribeEventsfilterendTimesTypeDef", {"from": datetime, "to": datetime}, total=False
)


class ClientDescribeEventsfilterendTimesTypeDef(_ClientDescribeEventsfilterendTimesTypeDef):
    """
    Type definition for `ClientDescribeEventsfilter` `endTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventsfilterlastUpdatedTimesTypeDef = TypedDict(
    "_ClientDescribeEventsfilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class ClientDescribeEventsfilterlastUpdatedTimesTypeDef(
    _ClientDescribeEventsfilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `ClientDescribeEventsfilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventsfilterstartTimesTypeDef = TypedDict(
    "_ClientDescribeEventsfilterstartTimesTypeDef", {"from": datetime, "to": datetime}, total=False
)


class ClientDescribeEventsfilterstartTimesTypeDef(_ClientDescribeEventsfilterstartTimesTypeDef):
    """
    Type definition for `ClientDescribeEventsfilter` `startTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_ClientDescribeEventsfilterTypeDef = TypedDict(
    "_ClientDescribeEventsfilterTypeDef",
    {
        "eventArns": List[str],
        "eventTypeCodes": List[str],
        "services": List[str],
        "regions": List[str],
        "availabilityZones": List[str],
        "startTimes": List[ClientDescribeEventsfilterstartTimesTypeDef],
        "endTimes": List[ClientDescribeEventsfilterendTimesTypeDef],
        "lastUpdatedTimes": List[ClientDescribeEventsfilterlastUpdatedTimesTypeDef],
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[str],
        "tags": List[Dict[str, str]],
        "eventStatusCodes": List[str],
    },
    total=False,
)


class ClientDescribeEventsfilterTypeDef(_ClientDescribeEventsfilterTypeDef):
    """
    Type definition for `ClientDescribeEvents` `filter`

    Values to narrow the results returned.

    - **eventArns** *(list) --*

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **eventTypeCodes** *(list) --*

      A list of unique identifiers for event types. For example,
      ``"AWS_EC2_SYSTEM_MAINTENANCE_EVENT","AWS_RDS_MAINTENANCE_SCHEDULED"``

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **regions** *(list) --*

      A list of AWS regions.

      - *(string) --*

    - **availabilityZones** *(list) --*

      A list of AWS availability zones.

      - *(string) --*

    - **startTimes** *(list) --*

      A list of dates and times that the event began.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **endTimes** *(list) --*

      A list of dates and times that the event ended.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **lastUpdatedTimes** *(list) --*

      A list of dates and times that the event was last updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of entity identifiers, such as EC2 instance IDs (``i-34ab692e`` ) or EBS volumes
      (``vol-426ab23e`` ).

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **eventStatusCodes** *(list) --*

      A list of event status codes.

      - *(string) --*
    """


_DescribeAffectedEntitiesPaginatePaginationConfigTypeDef = TypedDict(
    "_DescribeAffectedEntitiesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class DescribeAffectedEntitiesPaginatePaginationConfigTypeDef(
    _DescribeAffectedEntitiesPaginatePaginationConfigTypeDef
):
    """
    Type definition for `DescribeAffectedEntitiesPaginate` `PaginationConfig`

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


_DescribeAffectedEntitiesPaginateResponseentitiesTypeDef = TypedDict(
    "_DescribeAffectedEntitiesPaginateResponseentitiesTypeDef",
    {
        "entityArn": str,
        "eventArn": str,
        "entityValue": str,
        "entityUrl": str,
        "awsAccountId": str,
        "lastUpdatedTime": datetime,
        "statusCode": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class DescribeAffectedEntitiesPaginateResponseentitiesTypeDef(
    _DescribeAffectedEntitiesPaginateResponseentitiesTypeDef
):
    """
    Type definition for `DescribeAffectedEntitiesPaginateResponse` `entities`

    Information about an entity that is affected by a Health event.

    - **entityArn** *(string) --*

      The unique identifier for the entity. Format: ``arn:aws:health:*entity-region* :*aws-account*
      :entity/*entity-id* `` . Example:
      ``arn:aws:health:us-east-1:111222333444:entity/AVh5GGT7ul1arKr1sE1K``

    - **eventArn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **entityValue** *(string) --*

      The ID of the affected entity.

    - **entityUrl** *(string) --*

    - **awsAccountId** *(string) --*

      The 12-digit AWS account number that contains the affected entity.

    - **lastUpdatedTime** *(datetime) --*

      The most recent time that the entity was updated.

    - **statusCode** *(string) --*

      The most recent status of the entity affected by the event. The possible values are
      ``IMPAIRED`` , ``UNIMPAIRED`` , and ``UNKNOWN`` .

    - **tags** *(dict) --*

      A map of entity tags attached to the affected entity.

      - *(string) --*

        - *(string) --*
    """


_DescribeAffectedEntitiesPaginateResponseTypeDef = TypedDict(
    "_DescribeAffectedEntitiesPaginateResponseTypeDef",
    {"entities": List[DescribeAffectedEntitiesPaginateResponseentitiesTypeDef], "NextToken": str},
    total=False,
)


class DescribeAffectedEntitiesPaginateResponseTypeDef(
    _DescribeAffectedEntitiesPaginateResponseTypeDef
):
    """
    Type definition for `DescribeAffectedEntitiesPaginate` `Response`

    - **entities** *(list) --*

      The entities that match the filter criteria.

      - *(dict) --*

        Information about an entity that is affected by a Health event.

        - **entityArn** *(string) --*

          The unique identifier for the entity. Format: ``arn:aws:health:*entity-region*
          :*aws-account* :entity/*entity-id* `` . Example:
          ``arn:aws:health:us-east-1:111222333444:entity/AVh5GGT7ul1arKr1sE1K``

        - **eventArn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **entityValue** *(string) --*

          The ID of the affected entity.

        - **entityUrl** *(string) --*

        - **awsAccountId** *(string) --*

          The 12-digit AWS account number that contains the affected entity.

        - **lastUpdatedTime** *(datetime) --*

          The most recent time that the entity was updated.

        - **statusCode** *(string) --*

          The most recent status of the entity affected by the event. The possible values are
          ``IMPAIRED`` , ``UNIMPAIRED`` , and ``UNKNOWN`` .

        - **tags** *(dict) --*

          A map of entity tags attached to the affected entity.

          - *(string) --*

            - *(string) --*

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef = TypedDict(
    "_DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef(
    _DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `DescribeAffectedEntitiesPaginatefilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_RequiredDescribeAffectedEntitiesPaginatefilterTypeDef = TypedDict(
    "_RequiredDescribeAffectedEntitiesPaginatefilterTypeDef", {"eventArns": List[str]}
)
_OptionalDescribeAffectedEntitiesPaginatefilterTypeDef = TypedDict(
    "_OptionalDescribeAffectedEntitiesPaginatefilterTypeDef",
    {
        "entityArns": List[str],
        "entityValues": List[str],
        "lastUpdatedTimes": List[DescribeAffectedEntitiesPaginatefilterlastUpdatedTimesTypeDef],
        "tags": List[Dict[str, str]],
        "statusCodes": List[str],
    },
    total=False,
)


class DescribeAffectedEntitiesPaginatefilterTypeDef(
    _RequiredDescribeAffectedEntitiesPaginatefilterTypeDef,
    _OptionalDescribeAffectedEntitiesPaginatefilterTypeDef,
):
    """
    Type definition for `DescribeAffectedEntitiesPaginate` `filter`

    Values to narrow the results returned. At least one event ARN is required.

    - **eventArns** *(list) --* **[REQUIRED]**

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of IDs for affected entities.

      - *(string) --*

    - **lastUpdatedTimes** *(list) --*

      A list of the most recent dates and times that the entity was updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **statusCodes** *(list) --*

      A list of entity status codes (``IMPAIRED`` , ``UNIMPAIRED`` , or ``UNKNOWN`` ).

      - *(string) --*
    """


_DescribeEventAggregatesPaginatePaginationConfigTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class DescribeEventAggregatesPaginatePaginationConfigTypeDef(
    _DescribeEventAggregatesPaginatePaginationConfigTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginate` `PaginationConfig`

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


_DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef",
    {"aggregateValue": str, "count": int},
    total=False,
)


class DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef(
    _DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginateResponse` `eventAggregates`

    The number of events of each issue type. Returned by the  DescribeEventAggregates operation.

    - **aggregateValue** *(string) --*

      The issue type for the associated count.

    - **count** *(integer) --*

      The number of events of the associated issue type.
    """


_DescribeEventAggregatesPaginateResponseTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginateResponseTypeDef",
    {
        "eventAggregates": List[DescribeEventAggregatesPaginateResponseeventAggregatesTypeDef],
        "NextToken": str,
    },
    total=False,
)


class DescribeEventAggregatesPaginateResponseTypeDef(
    _DescribeEventAggregatesPaginateResponseTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginate` `Response`

    - **eventAggregates** *(list) --*

      The number of events in each category that meet the optional filter criteria.

      - *(dict) --*

        The number of events of each issue type. Returned by the  DescribeEventAggregates operation.

        - **aggregateValue** *(string) --*

          The issue type for the associated count.

        - **count** *(integer) --*

          The number of events of the associated issue type.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_DescribeEventAggregatesPaginatefilterendTimesTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginatefilterendTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeEventAggregatesPaginatefilterendTimesTypeDef(
    _DescribeEventAggregatesPaginatefilterendTimesTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginatefilter` `endTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef(
    _DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginatefilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventAggregatesPaginatefilterstartTimesTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginatefilterstartTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeEventAggregatesPaginatefilterstartTimesTypeDef(
    _DescribeEventAggregatesPaginatefilterstartTimesTypeDef
):
    """
    Type definition for `DescribeEventAggregatesPaginatefilter` `startTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventAggregatesPaginatefilterTypeDef = TypedDict(
    "_DescribeEventAggregatesPaginatefilterTypeDef",
    {
        "eventArns": List[str],
        "eventTypeCodes": List[str],
        "services": List[str],
        "regions": List[str],
        "availabilityZones": List[str],
        "startTimes": List[DescribeEventAggregatesPaginatefilterstartTimesTypeDef],
        "endTimes": List[DescribeEventAggregatesPaginatefilterendTimesTypeDef],
        "lastUpdatedTimes": List[DescribeEventAggregatesPaginatefilterlastUpdatedTimesTypeDef],
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[str],
        "tags": List[Dict[str, str]],
        "eventStatusCodes": List[str],
    },
    total=False,
)


class DescribeEventAggregatesPaginatefilterTypeDef(_DescribeEventAggregatesPaginatefilterTypeDef):
    """
    Type definition for `DescribeEventAggregatesPaginate` `filter`

    Values to narrow the results returned.

    - **eventArns** *(list) --*

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **eventTypeCodes** *(list) --*

      A list of unique identifiers for event types. For example,
      ``"AWS_EC2_SYSTEM_MAINTENANCE_EVENT","AWS_RDS_MAINTENANCE_SCHEDULED"``

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **regions** *(list) --*

      A list of AWS regions.

      - *(string) --*

    - **availabilityZones** *(list) --*

      A list of AWS availability zones.

      - *(string) --*

    - **startTimes** *(list) --*

      A list of dates and times that the event began.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **endTimes** *(list) --*

      A list of dates and times that the event ended.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **lastUpdatedTimes** *(list) --*

      A list of dates and times that the event was last updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of entity identifiers, such as EC2 instance IDs (``i-34ab692e`` ) or EBS volumes
      (``vol-426ab23e`` ).

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **eventStatusCodes** *(list) --*

      A list of event status codes.

      - *(string) --*
    """


_DescribeEventTypesPaginatePaginationConfigTypeDef = TypedDict(
    "_DescribeEventTypesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class DescribeEventTypesPaginatePaginationConfigTypeDef(
    _DescribeEventTypesPaginatePaginationConfigTypeDef
):
    """
    Type definition for `DescribeEventTypesPaginate` `PaginationConfig`

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


_DescribeEventTypesPaginateResponseeventTypesTypeDef = TypedDict(
    "_DescribeEventTypesPaginateResponseeventTypesTypeDef",
    {"service": str, "code": str, "category": str},
    total=False,
)


class DescribeEventTypesPaginateResponseeventTypesTypeDef(
    _DescribeEventTypesPaginateResponseeventTypesTypeDef
):
    """
    Type definition for `DescribeEventTypesPaginateResponse` `eventTypes`

    Metadata about a type of event that is reported by AWS Health. Data consists of the category
    (for example, ``issue`` ), the service (for example, ``EC2`` ), and the event type code (for
    example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

    - **service** *(string) --*

      The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

    - **code** *(string) --*

      The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
      for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

    - **category** *(string) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).
    """


_DescribeEventTypesPaginateResponseTypeDef = TypedDict(
    "_DescribeEventTypesPaginateResponseTypeDef",
    {"eventTypes": List[DescribeEventTypesPaginateResponseeventTypesTypeDef], "NextToken": str},
    total=False,
)


class DescribeEventTypesPaginateResponseTypeDef(_DescribeEventTypesPaginateResponseTypeDef):
    """
    Type definition for `DescribeEventTypesPaginate` `Response`

    - **eventTypes** *(list) --*

      A list of event types that match the filter criteria. Event types have a category (``issue`` ,
      ``accountNotification`` , or ``scheduledChange`` ), a service (for example, ``EC2`` , ``RDS``
      , ``DATAPIPELINE`` , ``BILLING`` ), and a code (in the format ``AWS_*SERVICE* _*DESCRIPTION*
      `` ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

      - *(dict) --*

        Metadata about a type of event that is reported by AWS Health. Data consists of the category
        (for example, ``issue`` ), the service (for example, ``EC2`` ), and the event type code (for
        example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` ).

        - **service** *(string) --*

          The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

        - **code** *(string) --*

          The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* ``
          ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

        - **category** *(string) --*

          A list of event type category codes (``issue`` , ``scheduledChange`` , or
          ``accountNotification`` ).

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_DescribeEventTypesPaginatefilterTypeDef = TypedDict(
    "_DescribeEventTypesPaginatefilterTypeDef",
    {"eventTypeCodes": List[str], "services": List[str], "eventTypeCategories": List[str]},
    total=False,
)


class DescribeEventTypesPaginatefilterTypeDef(_DescribeEventTypesPaginatefilterTypeDef):
    """
    Type definition for `DescribeEventTypesPaginate` `filter`

    Values to narrow the results returned.

    - **eventTypeCodes** *(list) --*

      A list of event type codes.

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*
    """


_DescribeEventsPaginatePaginationConfigTypeDef = TypedDict(
    "_DescribeEventsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class DescribeEventsPaginatePaginationConfigTypeDef(_DescribeEventsPaginatePaginationConfigTypeDef):
    """
    Type definition for `DescribeEventsPaginate` `PaginationConfig`

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


_DescribeEventsPaginateResponseeventsTypeDef = TypedDict(
    "_DescribeEventsPaginateResponseeventsTypeDef",
    {
        "arn": str,
        "service": str,
        "eventTypeCode": str,
        "eventTypeCategory": str,
        "region": str,
        "availabilityZone": str,
        "startTime": datetime,
        "endTime": datetime,
        "lastUpdatedTime": datetime,
        "statusCode": str,
    },
    total=False,
)


class DescribeEventsPaginateResponseeventsTypeDef(_DescribeEventsPaginateResponseeventsTypeDef):
    """
    Type definition for `DescribeEventsPaginateResponse` `events`

    Summary information about an event, returned by the  DescribeEvents operation. The
    DescribeEventDetails operation also returns this information, as well as the  EventDescription
    and additional event metadata.

    - **arn** *(string) --*

      The unique identifier for the event. Format: ``arn:aws:health:*event-region* ::event/*SERVICE*
      /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
      arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

    - **service** *(string) --*

      The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

    - **eventTypeCode** *(string) --*

      The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* `` ;
      for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

    - **eventTypeCategory** *(string) --*

      The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
      ``accountNotification`` .

    - **region** *(string) --*

      The AWS region name of the event.

    - **availabilityZone** *(string) --*

      The AWS Availability Zone of the event. For example, us-east-1a.

    - **startTime** *(datetime) --*

      The date and time that the event began.

    - **endTime** *(datetime) --*

      The date and time that the event ended.

    - **lastUpdatedTime** *(datetime) --*

      The most recent date and time that the event was updated.

    - **statusCode** *(string) --*

      The most recent status of the event. Possible values are ``open`` , ``closed`` , and
      ``upcoming`` .
    """


_DescribeEventsPaginateResponseTypeDef = TypedDict(
    "_DescribeEventsPaginateResponseTypeDef",
    {"events": List[DescribeEventsPaginateResponseeventsTypeDef], "NextToken": str},
    total=False,
)


class DescribeEventsPaginateResponseTypeDef(_DescribeEventsPaginateResponseTypeDef):
    """
    Type definition for `DescribeEventsPaginate` `Response`

    - **events** *(list) --*

      The events that match the specified filter criteria.

      - *(dict) --*

        Summary information about an event, returned by the  DescribeEvents operation. The
        DescribeEventDetails operation also returns this information, as well as the
        EventDescription and additional event metadata.

        - **arn** *(string) --*

          The unique identifier for the event. Format: ``arn:aws:health:*event-region*
          ::event/*SERVICE* /*EVENT_TYPE_CODE* /*EVENT_TYPE_PLUS_ID* `` . Example: ``Example:
          arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-DEF456``

        - **service** *(string) --*

          The AWS service that is affected by the event. For example, ``EC2`` , ``RDS`` .

        - **eventTypeCode** *(string) --*

          The unique identifier for the event type. The format is ``AWS_*SERVICE* _*DESCRIPTION* ``
          ; for example, ``AWS_EC2_SYSTEM_MAINTENANCE_EVENT`` .

        - **eventTypeCategory** *(string) --*

          The category of the event. Possible values are ``issue`` , ``scheduledChange`` , and
          ``accountNotification`` .

        - **region** *(string) --*

          The AWS region name of the event.

        - **availabilityZone** *(string) --*

          The AWS Availability Zone of the event. For example, us-east-1a.

        - **startTime** *(datetime) --*

          The date and time that the event began.

        - **endTime** *(datetime) --*

          The date and time that the event ended.

        - **lastUpdatedTime** *(datetime) --*

          The most recent date and time that the event was updated.

        - **statusCode** *(string) --*

          The most recent status of the event. Possible values are ``open`` , ``closed`` , and
          ``upcoming`` .

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_DescribeEventsPaginatefilterendTimesTypeDef = TypedDict(
    "_DescribeEventsPaginatefilterendTimesTypeDef", {"from": datetime, "to": datetime}, total=False
)


class DescribeEventsPaginatefilterendTimesTypeDef(_DescribeEventsPaginatefilterendTimesTypeDef):
    """
    Type definition for `DescribeEventsPaginatefilter` `endTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventsPaginatefilterlastUpdatedTimesTypeDef = TypedDict(
    "_DescribeEventsPaginatefilterlastUpdatedTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeEventsPaginatefilterlastUpdatedTimesTypeDef(
    _DescribeEventsPaginatefilterlastUpdatedTimesTypeDef
):
    """
    Type definition for `DescribeEventsPaginatefilter` `lastUpdatedTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventsPaginatefilterstartTimesTypeDef = TypedDict(
    "_DescribeEventsPaginatefilterstartTimesTypeDef",
    {"from": datetime, "to": datetime},
    total=False,
)


class DescribeEventsPaginatefilterstartTimesTypeDef(_DescribeEventsPaginatefilterstartTimesTypeDef):
    """
    Type definition for `DescribeEventsPaginatefilter` `startTimes`

    A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
    ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` , ``endTime``
    , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from`` is set and
    ``to`` is not set: match items where the timestamp value is equal to or after ``from`` . If
    ``from`` is not set and ``to`` is set: match items where the timestamp value is equal to or
    before ``to`` .

    - **from** *(datetime) --*

      The starting date and time of a time range.

    - **to** *(datetime) --*

      The ending date and time of a time range.
    """


_DescribeEventsPaginatefilterTypeDef = TypedDict(
    "_DescribeEventsPaginatefilterTypeDef",
    {
        "eventArns": List[str],
        "eventTypeCodes": List[str],
        "services": List[str],
        "regions": List[str],
        "availabilityZones": List[str],
        "startTimes": List[DescribeEventsPaginatefilterstartTimesTypeDef],
        "endTimes": List[DescribeEventsPaginatefilterendTimesTypeDef],
        "lastUpdatedTimes": List[DescribeEventsPaginatefilterlastUpdatedTimesTypeDef],
        "entityArns": List[str],
        "entityValues": List[str],
        "eventTypeCategories": List[str],
        "tags": List[Dict[str, str]],
        "eventStatusCodes": List[str],
    },
    total=False,
)


class DescribeEventsPaginatefilterTypeDef(_DescribeEventsPaginatefilterTypeDef):
    """
    Type definition for `DescribeEventsPaginate` `filter`

    Values to narrow the results returned.

    - **eventArns** *(list) --*

      A list of event ARNs (unique identifiers). For example:
      ``"arn:aws:health:us-east-1::event/EC2/EC2_INSTANCE_RETIREMENT_SCHEDULED/EC2_INSTANCE_RETIREMENT_SCHEDULED_ABC123-CDE456",
      "arn:aws:health:us-west-1::event/EBS/AWS_EBS_LOST_VOLUME/AWS_EBS_LOST_VOLUME_CHI789_JKL101"``

      - *(string) --*

    - **eventTypeCodes** *(list) --*

      A list of unique identifiers for event types. For example,
      ``"AWS_EC2_SYSTEM_MAINTENANCE_EVENT","AWS_RDS_MAINTENANCE_SCHEDULED"``

      - *(string) --*

    - **services** *(list) --*

      The AWS services associated with the event. For example, ``EC2`` , ``RDS`` .

      - *(string) --*

    - **regions** *(list) --*

      A list of AWS regions.

      - *(string) --*

    - **availabilityZones** *(list) --*

      A list of AWS availability zones.

      - *(string) --*

    - **startTimes** *(list) --*

      A list of dates and times that the event began.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **endTimes** *(list) --*

      A list of dates and times that the event ended.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **lastUpdatedTimes** *(list) --*

      A list of dates and times that the event was last updated.

      - *(dict) --*

        A range of dates and times that is used by the  EventFilter and  EntityFilter objects. If
        ``from`` is set and ``to`` is set: match items where the timestamp (``startTime`` ,
        ``endTime`` , or ``lastUpdatedTime`` ) is between ``from`` and ``to`` inclusive. If ``from``
        is set and ``to`` is not set: match items where the timestamp value is equal to or after
        ``from`` . If ``from`` is not set and ``to`` is set: match items where the timestamp value
        is equal to or before ``to`` .

        - **from** *(datetime) --*

          The starting date and time of a time range.

        - **to** *(datetime) --*

          The ending date and time of a time range.

    - **entityArns** *(list) --*

      A list of entity ARNs (unique identifiers).

      - *(string) --*

    - **entityValues** *(list) --*

      A list of entity identifiers, such as EC2 instance IDs (``i-34ab692e`` ) or EBS volumes
      (``vol-426ab23e`` ).

      - *(string) --*

    - **eventTypeCategories** *(list) --*

      A list of event type category codes (``issue`` , ``scheduledChange`` , or
      ``accountNotification`` ).

      - *(string) --*

    - **tags** *(list) --*

      A map of entity tags attached to the affected entity.

      - *(dict) --*

        - *(string) --*

          - *(string) --*

    - **eventStatusCodes** *(list) --*

      A list of event status codes.

      - *(string) --*
    """
