# app/services/location_service.py
import pandas as pd
import os

# --- CORRECTED PATH LOGIC ---
# Get the directory of the currently running script (.../app/services)
SERVICES_DIR = os.path.dirname(os.path.abspath(__file__))
# Go two levels up to get the project's root directory (e.g., /.../legal_aid_chatbot)
PROJECT_ROOT = os.path.dirname(os.path.dirname(SERVICES_DIR))
# Now, correctly build the path to the data directory from the root
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "legal_aid_centers.csv")

try:
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Location Service: Successfully loaded data from {DATA_PATH}")
except FileNotFoundError:
    print(f"❌ Location Service: FATAL ERROR - Cannot find data file at the corrected path: {DATA_PATH}")
    # Create an empty dataframe to prevent the app from crashing completely
    df = pd.DataFrame(columns=['city', 'state', 'center_name', 'address', 'phone'])

def find_centers(city: str):
    """Finds legal aid centers in a given city (case-insensitive)."""
    if not city or df.empty:
        return []
    
    results = df[df['city'].str.lower() == city.lower()]
    if results.empty:
        return []
        
    return results.to_dict(orient='records')