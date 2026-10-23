import pandas as pd

path_input = r"D:\Research\PAG-DrugTarget\references\ADR_DP_Networks\data\raw\Gene_disease\genes_to_disease.txt"

columns = [
    "ncbi_gene_id",
    "gene_symbol",
    "association_type",
    "disease_id",
    "source"
]

# 1. Read file
df = pd.read_csv(
    path_input,
    sep="\t",
    comment="#",
    header=None,
    names=columns,
    dtype=str,
    keep_default_na=False
)

# 2. Keep valid Gene IDs
df = df[
    df["ncbi_gene_id"].str.fullmatch(r"(NCBIGene:)?\d+")
].copy()

# 3. Convert NCBIGene to hsa
df["ncbi_gene_id"] = (
    "hsa:" +
    df["ncbi_gene_id"].str.replace(
        "NCBIGene:", "", regex=False
    )
)

# 4. Rename column
df = df.rename(columns={
    "ncbi_gene_id": "hsa"
})

# 5. Save CSV
df.to_csv(
    "genes_to_disease_hsa.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.shape)
print(df.head(10))
