import json

with open("credentials.json") as f:
    data = json.load(f)

# Fix private_key newline issue
data["private_key"] = data["private_key"].replace("\n", "\\n")

print(json.dumps(data))
