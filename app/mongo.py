"""
MongoDB helper for FitSync (hybrid setup)

Usage:
  from .mongo import get_db, get_collection, mongo_enabled

  if mongo_enabled():
      workouts = get_collection("workouts")
      workouts.insert_one({...})

This module gracefully no-ops if MONGODB_URI is not configured.
"""

from __future__ import annotations

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

_client: Optional[MongoClient] = None
_db: Optional[Database] = None


def _connect() -> None:
    global _client, _db
    if _client is not None:
        return

    uri = os.getenv("MONGODB_URI")
    if not uri:
        # Mongo is disabled if URI is not set
        return

    # Allow specifying DB name separately (for mongodb:// URIs without path)
    db_name = os.getenv("MONGODB_DB")

    try:
        _client = MongoClient(uri, uuidRepresentation="standard")
        if db_name:
            _db = _client[db_name]
        else:
            # get_default_database works for URI that includes the db path
            _db = _client.get_default_database() or _client["fitsync"]
    except Exception as e:
        # On failure, keep disabled state but don't crash the app
        print(f"[Mongo] Failed to initialize client: {e}")
        _client = None
        _db = None


def mongo_enabled() -> bool:
    """Return True if MongoDB is configured and reachable (lazy init)."""
    if os.getenv("MONGODB_URI") is None:
        return False
    if _client is None:
        _connect()
    return _db is not None


def get_db() -> Optional[Database]:
    """Get the Database object or None if not configured."""
    if _db is None:
        _connect()
    return _db


def get_collection(name: str) -> Optional[Collection]:
    """Get a collection by name or None if MongoDB is disabled."""
    db = get_db()
    return db[name] if db else None


def ensure_indexes() -> None:
    """Create useful indexes if MongoDB is enabled.

    Call this once at startup (optional). Safe to call multiple times.
    """
    db = get_db()
    if not db:
        return

    try:
        # Workouts: fast queries per user and by date
        db["workouts"].create_index([("userId", 1), ("date", -1)])
        db["workouts"].create_index([("exercises.exerciseId", 1)])

        # Habits
        db["habits"].create_index([("userId", 1)])
        db["habits"].create_index([("logs.date", -1)])

        # Food and Water logs
        db["food_logs"].create_index([("userId", 1), ("date", -1)])
        db["water_logs"].create_index([("userId", 1), ("date", -1)])
    except Exception as e:
        print(f"[Mongo] Failed to create indexes: {e}")
