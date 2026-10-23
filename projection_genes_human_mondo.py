
import pandas as pd

path_gene = r"D:\Research\PAG-DrugTarget\genes_to_disease_hsa.csv"
path_mapping = r"D:\Research\PAG-DrugTarget\mondo_human_mapping.csv"
path_human = r"D:\Research\PAG-DrugTarget\mondo_human_diseases.csv"

# 1. Read files
gene = pd.read_csv(path_gene, dtype=str)
mapping = pd.read_csv(path_mapping, dtype=str)
human = pd.read_csv(path_human, dtype=str)

# 2. Normalize Disease IDs
def normalize_id(value):
    value = str(value).strip()

    if value.startswith("ORPHA:"):
        return value.replace("ORPHA:", "Orphanet:", 1)

    if value.startswith("MIM:"):
        return value.replace("MIM:", "OMIM:", 1)

    return value


gene["disease_id"] = gene["disease_id"].map(normalize_id)
mapping["object_id"] = mapping["object_id"].map(normalize_id)

# 3. JOIN Gene-Disease with MONDO mapping
result = gene.merge(
    mapping[["MONDO_ID", "object_id"]],
    left_on="disease_id",
    right_on="object_id",
    how="inner"
)

# 4. Filter Human Disease
result = result[
    result["MONDO_ID"].isin(human["MONDO_ID"])
].copy()

# 5. Select columns
result = result[[
    "hsa",
    "gene_symbol",
    "association_type",
    "MONDO_ID"
]].copy()

result = result.rename(columns={
    "MONDO_ID": "mondo_id"
})

result = result.drop_duplicates()

# 6. Save CSV
result.to_csv(
    "mondo_human_gene_disease.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Total records:", len(result))
print("Genes:", result["hsa"].nunique())
print("Diseases:", result["mondo_id"].nunique())
print(result.head(10))
