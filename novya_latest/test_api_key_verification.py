#!/usr/bin/env python
"""
API Key Verification Test
Tests if the new API key is working properly
"""
import requests
import time

def test_api_key():
    """Test if the API key is working"""
    
    print("🔑 API KEY VERIFICATION TEST")
    print("=" * 50)
    
    # Wait a moment for servers to start
    print("⏳ Waiting for servers to start...")
    time.sleep(5)
    
    # Test AI Backend
    print("\n1️⃣ Testing AI Backend Connection...")
    try:
        # Test a simple quiz generation
        test_url = "http://localhost:8000/quiz?subtopic=Multiplication%20of%20integers&currentLevel=1&language=English"
        response = requests.get(test_url, timeout=15)
        
        if response.status_code == 200:
            quiz_data = response.json()
            questions = quiz_data.get('quiz', [])
            
            print(f"   ✅ AI Backend Response: HTTP {response.status_code}")
            print(f"   📊 Questions Generated: {len(questions)}")
            
            if len(questions) >= 3:
                # Check first 3 questions for real content
                print(f"\n   📝 Sample Questions:")
                for i, q in enumerate(questions[:3]):
                    question_text = q.get('question', '')
                    options = q.get('options', [])
                    
                    print(f"      Q{i+1}: {question_text[:80]}...")
                    print(f"         Options: {options}")
                    
                    # Check if options are real content (not generic)
                    generic_patterns = ['Process A', 'Process B', 'Process C', 'Type 1', 'Type 2', 'Characteristic 1']
                    is_generic = any(pattern in str(options) for pattern in generic_patterns)
                    
                    if is_generic:
                        print(f"         ⚠️ Still using generic options (API might not be working)")
                    else:
                        print(f"         ✅ Real content detected!")
                
                # Check if we're getting real AI content
                source = quiz_data.get('source', 'unknown')
                if source == 'ai':
                    print(f"\n   🎉 SUCCESS: Real AI-generated content!")
                    print(f"   📈 Source: {source}")
                else:
                    print(f"\n   ⚠️ Still using fallback content")
                    print(f"   📈 Source: {source}")
                    
            else:
                print(f"   ❌ Not enough questions generated")
                
        else:
            print(f"   ❌ AI Backend Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ AI Backend Connection Error: {e}")
    
    # Test Django Backend
    print(f"\n2️⃣ Testing Django Backend Connection...")
    try:
        django_url = "http://localhost:8001/api/"
        response = requests.get(django_url, timeout=5)
        
        if response.status_code in [200, 404]:  # 404 is fine for root API
            print(f"   ✅ Django Backend: CONNECTED")
        else:
            print(f"   ⚠️ Django Backend Response: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Django Backend Error: {e}")
    
    print(f"\n🎯 VERIFICATION COMPLETE!")
    print("=" * 50)
    print("\n📋 NEXT STEPS:")
    print("1. If you see 'Real AI-generated content!' - API key is working! 🎉")
    print("2. If you see 'Still using fallback content' - API key needs verification")
    print("3. Test a quiz in your frontend to see the difference")
    print("4. Look for real educational content instead of 'Process A, B, C'")

if __name__ == "__main__":
    test_api_key()
