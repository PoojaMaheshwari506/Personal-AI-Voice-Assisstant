import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# Load env vars
load_dotenv()
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# Input from user
prompt = input("Enter your message: ")
first_message = "Hello! I’m your personal assistant."

# Override configuration (optional)
conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

# ✅ Add user_id here
config = ConversationConfig(
    user_id="local_dev_user",  # can be any string
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

# Create ElevenLabs client
client = ElevenLabs(api_key=API_KEY)

# Define callbacks
def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")

# Create conversation
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

# Start the conversation
conversation.start_session()
