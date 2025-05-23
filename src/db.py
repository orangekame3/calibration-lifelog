"""Database initialization module."""

import os

from bunnet import init_bunnet
from pymongo import MongoClient
from .dbmodel.chip_history import ChipHistoryDocument
from .dbmodel.chip import ChipDocument

mongo_ip = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))
client: MongoClient = MongoClient(
        mongo_ip, mongo_port, username="root", password="example"
    )


def initialize() -> None:
    """Initialize the repository and create initial data if needed."""
    init_bunnet(
        database=client.qubex,
        document_models=[ChipDocument,ChipHistoryDocument],  # type: ignore[arg-type] # noqa: F821
    )
