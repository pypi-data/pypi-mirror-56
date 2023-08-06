# -*- coding: utf-8 -*-
import json
from abc import ABCMeta
from copy import deepcopy

from django.conf import settings
from django.utils.module_loading import import_string
from six import with_metaclass

from scarface.settings import SCARFACE_DEFAULT_PLATFORM_STRATEGIES, SCARFACE_DEFAULT_MESSAGE_TRIM_LENGTH


def get_strategies():
    strategy_modules = deepcopy(SCARFACE_DEFAULT_PLATFORM_STRATEGIES)
    if hasattr(settings, 'SCARFACE_PLATFORM_STRATEGIES'):
        strategy_modules += settings.SCARFACE_PLATFORM_STRATEGIES

    strategies = {}
    for strategy_path in strategy_modules:
        strategy_class = import_string(strategy_path)
        strategies[strategy_class.id] = strategy_class
    return strategies


def get_strategy_choices():
    strategies = get_strategies()
    choices = {}
    for id, strategy_class in strategies.items():
        choices[id] = strategy_class.service_name
    return choices


class PlatformStrategy(with_metaclass(ABCMeta)):
    def __init__(self, platform_application):
        super(PlatformStrategy, self).__init__()
        self.platform = platform_application

    ''' id which is used to refere to that strategy'''
    id = ''

    ''' Verbose name of that strategie's service'''
    service_name = ''

    def format_payload(self, data):
        return {self.platform.platform: json.dumps(data)}

    def format_push(self, badgeCount, context, context_id, has_new_content, message,
            sound):
        if message:
            message = self.trim_message(message)

        payload = {
            'aps': {
                "content-available": has_new_content,
            },
            "ctx": context,
            "id": context_id
        }

        if message and len(message) > 0:
            payload['aps']['alert'] = message

        if not badgeCount is None:
            payload['aps'].update({
                "badge": badgeCount,
            })

        if not sound is None:
            payload['aps'].update({
                'sound': sound,
            })

        return payload

    def trim_message(self, message):
        import sys
        trim_length = SCARFACE_DEFAULT_MESSAGE_TRIM_LENGTH
        if hasattr(settings, 'SCARFACE_MESSAGE_TRIM_LENGTH'):
            trim_length = settings.SCARFACE_MESSAGE_TRIM_LENGTH

        if sys.getsizeof(message) > trim_length:
            while sys.getsizeof(message) > trim_length:
                message = message[:-3]
            message += '...'
        return message


class APNPlatformStrategy(PlatformStrategy):
    id = 'APNS'
    service_name = 'Apple Push Notification Service (APNS)'

    def format_payload(self, message):
        """
        :type message: PushMessage
        :param message:
        :return:
        """

        payload = self.format_push(
            message.badge_count,
            message.context,
            message.context_id,
            message.has_new_content,
            message.message, message.sound
        )

        if message.extra_payload:
            extra = message.extra_payload.copy()
            if 'aps' in extra:
                # Handle `aps` updating separately to not loose
                # any alert props
                payload['aps'].update(extra.pop('aps'))
            payload.update(extra)

        return super(
            APNPlatformStrategy,
            self
        ).format_payload(payload)


class APNSSandboxPlatformStrategy(PlatformStrategy):
    id = 'APNS_SANDBOX'
    service_name = 'Apple Push Notification Service Sandbox (APNS_SANDBOX)'

    def format_payload(self, message):
        """
        :type message: PushMessage
        :param message:
        :return:
        """

        payload = self.format_push(
            message.badge_count,
            message.context,
            message.context_id,
            message.has_new_content,
            message.message, message.sound
        )

        if message.extra_payload:
            payload.update(message.extra_payload)

        return super(
            APNSSandboxPlatformStrategy,
            self
        ).format_payload(payload)


class GCMPlatformStrategy(PlatformStrategy):
    id = 'GCM'
    service_name = 'Google Cloud Messaging (GCM)'

    def format_payload(self, message):
        """
        :type data: PushMessage
        :param data:
        :return:
        """
        data = message.as_dict()
        h = hash(frozenset(data.items()))
        return super(
            GCMPlatformStrategy,
            self
        ).format_payload({"collapse_key": h, "data": data})
