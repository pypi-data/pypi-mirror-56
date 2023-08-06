"Main interface for sms-voice type defs"
from __future__ import annotations

from typing import List
from typing_extensions import TypedDict


__all__ = (
    "ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef",
    "ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef",
    "ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef",
    "ClientCreateConfigurationSetEventDestinationEventDestinationTypeDef",
    "ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef",
    "ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef",
    "ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef",
    "ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef",
    "ClientGetConfigurationSetEventDestinationsResponseTypeDef",
    "ClientListConfigurationSetsResponseTypeDef",
    "ClientSendVoiceMessageContentCallInstructionsMessageTypeDef",
    "ClientSendVoiceMessageContentPlainTextMessageTypeDef",
    "ClientSendVoiceMessageContentSSMLMessageTypeDef",
    "ClientSendVoiceMessageContentTypeDef",
    "ClientSendVoiceMessageResponseTypeDef",
    "ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef",
    "ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef",
    "ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef",
    "ClientUpdateConfigurationSetEventDestinationEventDestinationTypeDef",
)


_ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef = TypedDict(
    "_ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef",
    {"IamRoleArn": str, "LogGroupArn": str},
    total=False,
)


class ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef(
    _ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef
):
    """
    Type definition for `ClientCreateConfigurationSetEventDestinationEventDestination`
    `CloudWatchLogsDestination`

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
    Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

    - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
    record events in.
    """


_ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef = TypedDict(
    "_ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef",
    {"DeliveryStreamArn": str, "IamRoleArn": str},
    total=False,
)


class ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef(
    _ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef
):
    """
    Type definition for `ClientCreateConfigurationSetEventDestinationEventDestination`
    `KinesisFirehoseDestination`

    - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
    write data to an Amazon Kinesis Data Firehose stream.

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
    Firehose destination that you want to use in the event destination.
    """


_ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef = TypedDict(
    "_ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef",
    {"TopicArn": str},
    total=False,
)


class ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef(
    _ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef
):
    """
    Type definition for `ClientCreateConfigurationSetEventDestinationEventDestination`
    `SnsDestination`

    - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
    want to publish events to.
    """


_ClientCreateConfigurationSetEventDestinationEventDestinationTypeDef = TypedDict(
    "_ClientCreateConfigurationSetEventDestinationEventDestinationTypeDef",
    {
        "CloudWatchLogsDestination": ClientCreateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef,
        "Enabled": bool,
        "KinesisFirehoseDestination": ClientCreateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef,
        "MatchingEventTypes": List[str],
        "SnsDestination": ClientCreateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef,
    },
    total=False,
)


class ClientCreateConfigurationSetEventDestinationEventDestinationTypeDef(
    _ClientCreateConfigurationSetEventDestinationEventDestinationTypeDef
):
    """
    Type definition for `ClientCreateConfigurationSetEventDestination` `EventDestination`

    - **CloudWatchLogsDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon CloudWatch Logs.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
      Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

      - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
      record events in.

    - **Enabled** *(boolean) --* Indicates whether or not the event destination is enabled. If the
    event destination is enabled, then Amazon Pinpoint sends response data to the specified event
    destination.

    - **KinesisFirehoseDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon Kinesis Data Firehose.

      - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
      write data to an Amazon Kinesis Data Firehose stream.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
      Firehose destination that you want to use in the event destination.

    - **MatchingEventTypes** *(list) --* An array of EventDestination objects. Each EventDestination
    object includes ARNs and other information that define an event destination.

      - *(string) --* The types of events that are sent to the event destination.

    - **SnsDestination** *(dict) --* An object that contains information about an event destination
    that sends data to Amazon SNS.

      - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
      want to publish events to.
    """


_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef = TypedDict(
    "_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef",
    {"IamRoleArn": str, "LogGroupArn": str},
    total=False,
)


class ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef(
    _ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef
):
    """
    Type definition for `ClientGetConfigurationSetEventDestinationsResponseEventDestinations`
    `CloudWatchLogsDestination`

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
    Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

    - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
    record events in.
    """


_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef = TypedDict(
    "_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef",
    {"DeliveryStreamArn": str, "IamRoleArn": str},
    total=False,
)


class ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef(
    _ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef
):
    """
    Type definition for `ClientGetConfigurationSetEventDestinationsResponseEventDestinations`
    `KinesisFirehoseDestination`

    - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
    write data to an Amazon Kinesis Data Firehose stream.

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
    Firehose destination that you want to use in the event destination.
    """


_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef = TypedDict(
    "_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef",
    {"TopicArn": str},
    total=False,
)


class ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef(
    _ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef
):
    """
    Type definition for `ClientGetConfigurationSetEventDestinationsResponseEventDestinations`
    `SnsDestination`

    - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
    want to publish events to.
    """


_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef = TypedDict(
    "_ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef",
    {
        "CloudWatchLogsDestination": ClientGetConfigurationSetEventDestinationsResponseEventDestinationsCloudWatchLogsDestinationTypeDef,
        "Enabled": bool,
        "KinesisFirehoseDestination": ClientGetConfigurationSetEventDestinationsResponseEventDestinationsKinesisFirehoseDestinationTypeDef,
        "MatchingEventTypes": List[str],
        "Name": str,
        "SnsDestination": ClientGetConfigurationSetEventDestinationsResponseEventDestinationsSnsDestinationTypeDef,
    },
    total=False,
)


class ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef(
    _ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef
):
    """
    Type definition for `ClientGetConfigurationSetEventDestinationsResponse` `EventDestinations`

    - **CloudWatchLogsDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon CloudWatch Logs.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
      Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

      - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
      record events in.

    - **Enabled** *(boolean) --* Indicates whether or not the event destination is enabled. If the
    event destination is enabled, then Amazon Pinpoint sends response data to the specified event
    destination.

    - **KinesisFirehoseDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon Kinesis Data Firehose.

      - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
      write data to an Amazon Kinesis Data Firehose stream.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
      Firehose destination that you want to use in the event destination.

    - **MatchingEventTypes** *(list) --* An array of EventDestination objects. Each EventDestination
    object includes ARNs and other information that define an event destination.

      - *(string) --* The types of events that are sent to the event destination.

    - **Name** *(string) --* A name that identifies the event destination configuration.

    - **SnsDestination** *(dict) --* An object that contains information about an event destination
    that sends data to Amazon SNS.

      - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
      want to publish events to.
    """


_ClientGetConfigurationSetEventDestinationsResponseTypeDef = TypedDict(
    "_ClientGetConfigurationSetEventDestinationsResponseTypeDef",
    {
        "EventDestinations": List[
            ClientGetConfigurationSetEventDestinationsResponseEventDestinationsTypeDef
        ]
    },
    total=False,
)


class ClientGetConfigurationSetEventDestinationsResponseTypeDef(
    _ClientGetConfigurationSetEventDestinationsResponseTypeDef
):
    """
    Type definition for `ClientGetConfigurationSetEventDestinations` `Response`

    - **EventDestinations** *(list) --* An array of EventDestination objects. Each EventDestination
    object includes ARNs and other information that define an event destination.

      - *(dict) --* An object that defines an event destination.

        - **CloudWatchLogsDestination** *(dict) --* An object that contains information about an
        event destination that sends data to Amazon CloudWatch Logs.

          - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and
          Access Management (IAM) role that is able to write event data to an Amazon CloudWatch
          destination.

          - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want
          to record events in.

        - **Enabled** *(boolean) --* Indicates whether or not the event destination is enabled. If
        the event destination is enabled, then Amazon Pinpoint sends response data to the specified
        event destination.

        - **KinesisFirehoseDestination** *(dict) --* An object that contains information about an
        event destination that sends data to Amazon Kinesis Data Firehose.

          - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that
          can write data to an Amazon Kinesis Data Firehose stream.

          - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
          Firehose destination that you want to use in the event destination.

        - **MatchingEventTypes** *(list) --* An array of EventDestination objects. Each
        EventDestination object includes ARNs and other information that define an event
        destination.

          - *(string) --* The types of events that are sent to the event destination.

        - **Name** *(string) --* A name that identifies the event destination configuration.

        - **SnsDestination** *(dict) --* An object that contains information about an event
        destination that sends data to Amazon SNS.

          - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that
          you want to publish events to.
    """


_ClientListConfigurationSetsResponseTypeDef = TypedDict(
    "_ClientListConfigurationSetsResponseTypeDef",
    {"ConfigurationSets": List[str], "NextToken": str},
    total=False,
)


