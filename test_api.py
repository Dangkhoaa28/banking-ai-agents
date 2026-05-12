"""
Simple test script to test the Banking AI-Agent API.
Run this after starting the server with: python run.py
"""
import json
import time
import requests
from pathlib import Path

API_URL = "http://localhost:8000"
SAMPLE_REQUESTS_FILE = "examples/sample_requests.json"

def load_sample_requests():
    """Load sample requests from JSON file."""
    try:
        with open(SAMPLE_REQUESTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Sample requests file not found: {SAMPLE_REQUESTS_FILE}")
        return []

def health_check():
    """Check if API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("   Make sure to run: python run.py")
        return False

def test_request(message, customer_id, test_num=None):
    """Send a test request to the API."""
    print("\n" + "="*70)
    if test_num:
        print(f"TEST {test_num}")
    print("="*70)
    print(f"📩 Customer ID: {customer_id}")
    print(f"💬 Message: {message}")
    print("-"*70)
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/api/chat",
            json={"message": message, "customer_id": customer_id},
            timeout=300
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract trace info
            trace = data.get("trace", {})
            
            # Print response
            print(f"\n✅ Response received in {elapsed:.2f}s")
            print(f"\n📤 Final Reply:")
            print(f"   {data['final_reply']}")
            
            print(f"\n🚦 Escalation Status: {'YES ⚠️' if data['escalate'] else 'NO ✅'}")
            
            # Print trace details
            print(f"\n📊 Analysis Trace:")
            print(f"   Intent: {trace.get('intent', 'N/A')} (confidence: {trace.get('intent_confidence', 0):.2%})")
            print(f"   Priority: {trace.get('priority', 'N/A')} (confidence: {trace.get('priority_confidence', 0):.2%})")
            print(f"   Validation: {trace.get('validation_status', 'N/A')} (confidence: {trace.get('validation_confidence', 0):.2%})")
            print(f"   Validation Issues: {', '.join(trace.get('validation_issues', [])) if trace.get('validation_issues') else 'None'}")
            print(f"   Routing Decision: {trace.get('routing_decision', 'N/A')}")
            print(f"   Processing Time: {trace.get('processing_time_ms', 0):.2f}ms")
            
            if trace.get('error_details'):
                print(f"\n⚠️  Errors: {trace['error_details']}")
            
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after 30 seconds")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*70)
    print("🚀 Banking AI-Agent API Test Suite")
    print("="*70)
    
    # Check API health
    print("\n🔍 Checking API health...")
    if not health_check():
        return
    
    # Load and run sample tests
    print(f"\n📂 Loading sample requests from: {SAMPLE_REQUESTS_FILE}")
    samples = load_sample_requests()
    
    if not samples:
        print("❌ No sample requests loaded. Using custom example.")
        samples = [
            {
                "message": "I can't log in, my account says it is blocked.",
                "customer_id": "CUST_004"
            }
        ]
    
    print(f"📝 Found {len(samples)} sample requests\n")
    
    # Run tests
    passed = 0
    for i, request in enumerate(samples, 1):
        if test_request(
            message=request["message"],
            customer_id=request["customer_id"],
            test_num=i
        ):
            passed += 1
        
        # Small delay between requests
        if i < len(samples):
            time.sleep(1)
    
    # Summary
    print("\n" + "="*70)
    print(f"📊 Test Summary: {passed}/{len(samples)} tests passed")
    print("="*70)
    
    if passed == len(samples):
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {len(samples) - passed} test(s) failed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
