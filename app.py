import os
import csv
from datetime import datetime, timedelta
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from google.generativeai import GenerativeModel
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# Get Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PERSONAL_PHONE = os.getenv('PERSONAL_PHONE')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# CSV file path for logging
LEADS_CSV = 'leads.csv'

# Cooldown tracking: {caller_number: last_text_time}
call_log = {}

# Conversation history: {caller_number: [{"role": "user", "content": "..."}]}
conversation_history = {}

def initialize_csv():
    """Create CSV file with headers if it doesn't exist."""
    if not os.path.exists(LEADS_CSV):
        with open(LEADS_CSV, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'Sender Number', 'Incoming Message', 'AI Response'])
        logger.info(f"{LEADS_CSV} created with headers")

def log_to_csv(sender_number, incoming_message, ai_response):
    """Log SMS interaction to CSV file."""
    try:
        with open(LEADS_CSV, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, sender_number, incoming_message, ai_response])
        logger.info(f"Logged SMS from {sender_number}")
    except Exception as e:
        logger.error(f"Error writing to CSV: {str(e)}")

def get_ai_response(sender_number, incoming_message):
    """
    Send incoming message to Gemini API with conversation history.
    Returns a response under 160 characters.
    """
    try:
        # Initialize conversation history for new callers
        if sender_number not in conversation_history:
            conversation_history[sender_number] = []
        
        # Add user message to history
        conversation_history[sender_number].append({
            "role": "user",
            "content": incoming_message
        })
        
        # Build conversation context (last 10 messages to keep context manageable)
        context = "\n".join([
            f"{'Customer' if msg['role'] == 'user' else 'Sarah'}: {msg['content']}"
            for msg in conversation_history[sender_number][-10:]
        ])
        
        system_instruction = """You are Sarah, a friendly receptionist for a Roofing Company. 
Your goal is to get the customer's Name, Issue, and Address. 
Keep replies short (under 160 chars). Be professional and helpful.
Do not make up prices or guarantees. If asked about pricing, say you'll have someone call them."""
        
        model = GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(
            f"{system_instruction}\n\nConversation:\n{context}\n\nRespond as Sarah:"
        )
        
        ai_response = response.text.strip()
        
        # Ensure response is under 160 characters
        if len(ai_response) > 160:
            ai_response = ai_response[:157] + "..."
        
        # Add AI response to history
        conversation_history[sender_number].append({
            "role": "assistant",
            "content": ai_response
        })
        
        logger.info(f"AI Response: {ai_response}")
        return ai_response
        
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return None

@app.route('/voice', methods=['POST'])
def handle_voice():
    """
    Handle incoming voice calls - forward to personal phone.
    """
    try:
        caller_number = request.form.get('From', 'Unknown')
        logger.info(f"Incoming call from {caller_number}")
        
        # Create TwiML response
        response = VoiceResponse()
        
        # Forward call to personal phone
        dial = response.dial(
            timeout=20,
            action='/call-status',
            caller_id=caller_number
        )
        dial.number(PERSONAL_PHONE)
        
        return str(response), 200
        
    except Exception as e:
        logger.error(f"Error in handle_voice: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, we're experiencing technical difficulties. Please try again later.")
        return str(response), 200

@app.route('/call-status', methods=['POST'])
def handle_call_status():
    """
    Handle call status - send text if call was missed.
    """
    try:
        dial_call_status = request.form.get('DialCallStatus', '')
        caller_number = request.form.get('From', '')
        
        logger.info(f"Call status for {caller_number}: {dial_call_status}")
        
        # Check if call was not completed (missed)
        if dial_call_status in ['no-answer', 'busy', 'failed', 'canceled']:
            logger.info(f"Missed call detected from {caller_number}")
            
            # Check cooldown - have we texted this caller in last 15 minutes?
            current_time = datetime.now()
            
            if caller_number in call_log:
                last_text_time = call_log[caller_number]
                time_diff = current_time - last_text_time
                
                if time_diff < timedelta(minutes=15):
                    logger.info(f"Cooldown active for {caller_number}, skipping text")
                    return '', 200
            
            # Send missed call text
            try:
                message = twilio_client.messages.create(
                    body="Sorry I missed you! I'm on a roof right now. How can I help you?",
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    to=caller_number
                )
                
                # Update cooldown tracker
                call_log[caller_number] = current_time
                
                logger.info(f"Missed call SMS sent to {caller_number}: {message.sid}")
                
            except Exception as e:
                logger.error(f"Error sending missed call SMS: {str(e)}")
        
        return '', 200
        
    except Exception as e:
        logger.error(f"Error in handle_call_status: {str(e)}")
        return '', 200

@app.route('/sms', methods=['POST'])
def handle_sms():
    """
    Handle incoming SMS from Twilio with AI chat.
    """
    try:
        # Extract incoming message and sender number from Twilio
        incoming_message = request.form.get('Body', '').strip()
        sender_number = request.form.get('From', '').strip()
        
        logger.info(f"Received SMS from {sender_number}: {incoming_message}")
        
        # Get AI response with conversation context
        ai_response = get_ai_response(sender_number, incoming_message)
        
        # Use fallback message if API fails
        if not ai_response:
            ai_response = "I'm a bit tied up, but I'll call you shortly!"
        
        # Log to CSV
        log_to_csv(sender_number, incoming_message, ai_response)
        
        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(ai_response)
        
        logger.info(f"Sent response to {sender_number}")
        
        # Send monitoring message to business owner
        send_monitoring_sms(sender_number, incoming_message, ai_response)
        
        return str(twiml_response), 200
        
    except Exception as e:
        logger.error(f"Error in handle_sms: {str(e)}")
        # Return fallback message as TwiML
        twiml_response = MessagingResponse()
        twiml_response.message("I'm a bit tied up, but I'll call you shortly!")
        return str(twiml_response), 200

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint."""
    return 'SMS Auto-Responder is running!', 200

if __name__ == '__main__':
    # Initialize CSV on startup
    initialize_csv()
    
    # Run Flask app
    # Set debug=False for production
    app.run(host='0.0.0.0', port=5000, debug=True)