class ClientListConfigurationSetsResponseTypeDef(_ClientListConfigurationSetsResponseTypeDef):
    """
    Type definition for `ClientListConfigurationSets` `Response`

    - **ConfigurationSets** *(list) --* An object that contains a list of configuration sets for
    your account in the current region.

      - *(string) --*

    - **NextToken** *(string) --* A token returned from a previous call to ListConfigurationSets to
    indicate the position in the list of configuration sets.
    """


_ClientSendVoiceMessageContentCallInstructionsMessageTypeDef = TypedDict(
    "_ClientSendVoiceMessageContentCallInstructionsMessageTypeDef", {"Text": str}, total=False
)


class ClientSendVoiceMessageContentCallInstructionsMessageTypeDef(
    _ClientSendVoiceMessageContentCallInstructionsMessageTypeDef
):
    """
    Type definition for `ClientSendVoiceMessageContent` `CallInstructionsMessage`

    - **Text** *(string) --* The language to use when delivering the message. For a complete list of
    supported languages, see the Amazon Polly Developer Guide.
    """


_ClientSendVoiceMessageContentPlainTextMessageTypeDef = TypedDict(
    "_ClientSendVoiceMessageContentPlainTextMessageTypeDef",
    {"LanguageCode": str, "Text": str, "VoiceId": str},
    total=False,
)


class ClientSendVoiceMessageContentPlainTextMessageTypeDef(
    _ClientSendVoiceMessageContentPlainTextMessageTypeDef
):
    """
    Type definition for `ClientSendVoiceMessageContent` `PlainTextMessage`

    - **LanguageCode** *(string) --* The language to use when delivering the message. For a complete
    list of supported languages, see the Amazon Polly Developer Guide.

    - **Text** *(string) --* The plain (not SSML-formatted) text to deliver to the recipient.

    - **VoiceId** *(string) --* The name of the voice that you want to use to deliver the message.
    For a complete list of supported voices, see the Amazon Polly Developer Guide.
    """


_ClientSendVoiceMessageContentSSMLMessageTypeDef = TypedDict(
    "_ClientSendVoiceMessageContentSSMLMessageTypeDef",
    {"LanguageCode": str, "Text": str, "VoiceId": str},
    total=False,
)


class ClientSendVoiceMessageContentSSMLMessageTypeDef(
    _ClientSendVoiceMessageContentSSMLMessageTypeDef
):
    """
    Type definition for `ClientSendVoiceMessageContent` `SSMLMessage`

    - **LanguageCode** *(string) --* The language to use when delivering the message. For a complete
    list of supported languages, see the Amazon Polly Developer Guide.

    - **Text** *(string) --* The SSML-formatted text to deliver to the recipient.

    - **VoiceId** *(string) --* The name of the voice that you want to use to deliver the message.
    For a complete list of supported voices, see the Amazon Polly Developer Guide.
    """


_ClientSendVoiceMessageContentTypeDef = TypedDict(
    "_ClientSendVoiceMessageContentTypeDef",
    {
        "CallInstructionsMessage": ClientSendVoiceMessageContentCallInstructionsMessageTypeDef,
        "PlainTextMessage": ClientSendVoiceMessageContentPlainTextMessageTypeDef,
        "SSMLMessage": ClientSendVoiceMessageContentSSMLMessageTypeDef,
    },
    total=False,
)


class ClientSendVoiceMessageContentTypeDef(_ClientSendVoiceMessageContentTypeDef):
    """
    Type definition for `ClientSendVoiceMessage` `Content`

    - **CallInstructionsMessage** *(dict) --* An object that defines a message that contains text
    formatted using Amazon Pinpoint Voice Instructions markup.

      - **Text** *(string) --* The language to use when delivering the message. For a complete list
      of supported languages, see the Amazon Polly Developer Guide.

    - **PlainTextMessage** *(dict) --* An object that defines a message that contains unformatted
    text.

      - **LanguageCode** *(string) --* The language to use when delivering the message. For a
      complete list of supported languages, see the Amazon Polly Developer Guide.

      - **Text** *(string) --* The plain (not SSML-formatted) text to deliver to the recipient.

      - **VoiceId** *(string) --* The name of the voice that you want to use to deliver the message.
      For a complete list of supported voices, see the Amazon Polly Developer Guide.

    - **SSMLMessage** *(dict) --* An object that defines a message that contains SSML-formatted
    text.

      - **LanguageCode** *(string) --* The language to use when delivering the message. For a
      complete list of supported languages, see the Amazon Polly Developer Guide.

      - **Text** *(string) --* The SSML-formatted text to deliver to the recipient.

      - **VoiceId** *(string) --* The name of the voice that you want to use to deliver the message.
      For a complete list of supported voices, see the Amazon Polly Developer Guide.
    """


