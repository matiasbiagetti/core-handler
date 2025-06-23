from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.events.schemas.base import CallbackRequest, EventTopic
from app.models.database import create_tables, get_db
from app.guilds.blockchain.services.topic_router import BlockchainTopicRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/callback")
async def handle_event(
    request: CallbackRequest,
    db: Session = Depends(get_db)
):
    """
    Handle events from different guilds based on topic.
    
    Topic-based routing:
    - crypto.payment, buy.crypto, sell.crypto -> blockchain guild
    - Future topics can be routed to other guilds
    """
    try:
        create_tables()
        print("Tables created")
        logger.info(f"Processing event: topic={request.topic}")
        
        # Route based on topic to determine guild
        if request.topic in [EventTopic.CRYPTO_PAYMENT, EventTopic.BUY_CRYPTO, EventTopic.SELL_CRYPTO]:
            result = BlockchainTopicRouter.route(request.topic, request.data, db)
            return {
                "status": "success", 
                "processed_id": result.id,
                "guild": "blockchain",
                "topic": request.topic
            }
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported topic: {request.topic}. Supported topics: crypto.payment, buy.crypto, sell.crypto"
            )
            
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")