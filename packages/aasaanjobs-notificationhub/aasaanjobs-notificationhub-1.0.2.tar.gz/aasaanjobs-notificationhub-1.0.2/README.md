# Python Aasaanjobs NotificationHub Client

[![Build Status](https://travis-ci.org/aasaanjobs/notification-hub-py-sdk.svg?branch=master)](https://travis-ci.org/aasaanjobs/notification-hub-py-sdk)
[![codecov](https://codecov.io/gh/aasaanjobs/notifications-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/aasaanjobs/notifications-python-sdk)

Python SDK to communicate with Aasaanjobs Notification Hub and send notifications to users.

## Supported Notification Channels
- Simple Messaging Service (SMS)
- Email
- WhatsApp
- Mobile Push (FCM)

## Installation
```
pip install aaasaanjobs-notificationhub
```

## Usage
Each notification is referred to as **Task** in this library. A single **Task** can contain
multiple channels, i.e., a single **Task** can contain both **Email** and **WhatsApp** notification data.
This **Task** is then validated via [Protocol Buffers](https://developers.google.com/protocol-buffers)
and pushed to corresponding Notification Hub Amazon SQS queue.

### Configuration
Each application which uses this library must configure Amazon SQS configurations to successfully
send notification task to Hub.

The following keys can be defined in the settings module if Django application or can be defined as environment variables

| **Setting**                            | **Description**                                                   |
|----------------------------------------|-------------------------------------------------------------------|
| NOTIFICATION_HUB_SQS_ACCESS_KEY_ID     | Access Key of the IAM role which has access to the Hub SQS        |
| NOTIFICATION_HUB_SQS_SECRET_ACCESS_KEY | Secret Access Key of the IAM role which has access to the Hub SQS |
| NOTIFICATION_HUB_SQS_REGION            | AWS Region where the Hub SQS resides                              |
| NOTIFICATION_HUB_SQS_QUEUE_NAME        | Name of the Hub SQS Queue                                         |
