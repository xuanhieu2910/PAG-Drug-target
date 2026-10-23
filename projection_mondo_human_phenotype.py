
import pandas as pd

path_mapping = r"D:\Research\PAG-DrugTarget\mondo_human_mapping.csv"
path_hpoa = r"D:\Research\PAG-DrugTarget\references\ADR_DP_Networks\data\raw\DP\phenotype.hpoa"

# 1. Read MONDO mapping
mapping = pd.read_csv(path_mapping, dtype=str)

# 2. Read phenotype.hpoa
columns = [
    "database_id", "disease_name", "qualifier",
    "hpo_id", "reference", "evidence", "onset",
    "frequency", "sex", "modifier", "aspect",
    "biocuration"
]

hpoa = pd.read_csv(
    path_hpoa,
    sep="\t",
    comment="#",
    header=None,
    names=columns,
    dtype=str,
    keep_default_na=False
)

# 3. Normalize Disease IDs
mapping["object_id"] = mapping["object_id"].str.strip()

hpoa["database_id"] = (
    hpoa["database_id"]
    .str.strip()
    .str.replace(r"^ORPHA:", "Orphanet:", regex=True)
)

# 4. Filter positive phenotype annotations
hpoa = hpoa[
    (hpoa["aspect"] == "P") &
    (hpoa["qualifier"].str.upper() != "NOT")
].copy()

# 5. JOIN
result = mapping.merge(
    hpoa,
    left_on="object_id",
    right_on="database_id",
    how="inner"
)

# 6. Select columns
result = result[[
    "MONDO_ID",
    "database_id",
    "hpo_id",
    "frequency"
]].copy()

result.columns = [
    "mondo_id",
    "database_id",
    "hpo_id",
    "frequency"
]

result = result.drop_duplicates()

# 7. Save CSV
result.to_csv(
    "mondo_human_phenotype.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Total records:", len(result))
print("MONDO Diseases:", result["mondo_id"].nunique())
print("HPO Phenotypes:", result["hpo_id"].nunique())
print(result.head(10))
