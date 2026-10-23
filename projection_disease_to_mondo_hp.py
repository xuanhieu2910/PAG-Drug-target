
import pandas as pd

path_mondo = r"D:\Research\PAG-DrugTarget\mondo_human_diseases.csv"
path_mapping = r"D:\Research\PAG-DrugTarget\references\ADR_DP_Networks\data\raw\Disease\mondo.sssom.tsv"

# 1. Read Human Disease
mondo = pd.read_csv(path_mondo, dtype=str)

# 2. Read MONDO SSSOM
mapping = pd.read_csv(
    path_mapping,
    sep="\t",
    comment="#",
    dtype=str
)

# 3. Filter exact mappings
mapping = mapping[
    mapping["predicate_id"] == "skos:exactMatch"
].copy()

# 4. Map MONDO_ID to subject_id
result = mondo[["MONDO_ID"]].merge(
    mapping[["subject_id", "object_id"]],
    left_on="MONDO_ID",
    right_on="subject_id",
    how="inner"
)

# 5. Select columns
result = result[[
    "MONDO_ID",
    "object_id"
]].drop_duplicates()

# 6. Save CSV
result.to_csv(
    "mondo_human_mapping.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Total mappings:", len(result))
print("Mapped diseases:", result["MONDO_ID"].nunique())
print(result.head(10))
