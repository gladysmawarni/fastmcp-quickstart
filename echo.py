from fastmcp import FastMCP
from firebase_admin import credentials, firestore, initialize_app
import os, json

from dotenv import load_dotenv
load_dotenv()

# credentials
json_creds = json.loads(os.environ["FIREBASE_CRED"])

# --- Firebase Setup ---
cred = credentials.Certificate(json_creds)
initialize_app(cred)
db = firestore.client()



# Instantiate the server, giving it a name
mcp = FastMCP(name="Firebase DB connection")

@mcp.tool()
def get_restaurant_info(name: str):
    """Fetch restaurant info by name from Firestore."""
    doc_ref = db.collection("restaurants").document(name)
    doc = doc_ref.get()

    # if restaurant exist
    if doc.exists:
      data = doc.to_dict()
      return {"Restaurant name": data['GoogleData']['restaurant'],
              "Restaurant address": data['Address'],
              "Restaurant website": data['Website'],
              "Restaurant rating": data['GoogleData']['google_rating']}
              
    # if it doesn't exist
    else:
      return {"error": f"Restaurant '{name}' not found"}
    

