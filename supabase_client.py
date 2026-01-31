"""
Affiliate AI Pro - Python Supabase Client
Handles database operations from the Python AI service
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class CampaignDB:
    """Campaign database operations"""
    
    @staticmethod
    def create(user_id: str, campaign_data: dict) -> dict:
        """Create a new campaign"""
        try:
            response = supabase.table("campaigns").insert({
                "user_id": user_id,
                "name": campaign_data.get("name"),
                "platform": campaign_data.get("platform"),
                "affiliate_link": campaign_data.get("affiliate_link"),
                "content": campaign_data.get("content"),
                "status": campaign_data.get("status", "draft"),
                "clicks": campaign_data.get("clicks", 0),
                "conversions": campaign_data.get("conversions", 0),
                "earnings": campaign_data.get("earnings", 0),
                "image_url": campaign_data.get("image_url"),
                "scheduled_date": campaign_data.get("scheduled_date"),
                "tags": campaign_data.get("tags", []),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get(user_id: str, campaign_id: str) -> dict:
        """Get a specific campaign"""
        try:
            response = supabase.table("campaigns").select("*").eq(
                "id", campaign_id
            ).eq("user_id", user_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_all(user_id: str) -> list:
        """Get all campaigns for a user"""
        try:
            response = supabase.table("campaigns").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            return []

    @staticmethod
    def update(user_id: str, campaign_id: str, updates: dict) -> dict:
        """Update a campaign"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = supabase.table("campaigns").update(updates).eq(
                "id", campaign_id
            ).eq("user_id", user_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete(user_id: str, campaign_id: str) -> dict:
        """Delete a campaign"""
        try:
            supabase.table("campaigns").delete().eq(
                "id", campaign_id
            ).eq("user_id", user_id).execute()
            return {"success": True, "message": "Campaign deleted"}
        except Exception as e:
            return {"error": str(e)}


class TransactionDB:
    """Transaction database operations"""
    
    @staticmethod
    def create(user_id: str, transaction_data: dict) -> dict:
        """Create a new transaction"""
        try:
            response = supabase.table("transactions").insert({
                "user_id": user_id,
                "amount": transaction_data.get("amount"),
                "type": transaction_data.get("type"),
                "description": transaction_data.get("description", ""),
                "payment_method": transaction_data.get("payment_method"),
                "status": transaction_data.get("status", "completed"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_all(user_id: str) -> list:
        """Get all transactions for a user"""
        try:
            response = supabase.table("transactions").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            return []

    @staticmethod
    def get_summary(user_id: str) -> dict:
        """Get transaction summary"""
        try:
            transactions = TransactionDB.get_all(user_id)
            summary = {
                "total_earnings": 0,
                "total_expenses": 0,
                "by_type": {}
            }
            
            for txn in transactions:
                txn_type = txn.get("type")
                amount = txn.get("amount", 0)
                
                summary["by_type"][txn_type] = summary["by_type"].get(txn_type, 0) + amount
                
                if txn_type in ["affiliate_payout", "dividend", "deposit"]:
                    summary["total_earnings"] += amount
                else:
                    summary["total_expenses"] += amount
            
            return summary
        except Exception as e:
            return {"error": str(e)}


class StockDB:
    """Stock database operations"""
    
    @staticmethod
    def create(user_id: str, stock_data: dict) -> dict:
        """Create a stock record"""
        try:
            response = supabase.table("stocks").insert({
                "user_id": user_id,
                "ticker": stock_data.get("ticker"),
                "shares": stock_data.get("shares"),
                "purchase_price": stock_data.get("purchase_price"),
                "current_price": stock_data.get("current_price", stock_data.get("purchase_price")),
                "purchase_date": stock_data.get("purchase_date", datetime.now().isoformat()),
                "broker": stock_data.get("broker", "unknown"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_all(user_id: str) -> list:
        """Get all stocks for a user"""
        try:
            response = supabase.table("stocks").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            return []

    @staticmethod
    def update(user_id: str, stock_id: str, updates: dict) -> dict:
        """Update a stock record"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = supabase.table("stocks").update(updates).eq(
                "id", stock_id
            ).eq("user_id", user_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}


class LearningDB:
    """Learning module database operations"""
    
    @staticmethod
    def create(user_id: str, module_data: dict) -> dict:
        """Create a learning module"""
        try:
            response = supabase.table("learning_modules").insert({
                "user_id": user_id,
                "title": module_data.get("title"),
                "platform": module_data.get("platform", "custom"),
                "description": module_data.get("description", ""),
                "progress": module_data.get("progress", 0),
                "target_completion": module_data.get("target_completion"),
                "status": module_data.get("status", "in_progress"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_all(user_id: str) -> list:
        """Get all learning modules for a user"""
        try:
            response = supabase.table("learning_modules").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            return []

    @staticmethod
    def update(user_id: str, module_id: str, updates: dict) -> dict:
        """Update a learning module"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = supabase.table("learning_modules").update(updates).eq(
                "id", module_id
            ).eq("user_id", user_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}


class PreferencesDB:
    """User preferences database operations"""
    
    @staticmethod
    def get(user_id: str) -> dict:
        """Get user preferences"""
        try:
            response = supabase.table("user_preferences").select("*").eq(
                "user_id", user_id
            ).execute()
            
            if response.data:
                return response.data[0]
            else:
                # Return defaults if no preferences exist
                return {
                    "user_id": user_id,
                    "theme": "dark",
                    "language": "en",
                    "currency": "USD",
                    "notifications_enabled": True,
                    "default_view": "dashboard",
                }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update(user_id: str, preferences: dict) -> dict:
        """Update user preferences"""
        try:
            preferences["user_id"] = user_id
            preferences["updated_at"] = datetime.now().isoformat()
            
            response = supabase.table("user_preferences").upsert(
                preferences
            ).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            return {"error": str(e)}


# Export classes for easy access
__all__ = [
    'supabase',
    'CampaignDB',
    'TransactionDB',
    'StockDB',
    'LearningDB',
    'PreferencesDB',
]
