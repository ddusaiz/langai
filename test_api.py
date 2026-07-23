"""
Quick test script to verify your Gemini API key
Run this to diagnose the issue: python3 test_api.py
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

print("=" * 60)
print("GEMINI API KEY TEST")
print("=" * 60)
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key starts with: {api_key[:10] if api_key else 'N/A'}...")
print(f"API Key length: {len(api_key) if api_key else 0}")
print("=" * 60)

if not api_key:
    print("\n❌ ERROR: No API key found in .env file")
    print("\n📝 Please add to .env file:")
    print("GEMINI_API_KEY=your-actual-key-here")
    exit(1)

print("\n🔍 Testing API connection...")

try:
    client = genai.Client(api_key=api_key)
    print("✅ Client created successfully")
    
    print("\n🔍 Attempting to list available models...")
    models = client.models.list()
    print(f"✅ Successfully connected! Found {len(list(models))} models")
    
    print("\n📋 Available models:")
    for model in client.models.list():
        print(f"  - {model.name}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n" + "=" * 60)
    print("DIAGNOSIS:")
    print("=" * 60)
    
    if "404" in str(e) or "NOT_FOUND" in str(e):
        print("❌ Your API key is NOT valid for Gemini API")
        print("\n🔑 Your key format suggests it's from a different service.")
        print("\n✅ TO FIX:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Click 'Create API key' or 'Get API key'")
        print("3. Copy the NEW key (should start with 'AIza...')")
        print("4. Replace the key in your .env file")
        print("\n⚠️  Make sure you're getting a 'Gemini API key'")
        print("   NOT a Google Cloud API key or Vertex AI key")
    elif "401" in str(e) or "UNAUTHENTICATED" in str(e):
        print("❌ Authentication failed - key may be invalid or expired")
        print("\n✅ Get a new key from: https://aistudio.google.com/app/apikey")
    else:
        print(f"❌ Unexpected error: {e}")
    
    print("=" * 60)
