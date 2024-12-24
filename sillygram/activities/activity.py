import asyncio
from abc import abstractmethod
from ..manager import SillyManager


class SillyRegularActivity:

    @abstractmethod
    async def _condition(self, manager: SillyManager) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def _activity(self, manager: SillyManager):
        raise NotImplementedError()

    async def execute(self, manager: SillyManager):
        if await self._condition(manager):
            asyncio.create_task(self._activity(manager))
