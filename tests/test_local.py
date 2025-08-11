#!/usr/bin/env python3
"""
Test script to debug the local Flask app vs Vercel service
"""
import requests
import json

# Test data
test_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "data/movies.json"},
    "mark": "circle",
    "encoding": {
        "x": {"bin": {"maxbins": 10}, "field": "IMDB Rating"},
        "y": {"bin": {"maxbins": 10}, "field": "Rotten Tomatoes Rating"},
        "size": {"aggregate": "count"}
    }
}

def test_endpoint(base_url, endpoint="/api/vl2png", params=None, with_content_type=True):
    """Test an endpoint with the given spec"""
    if params is None:
        params = {"scale": "2.0", "theme": "dark"}
    
    url = f"{base_url}{endpoint}"
    headers = {}
    if with_content_type:
        headers["Content-Type"] = "application/json"
    
    print(f"Testing: {url}")
    print(f"Params: {params}")
    print(f"Headers: {headers}")
    print(f"Data length: {len(json.dumps(test_spec))}")
    
    try:
        response = requests.post(
            url,
            params=params,
            data=json.dumps(test_spec),
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response length: {len(response.content)}")
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            print("Success!")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Vercel (original) with Content-Type ===")
    vercel_success_ct = test_endpoint("https://vl-convert-service.vercel.app", with_content_type=True)
    
    print("\n=== Testing Vercel (original) without Content-Type (like curl) ===")
    vercel_success_no_ct = test_endpoint("https://vl-convert-service.vercel.app", with_content_type=False)
    
    print("\n=== Testing Local Flask App with Content-Type ===")
    local_success_ct = test_endpoint("http://localhost:8080", with_content_type=True)
    
    print("\n=== Testing Local Flask App without Content-Type (like curl) ===")
    local_success_no_ct = test_endpoint("http://localhost:8080", with_content_type=False)
    
    print(f"\nResults:")
    print(f"Vercel (with CT):    {'✓' if vercel_success_ct else '✗'}")
    print(f"Vercel (without CT): {'✓' if vercel_success_no_ct else '✗'}")
    print(f"Local (with CT):     {'✓' if local_success_ct else '✗'}")
    print(f"Local (without CT):  {'✓' if local_success_no_ct else '✗'}")