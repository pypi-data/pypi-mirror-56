from dataclasses import dataclass
from dataclasses_json import dataclass_json
from petisco.events.event import Event


def event_cool(_cls=None):
    @dataclass_json
    @dataclass
    def wrap(cls):
        return cls

    if _cls is None:
        return wrap
    return wrap(_cls)


#
# def _process_class(cls):
#     #DataClassJsonMixin.register(cls)
#     return cls


class _EventDecorator:
    def __call__(self, cls):
        if not issubclass(cls, Event):
            raise TypeError("_EventDecorator only decorates UseCase subclasses")

        @dataclass_json
        @dataclass
        class EventWrapped(cls):
            def __init__(self, *args, **kwargs):
                import pdb

                pdb.set_trace()
                cls(*args, **kwargs)

        return EventWrapped


event = _EventDecorator
