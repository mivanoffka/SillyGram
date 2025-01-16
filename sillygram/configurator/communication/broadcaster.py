import asyncio
from typing import Optional
from ...manager import SillyManager
from ...text import SillyText

TIME_DELTA = 100


class _Broadcaster:
    _is_busy: bool = False

    _total_users_count: Optional[int] = None
    _processed_users_count: Optional[int] = None

    _should_stop: bool = False

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @property
    def total_users_count(self) -> Optional[int]:
        return self._total_users_count

    @property
    def processed_users_count(self) -> Optional[int]:
        return self._processed_users_count

    @property
    def progress(self) -> Optional[float]:
        if (
            self._total_users_count is not None
            and self._processed_users_count is not None
        ):
            return (
                self._total_users_count / float(self._processed_users_count)
                if self._processed_users_count > 0
                else None
            )

    async def try_show_broadcast_notice(self, manager: SillyManager, text: str) -> bool:
        if self._is_busy:
            return False

        asyncio.create_task(self._show_broadcast_notice(manager, text))
        return True

    async def _show_broadcast_notice(self, manager: SillyManager, text: str) -> None:
        users = manager.users.get_all()

        self._is_busy = True
        self._total_users_count = len(users)
        self._processed_users_count = 0
        self._should_stop = False


        for user in users:
            if self._should_stop:
                break

            try:
                await manager.show_notice(user, SillyText(text))
            except Exception as e:  # noqa: F841
                ...

            self._processed_users_count += 1
            await asyncio.sleep(TIME_DELTA)

        self._is_busy = False
        self._total_users_count = None
        self._processed_users_count = None
        self._should_stop = False

    async def stop(self) -> None:
        self._should_stop = True

broadcaster = _Broadcaster()
