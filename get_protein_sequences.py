import json
import csv
import numpy as np
import pandas as pd

def main():
    file_proteins_sequences = 'C:\\Users\\hieux\\Desktop\\Protein_sequences\\10\\idmapping_accession_Q14432_OR_accession_2026_10_12.json'
    with open(file_proteins_sequences, 'r') as f:
        data = json.load(f)
        # print(data['results'][0])
        link_records_from = np.array([])
        sequence_value = np.array([])
        sequence_length = np.array([])
        sequence_crc64 = np.array([])
        sequence_md5 = np.array([])
        for record in data['results']:
            link_records_from = np.append(link_records_from, record['from'])
            sequence_value = np.append(sequence_value, record['to']['sequence']['value'])
            sequence_length = np.append(sequence_length, record['to']['sequence']['length'])
            sequence_crc64 = np.append(sequence_crc64, record['to']['sequence']['crc64'])
            sequence_md5 = np.append(sequence_md5, record['to']['sequence']['md5'])

        data = pd.DataFrame(
            {
                'link_records_from': link_records_from,
                'sequence_value': sequence_value,
                'sequence_length': sequence_length,
                'sequence_crc64': sequence_crc64,
                'sequence_md5': sequence_md5,
            }
        )
        data.to_csv('C:\\Users\\hieux\\Downloads\\proteins_sequences_10.csv', index=False)


if '__main__' == __name__:
    main()