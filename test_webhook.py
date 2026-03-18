import httpx
import asyncio

async def test_webhook():
    print("Testing /webhook endpoint...")
    async with httpx.AsyncClient() as client:
        # Simulate Twilio x-www-form-urlencoded payload
        data = {
            "From": "whatsapp:+1234567890",
            "Body": "Is this news true?",
            "NumMedia": "0"
        }
        try:
            response = await client.post("http://localhost:10000/webhook", data=data)
            print(f"Status: {response.status_code}")
            print(f"Headers: {response.headers.get('content-type')}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200 and "<Response></Response>" in response.text:
                print("✅ Webhook test passed!")
            else:
                print("❌ Webhook test failed!")
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_webhook())