_ClientSendVoiceMessageResponseTypeDef = TypedDict(
    "_ClientSendVoiceMessageResponseTypeDef", {"MessageId": str}, total=False
)


class ClientSendVoiceMessageResponseTypeDef(_ClientSendVoiceMessageResponseTypeDef):
    """
    Type definition for `ClientSendVoiceMessage` `Response`

    - **MessageId** *(string) --* A unique identifier for the voice message.
    """


_ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef = TypedDict(
    "_ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef",
    {"IamRoleArn": str, "LogGroupArn": str},
    total=False,
)


class ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef(
    _ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef
):
    """
    Type definition for `ClientUpdateConfigurationSetEventDestinationEventDestination`
    `CloudWatchLogsDestination`

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
    Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

    - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
    record events in.
    """


_ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef = TypedDict(
    "_ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef",
    {"DeliveryStreamArn": str, "IamRoleArn": str},
    total=False,
)


class ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef(
    _ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef
):
    """
    Type definition for `ClientUpdateConfigurationSetEventDestinationEventDestination`
    `KinesisFirehoseDestination`

    - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
    write data to an Amazon Kinesis Data Firehose stream.

    - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
    Firehose destination that you want to use in the event destination.
    """


_ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef = TypedDict(
    "_ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef",
    {"TopicArn": str},
    total=False,
)


class ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef(
    _ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef
):
    """
    Type definition for `ClientUpdateConfigurationSetEventDestinationEventDestination`
    `SnsDestination`

    - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
    want to publish events to.
    """


_ClientUpdateConfigurationSetEventDestinationEventDestinationTypeDef = TypedDict(
    "_ClientUpdateConfigurationSetEventDestinationEventDestinationTypeDef",
    {
        "CloudWatchLogsDestination": ClientUpdateConfigurationSetEventDestinationEventDestinationCloudWatchLogsDestinationTypeDef,
        "Enabled": bool,
        "KinesisFirehoseDestination": ClientUpdateConfigurationSetEventDestinationEventDestinationKinesisFirehoseDestinationTypeDef,
        "MatchingEventTypes": List[str],
        "SnsDestination": ClientUpdateConfigurationSetEventDestinationEventDestinationSnsDestinationTypeDef,
    },
    total=False,
)


class ClientUpdateConfigurationSetEventDestinationEventDestinationTypeDef(
    _ClientUpdateConfigurationSetEventDestinationEventDestinationTypeDef
):
    """
    Type definition for `ClientUpdateConfigurationSetEventDestination` `EventDestination`

    - **CloudWatchLogsDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon CloudWatch Logs.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of an Amazon Identity and Access
      Management (IAM) role that is able to write event data to an Amazon CloudWatch destination.

      - **LogGroupArn** *(string) --* The name of the Amazon CloudWatch Log Group that you want to
      record events in.

    - **Enabled** *(boolean) --* Indicates whether or not the event destination is enabled. If the
    event destination is enabled, then Amazon Pinpoint sends response data to the specified event
    destination.

    - **KinesisFirehoseDestination** *(dict) --* An object that contains information about an event
    destination that sends data to Amazon Kinesis Data Firehose.

      - **DeliveryStreamArn** *(string) --* The Amazon Resource Name (ARN) of an IAM role that can
      write data to an Amazon Kinesis Data Firehose stream.

      - **IamRoleArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon Kinesis Data
      Firehose destination that you want to use in the event destination.

    - **MatchingEventTypes** *(list) --* An array of EventDestination objects. Each EventDestination
    object includes ARNs and other information that define an event destination.

      - *(string) --* The types of events that are sent to the event destination.

    - **SnsDestination** *(dict) --* An object that contains information about an event destination
    that sends data to Amazon SNS.

      - **TopicArn** *(string) --* The Amazon Resource Name (ARN) of the Amazon SNS topic that you
      want to publish events to.
    """
