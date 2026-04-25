#!/usr/bin/env python3
"""
Test script for the ML Classification API
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5001"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    print("\nTesting model info...")
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Model info test failed: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("\nTesting prediction...")
    
    # Test cases with known iris data
    test_cases = [
        {
            "name": "Setosa",
            "features": [5.1, 3.5, 1.4, 0.2],
            "expected_class": "setosa"
        },
        {
            "name": "Versicolor", 
            "features": [6.3, 3.3, 4.7, 1.6],
            "expected_class": "versicolor"
        },
        {
            "name": "Virginica",
            "features": [6.4, 3.2, 5.3, 2.3],
            "expected_class": "virginica"
        }
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            print(f"\nTesting {test_case['name']}...")
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json={"features": test_case["features"]},
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            result = response.json()
            print(f"Predicted Class: {result.get('predicted_class')}")
            print(f"Confidence: {max(result.get('probabilities', {}).values()):.3f}")
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"Error: {result}")
                
        except Exception as e:
            print(f"Prediction test failed for {test_case['name']}: {e}")
    
    return success_count == len(test_cases)

def test_invalid_input():
    """Test the API with invalid input"""
    print("\nTesting invalid input handling...")
    
    invalid_cases = [
        {
            "name": "Missing features",
            "data": {}
        },
        {
            "name": "Wrong number of features",
            "data": {"features": [1, 2, 3]}
        },
        {
            "name": "Non-numeric features",
            "data": {"features": ["a", "b", "c", "d"]}
        }
    ]
    
    success_count = 0
    for test_case in invalid_cases:
        try:
            print(f"\nTesting {test_case['name']}...")
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            if response.status_code >= 400:
                print("✓ Correctly rejected invalid input")
                success_count += 1
            else:
                print("✗ Should have rejected invalid input")
                
        except Exception as e:
            print(f"Invalid input test failed: {e}")
    
    return success_count == len(invalid_cases)

def wait_for_api(max_attempts=30, delay=2):
    """Wait for the API to become available"""
    print("Waiting for API to become available...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✓ API is ready!")
                return True
        except:
            pass
        
        print(f"Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(delay)
    
    print("✗ API did not become available in time")
    return False

def main():
    """Run all tests"""
    print("=== ML Classification API Test Suite ===\n")
    
    # Wait for API to be ready
    if not wait_for_api():
        return False
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_model_info),
        ("Prediction", test_prediction),
        ("Invalid Input", test_invalid_input)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Print summary
    print("\n=== Test Summary ===")
    passed = 0
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
