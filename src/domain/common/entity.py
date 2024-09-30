"""Base entity classes."""

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapper
    from sqlalchemy.sql import FromClause


@dataclass(kw_only=True)
class Entity:
    """Base entity class."""

    if TYPE_CHECKING:
        __table__: FromClause = field(init=False)
        __mapper__: Mapper[Any] = field(init=False)
        __name__: str = field(init=False)

    # noinspection PyArgumentList
    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Create entity from dictionary."""
        # Get the set of field names in the dataclass
        field_names = {f.name for f in fields(cls)}

        # Filter the dictionary to only include keys that are dataclass fields
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        # Create and return an instance of the dataclass
        return cls(**filtered_data)

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """Convert entity to dictionary."""
        if exclude is None:
            exclude = set()
        return asdict(
            self,
            dict_factory=lambda _: {k: v for k, v in _ if k not in exclude},
        )

