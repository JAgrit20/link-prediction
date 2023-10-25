import requests
import pandas as pd
import os

import pandas as pd

# Load the Excel file
data = pd.read_excel("all_firefox_enh.xlsx")


label_1_array = data['Id'].to_numpy()

label_1_array

start_id = label_1_array[0]
end_id = label_1_array[-1]

all_ids = list(label_1_array)

urls = [f"https://bugzilla.mozilla.org/rest/bug/{bug_id}" for bug_id in all_ids]

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {url}")
        return None

expected_columns = ['id', 'summary', 'product', 'component', 'type', 'keywords', 
                    'priority', 'status', 'blocks', 'depends_on', ...]  # Add all expected columns

def save_to_csv(data, filename):
    # Ensure all expected columns are present
    for col in expected_columns:
        if col not in data:
            data[col] = None  # or 'NaN' or any other placeholder value

    write_header = not os.path.exists(filename)
    df = pd.DataFrame([data])
    df.to_csv(filename, mode='a', header=write_header, index=False, columns=expected_columns)

for url in urls:
    data = fetch_data(url)
    if data and 'bugs' in data and data['bugs']:
        bug = data['bugs'][0]
        if 'id' in bug:
            print(f"Processing bugId: {bug['id']}") 

            if bug.get('type') == 'enhancement' and bug.get('product') == "Firefox":
                save_to_csv(bug, "enhancements.csv")

print("Data saved successfully!")
