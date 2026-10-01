from __future__ import annotations

from typing import Any

from wizardgram.context import Context
from wizardgram.middleware import Middleware
from wizardgram.router import Handler


class MemoryStateStore:
    """In-memory state store keyed by chat id. State is not persistent."""

    def __init__(self) -> None:
        self._data: dict[int, dict[str, Any]] = {}

    async def get(self, chat_id: int) -> dict[str, Any]:
        """Return a copy of the stored chat state."""
        return self._data.get(chat_id, {}).copy()

    async def set(self, chat_id: int, data: dict[str, Any]) -> None:
        """Replace the stored state for a chat."""
        self._data[chat_id] = data.copy()

    async def clear(self, chat_id: int) -> None:
        """Remove all state for a chat."""
        self._data.pop(chat_id, None)


class Scene:
    """A named sequence of asynchronous update handlers."""

    def __init__(self, name: str, steps: list[Handler]) -> None:
        self.name = name
        self.steps = steps


class SceneContext:
    """Control the active scene and access its shared state."""

    def __init__(self, stage: Stage, ctx: Context, state: dict[str, Any]) -> None:
        self._stage = stage
        self._ctx = ctx
        self.state = state

    async def next(self) -> None:
        """Advance to the next step, leaving the scene after its final step."""
        current = int(self.state.get("step", 0)) + 1
        scene = self._stage._scenes[str(self.state["scene"])]
        if current >= len(scene.steps):
            await self.leave()
        else:
            self.state["step"] = current
            await self._save()

    async def leave(self) -> None:
        """Clear the active scene and its state."""
        if self._ctx.chat is not None:
            await self._stage.store.clear(self._ctx.chat["id"])
        self.state.clear()

    async def enter(self, scene_name: str) -> None:
        """Enter a registered scene at its first step."""
        if scene_name not in self._stage._scenes:
            raise KeyError(f"Unknown scene: {scene_name}")
        self.state.clear()
        self.state.update({"scene": scene_name, "step": 0})
        await self._save()

    async def _save(self) -> None:
        if self._ctx.chat is not None:
            await self._stage.store.set(self._ctx.chat["id"], self.state)


class Stage:
    """Route updates to the active scene step for each chat."""

    def __init__(self, scenes: list[Scene], *, store: MemoryStateStore | None = None) -> None:
        self._scenes = {scene.name: scene for scene in scenes}
        self.store = store or MemoryStateStore()

    def middleware(self) -> Middleware:
        """Create middleware that runs active scene handlers."""

        async def middleware(ctx: Context, next_: Any) -> None:
            if ctx.chat is None:
                await next_()
                return
            state = await self.store.get(ctx.chat["id"])
            scene_name = state.get("scene")
            ctx.scene = SceneContext(self, ctx, state)
            if scene_name not in self._scenes:
                await next_()
                return
            scene = self._scenes[str(scene_name)]
            step = int(state.get("step", 0))
            if step < 0 or step >= len(scene.steps):
                await self.store.clear(ctx.chat["id"])
                await next_()
                return
            await scene.steps[step](ctx)

        return middleware
