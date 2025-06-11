import json

with open("credentials.json") as f:
    data = json.load(f)

# Escape newline characters in private key
data["private_key"] = data["private_key"].replace("\n", "\\n")

# Print properly escaped JSON string
print(json.dumps(data))
