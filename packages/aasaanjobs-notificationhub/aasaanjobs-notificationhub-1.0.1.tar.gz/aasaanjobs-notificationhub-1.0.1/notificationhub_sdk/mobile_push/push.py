import json
from typing import List

from ..base import get_expiry, validate_template, validate_arn_endpoint
from ..common import Waterfall
from ..proto import notification_hub_pb2 as pb


class Push:
    _default_expiry_offset = 7  # 7 Days

    def __init__(
            self,
            arn_endpoints: List[str],
            template: str,
            context: dict = None,
            user_id: str = None,
            waterfall_config: Waterfall = None,
            expiry: int = None
    ):
        """
        Parameters:
            arn_endpoints (str[]): List of ARN endpoints to whom the push message will be sent
            template (str): The template URL which will get rendered with the variable data provided
            context (dict, optional): A dictionary of variable data to be rendered in the template
            user_id (str, optional): The ID of the user to whom the notification is being sent
            waterfall_config (Waterfall, optional): The configuration to be used by Hub priority engine to schedule
                this channel
            expiry (int, optional): The Epoch timestamp at which this notification task should expire if still not sent
        """
        self._push = pb.Push()

        for _ in arn_endpoints:
            validate_arn_endpoint(_)
        self.__set_arn_endpoints(arn_endpoints)

        validate_template(template)
        self._push.template = template
        self._push.context = json.dumps(context) if context else '{}'
        self._push.userID = user_id if user_id else ''
        self._push.expiry = expiry if expiry else get_expiry(self._default_expiry_offset)
        self.__set_waterfall(waterfall_config)

    def __set_arn_endpoints(self, arn_endpoints: List[str]):
        for _ in arn_endpoints:
            self._push.arnEndpoints.append(_)

    def __set_waterfall(self, value: Waterfall = None):
        if not value:
            value = Waterfall()
        self._push.waterfallConfig.CopyFrom(value.proto)

    @property
    def proto(self) -> pb.Push:
        return self._push
