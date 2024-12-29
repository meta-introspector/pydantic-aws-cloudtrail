import boto3
import os
import glob
from datetime import datetime, timezone
from pathlib import Path

# aws cloudtrail lookup-events --start-time $NEW_DATE  --output json >>  logs/$(date -d "today" +"%Y%m%d%H%M").log
#     #--profile "${AWS_PROFILE}" --region "${AWS_REGION}"
#     #--max-items 1000 


# Initialize the CloudTrail client
client = boto3.client('cloudtrail')

Path("logs").mkdir(parents=True, exist_ok=True)

opts = {}
# Find the latest log file
log_files = sorted(glob.glob('logs/*.log'), key=os.path.getmtime)
if not log_files:
    print("No log files found.")

else:
    latest_file = log_files[-1]
    new_date = datetime.fromtimestamp(os.path.getmtime(latest_file), tz=timezone.utc).isoformat()
    opts["StartTime"]=new_date



def main():
    response = client.lookup_events(
    **opts
    # Optionally, add other parameters as needed
    # MaxResults=1000, 
    )

    # Create a log filename with the current timestamp
    log_filename = f'logs/{datetime.now().strftime("%Y%m%d%H%M")}.log'
    
    # Write response to log file
    with open(log_filename, 'w') as log_file:
        log_file.write(str(response))
        
        print(f"CloudTrail events logged to {log_filename}")
