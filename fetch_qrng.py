import numpy as np
import pandas as pd
import requests
import time

TOTAL_PARTIES = 4
NUM_SAMPLES = 1000

def fetch_qrng_bits(length=1024, retries=3, delay=65.0):
    """Fetch real quantum random bits from ANU QRNG API"""
    # Faced error with the ANU QRNG API as its limited to 1 request per minute
    # Added delay to handle rate limiting
    num_bytes = length // 8
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={num_bytes}&type=uint8"

    for attempt in range(retries):
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("success"):
                return data["data"]
            else:
                print(f"API error: {data.get('message')}")
        except Exception as e:
            print(f"QRNG API error: {e}")

        print(f"Retrying... ({attempt+1}/{retries})")
        time.sleep(delay)

    return None

def uint8_to_angles(uint8_array):
    """Convert 8-bit integers to angles in radians: [0, 2π)."""
    return (np.array(uint8_array) / 256) * (2 * np.pi)

def generate_qrng_angles_df(num_parties=TOTAL_PARTIES, num_samples=NUM_SAMPLES):
    """Generate a DataFrame of quantum angles (radians) per party per sample."""
    angles_dict = {}
    
    for i in range(num_parties):
        party_label = f"party_{chr(65 + i)}"
        print(f"Fetching QRNG values for {party_label}...")
        raw = fetch_qrng_bits(num_samples * 8)  # get 1000 bytes = 8000 bits
        if raw is None:
            raise RuntimeError(f"Failed to fetch QRNG values for {party_label}")
        
        angles = uint8_to_angles(raw[:num_samples])  # use first 1000 bytes
        angles_dict[party_label] = angles
    
    return pd.DataFrame(angles_dict)

qrng_angles = generate_qrng_angles_df()
qrng_angles.to_csv('./data/qrng_angles.csv', index=False)
print("✅ QRNG angles saved to qrng_angles.csv")