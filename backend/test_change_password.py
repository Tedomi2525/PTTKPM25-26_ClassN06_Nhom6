"""
Test script for change password functionality
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "test_user"  # Replace with actual username
PASSWORD = "old_password"  # Replace with actual password
NEW_PASSWORD = "new_password123"

def test_change_password():
    """Test the complete change password flow"""
    
    # Step 1: Login to get access token
    print("Step 1: Logging in...")
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data["access_token"]
    print("Login successful!")
    
    # Step 2: Change password
    print("Step 2: Changing password...")
    headers = {"Authorization": f"Bearer {access_token}"}
    change_password_data = {
        "currentPassword": PASSWORD,
        "newPassword": NEW_PASSWORD,
        "confirmPassword": NEW_PASSWORD
    }
    
    response = requests.put(f"{BASE_URL}/auth/change-password", json=change_password_data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"Password change successful: {result['message']}")
    else:
        print(f"Password change failed: {response.text}")
        return
    
    # Step 3: Verify new password works by logging in
    print("Step 3: Verifying new password...")
    login_data_new = {
        "username": USERNAME,
        "password": NEW_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_new)
    if response.status_code == 200:
        print("New password verification successful!")
    else:
        print(f"New password verification failed: {response.text}")

def test_change_password_errors():
    """Test error cases for change password"""
    
    # Login first
    login_data = {
        "username": USERNAME,
        "password": NEW_PASSWORD  # Use new password from previous test
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed for error testing: {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 1: Wrong current password
    print("\nTesting wrong current password...")
    change_password_data = {
        "currentPassword": "wrong_password",
        "newPassword": "another_new_password",
        "confirmPassword": "another_new_password"
    }
    
    response = requests.put(f"{BASE_URL}/auth/change-password", json=change_password_data, headers=headers)
    if response.status_code == 400:
        print("✓ Correctly rejected wrong current password")
    else:
        print(f"✗ Unexpected response for wrong current password: {response.text}")
    
    # Test 2: Password confirmation mismatch
    print("Testing password confirmation mismatch...")
    change_password_data = {
        "currentPassword": NEW_PASSWORD,
        "newPassword": "another_new_password",
        "confirmPassword": "different_confirmation"
    }
    
    response = requests.put(f"{BASE_URL}/auth/change-password", json=change_password_data, headers=headers)
    if response.status_code == 400:
        print("✓ Correctly rejected password confirmation mismatch")
    else:
        print(f"✗ Unexpected response for password mismatch: {response.text}")
    
    # Test 3: Same password as current
    print("Testing same password as current...")
    change_password_data = {
        "currentPassword": NEW_PASSWORD,
        "newPassword": NEW_PASSWORD,
        "confirmPassword": NEW_PASSWORD
    }
    
    response = requests.put(f"{BASE_URL}/auth/change-password", json=change_password_data, headers=headers)
    if response.status_code == 400:
        print("✓ Correctly rejected same password")
    else:
        print(f"✗ Unexpected response for same password: {response.text}")

if __name__ == "__main__":
    print("Testing Change Password Functionality")
    print("=" * 40)
    
    # Run basic test
    test_change_password()
    
    # Run error tests
    print("\n" + "=" * 40)
    print("Testing Error Cases")
    print("=" * 40)
    test_change_password_errors()