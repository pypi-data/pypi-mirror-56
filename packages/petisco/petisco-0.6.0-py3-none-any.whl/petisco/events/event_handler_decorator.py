import inspect
from functools import wraps
import traceback
from typing import Callable, Tuple, Dict, List, Any

from meiga import Result
from meiga.decorators import meiga

from petisco.controller.errors.bad_request_http_error import BadRequestHttpError
from petisco.controller.errors.known_result_failure_handler import (
    KnownResultFailureHandler,
)
from petisco.controller.tokens.jwt_decorator import jwt
from petisco.logger.interface_logger import ERROR, INFO
from petisco.controller.errors.http_error import HttpError
from petisco.controller.tokens.jwt_config import JwtConfig
from petisco.frameworks.flask.correlation_id_provider import (
    flask_correlation_id_provider,
)
from petisco.logger.log_message import LogMessage
from petisco.logger.not_implemented_logger import NotImplementedLogger


class EventHandlerDecorator:
    def __init__(
        self,
        logger=NotImplementedLogger(),
        input_parameter: str = None,
        event_from_specific_event_data: Callable = None,
    ):
        self.logger = logger
        self.input_parameter = input_parameter
        self.event_from_specific_event_data = event_from_specific_event_data

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):

            log_message = LogMessage(
                layer="event_handler", operation=f"{func.__name__}"
            )

            try:
                result = func(*args, **kwargs)
                if result.is_success:
                    if self.event_from_specific_event_data:
                        input_parameter = kwargs.get(self.input_parameter)
                        event = self.event_from_specific_event_data(input_parameter)
                        log_message.message = f"Event: {event}"
                else:
                    log_message.message = f"{result}"
                    self.logger.log(ERROR, log_message.to_json())

            except Exception as e:
                log_message.message = f"Event handling Error {func.__name__}: {e} | {traceback.print_exc()}"
                self.logger.log(ERROR, log_message.to_json())

        return wrapper


event_handler = EventHandlerDecorator
