
import pandas as pd

path_hp_obo = r"D:\Research\PAG-DrugTarget\references\ADR_DP_Networks\data\raw\DP\hp.obo"

hpo_records = []

current_id = None
current_name = None
parent_ids = []
is_obsolete = False


def save_term():
    if current_id is None:
        return

    if parent_ids:
        for parent_id in parent_ids:
            hpo_records.append({
                "id": current_id,
                "name": current_name,
                "parent_id": parent_id,
                "is_obsolete": is_obsolete
            })
    else:
        hpo_records.append({
            "id": current_id,
            "name": current_name,
            "parent_id": None,
            "is_obsolete": is_obsolete
        })


with open(path_hp_obo, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if line == "[Term]":
            save_term()

            current_id = None
            current_name = None
            parent_ids = []
            is_obsolete = False

        elif line == "[Typedef]":
            save_term()
            current_id = None
            current_name = None
            parent_ids = []
            is_obsolete = False

        elif line.startswith("id: ") and current_id is None:
            current_id = line.split("id: ", 1)[1]

        elif line.startswith("name: "):
            current_name = line.split("name: ", 1)[1]

        elif line.startswith("is_a: "):
            parent_id = line.split("is_a: ", 1)[1].split(" ! ")[0]
            parent_ids.append(parent_id)

        elif line.startswith("is_obsolete: "):
            is_obsolete = line.split("is_obsolete: ", 1)[1].lower() == "true"

    save_term()


df = pd.DataFrame(
    hpo_records,
    columns=["id", "name", "parent_id", "is_obsolete"]
)

df.to_csv(
    "hpo_terms.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.shape)
print(df.head(10))
