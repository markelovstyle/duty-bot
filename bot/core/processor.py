import asyncio
import typing

from vkbottle.framework.framework.handler import MiddlewareFlags
from vkbottle.framework.framework.handler.user.events import ADDITIONAL_FIELDS
from vkbottle.framework.user.processor import UserProcessor
from vkbottle.types.user_longpoll import Message
from vkbottle.utils import logger


class Processor(UserProcessor):
    async def message_processor(
        self, update: dict, update_code: int, update_fields: typing.List[int],
    ) -> None:
        """ Process message events. Use base fields to make a dataclass
        Params described in parent_processor
        """
        # Expanding data
        fields = ("message_id", "flags", *ADDITIONAL_FIELDS)
        data = dict(zip(fields, update_fields))
        middleware_args, tasks = [], []

        if self.expand_models:
            data.update(await self.expand_data(update_code, data))

        message = Message(**data)

        # Executing middleware
        async for mr in self.middleware.run_middleware(
            message, MiddlewareFlags.PRE
        ):
            if self.status.middleware_expressions:
                if mr is False:
                    return
                elif mr is not None:
                    middleware_args.append(mr)

        # Executing branch queue
        if message.dict()[self.branch.checkup_key.value] in await self.branch.queue:
            return await self.branch_processor(message, middleware_args)

        # Rule checkup
        for rules in self.handler.message_rules:
            rule = rules[0]  # API Complexity #FIXME
            check = await rule.check(update)

            if check is not None:
                args, kwargs = [], {}

                if isinstance(check, tuple):
                    check = await self.filter(message, check)
                    if not check:
                        continue
                    args, kwargs = check

                tasks.append(rule.call(message, *args, **kwargs))
        result = await asyncio.gather(*tasks)
        await asyncio.gather(*[self.handler_return(i, data) for i in result])

        async for mr in self.middleware.run_middleware(
            message, MiddlewareFlags.POST, *middleware_args
        ):
            logger.debug(f"POST Middleware handler returned: {mr}")