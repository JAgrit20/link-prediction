
import requests
import pandas as pd

# Construct URLs from the generated IDs
start_id = 1755815
end_id = 1855815

all_ids = list(range(start_id, end_id + 1))

urls = [f"https://bugzilla.mozilla.org/rest/bug/{bug_id}" for bug_id in all_ids]

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {url}")
        return None

enhancements = []
bugs = []

for url in urls:
    data = fetch_data(url)
    if data and 'bugs' in data and data['bugs']:
        bug = data['bugs'][0]
        if 'id' in bug:
            print(f"Processing bugId: {bug['id']}")  # Tracking the current bugId being processed

            if bug.get('type') == 'enhancement':
                enhancements.append(bug)
            elif bug.get('type') == 'defect':
                bugs.append(bug)

# Save dataframes to CSV
df_enhancements = pd.DataFrame(enhancements)
df_bugs = pd.DataFrame(bugs)

df_enhancements.to_csv("enhancements.csv", index=False)
df_bugs.to_csv("bugs.csv", index=False)

print("Data saved successfully!")