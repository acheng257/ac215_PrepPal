import os
from typing import Dict, List
from fastapi import HTTPException
import base64
from pathlib import Path
import traceback
from vertexai.generative_models import GenerativeModel, ChatSession, Part
from google.oauth2 import service_account
import vertexai

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-002"

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.1,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}
# Initialize the GenerativeModel with specific system instructions
SYSTEM_INSTRUCTION = """
You are an AI assistant specialized in recipe recommendations.

When answering a query:
1. Demonstrate expertise in recipes, including aspects like:
  - Ingredients and their substitutions
  - Cooking methods and techniques
  - Flavor profiles and balancing
  - Regional and cultural recipe traditions
  - Pairing recommendations for meals and beverages
  - Dietary adaptations and restrictions
  - Presentation and serving suggestions
2. Always maintain a professional and knowledgeable tone, befitting a culinary expert.

Your goal is to provide accurate, helpful information about recipes for each query, ensuring users can confidently prepare and enjoy their meals.
"""
generative_model = GenerativeModel(GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION])

# Initialize chat sessions
chat_sessions: Dict[str, ChatSession] = {}


def create_chat_session(recommendations, pantry) -> ChatSession:
    """Create a new chat session with the model"""
    fine_tuning_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(fine_tuning_key_path)
    vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION, credentials=credentials)

    chat_session = generative_model.start_chat()
    if recommendations or pantry:
        initialize_session_with_context(chat_session, recommendations, pantry)
    return chat_session


def initialize_session_with_context(chat_session: ChatSession, recommendations: str, pantry: str):
    """Initialize a chat session with recipe context."""
    context_message = f"Here are some recipe recommendations the user currently has:\n{recommendations}. They may refer to this list of recommendations in their query. \
        The user also currently has these items in their pantry: {pantry}"
    chat_session.send_message([context_message])


def generate_chat_response(chat_session: ChatSession, message: Dict) -> str:
    """
    Generate a response using the chat session to maintain history.
    Handles both text and image inputs.

    Args:
        chat_session: The Vertex AI chat session
        message: Dict containing 'content' (text) and optionally 'image' (base64 string)

    Returns:
        str: The model's response
    """
    # response = chat_session.send_message(
    #     message,
    #     generation_config=generation_config
    # )
    # return response.text
    try:
        # Initialize parts list for the message
        message_parts = []

        # Process image if present
        if message.get("image"):
            try:
                # Extract the actual base64 data and mime type
                base64_string = message.get("image")
                if "," in base64_string:
                    header, base64_data = base64_string.split(",", 1)
                    mime_type = header.split(":")[1].split(";")[0]
                else:
                    base64_data = base64_string
                    mime_type = "image/jpeg"  # default to JPEG if no header

                # Decode base64 to bytes
                image_bytes = base64.b64decode(base64_data)

                # Create an image Part using FileData
                image_part = Part.from_data(image_bytes, mime_type=mime_type)
                message_parts.append(image_part)

                # Add text content if present
                if message.get("content"):
                    message_parts.append(message["content"])
                else:
                    message_parts.append("Name the cheese in the image, no descriptions needed")

            except ValueError as e:
                print(f"Error processing image: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")
        elif message.get("image_path"):
            # Read the image file
            image_path = os.path.join("chat-history", "llm", message.get("image_path"))
            with Path(image_path).open("rb") as f:
                image_bytes = f.read()

            # Determine MIME type based on file extension
            mime_type = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif"}.get(Path(image_path).suffix.lower(), "image/jpeg")

            # Create an image Part using FileData
            image_part = Part.from_data(image_bytes, mime_type=mime_type)
            message_parts.append(image_part)

            # Add text content if present
            if message.get("content"):
                message_parts.append(message["content"])
            else:
                message_parts.append("Name the cheese in the image, no descriptions needed")
        else:
            # Add text content if present
            if message.get("content"):
                message_parts.append(message["content"])

        if not message_parts:
            raise ValueError("Message must contain either text content or image")

        # Send message with all parts to the model
        response = chat_session.send_message(message_parts, generation_config=generation_config)

        return response.text

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")


def rebuild_chat_session(chat_history: List[Dict], recommendations: str, pantry: str) -> ChatSession:
    """Rebuild a chat session with complete context"""
    new_session = create_chat_session(recommendations, pantry)

    for message in chat_history:
        if message["role"] == "user":
            generate_chat_response(new_session, message)
        #
        #     response = new_session.send_message(
        #         message["content"],
        #         generation_config=generation_config
        #     )

    return new_session
