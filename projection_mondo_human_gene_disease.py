import pandas as pd


gene_disease = pd.read_csv(
    "mondo_human_gene_disease.csv",
    dtype=str
)

mapping = pd.read_csv(
    "ncbi_kegg_gene_mapping.csv",
    dtype=str
)

result = gene_disease.merge(
    mapping,
    left_on="gene_id",
    right_on="ncbi_gene_id",
    how="inner"
)

result = result[[
    "MONDO_ID",
    "ncbi_gene_id",
    "kegg_gene_id"
]].drop_duplicates()

result.to_csv(
    "mondo_human_kegg_gene.csv",
    index=False,
    encoding="utf-8-sig"
)

print(result.shape)