# Plain Customer Card Demo

Demonstration of a custom Customer Card integration for Plain.

## Live URL
[https://plain-customer-card-demo.onrender.com](https://plain-customer-card-demo.onrender.com)

## How It Works
- Receives a POST request to `/customer_card` with a customer's `external_id`
- Returns a structured Customer Card based on mock data (`customers_sample.json`)
- Deploys automatically with Render via GitHub

## Example Payload
```json
{
  "external_id": "1001"
}
