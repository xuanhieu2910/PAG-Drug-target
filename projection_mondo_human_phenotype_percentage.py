
import pandas as pd

path_input = "mondo_human_phenotype.csv"

df = pd.read_csv(path_input, dtype=str)

frequency_mapping = {
    "HP:0040280": "100%",
    "HP:0040281": "80-99%",
    "HP:0040282": "30-79%",
    "HP:0040283": "5-29%",
    "HP:0040284": "1-4%",
    "HP:0040285": "0%"
}

# Convert frequency to percentage ranges
df["frequency"] = df["frequency"].replace(frequency_mapping)

# Save CSV
df.to_csv(
    "mondo_human_phenotype_percent.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head(10))
