import time
import requests

# Give server a moment to be ready
time.sleep(1)

print("Testing connection to http://localhost:3001/api/health...")
try:
    response = requests.get("http://localhost:3001/api/health")
    print(f"✅ Server is running! Response: {response.json()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Now test creating a campaign
print("\nCreating a test campaign...")
payload = {
    "name": "Test Campaign",
    "platform": "Instagram",
    "affiliate_link": "https://example.com/ref",
    "content": "Check out this amazing product!"
}

try:
    response = requests.post("http://localhost:3001/api/campaigns", json=payload)
    campaign = response.json()
    print(f"✅ Campaign created! ID: {campaign.get('id')}")
    print(f"Campaign: {campaign}")
except Exception as e:
    print(f"❌ Failed to create campaign: {e}")
