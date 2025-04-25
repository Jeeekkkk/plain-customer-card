from fastapi import FastAPI, Request, HTTPException
import json

app = FastAPI()

# Load mock data at startup
with open("customers_sample.json") as f:
    customer_data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Customer Card API is running"}

# Endpoint to return formatted Customer Card to Plain
@app.post("/customer_card")
async def customer_card(request: Request):
    try:
        payload = await request.json()
        external_id = payload.get("customer", {}).get("externalId")
        email = payload.get("customer", {}).get("email")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload format")

    # Find customer by external_id or by email
    customer = None
    if external_id and external_id in customer_data:
        customer = customer_data[external_id]
    else:
        # fallback to email lookup
        for record in customer_data.values():
            if record.get("email") == email:
                customer = record
                break

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

# Return JSON structure matching expected Customer Card format
    return {
        "cards": [
            {
                "key": "trackly-insights", 
                "timeToLiveSeconds": 86400,
                "components": [
                    {
                        "componentText": {
                            "text": f"Monthly Usage: {customer['usage']} events"
                        }
                    },
                    {
                        "componentText": {
                            "text": f"Contract Value: ${customer['contract_value']}"
                        }
                    },
                                        {
                        "componentText": {
                            "text": f"Customer ID: {external_id or 'unknown'}"
                        }
                    },
                    {
                        "componentText": {
                            "text": f"Team: {customer['team_name']}"
                        }
                    },
                    {
                        "componentText": {
                            "text": f"Role: {customer['role']}"
                        }
                    },
                    {
                        "componentText": {
                            "text": f"[Edit in Trackly](https://trackly.example.com/edit?id={external_id or 'unknown'})"
                        }
                    }
                ]
            }
        ]
    }
