# Multi-Guild Event Processor

A FastAPI-based event processing system that handles events from different guilds and transforms them into a star schema data warehouse.

## Architecture

The system follows a guild-based architecture where different types of events are processed by specialized guilds based on the topic:

- **Blockchain Guild**: Handles crypto-related events (payments, buy/sell crypto)
- **Future Guilds**: Can be easily added for other event types

## Supported Event Topics

### Blockchain Guild
- `crypto.payment` - Crypto payment transactions
- `buy.crypto` - Crypto purchase transactions  
- `sell.crypto` - Crypto sale transactions

## API Endpoints

### POST /events/callback
Receives events and routes them to appropriate guilds based on topic.

**Request Body:**
```json
{
  "topic": "crypto.payment",
  "data": {
    "transactionId": "tx_123",
    "fromEmail": "user1@example.com",
    "toEmail": "user2@example.com",
    "amount": "100.50",
    "concept": "Payment for services",
    "status": "completed",
    "blockchainTxHash": "0xabc123...",
    "transactionDate": "2024-01-15T10:30:00Z"
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "source": "webhook"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "processed_id": 1,
  "guild": "blockchain",
  "topic": "crypto.payment"
}
```

## Database Schema

The system uses a star schema with the following tables:

### Dimension Tables
- `dim_users` - User information
- `dim_statuses` - Transaction statuses
- `dim_dates` - Date dimensions with attributes
- `dim_concepts` - Transaction concepts/categories

### Fact Table
- `fact_transactions` - Main transaction facts with foreign keys to dimensions

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=your_password
   export POSTGRES_DB=blockchain_analytics
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

## Adding New Guilds

To add a new guild (e.g., for e-commerce events):

1. Create guild directory: `app/guilds/ecommerce/`
2. Add schemas, services, and processors
3. Update the callback router to handle the new topics
4. Add new dimension tables if needed

## Example Usage

```bash
curl -X POST "http://localhost:8000/events/callback" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "crypto.payment",
    "data": {
      "transactionId": "tx_123",
      "fromEmail": "alice@example.com",
      "toEmail": "bob@example.com", 
      "amount": "50.00",
      "concept": "Payment",
      "status": "completed",
      "blockchainTxHash": "0xabc123",
      "transactionDate": "2024-01-15T10:30:00Z"
    },
    "metadata": {
      "timestamp": "2024-01-15T10:30:00Z",
      "source": "webhook"
    }
  }'
```