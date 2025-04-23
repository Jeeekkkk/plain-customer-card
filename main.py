from fastapi import FastAPI, Request, HTTPException
import json

app = FastAPI()

# Load mock data at startup
with open("customers_sample.json") as f:
    customer_data = json.load(f)

@app.post("/customer_card")
async def customer_card(request: Request):
    payload = await request.json()
    external_id = payload.get("external_id")

    if not external_id or external_id not in customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = customer_data[external_id]

    return {
        "type": "card",
        "title": "Trackly Overview",
        "body": [
            {"type": "label", "label": "Monthly Usage", "value": f"{customer['usage']} events"},
            {"type": "label", "label": "Contract Value", "value": f"${customer['contract_value']}"},
            {"type": "label", "label": "Team", "value": customer['team_name']},
            {"type": "label", "label": "Role", "value": customer['role']},
            {
                "type": "button",
                "label": "Edit in Trackly",
                "action": {
                    "type": "url",
                    "url": f"https://trackly.example.com/edit?id={external_id}"
                }
            }
        ]
    }