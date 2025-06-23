from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventTopic(str, Enum):
    CRYPTO_PAYMENT = "crypto.payment"
    BUY_CRYPTO = "buy.crypto"
    SELL_CRYPTO = "sell.crypto"

class EventMetadata(BaseModel):
    timestamp: datetime
    source: Optional[str] = None
    guild: Optional[str] = None  # Optional, will be determined by topic

class CallbackRequest(BaseModel):
    topic: EventTopic
    data: dict


class EventPayload(BaseModel):
    topic: EventTopic
    data: dict  # Will be validated by topic-specific schemas