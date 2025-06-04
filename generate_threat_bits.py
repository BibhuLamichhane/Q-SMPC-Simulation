import pandas as pd
import numpy as np

total_parties = 4
num_samples = 1000

def generate_data(num_samples):
    """
    Generate a list of threat bits based on the number of bits specified.
    """
    return np.random.choice([0, 1], size=num_samples)

def generate_threat_bits(num_samples, total_parties):
    """
    Generate a DataFrame with threat bits for each party.
    """
    data = {
        f'party_{chr(65 + i)}': generate_data(num_samples) for i in range(total_parties)
    }
    
    return pd.DataFrame(data)

threat_bits = generate_threat_bits(num_samples, total_parties)

threat_bits.to_csv('./data/threat_bits.csv', index=False)


