class BaseEventHandler:
    async def handle(self, data, message):
        raise NotImplementedError(
            "handle method must be implemented in subclass")