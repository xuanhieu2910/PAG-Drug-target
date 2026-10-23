import pandas as pd
import requests

url = "https://rest.kegg.jp/conv/hsa/ncbi-geneid"

response = requests.get(url, timeout=60)
response.raise_for_status()

records = []

for line in response.text.splitlines():
    ncbi_id, kegg_id = line.split("\t")

    records.append({
        "ncbi_gene_id": ncbi_id.replace("ncbi-geneid:", ""),
        "kegg_gene_id": kegg_id
    })

df = pd.DataFrame(records).drop_duplicates()

df.to_csv(
    "ncbi_kegg_gene_mapping.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.shape)
print(df.head(10))