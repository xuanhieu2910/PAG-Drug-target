import numpy as np
import csv
import json
import os
import pandas as pd

def main():
    path_file_json = 'C:\\Users\\hieux\\Downloads\\PubChemAnnotations_DrugBank_DrugBank-Target-ID-Protein.json'

    with open(path_file_json, 'r') as f:
        data = json.load(f)
        source_name = np.array([])
        source_id = np.array([])
        description = np.array([])
        url = np.array([])
        code = np.array([])
        link_records = np.array([])
        for d in data['Annotations']['Annotation']:
                source_name = np.append(source_name,['SourceName'])
                source_id = np.append(source_id,d['SourceID'])
                description = np.append(description,d['Description'])
                url = np.append(url,d['URL'])
                code = np.append(code,d['Data'][0]['Value']['StringWithMarkup'][0]['String'])
                link_records = np.append(link_records,d['LinkedRecords']['ProteinAccession'][0])
        data = pd.DataFrame(
            {
                'source_name': source_name,
                'source_id': source_id,
                'description': description,
                'url': url,
                'code': code,
                'link_records': link_records
            }
        )
        data.to_csv('C:\\Users\\hieux\\Downloads\\proteins.csv', index=False)


if "__main__" == __name__:
    main()