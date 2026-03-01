"""
Supabase Client Configuration for Python AI Service
This module provides database access and authentication helpers for the AI service
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[WARNING] Supabase credentials not found in environment variables")
    print("Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
    supabase_client: Client = None
else:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseManager:
    """Manager class for all Supabase operations"""
    
    def __init__(self, client: Client = None):
        self.client = client or supabase_client
    
    def create_campaign(self, user_id: str, campaign_data: dict) -> dict:
        """Create a new campaign for a user"""
        try:
            campaign_data['user_id'] = user_id
            response = self.client.table('campaigns').insert(campaign_data).execute()
            return response.data[0] if response.data else {"error": "Failed to create campaign"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_campaigns(self, user_id: str) -> list:
        """Get all campaigns for a specific user"""
        try:
            response = self.client.table('campaigns').select('*').eq('user_id', user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[Supabase Error]: {e}")
            return []
    
    def get_campaign(self, user_id: str, campaign_id: str) -> dict:
        """Get a specific campaign for a user"""
        try:
            response = self.client.table('campaigns').select('*').eq('user_id', user_id).eq('id', campaign_id).single().execute()
            return response.data if response.data else {"error": "Campaign not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def update_campaign(self, user_id: str, campaign_id: str, updates: dict) -> dict:
        """Update a campaign"""
        try:
            response = self.client.table('campaigns').update(updates).eq('user_id', user_id).eq('id', campaign_id).execute()
            return response.data[0] if response.data else {"error": "Failed to update campaign"}
        except Exception as e:
            return {"error": str(e)}
    
    def delete_campaign(self, user_id: str, campaign_id: str) -> dict:
        """Delete a campaign"""
        try:
            response = self.client.table('campaigns').delete().eq('user_id', user_id).eq('id', campaign_id).execute()
            return {"success": True, "message": "Campaign deleted"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_transaction(self, user_id: str, transaction_data: dict) -> dict:
        """Create a new transaction for a user"""
        try:
            transaction_data['user_id'] = user_id
            response = self.client.table('transactions').insert(transaction_data).execute()
            return response.data[0] if response.data else {"error": "Failed to create transaction"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_transactions(self, user_id: str, limit: int = 50) -> list:
        """Get all transactions for a specific user"""
        try:
            response = (self.client.table('transactions')
                       .select('*')
                       .eq('user_id', user_id)
                       .order('created_at', desc=True)
                       .limit(limit)
                       .execute())
            return response.data if response.data else []
        except Exception as e:
            print(f"[Supabase Error]: {e}")
            return []
    
    def create_stock(self, user_id: str, stock_data: dict) -> dict:
        """Create a new stock entry for a user"""
        try:
            stock_data['user_id'] = user_id
            response = self.client.table('stocks').insert(stock_data).execute()
            return response.data[0] if response.data else {"error": "Failed to create stock"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_stocks(self, user_id: str) -> list:
        """Get all stocks for a specific user"""
        try:
            response = self.client.table('stocks').select('*').eq('user_id', user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[Supabase Error]: {e}")
            return []
    
    def create_learning_module(self, user_id: str, module_data: dict) -> dict:
        """Create a new learning module for a user"""
        try:
            module_data['user_id'] = user_id
            response = self.client.table('learning_modules').insert(module_data).execute()
            return response.data[0] if response.data else {"error": "Failed to create learning module"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_learning_modules(self, user_id: str) -> list:
        """Get all learning modules for a specific user"""
        try:
            response = self.client.table('learning_modules').select('*').eq('user_id', user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[Supabase Error]: {e}")
            return []
    
    def get_user_preferences(self, user_id: str) -> dict:
        """Get user preferences"""
        try:
            response = self.client.table('user_preferences').select('*').eq('user_id', user_id).single().execute()
            if response.data:
                return response.data
            # Return defaults if not found
            return {
                'user_id': user_id,
                'theme': 'dark',
                'default_view': 'dashboard',
                'notifications_enabled': True,
                'currency': 'USD',
                'language': 'en'
            }
        except Exception as e:
            print(f"[Supabase Error]: {e}")
            return None
    
    def save_user_preferences(self, user_id: str, preferences: dict) -> dict:
        """Save user preferences"""
        try:
            preferences['user_id'] = user_id
            response = self.client.table('user_preferences').upsert(preferences).execute()
            return response.data[0] if response.data else {"error": "Failed to save preferences"}
        except Exception as e:
            return {"error": str(e)}


# Global instance
db = SupabaseManager(supabase_client)
