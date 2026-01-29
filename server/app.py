import random
import logging
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors as mongo_errors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MONGO_HOST = os.getenv('MONGO_HOST', 'db')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Database connection helper
def get_db_connection():
    """
    Establishes and returns a MongoDB connection.
    Raises an exception if connection fails.
    """
    try:
        client = MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            serverSelectionTimeoutMS=5000
        )
        # Test the connection
        client.server_info()
        logger.info(f"Successfully connected to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
        return client
    except mongo_errors.ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise


# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.url}")
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"Unhandled exception: {error}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500


# Request logging middleware
@app.before_request
def log_request():
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")


@app.after_request
def log_response(response):
    logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
    return response


@app.route('/')
def index():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return jsonify({"status": "OK", "message": "Server is running"}), 200


@app.route('/quote')
def quote():
    """
    Returns a random quote from the database.
    Handles various error scenarios gracefully.
    """
    logger.info(f"Quote requested from {request.remote_addr}")
    
    client = None
    try:
        # Establish database connection
        client = get_db_connection()
        db = client.quotesdb
        
        # Query quotes collection
        logger.debug("Fetching quotes from database")
        data = list(db.quotes.find())
        
        # Check if database is empty
        if len(data) < 1:
            logger.warning("No quotes found in database")
            return jsonify({
                "id": 0,
                "quote": "Remember to init the db with InitDB.js",
                "warning": "Database is empty"
            }), 200
        
        # Select and return a random quote
        row = random.choice(data)
        logger.info(f"Returning quote with id: {row.get('id', 'unknown')}")
        
        return jsonify({
            "id": int(row['id']),
            "quote": row['quote']
        }), 200
        
    except mongo_errors.ServerSelectionTimeoutError:
        logger.error("Database connection timeout")
        return jsonify({
            "error": "Database connection failed",
            "message": "Unable to connect to the database server"
        }), 503
        
    except mongo_errors.PyMongoError as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "error": "Database error",
            "message": "An error occurred while accessing the database"
        }), 500
        
    except KeyError as e:
        logger.error(f"Missing required field in database record: {e}")
        return jsonify({
            "error": "Data integrity error",
            "message": "Invalid data structure in database"
        }), 500
        
    except ValueError as e:
        logger.error(f"Data conversion error: {e}")
        return jsonify({
            "error": "Data format error",
            "message": "Unable to process quote data"
        }), 500
        
    except Exception as e:
        logger.error(f"Unexpected error in /quote endpoint: {e}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500
        
    finally:
        # Ensure database connection is closed
        if client:
            try:
                client.close()
                logger.debug("Database connection closed")
            except Exception as e:
                logger.warning(f"Error closing database connection: {e}")


if __name__ == '__main__':
    try:
        logger.info(f"Starting Flask server in {'DEBUG' if DEBUG_MODE else 'PRODUCTION'} mode")
        logger.info(f"Connecting to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
        app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f"Failed to start Flask server: {e}", exc_info=True)
        raise
