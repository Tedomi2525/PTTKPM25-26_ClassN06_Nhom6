"""
Script to test and analyze login performance
"""
import time
import requests
import json
from statistics import mean, median

def test_login_performance(username="SV25000002", password="SV25000002@", num_tests=10):
    """Test login performance multiple times"""
    
    url = "http://127.0.0.1:8000/auth/login"
    me_url = "http://127.0.0.1:8000/auth/me"
    
    login_times = []
    me_times = []
    total_times = []
    
    print(f"🔄 Testing login performance {num_tests} times...")
    print("=" * 60)
    
    for i in range(num_tests):
        # Test login
        start_time = time.time()
        try:
            response = requests.post(url, json={"username": username, "password": password})
            login_end = time.time()
            login_time = (login_end - start_time) * 1000  # convert to ms
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("accessToken") or data.get("access_token")
                
                # Test /auth/me
                me_start = time.time()
                me_response = requests.get(me_url, headers={"Authorization": f"Bearer {token}"})
                me_end = time.time()
                me_time = (me_end - me_start) * 1000
                
                total_time = login_time + me_time
                
                login_times.append(login_time)
                me_times.append(me_time)
                total_times.append(total_time)
                
                print(f"Test {i+1:2d}: Login={login_time:6.1f}ms | /me={me_time:5.1f}ms | Total={total_time:6.1f}ms")
            else:
                print(f"Test {i+1:2d}: ❌ Login failed - {response.status_code}")
                
        except Exception as e:
            print(f"Test {i+1:2d}: ❌ Error - {e}")
    
    if login_times:
        print("=" * 60)
        print("📊 Performance Summary:")
        print(f"   Login API:")
        print(f"     Average: {mean(login_times):6.1f}ms")
        print(f"     Median:  {median(login_times):6.1f}ms")
        print(f"     Min:     {min(login_times):6.1f}ms")
        print(f"     Max:     {max(login_times):6.1f}ms")
        
        print(f"   /auth/me API:")
        print(f"     Average: {mean(me_times):6.1f}ms")
        print(f"     Median:  {median(me_times):6.1f}ms")
        
        print(f"   Total Flow:")
        print(f"     Average: {mean(total_times):6.1f}ms")
        print(f"     Median:  {median(total_times):6.1f}ms")
        
        avg_total = mean(total_times)
        if avg_total > 1000:
            print(f"⚠️  WARNING: Login flow is slow (>{avg_total:.0f}ms)")
        elif avg_total > 500:
            print(f"🐌 SLOW: Login flow could be faster ({avg_total:.0f}ms)")
        else:
            print(f"✅ GOOD: Login performance is acceptable ({avg_total:.0f}ms)")
            
        # Analyze bottleneck
        avg_login = mean(login_times)
        if avg_login > 300:
            print(f"\n🔍 Analysis:")
            print(f"   Main bottleneck: bcrypt password verification ({avg_login:.0f}ms)")
            print(f"   Recommendations:")
            print(f"   - Consider reducing bcrypt rounds (currently using default)")
            print(f"   - Add caching for frequently accessed users")
            print(f"   - Monitor database query performance")

def test_bcrypt_performance():
    """Test bcrypt hashing performance with different rounds"""
    try:
        from passlib.context import CryptContext
        
        print("\n🔐 Testing bcrypt performance:")
        print("=" * 40)
        
        test_password = "SV25000002@"
        rounds_to_test = [10, 11, 12, 13]
        
        for rounds in rounds_to_test:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=rounds)
            
            # Test hashing
            start = time.time()
            hashed = pwd_context.hash(test_password)
            hash_time = (time.time() - start) * 1000
            
            # Test verification
            start = time.time()
            pwd_context.verify(test_password, hashed)
            verify_time = (time.time() - start) * 1000
            
            print(f"Rounds {rounds}: Hash={hash_time:5.1f}ms | Verify={verify_time:5.1f}ms")
            
    except ImportError:
        print("❌ passlib not available for bcrypt testing")

if __name__ == "__main__":
    print("🚀 Login Performance Analysis")
    print("=" * 60)
    
    # Test login performance
    test_login_performance()
    
    # Test bcrypt performance
    test_bcrypt_performance()