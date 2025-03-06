import requests
import pandas as pd
import json
import base64

# API Configuration
BASE_URL = "http://10.160.0.85:30000/1.0/kb/invoices/charges"
USERNAME = "admin"
PASSWORD = "password"  # Replace with the actual password
AUTH_STRING = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Killbill-ApiKey": "tenant01",
    "X-Killbill-ApiSecret": "secret01",
    "X-Killbill-CreatedBy": "admin",
    "X-Killbill-Reason": "Creating charge",
    "X-Killbill-Comment": "Manual charge",
    "Authorization": f"Basic {AUTH_STRING}"
}

# Read CSV file
CSV_FILE = "charges.csv"
df = pd.read_csv(CSV_FILE)

# Validate CSV structure
if "accountId" not in df.columns or "amount" not in df.columns:
    print("Error: CSV file must contain 'accountId' and 'amount' columns.")
    exit(1)

# If 'description' column is missing, add a default value
if "description" not in df.columns:
    df["description"] = "Manual charge"

# Initialize logs
log_results = []

# Display header in terminal
print("\nProcessing Charges...")
print("=" * 60)
print(f"{'Account ID':<40} {'Amount':<10} {'Status'}")
print("=" * 60)

# Process each charge
for _, row in df.iterrows():
    account_id = str(row["accountId"]).strip()
    amount = float(row["amount"])
    description = row["description"]

    # Construct the correct API URL (accountId in the URL)
    API_URL = f"{BASE_URL}/{account_id}?autoCommit=true"

    # Prepare API payload (without accountId inside)
    payload = [
        {
            "amount": amount,
            "currency": "PHP",  # Modify if needed
            "description": description
        }
    ]

    # Send API request
    response = requests.post(API_URL, headers=HEADERS, json=payload)  # Use 'json=' instead of 'data='

    # Check response status
    if response.status_code in [200, 201]:
        status = "Success"
    else:
        status = f"Failed - {response.status_code}: {response.text}"

    # Print log in terminal
    print(f"{account_id:<40} {amount:<10} {status}")

    # Append to log list
    log_results.append({"accountId": account_id, "amount": amount, "description": description, "status": status})

# Save log results to a CSV file
log_df = pd.DataFrame(log_results)
log_df.to_csv("charge_log.csv", index=False)

print("\nProcess completed. Log saved as 'charge_log.csv'.")
