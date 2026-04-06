from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_validator

MISSING_REASONING_PREFIX = "[NO_REASONING"

MAX_REASONING_CHARS = 10_000


class ReasoningModel(BaseModel):
    run_id: str
    reasoning: str
    exported: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def primary_key(self):
        return ["run_id"]

    @field_validator("exported", mode="before")
    def parse_exported_as_bool(cls, v: Any) -> bool:
        if isinstance(v, int):
            return bool(v)
        return v


REASONING_FIELDS = ReasoningModel.model_fields.keys()
