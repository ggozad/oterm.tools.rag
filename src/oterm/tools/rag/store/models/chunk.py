from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

import numpy
from pgvector.sqlalchemy import Vector
from pydantic import field_serializer
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from oterm.tools.rag.config import Config

if TYPE_CHECKING:
    from oterm.tools.rag.store.models.document import Document


class Chunk(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    document_id: UUID = Field(foreign_key="document.id", nullable=False)
    document: "Document" = Relationship(back_populates="chunks")

    text: str = Field(nullable=False)
    meta: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))
    embedding: list[float] = Field(
        sa_column=Column(Vector(Config.EMBEDDING_VECTOR_DIM))
    )

    @field_serializer("embedding")
    def serialize_embedding(self, embedding: numpy.ndarray) -> list[float]:
        return embedding.tolist()
