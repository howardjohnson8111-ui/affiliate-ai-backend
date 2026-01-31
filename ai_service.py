import requests
import json
import os
import re
import google.genai as genai
from google.genai import types

# Get API Key
API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    print("[WARNING] GOOGLE_API_KEY environment variable not set!")
    print("   Please set it before using Gemini integration.")

# --- Your ACTUAL default_api functions ---
# This class will contain methods that make HTTP requests to your Node.js backend (localhost:3001).
# Each method here corresponds to a function in the default_api that Gemini can call.
class YourActualDefaultApi:
    def __init__(self, base_url="http://localhost:3001/api"):
        self.base_url = base_url

    # --- Campaign Functions ---
    def create_Campaign(self, name: str, platform: str, affiliate_link: str = None, 
                        clicks: float = 0, content: str = None, conversions: float = 0, 
                        earnings: float = 0, image_url: str = None, scheduled_date: str = None, 
                        status: str = "draft", tags: list[str] = None) -> dict:
        """
        Creates a new Campaign entity by making an HTTP POST request to your Node.js backend.
        """
        url = f"{self.base_url}/campaigns"
        payload = {
            "name": name,
            "platform": platform,
            "affiliate_link": affiliate_link,
            "clicks": clicks,
            "content": content,
            "conversions": conversions,
            "earnings": earnings,
            "image_url": image_url,
            "scheduled_date": scheduled_date,
            "status": status,
            "tags": tags
        }
        # Filter out None values - your Node.js backend should handle default values.
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            print(f"[Your App Backend]: Making POST request to {url} with payload: {payload}")
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            print(f"[Your App Backend]: create_Campaign successful. Response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if 'response' in locals():
                try:
                    error_details["details"] = response.json()
                except json.JSONDecodeError:
                    error_details["details"] = response.text
            print(f"[Your App Backend]: create_Campaign failed. Error: {error_details}")
            return error_details

    def read_Campaign(self, campaign_id: str) -> dict:
        """
        Retrieves a Campaign by ID from your Node.js backend.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}"
        
        try:
            print(f"[Your App Backend]: Making GET request to {url}")
            response = requests.get(url)
            response.raise_for_status()
            print(f"[Your App Backend]: read_Campaign successful. Response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if 'response' in locals():
                try:
                    error_details["details"] = response.json()
                except json.JSONDecodeError:
                    error_details["details"] = response.text
            print(f"[Your App Backend]: read_Campaign failed. Error: {error_details}")
            return error_details

    def update_Campaign(self, campaign_id: str, **kwargs) -> dict:
        """
        Updates a Campaign by ID on your Node.js backend.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}"
        payload = {k: v for k, v in kwargs.items() if v is not None}
        
        try:
            print(f"[Your App Backend]: Making PUT request to {url} with payload: {payload}")
            response = requests.put(url, json=payload)
            response.raise_for_status()
            print(f"[Your App Backend]: update_Campaign successful. Response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if 'response' in locals():
                try:
                    error_details["details"] = response.json()
                except json.JSONDecodeError:
                    error_details["details"] = response.text
            print(f"[Your App Backend]: update_Campaign failed. Error: {error_details}")
            return error_details

    def delete_Campaign(self, campaign_id: str) -> dict:
        """
        Deletes a Campaign by ID from your Node.js backend.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}"
        
        try:
            print(f"[Your App Backend]: Making DELETE request to {url}")
            response = requests.delete(url)
            response.raise_for_status()
            print(f"[Your App Backend]: delete_Campaign successful. Response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if 'response' in locals():
                try:
                    error_details["details"] = response.json()
                except json.JSONDecodeError:
                    error_details["details"] = response.text
            print(f"[Your App Backend]: delete_Campaign failed. Error: {error_details}")
            return error_details


# --- Gemini Integration Functions ---
# These functions will be used as tools for Gemini to call
def gemini_create_campaign(name: str, platform: str, **kwargs) -> dict:
    """Gemini wrapper for creating a campaign."""
    api = YourActualDefaultApi()
    return api.create_Campaign(name, platform, **kwargs)

def gemini_read_campaign(campaign_id: str) -> dict:
    """Gemini wrapper for reading a campaign."""
    api = YourActualDefaultApi()
    return api.read_Campaign(campaign_id)

def gemini_update_campaign(campaign_id: str, **kwargs) -> dict:
    """Gemini wrapper for updating a campaign."""
    api = YourActualDefaultApi()
    return api.update_Campaign(campaign_id, **kwargs)

def gemini_delete_campaign(campaign_id: str) -> dict:
    """Gemini wrapper for deleting a campaign."""
    api = YourActualDefaultApi()
    return api.delete_Campaign(campaign_id)


# --- Gemini Function Schema ---
# These schemas tell Gemini what functions are available and how to call them
# Using proper types.FunctionDeclaration for SDK compatibility
CAMPAIGN_TOOLS = [
    types.FunctionDeclaration(
        name="create_campaign",
        description="Creates a new campaign with the specified details. Used when user wants to create a marketing campaign.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "name": types.Schema(type=types.Type.STRING, description="The name of the campaign (required)"),
                "platform": types.Schema(type=types.Type.STRING, description="The platform for the campaign, e.g., 'Instagram', 'Facebook', 'TikTok', 'Twitter' (required)"),
                "affiliate_link": types.Schema(type=types.Type.STRING, description="The affiliate link for the campaign (optional)"),
                "content": types.Schema(type=types.Type.STRING, description="The content or description of the campaign (optional)"),
                "status": types.Schema(type=types.Type.STRING, description="The status of the campaign (default: draft)")
            },
            required=["name", "platform"]
        )
    ),
    types.FunctionDeclaration(
        name="read_campaign",
        description="Retrieves the details of a specific campaign by ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "campaign_id": types.Schema(type=types.Type.STRING, description="The unique ID of the campaign to retrieve (required)")
            },
            required=["campaign_id"]
        )
    ),
    types.FunctionDeclaration(
        name="update_campaign",
        description="Updates an existing campaign with new details.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "campaign_id": types.Schema(type=types.Type.STRING, description="The unique ID of the campaign to update (required)"),
                "name": types.Schema(type=types.Type.STRING, description="New name for the campaign (optional)"),
                "platform": types.Schema(type=types.Type.STRING, description="New platform for the campaign (optional)"),
                "content": types.Schema(type=types.Type.STRING, description="New content for the campaign (optional)"),
                "status": types.Schema(type=types.Type.STRING, description="New status for the campaign (optional)")
            },
            required=["campaign_id"]
        )
    ),
    types.FunctionDeclaration(
        name="delete_campaign",
        description="Deletes a campaign by ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "campaign_id": types.Schema(type=types.Type.STRING, description="The unique ID of the campaign to delete (required)")
            },
            required=["campaign_id"]
        )
    )
]


# --- Transaction Tool Schema ---
TRANSACTION_TOOLS = [
    types.FunctionDeclaration(
        name="create_transaction",
        description="Log a new financial transaction (deposit, withdrawal, dividend, affiliate_payout, etc.)",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "amount": types.Schema(type=types.Type.NUMBER, description="The dollar amount (required)"),
                "type": types.Schema(
                    type=types.Type.STRING,
                    description="Transaction type: deposit, withdrawal, dividend, affiliate_payout, stock_purchase, or stock_sale (required)",
                    enum=["deposit", "withdrawal", "dividend", "affiliate_payout", "stock_purchase", "stock_sale"]
                ),
                "description": types.Schema(type=types.Type.STRING, description="Notes about the transaction (optional)"),
                "payment_method": types.Schema(
                    type=types.Type.STRING,
                    description="Payment method: paypal, apple_pay, cash_app, chime, bank_transfer, or crypto (optional)",
                    enum=["paypal", "apple_pay", "cash_app", "chime", "bank_transfer", "crypto"]
                ),
                "status": types.Schema(
                    type=types.Type.STRING,
                    description="Transaction status: pending, completed, or failed (default: pending)",
                    enum=["pending", "completed", "failed"]
                )
            },
            required=["amount", "type"]
        )
    )
]


# --- PayPal Payment Tools ---
PAYPAL_TOOLS = [
    types.FunctionDeclaration(
        name="create_PayPalPayment",
        description="Initiate a new PayPal payment. Creates a payment request in the backend that can be sent to PayPal for processing.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "amount": types.Schema(type=types.Type.NUMBER, description="The payment amount in dollars (required)"),
                "description": types.Schema(type=types.Type.STRING, description="A short description of what the payment is for (required)"),
                "orderId": types.Schema(type=types.Type.STRING, description="Optional order reference ID to link payment to an order")
            },
            required=["amount", "description"]
        )
    ),
    types.FunctionDeclaration(
        name="get_PayPalPaymentDetails",
        description="Retrieve the details and status of a specific PayPal payment by its ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "payment_id": types.Schema(type=types.Type.STRING, description="The unique ID of the PayPal payment to retrieve (required)")
            },
            required=["payment_id"]
        )
    ),
    types.FunctionDeclaration(
        name="list_PayPalPayments",
        description="Get a list of all PayPal payments made by the current user.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={}
        )
    ),
    types.FunctionDeclaration(
        name="verify_PayPalPayment",
        description="Verify a PayPal payment after the user has completed the transaction on PayPal. Updates the payment status to completed.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "payment_id": types.Schema(type=types.Type.STRING, description="The unique ID of the payment to verify (required)"),
                "transactionId": types.Schema(type=types.Type.STRING, description="The PayPal transaction ID from the payment confirmation (required)")
            },
            required=["payment_id", "transactionId"]
        )
    ),
    types.FunctionDeclaration(
        name="cancel_PayPalPayment",
        description="Cancel a pending or failed PayPal payment. Mark the payment as cancelled.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "payment_id": types.Schema(type=types.Type.STRING, description="The unique ID of the payment to cancel (required)")
            },
            required=["payment_id"]
        )
    ),
    types.FunctionDeclaration(
        name="get_PayPalConfig",
        description="Retrieve PayPal configuration including the PayPal email address for payments.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={}
        )
    )
]


# --- AI Persona Definitions ---
# Each persona has a name, description, and list of tools they can access
PERSONAS = {
    "campaign_manager": {
        "name": "Campaign Manager",
        "description": "Manages marketing campaigns across platforms (Instagram, Facebook, TikTok, Twitter, etc.). Specializes in creating, tracking, and optimizing affiliate marketing campaigns.",
        "tools": ["create_campaign", "read_campaign", "update_campaign", "delete_campaign"]
    },
    "stock_analyst": {
        "name": "Stock Market Analyst",
        "description": "Tracks stock investments, dividends, and stock market insights. Manages stock purchases, sales, and dividend tracking.",
        "tools": ["create_stock", "read_stock", "update_stock", "delete_stock", "create_transaction"]
    },
    "learning_manager": {
        "name": "Learning & Development Manager",
        "description": "Tracks educational progress and learning modules. Helps you stay updated with courses, certifications, and skill development.",
        "tools": ["create_learning_module", "read_learning_module", "update_learning_module", "delete_learning_module"]
    },
    "financial_assistant": {
        "name": "Financial Assistant",
        "description": "Logs all financial transactions including deposits, withdrawals, affiliate payouts, dividends, and bank transfers. Manages PayPal payments. Maintains comprehensive financial records.",
        "tools": ["create_transaction", "create_PayPalPayment", "get_PayPalPaymentDetails", "list_PayPalPayments", "verify_PayPalPayment", "cancel_PayPalPayment", "get_PayPalConfig"]
    },
    "app_customizer": {
        "name": "App Customizer",
        "description": "Manages user preferences and application settings including theme, default views, notifications, and display options.",
        "tools": ["update_app_settings", "get_app_settings"]
    },
    "language_assistant": {
        "name": "Language Assistant",
        "description": "Provides multilingual support including translation, language switching, and content generation in 65+ languages.",
        "tools": ["translate_content", "set_language", "get_supported_languages"]
    }
}

# Persona detection keywords
PERSONA_KEYWORDS = {
    "campaign_manager": ["campaign", "marketing", "campaign manager", "ads", "instagram", "facebook", "tiktok", "twitter", "platform"],
    "stock_analyst": ["stock", "analyst", "market", "dividend", "portfolio", "shares", "equity", "investment"],
    "learning_manager": ["learning", "module", "course", "education", "training", "skill", "progress", "module"],
    "financial_assistant": ["transaction", "deposit", "withdrawal", "payout", "payment", "paypal", "pay", "invoice", "billing", "financial", "money", "finance"],
    "app_customizer": ["setting", "preference", "theme", "customize", "custom", "view", "notification", "display"],
    "language_assistant": ["translate", "language", "spanish", "french", "german", "chinese", "japanese", "korean", "arabic", "portuguese", "russian", "italian", "dutch", "swedish", "hindi", "translate to", "language assistant"]
}


# --- Stock Tool Schema (Placeholder) ---
STOCK_TOOLS = [
    types.FunctionDeclaration(
        name="create_stock",
        description="Log a new stock purchase with details like ticker symbol, shares, and purchase price.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "ticker": types.Schema(type=types.Type.STRING, description="Stock ticker symbol (e.g., AAPL, MSFT) (required)"),
                "shares": types.Schema(type=types.Type.NUMBER, description="Number of shares purchased (required)"),
                "purchase_price": types.Schema(type=types.Type.NUMBER, description="Price per share at purchase (required)"),
                "purchase_date": types.Schema(type=types.Type.STRING, description="Date of purchase (optional)"),
                "broker": types.Schema(type=types.Type.STRING, description="Broker name (e.g., Fidelity, Robinhood) (optional)")
            },
            required=["ticker", "shares", "purchase_price"]
        )
    ),
    types.FunctionDeclaration(
        name="read_stock",
        description="Retrieve details about a specific stock holding.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "stock_id": types.Schema(type=types.Type.STRING, description="The unique ID of the stock record (required)")
            },
            required=["stock_id"]
        )
    ),
    types.FunctionDeclaration(
        name="update_stock",
        description="Update stock holding details like current shares or broker information.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "stock_id": types.Schema(type=types.Type.STRING, description="The unique ID of the stock record (required)"),
                "shares": types.Schema(type=types.Type.NUMBER, description="Updated number of shares (optional)"),
                "current_price": types.Schema(type=types.Type.NUMBER, description="Current market price (optional)"),
                "notes": types.Schema(type=types.Type.STRING, description="Additional notes (optional)")
            },
            required=["stock_id"]
        )
    ),
    types.FunctionDeclaration(
        name="delete_stock",
        description="Remove a stock holding record.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "stock_id": types.Schema(type=types.Type.STRING, description="The unique ID of the stock record to delete (required)")
            },
            required=["stock_id"]
        )
    )
]


# --- Learning Module Tool Schema (Placeholder) ---
LEARNING_TOOLS = [
    types.FunctionDeclaration(
        name="create_learning_module",
        description="Create a new learning module to track progress on courses, certifications, or skill development.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "title": types.Schema(type=types.Type.STRING, description="Title of the learning module (required)"),
                "platform": types.Schema(type=types.Type.STRING, description="Platform (e.g., Coursera, Udemy, LinkedIn Learning) (optional)"),
                "description": types.Schema(type=types.Type.STRING, description="Description of what you're learning (optional)"),
                "progress": types.Schema(type=types.Type.NUMBER, description="Progress percentage (0-100) (optional)"),
                "target_completion": types.Schema(type=types.Type.STRING, description="Target completion date (optional)")
            },
            required=["title"]
        )
    ),
    types.FunctionDeclaration(
        name="read_learning_module",
        description="Retrieve details about a specific learning module.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "module_id": types.Schema(type=types.Type.STRING, description="The unique ID of the learning module (required)")
            },
            required=["module_id"]
        )
    ),
    types.FunctionDeclaration(
        name="update_learning_module",
        description="Update learning module progress and details.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "module_id": types.Schema(type=types.Type.STRING, description="The unique ID of the learning module (required)"),
                "progress": types.Schema(type=types.Type.NUMBER, description="Updated progress percentage (0-100) (optional)"),
                "notes": types.Schema(type=types.Type.STRING, description="Learning notes or achievements (optional)"),
                "status": types.Schema(type=types.Type.STRING, description="Status (in_progress, completed, paused) (optional)")
            },
            required=["module_id"]
        )
    ),
    types.FunctionDeclaration(
        name="delete_learning_module",
        description="Remove a learning module record.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "module_id": types.Schema(type=types.Type.STRING, description="The unique ID of the learning module to delete (required)")
            },
            required=["module_id"]
        )
    )
]


# --- App Settings Tool Schema (Placeholder) ---
APP_CUSTOMIZER_TOOLS = [
    types.FunctionDeclaration(
        name="update_app_settings",
        description="Update user application preferences and settings.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "theme": types.Schema(type=types.Type.STRING, description="App theme: light, dark, or auto (optional)", enum=["light", "dark", "auto"]),
                "default_view": types.Schema(type=types.Type.STRING, description="Default view when opening app (optional)", enum=["dashboard", "campaigns", "transactions", "stocks", "learning"]),
                "notifications_enabled": types.Schema(type=types.Type.BOOLEAN, description="Enable/disable notifications (optional)"),
                "currency": types.Schema(type=types.Type.STRING, description="Preferred currency (e.g., USD, EUR) (optional)"),
                "language": types.Schema(type=types.Type.STRING, description="Preferred language code (e.g., 'en', 'es', 'fr', 'de', 'zh') (optional)")
            }
        )
    ),
    types.FunctionDeclaration(
        name="get_app_settings",
        description="Retrieve current application settings and preferences.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={}
        )
    )
]

# --- Language Tools (Conversational) ---
LANGUAGE_TOOLS = [
    types.FunctionDeclaration(
        name="translate_content",
        description="Translate text content to a specified language.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "content": types.Schema(type=types.Type.STRING, description="The text content to translate (required)"),
                "target_language": types.Schema(type=types.Type.STRING, description="Target language (e.g., 'Spanish', 'French', 'German', 'Mandarin Chinese') (required)"),
                "source_language": types.Schema(type=types.Type.STRING, description="Source language (optional, default: English)")
            },
            required=["content", "target_language"]
        )
    ),
    types.FunctionDeclaration(
        name="set_language",
        description="Set the preferred language for the application and AI responses.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "language_code": types.Schema(type=types.Type.STRING, description="ISO 639-1 language code (e.g., 'en', 'es', 'fr', 'de', 'zh', 'ja', 'ko', 'ar') (required)"),
                "language_name": types.Schema(type=types.Type.STRING, description="Full language name (e.g., 'English', 'Spanish', 'French') (required)")
            },
            required=["language_code", "language_name"]
        )
    ),
    types.FunctionDeclaration(
        name="get_supported_languages",
        description="Get a list of all supported languages (65+ languages).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={}
        )
    )
]


# --- Detect Persona from User Message ---
def detect_persona(user_message: str) -> str:
    """
    Detects which persona is most relevant to the user's message.
    Returns the persona key (e.g., 'campaign_manager', 'stock_analyst').
    Defaults to a general assistant if no clear persona is detected.
    """
    message_lower = user_message.lower()
    
    # First, check for explicit persona mentions (e.g., "Hey Campaign Manager, ...")
    for persona_key, persona_data in PERSONAS.items():
        persona_name = persona_data["name"].lower()
        if persona_name in message_lower or persona_key.replace("_", " ") in message_lower:
            return persona_key
    
    # Then, check for keyword matches
    persona_scores = {persona: 0 for persona in PERSONAS.keys()}
    
    for persona_key, keywords in PERSONA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                persona_scores[persona_key] += 1
    
    # Return persona with highest score, or default
    best_persona = max(persona_scores, key=persona_scores.get)
    if persona_scores[best_persona] > 0:
        return best_persona
    
    # Default to campaign_manager if no clear match
    return "campaign_manager"


def get_persona_from_query(query: str) -> str:
    """
    Analyzes the user's query to suggest the most relevant AI persona.
    Returns a persona name string for display purposes.
    This function provides additional context for the chat method.
    """
    query = query.lower()
    
    # Check campaign-related queries
    if any(word in query for word in ["campaign", "facebook", "pinterest", "instagram", "ad", "marketing", "tiktok", "youtube", "twitter"]):
        return "Campaign Manager"
    
    # Check stock/investment-related queries
    elif any(word in query for word in ["stock", "dividend", "invest", "share", "price", "portfolio", "market", "nasdaq", "sp500", "aapl", "msft"]):
        return "Stock Market Analyst"
    
    # Check learning-related queries
    elif any(word in query for word in ["learn", "module", "progress", "lesson", "course", "skill", "education", "coursera", "udemy"]):
        return "Learning & Development Manager"
    
    # Check financial-related queries
    elif any(word in query for word in ["payout", "deposit", "withdrawal", "money", "finance", "amount", "transaction", "paypal", "bank"]):
        return "Financial Assistant"
    
    # Check app customization queries
    elif any(word in query for word in ["theme", "view", "settings", "layout", "app", "mode", "dark", "light", "customize"]):
        return "App Customizer"
    
    # Check language-related queries
    elif any(word in query for word in ["translate", "language", "speak", "english", "spanish", "french", "german", "chinese", "japanese", "korean", "arabic", "portuguese", "russian", "italian", "dutch", "swedish"]):
        return "Language Assistant"
    
    return "General Assistant"


def get_tools_for_persona(persona_key: str):
    """
    Returns the appropriate tools for a given persona.
    Combines persona-specific tools with some universal tools.
    """
    persona_tools = PERSONAS[persona_key]["tools"]
    
    # Build the tool list based on requested tools
    available_tools = {
        # Campaign tools
        "create_campaign": CAMPAIGN_TOOLS[0],
        "read_campaign": CAMPAIGN_TOOLS[1],
        "update_campaign": CAMPAIGN_TOOLS[2],
        "delete_campaign": CAMPAIGN_TOOLS[3],
        
        # Transaction tools
        "create_transaction": TRANSACTION_TOOLS[0],
        
        # PayPal tools
        "create_PayPalPayment": PAYPAL_TOOLS[0],
        "get_PayPalPaymentDetails": PAYPAL_TOOLS[1],
        "list_PayPalPayments": PAYPAL_TOOLS[2],
        "verify_PayPalPayment": PAYPAL_TOOLS[3],
        "cancel_PayPalPayment": PAYPAL_TOOLS[4],
        "get_PayPalConfig": PAYPAL_TOOLS[5],
        
        # Stock tools
        "create_stock": STOCK_TOOLS[0],
        "read_stock": STOCK_TOOLS[1],
        "update_stock": STOCK_TOOLS[2],
        "delete_stock": STOCK_TOOLS[3],
        
        # Learning tools
        "create_learning_module": LEARNING_TOOLS[0],
        "read_learning_module": LEARNING_TOOLS[1],
        "update_learning_module": LEARNING_TOOLS[2],
        "delete_learning_module": LEARNING_TOOLS[3],
        
        # App customizer tools
        "update_app_settings": APP_CUSTOMIZER_TOOLS[0],
        "get_app_settings": APP_CUSTOMIZER_TOOLS[1],
        
        # Language tools
        "translate_content": LANGUAGE_TOOLS[0],
        "set_language": LANGUAGE_TOOLS[1],
        "get_supported_languages": LANGUAGE_TOOLS[2],
    }
    
    # Filter to only persona-allowed tools
    filtered_tools = [available_tools[tool_name] for tool_name in persona_tools if tool_name in available_tools]
    return filtered_tools


# --- Function Call Handler (Updated) ---
def process_function_call(tool_name, tool_input):
    """
    Processes a function call from Gemini and returns the result.
    Routes to appropriate handler based on tool type.
    """
    api = YourActualDefaultApi()
    
    try:
        # Campaign tools
        if tool_name == "create_campaign":
            return api.create_Campaign(
                name=tool_input.get("name"),
                platform=tool_input.get("platform"),
                affiliate_link=tool_input.get("affiliate_link"),
                content=tool_input.get("content"),
                status=tool_input.get("status", "draft")
            )
        elif tool_name == "read_campaign":
            return api.read_Campaign(campaign_id=tool_input.get("campaign_id"))
        elif tool_name == "update_campaign":
            campaign_id = tool_input.pop("campaign_id", None)
            if campaign_id:
                return api.update_Campaign(campaign_id=campaign_id, **tool_input)
            return {"error": "campaign_id is required"}
        elif tool_name == "delete_campaign":
            return api.delete_Campaign(campaign_id=tool_input.get("campaign_id"))
        
        # Transaction tools
        elif tool_name == "create_transaction":
            url = f"{api.base_url}/transactions"
            payload = {k: v for k, v in tool_input.items() if v is not None}
            print(f"[Your App Backend]: Making POST request to {url} with payload: {payload}")
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                print(f"[Your App Backend]: create_transaction successful. Response: {response.json()}")
                return response.json()
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e)}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[Your App Backend]: create_transaction failed. Error: {error_details}")
                return error_details
        
        # PayPal tools
        elif tool_name == "create_PayPalPayment":
            url = f"{api.base_url}/payments"
            payload = {
                "amount": tool_input.get("amount"),
                "description": tool_input.get("description"),
                "orderId": tool_input.get("orderId")
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            print(f"[PayPal Assistant]: Creating payment with amount ${payload.get('amount')} - {payload.get('description')}")
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                print(f"[PayPal Assistant]: Payment created successfully. ID: {result.get('id')}")
                return {
                    "status": "success",
                    "message": f"PayPal payment created for ${payload.get('amount')}",
                    "payment_id": result.get('id'),
                    "amount": payload.get('amount'),
                    "description": payload.get('description'),
                    "next_step": "User should complete payment on PayPal, then verify with payment ID"
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Payment creation failed. Error: {error_details}")
                return error_details
        
        elif tool_name == "get_PayPalPaymentDetails":
            payment_id = tool_input.get("payment_id")
            url = f"{api.base_url}/payments/{payment_id}"
            print(f"[PayPal Assistant]: Retrieving payment details for ID: {payment_id}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()
                print(f"[PayPal Assistant]: Payment details retrieved. Status: {result.get('status')}")
                return {
                    "status": "success",
                    "payment_id": result.get('id'),
                    "amount": result.get('amount'),
                    "description": result.get('description'),
                    "payment_status": result.get('status'),
                    "created_at": result.get('created_at'),
                    "updated_at": result.get('updated_at')
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Failed to retrieve payment. Error: {error_details}")
                return error_details
        
        elif tool_name == "list_PayPalPayments":
            url = f"{api.base_url}/payments"
            print(f"[PayPal Assistant]: Retrieving all payments")
            try:
                response = requests.get(url)
                response.raise_for_status()
                payments = response.json()
                print(f"[PayPal Assistant]: Retrieved {len(payments) if isinstance(payments, list) else 1} payment(s)")
                return {
                    "status": "success",
                    "total_payments": len(payments) if isinstance(payments, list) else 1,
                    "payments": payments if isinstance(payments, list) else [payments]
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Failed to retrieve payments. Error: {error_details}")
                return error_details
        
        elif tool_name == "verify_PayPalPayment":
            payment_id = tool_input.get("payment_id")
            transaction_id = tool_input.get("transactionId")
            url = f"{api.base_url}/payments/{payment_id}/verify"
            payload = {"transactionId": transaction_id}
            print(f"[PayPal Assistant]: Verifying payment {payment_id} with transaction {transaction_id}")
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                print(f"[PayPal Assistant]: Payment verified successfully. Status: completed")
                return {
                    "status": "success",
                    "message": f"Payment {payment_id} verified and marked as completed",
                    "payment_id": payment_id,
                    "transaction_id": transaction_id,
                    "payment_status": "completed"
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Payment verification failed. Error: {error_details}")
                return error_details
        
        elif tool_name == "cancel_PayPalPayment":
            payment_id = tool_input.get("payment_id")
            url = f"{api.base_url}/payments/{payment_id}"
            print(f"[PayPal Assistant]: Cancelling payment {payment_id}")
            try:
                response = requests.delete(url)
                response.raise_for_status()
                print(f"[PayPal Assistant]: Payment cancelled successfully")
                return {
                    "status": "success",
                    "message": f"Payment {payment_id} has been cancelled",
                    "payment_id": payment_id,
                    "payment_status": "cancelled"
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Payment cancellation failed. Error: {error_details}")
                return error_details
        
        elif tool_name == "get_PayPalConfig":
            url = f"{api.base_url}/paypal-config"
            print(f"[PayPal Assistant]: Retrieving PayPal configuration")
            try:
                response = requests.get(url)
                response.raise_for_status()
                config = response.json()
                print(f"[PayPal Assistant]: Config retrieved. PayPal email: {config.get('email', 'Not set')}")
                return {
                    "status": "success",
                    "paypal_email": config.get('email'),
                    "message": f"Payments should be sent to: {config.get('email')}"
                }
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e), "status": "failed"}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[PayPal Assistant]: Failed to retrieve config. Error: {error_details}")
                return error_details
        
        # Stock tools (placeholder - return simulated response)
        elif tool_name in ["create_stock", "read_stock", "update_stock", "delete_stock"]:
            print(f"[Stock Tool]: {tool_name} called with input: {tool_input}")
            return {
                "status": "success",
                "message": f"Stock operation '{tool_name}' executed. (Placeholder - ready for Supabase integration)",
                "data": tool_input
            }
        
        # Learning tools (placeholder - return simulated response)
        elif tool_name in ["create_learning_module", "read_learning_module", "update_learning_module", "delete_learning_module"]:
            print(f"[Learning Tool]: {tool_name} called with input: {tool_input}")
            return {
                "status": "success",
                "message": f"Learning module operation '{tool_name}' executed. (Placeholder - ready for Supabase integration)",
                "data": tool_input
            }
        
        # App customizer tools (placeholder - return simulated response)
        elif tool_name in ["update_app_settings", "get_app_settings"]:
            print(f"[App Customizer]: {tool_name} called with input: {tool_input}")
            if tool_name == "get_app_settings":
                return {
                    "status": "success",
                    "settings": {
                        "theme": "dark",
                        "default_view": "dashboard",
                        "notifications_enabled": True,
                        "currency": "USD",
                        "language": "en"
                    }
                }
            else:
                return {
                    "status": "success",
                    "message": "Settings updated successfully",
                    "updated_settings": tool_input
                }
        
        # Language tools (placeholder - return simulated response)
        elif tool_name in ["translate_content", "set_language", "get_supported_languages"]:
            print(f"[Language Assistant]: {tool_name} called with input: {tool_input}")
            if tool_name == "translate_content":
                return {
                    "status": "success",
                    "message": f"Content translated to {tool_input.get('target_language')}",
                    "original": tool_input.get('content'),
                    "translated": f"[Translated to {tool_input.get('target_language')}]"
                }
            elif tool_name == "set_language":
                return {
                    "status": "success",
                    "message": f"Language set to {tool_input.get('language_name')} ({tool_input.get('language_code')})",
                    "language_code": tool_input.get('language_code')
                }
            elif tool_name == "get_supported_languages":
                return {
                    "status": "success",
                    "total_languages": 65,
                    "languages": [
                        {"code": "en", "name": "English"},
                        {"code": "es", "name": "Spanish"},
                        {"code": "fr", "name": "French"},
                        {"code": "de", "name": "German"},
                        {"code": "it", "name": "Italian"},
                        {"code": "pt", "name": "Portuguese"},
                        {"code": "nl", "name": "Dutch"},
                        {"code": "pl", "name": "Polish"},
                        {"code": "ru", "name": "Russian"},
                        {"code": "ja", "name": "Japanese"},
                        {"code": "zh", "name": "Mandarin Chinese"},
                        {"code": "ko", "name": "Korean"},
                        {"code": "ar", "name": "Arabic"},
                        {"code": "hi", "name": "Hindi"},
                        {"code": "th", "name": "Thai"},
                        {"code": "vi", "name": "Vietnamese"},
                        {"code": "id", "name": "Indonesian"},
                        {"code": "tr", "name": "Turkish"},
                        {"code": "sv", "name": "Swedish"},
                        {"code": "da", "name": "Danish"},
                        # ... 45+ more languages
                    ]
                }
        
        else:
            return {"error": f"Unknown function: {tool_name}"}
    except Exception as e:
        return {"error": str(e)}


# --- System Instruction for Multi-Persona ---
SYSTEM_INSTRUCTION = (
    "You are Affiliate AI Pro, a suite of specialized AI Executive Assistants. "
    "Your main goal is to help the user manage their affiliate marketing business, finances, investments, learning, and communications. "
    "You have access to several executive personas, each with specific tools and expertise:\n"
    "- **Campaign Manager:** Manages marketing campaigns (create, read, update, delete campaigns; optimize content and platforms).\n"
    "- **Stock Market Analyst:** Tracks stock investments and dividends (create, read, update, delete stocks; log stock-related transactions).\n"
    "- **Learning & Development Manager:** Helps track learning modules (create, read, update, complete learning modules).\n"
    "- **Financial Assistant:** Logs all financial transactions (deposits, withdrawals, affiliate payouts, stock purchases/sales, dividends) and manages PayPal payments (create payments, verify transactions, manage payment status).\n"
    "- **App Customizer:** Manages user application preferences and settings (e.g., theme, default view, dashboard layout, notifications, currency).\n"
    "- **Language Assistant:** Provides translation and content generation in a wide range of languages (over 65), including but not limited to English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Portuguese, Russian, Italian, Dutch, Swedish, Hindi, Thai, Vietnamese, Indonesian, Turkish, and many more.\n\n"
    "Respond in the persona most relevant to the user's request. Always be helpful, encouraging, educational, and provide actionable advice. "
    "When using tools, clearly indicate what action you are taking. "
    "If the user explicitly mentions a persona name, prioritize that persona. "
    "Otherwise, infer the best persona based on the keywords and intent in the user's message. "
    "When handling PayPal payments, be prepared to create payment records, verify completed transactions, check payment status, and provide PayPal configuration details."
)


# --- Function Call Handler ---
def process_function_call(tool_name, tool_input):
    """
    Processes a function call from Gemini and returns the result.
    Routes to appropriate handler based on tool type.
    """
    api = YourActualDefaultApi()
    
    try:
        # Campaign tools
        if tool_name == "create_campaign":
            return api.create_Campaign(
                name=tool_input.get("name"),
                platform=tool_input.get("platform"),
                affiliate_link=tool_input.get("affiliate_link"),
                content=tool_input.get("content"),
                status=tool_input.get("status", "draft")
            )
        elif tool_name == "read_campaign":
            return api.read_Campaign(campaign_id=tool_input.get("campaign_id"))
        elif tool_name == "update_campaign":
            campaign_id = tool_input.pop("campaign_id")
            return api.update_Campaign(campaign_id=campaign_id, **tool_input)
        elif tool_name == "delete_campaign":
            return api.delete_Campaign(campaign_id=tool_input.get("campaign_id"))
        elif tool_name == "create_transaction":
            # Log transaction to Node.js backend
            url = f"{api.base_url}/transactions"
            payload = {k: v for k, v in tool_input.items() if v is not None}
            print(f"[Your App Backend]: Making POST request to {url} with payload: {payload}")
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                print(f"[Your App Backend]: create_transaction successful. Response: {response.json()}")
                return response.json()
            except requests.exceptions.RequestException as e:
                error_details = {"error": str(e)}
                if 'response' in locals():
                    try:
                        error_details["details"] = response.json()
                    except json.JSONDecodeError:
                        error_details["details"] = response.text
                print(f"[Your App Backend]: create_transaction failed. Error: {error_details}")
                return error_details
        else:
            return {"error": f"Unknown function: {tool_name}"}
    except Exception as e:
        return {"error": str(e)}


# --- Gemini AI Integration ---
class AffiliateAIExecutive:
    """
    This is your AI Executive Assistant powered by Gemini.
    It understands natural language and executes commands against your backend.
    """
    
    def __init__(self):
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set!")
        
        self.client = genai.Client(api_key=API_KEY)
        self.conversation_history = []
        self.api = YourActualDefaultApi()
    
    def chat(self, user_message: str) -> str:
        """Chat with the AI Executive Assistant using natural language and proper function calling."""
        print(f"\n[You]: {user_message}")
        
        # Detect which persona this message is for
        detected_persona = detect_persona(user_message)
        persona_data = PERSONAS[detected_persona]
        print(f"\n[Assistant Detected]: {persona_data['name']} 🎯")
        
        # Get tools available to this persona
        persona_tools = get_tools_for_persona(detected_persona)
        
        # Add user message to history
        self.conversation_history.append(types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        ))
        
        # Keep looping until we get a final text response (not a function call)
        while True:
            try:
                # Get response from Gemini with persona-specific tools and system instruction
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=self.conversation_history,
                    system_instruction=SYSTEM_INSTRUCTION,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(functionDeclarations=persona_tools)]
                    )
                )
                
                # Check for empty response
                if not response.candidates or not response.candidates[0].content.parts:
                    final_response = "Operation completed."
                    self.conversation_history.append(types.Content(
                        role="assistant",
                        parts=[types.Part(text=final_response)]
                    ))
                    print(f"\n[AI]: {final_response}")
                    return final_response
                
                # Get the response content
                response_content = response.candidates[0].content
                
                # Check if this is a function call
                has_function_call = False
                function_calls_made = []
                
                for part in response_content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_call = True
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = {k: v for k, v in function_call.args.items()}
                        
                        print(f"\n[{persona_data['name']} Tool Call]: {function_name}({function_args})")
                        
                        # Execute the function
                        try:
                            tool_output = process_function_call(function_name, function_args)
                            print(f"[Tool Output]: {tool_output}")
                            function_calls_made.append({
                                'function_call': part.function_call,
                                'result': tool_output
                            })
                        except Exception as e:
                            error_output = {"error": f"Failed to execute {function_name}: {str(e)}"}
                            print(f"[Tool Error]: {error_output}")
                            function_calls_made.append({
                                'function_call': part.function_call,
                                'result': error_output
                            })
                    
                    elif hasattr(part, 'text') and part.text:
                        # This is a text response
                        pass
                
                # If we had function calls, add the response to history and include tool results
                if has_function_call:
                    # Add the assistant's response (with function calls) to history
                    self.conversation_history.append(response_content)
                    
                    # Add function results as tool responses
                    for call_result in function_calls_made:
                        self.conversation_history.append(types.Content(
                            role="user",
                            parts=[types.Part(
                                function_response=types.FunctionResponse(
                                    name=call_result['function_call'].name,
                                    response=call_result['result']
                                )
                            )]
                        ))
                    
                    # Continue the loop to get Gemini's next response (should be text summary)
                    continue
                
                else:
                    # No function call, just text response - this is our final answer
                    final_response = ""
                    for part in response_content.parts:
                        if hasattr(part, 'text'):
                            final_response += part.text
                    
                    final_response = final_response.strip()
                    if not final_response:
                        final_response = "Operation completed."
                    
                    print(f"\n[AI]: {final_response}")
                    
                    # Add to history
                    self.conversation_history.append(response_content)
                    
                    return final_response
                
            except Exception as e:
                error_msg = f"Error during chat: {e}"
                print(f"[Error]: {error_msg}")
                import traceback
                traceback.print_exc()
                return error_msg


if __name__ == "__main__":
    # Check if API key is set
    if not API_KEY:
        print("[ERROR] GOOGLE_API_KEY environment variable is not set!")
        print("\nTo use Gemini integration, please set your API key:")
        print("  Windows (PowerShell): $env:GOOGLE_API_KEY='your-api-key-here'")
        print("  Windows (CMD): set GOOGLE_API_KEY=your-api-key-here")
        print("\nGet your free API key from: https://makersuite.google.com/app/apikey")
        exit(1)
    
    # Initialize the AI Executive
    print("[*] Initializing Affiliate AI Pro Executive Assistant...")
    assistant = AffiliateAIExecutive()
    
    print("\n" + "="*70)
    print("Welcome to Affiliate AI Pro - Multi-Persona Executive Assistant!")
    print("="*70)
    print("\nYou have access to 6 specialized AI personas:\n")
    print("  🎯 Campaign Manager - Manage marketing campaigns across platforms")
    print("  📈 Stock Market Analyst - Track investments, stocks, and dividends")
    print("  🎓 Learning Manager - Track courses and skill development")
    print("  💰 Financial Assistant - Log all financial transactions")
    print("  ⚙️  App Customizer - Customize your application settings")
    print("  🌍 Language Assistant - Translate & support 65+ languages\n")
    print("Examples of how to interact:")
    print("  - 'Create a new Instagram campaign called Summer Sale'")
    print("  - 'Hey Stock Analyst, log my Apple stock purchase: 10 shares at $150'")
    print("  - 'Learning Manager, update my AI Tools course to 50% progress'")
    print("  - 'Log an affiliate payout of $500 via PayPal'")
    print("  - 'Set my theme to dark mode'")
    print("  - 'Language Assistant, translate this to Spanish: Hello world!'\n")
    print("Type 'exit' to quit.")
    print("="*70 + "\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("[You]: ").strip()
            if user_input.lower() == 'exit':
                print("\n[Goodbye] Thanks for using Affiliate AI Pro!")
                break
            if not user_input:
                continue
            
            # Chat with the AI
            assistant.chat(user_input)
        except KeyboardInterrupt:
            print("\n\n[Goodbye] Thanks for using Affiliate AI Pro!")
            break
        except Exception as e:
            print(f"[Error]: {e}")
