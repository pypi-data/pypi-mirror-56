import ioc

from aorta.lib.datastructures import ImmutableDTO


@ioc.inject('publisher', 'EventPublisher')
@ioc.inject('gateway', 'CommandGateway')
class Context:

    @classmethod
    def fromincoming(cls, incoming):
        return cls(incoming)

    def __init__(self, message):
        self.message = message

    def handle(self, func):
        """Invokes callable `func` with the message parameters as
        its first positional argument. The message is considered to
        be cleaned and validated at this point, so we may assume
        that the message body is of the appropriate type (e.g. a
        Python dictionary).
        """
        return func(ImmutableDTO.fromdict(self.message.body))

    def observe(self, *args, **kwargs):
        """Invokes :meth:`~aorta.EventPublisher.observe()`."""
        return self.publisher.observe(*args, **kwargs)

    def issue(self, *args, **kwargs):
        """Invokes :meth:`~aorta.CommandGateway.issue()`."""
        return self.gateway.issue(*args, **kwargs)
