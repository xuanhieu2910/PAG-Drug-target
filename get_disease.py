from collections import defaultdict, deque
import pandas as pd

path = "D:\\Research\\PAG-DrugTarget\\references\\ADR_DP_Networks\\data\\raw\\Disease\\mondo.obo"

diseases = {}
current = None

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line == "[Term]":
            if current and "id" in current:
                diseases[current["id"]] = current

            current = {
                "parents": [],
                "obsolete": False
            }

        elif line.startswith("["):
            if current and "id" in current:
                diseases[current["id"]] = current
            current = None

        elif current is not None:
            if line.startswith("id: "):
                current["id"] = line[4:]

            elif line.startswith("name: "):
                current["name"] = line[6:]

            elif line.startswith("is_a: "):
                parent = line.split()[1]
                current["parents"].append(parent)

            elif line == "is_obsolete: true":
                current["obsolete"] = True

# Lưu Term cuối cùng
if current and "id" in current:
    diseases[current["id"]] = current

print("Total MONDO terms:", len(diseases))

children = defaultdict(list)

for disease_id, disease in diseases.items():

    if disease["obsolete"]:
        continue

    for parent_id in disease["parents"]:
        children[parent_id].append(disease_id)

root_id = "MONDO:0700096"

queue = deque([root_id])
human_diseases = set()

while queue:
    disease_id = queue.popleft()

    if disease_id in human_diseases:
        continue

    human_diseases.add(disease_id)

    for child_id in children[disease_id]:
        queue.append(child_id)

# Bỏ node gốc, chỉ lấy các Disease con
human_diseases.discard(root_id)

print("Total Human Diseases:", len(human_diseases))
results = []

for disease_id in sorted(human_diseases):
    disease = diseases[disease_id]

    for parent_id in disease["parents"]:
        results.append({
            "MONDO_ID": disease_id,
            "Disease_Name": disease.get("name"),
            "Parent_ID": parent_id
        })

df = pd.DataFrame(results).drop_duplicates()

df.to_csv(
    "mondo_human_diseases.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head(10))
print("Total records:", len(df))