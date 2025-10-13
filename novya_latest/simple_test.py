import requests
import time

print("🔑 Testing API Key...")
time.sleep(3)  # Wait for server to start

try:
    response = requests.get("http://localhost:8000/quiz?subtopic=Multiplication%20of%20integers&currentLevel=1&language=English", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        source = data.get('source', 'unknown')
        questions = data.get('quiz', [])
        
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Source: {source}")
        print(f"📝 Questions: {len(questions)}")
        
        if len(questions) > 0:
            first_q = questions[0]
            print(f"🎯 First Question: {first_q.get('question', '')[:60]}...")
            print(f"📋 Options: {first_q.get('options', [])}")
            
            # Check for generic patterns
            options_text = str(first_q.get('options', []))
            if 'Process A' in options_text or 'Type 1' in options_text:
                print("⚠️ Still using FALLBACK (generic options)")
            else:
                print("🎉 SUCCESS! Using REAL AI content!")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
