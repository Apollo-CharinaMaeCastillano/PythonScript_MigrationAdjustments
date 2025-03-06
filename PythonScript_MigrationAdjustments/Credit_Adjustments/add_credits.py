import requests
import pandas as pd
import base64
import json

# API Configuration
API_URL = "http://10.160.0.85:30000/1.0/kb/credits?autoCommit=true"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Killbill-ApiKey": "tenant01",
    "X-Killbill-ApiSecret": "secret01",
    "X-Killbill-CreatedBy": "admin",
    "X-Killbill-Reason": "Adding credit",
    "X-Killbill-Comment": "Manual credit",
    "Authorization": "Basic " + base64.b64encode("admin:password".encode()).decode()  # Replace 'password' with actual password
}

# Read CSV file
CSV_FILE = "credits.csv"
df = pd.read_csv(CSV_FILE)

# Validate CSV file structure
if "accountId" not in df.columns or "amount" not in df.columns:
    print("Error: CSV file must contain 'accountId' and 'amount' columns.")
    exit(1)

# Initialize log list
log_results = []

# Display header in terminal
print("\nProcessing Credits...")
print("=" * 50)
print(f"{'Account ID':<40} {'Amount':<10} {'Status'}")
print("=" * 50)

# Process each account
for _, row in df.iterrows():
    account_id = row["accountId"]
    amount = row["amount"]
    
    # Prepare API payload
    payload = [{"accountId": account_id, "amount": amount}]
    
    # Send API request
    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
    
    # Check response and log status
    if response.status_code in [200, 201]:
        status = "Success"
    else:
        status = f"Failed - {response.text}"

    # Print log in terminal
    print(f"{account_id:<40} {amount:<10} {status}")

    # Append to log list
    log_results.append({"accountId": account_id, "amount": amount, "status": status})

# Save log results to a CSV file
log_df = pd.DataFrame(log_results)
log_df.to_csv("credit_log.csv", index=False)

print("\nProcess completed. Log saved as 'credit_log.csv'.")
