#!/usr/bin/env python3
"""
Quick startup script for Affiliate AI Pro
Sets environment and runs the interactive assistant
"""
import os
import sys

# Set API key
api_key = 'AIzaSyBpPjvvrVwVXr9MRC5lv3ZqoxbXetnLS3E'
os.environ['GOOGLE_API_KEY'] = api_key

print("=" * 70)
print("  AFFILIATE AI PRO - STARTUP")
print("=" * 70)
print(f"\n✓ API Key loaded: {len(api_key)} characters")
print(f"✓ Python interpreter: {sys.executable}")

# Now import and run ai_service
try:
    from ai_service import AffiliateAIExecutive
    
    print("\n✓ Modules imported successfully")
    print("\n" + "=" * 70)
    print("  Initializing AI Executive Assistant...")
    print("=" * 70)
    
    # Create assistant
    assistant = AffiliateAIExecutive()
    
    print("\n" + "=" * 70)
    print("Welcome to Affiliate AI Pro!")
    print("I'm your AI Executive Assistant. Type your commands naturally.")
    print("\nExamples:")
    print("  - 'Create a new Instagram campaign called Summer Sale'")
    print("  - 'Show me the campaign with ID: 123456'")
    print("  - 'Update my campaign to active status'")
    print("  - 'Delete the campaign with ID: 123456'")
    print("\nType 'exit' to quit.")
    print("=" * 70 + "\n")
    
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
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"\n✗ Failed to start: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
