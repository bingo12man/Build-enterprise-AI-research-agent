from typing import List

from pydantic import BaseModel


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]