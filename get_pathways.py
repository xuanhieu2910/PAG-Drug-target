import requests
import pandas as pd
import numpy as np


def get_kegg_gene_id(uniprot_id):
    url = f"https://rest.kegg.jp/conv/hsa/uniprot:{uniprot_id}"

    uniprot_list = []
    kegg_gene_list = []

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        for line in response.text.strip().splitlines():
            parts = line.split("\t")

            if len(parts) != 2:
                continue

            uniprot_value = parts[0].replace("up:", "").strip()
            kegg_gene_value = parts[1].strip()

            # Chỉ lấy gene người
            if (uniprot_value and
                    kegg_gene_value.startswith("hsa:")):
                uniprot_list.append(uniprot_value)
                kegg_gene_list.append(kegg_gene_value)

        # Không tìm thấy mapping
        if not kegg_gene_list:
            uniprot_list.append(uniprot_id)
            kegg_gene_list.append(None)

    except requests.RequestException as e:
        raise RuntimeError(
            f"KEGG API Error for {uniprot_id}: {e}"
        ) from e

    return (
        np.array(uniprot_list, dtype=object),
        np.array(kegg_gene_list, dtype=object)
    )


def get_kegg_properties(hsa):
    url = f"https://rest.kegg.jp/get/{hsa}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    lines = response.text.strip().splitlines()
    return lines


def extract_pathways(lines, hsa):
    pathways = []
    current_field = None

    for line in lines:
        field = line[:12].strip()
        value = line[12:].strip()
        # Nếu gặp một trường mới
        if field:
            current_field = field

        # Chỉ lấy dữ liệu thuộc PATHWAY
        if current_field == "PATHWAY" and value:
            parts = value.split(maxsplit=1)

            pathways.append({
                "hsa": hsa,
                "pathway_id": parts[0],
                "pathway_name": parts[1] if len(parts) > 1 else ""
            })

    return pathways


def extract_network(lines, hsa):
    network = []
    current_field = None

    for line in lines:
        field = line[:12].strip()
        value = line[12:].strip()
        # Nếu gặp một trường mới
        if field:
            current_field = field

        # Chỉ lấy dữ liệu thuộc PATHWAY
        if current_field == "NETWORK" and value:
            parts = value.split(maxsplit=1)

            network.append({
                "hsa": hsa,
                "network_id": parts[0],
                "network_name": parts[1] if len(parts) > 1 else ""
            })

    return network


def extract_element(lines, hsa):
    elements = []
    current_field = None

    for line in lines:
        field = line[:12].strip()
        value = line[12:].strip()
        # Nếu gặp một trường mới
        if field:
            current_field = field

        # Chỉ lấy dữ liệu thuộc ELEMENT
        if current_field == "ELEMENT" and value:
            parts = value.split(maxsplit=1)

            elements.append({
                "hsa": hsa,
                "element_id": parts[0],
                "element_name": parts[1] if len(parts) > 1 else ""
            })

    return elements


def extract_DISEASE(lines, hsa):
    diseases = []
    current_field = None

    for line in lines:
        field = line[:12].strip()
        value = line[12:].strip()
        # Nếu gặp một trường mới
        if field:
            current_field = field

        # Chỉ lấy dữ liệu thuộc DISEASE
        if current_field == "DISEASE" and value:
            parts = value.split(maxsplit=1)

            diseases.append({
                "hsa": hsa,
                "disease_id": parts[0],
                "disease_name": parts[1] if len(parts) > 1 else ""
            })

    return diseases


def extract_drug_target(lines, hsa):
    drug_targets = []
    current_field = None

    for line in lines:
        field = line[:12].strip()
        value = line[12:].strip()
        # Nếu gặp một trường mới
        if field:
            current_field = field

        # Chỉ lấy dữ liệu thuộc DRUG_TARGET
        if current_field == "DRUG_TARGET" and value:
            parts = value.split(":", maxsplit=1)

            drug_targets.append({
                "hsa": hsa,
                "drug_target_id": parts[0],
                "drug_target_name": parts[1] if len(parts) > 1 else ""
            })

    return drug_targets


def export_kegg_properties(kegg_hsa_final,
                           kegg_entry_final,
                           kegg_symbol_final,
                           kegg_name_final,
                           kegg_orthology_final,
                           kegg_organism_final
                           ):
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa_final,
            'kegg_entry': kegg_entry_final,
            'kegg_symbol': kegg_symbol_final,
            'kegg_name': kegg_name_final,
            'kegg_orthology': kegg_orthology_final,
            'kegg_organism': kegg_organism_final
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_properties.csv', index=False)


def export_kegg_pathway(kegg_pathway_final):
    kegg_hsa = np.array([], dtype=object)
    pathway_id = np.array([], dtype=object)
    pathway_name = np.array([], dtype=object)
    for pathways in kegg_pathway_final:
        kegg_hsa = np.concatenate([kegg_hsa, np.array([pathways['hsa']], dtype=object)])
        pathway_id = np.concatenate([pathway_id, np.array([pathways['pathway_id']], dtype=object)])
        pathway_name = np.concatenate([pathway_name, np.array([pathways['pathway_name']], dtype=object)])
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa,
            'pathway_id': pathway_id,
            'pathway_name': pathway_name
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_pathway.csv', index=False)


def export_kegg_network(kegg_network_final):
    kegg_hsa = np.array([], dtype=object)


    network_id = np.array([], dtype=object)
    network_name = np.array([], dtype=object)
    for networks in kegg_network_final:
        kegg_hsa = np.concatenate([kegg_hsa, np.array([networks['hsa']], dtype=object)])
        network_id = np.concatenate([network_id, np.array([networks['network_id']], dtype=object)])
        network_name = np.concatenate([network_name, np.array([networks['network_name']], dtype=object)])
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa,
            'network_id': network_id,
            'network_name': network_name
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_network.csv', index=False)


def export_kegg_element(kegg_element_final):
    kegg_hsa = np.array([], dtype=object)
    element_id = np.array([], dtype=object)
    element_name = np.array([], dtype=object)
    for elements in kegg_element_final:
        kegg_hsa = np.concatenate([kegg_hsa, np.array([elements['hsa']], dtype=object)])
        element_id = np.concatenate([element_id, np.array([elements['element_id']], dtype=object)])
        element_name = np.concatenate([element_name, np.array([elements['element_name']], dtype=object)])
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa,
            'element_id': element_id,
            'element_name': element_name
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_element.csv', index=False)


def export_kegg_disease(kegg_disease_final):
    kegg_hsa = np.array([], dtype=object)
    disease_id = np.array([], dtype=object)
    disease_name = np.array([], dtype=object)
    for diseases in kegg_disease_final:
        kegg_hsa = np.concatenate([kegg_hsa, np.array([diseases['hsa']], dtype=object)])
        disease_id = np.concatenate([disease_id, np.array([diseases['disease_id']], dtype=object)])
        disease_name = np.concatenate([disease_name, np.array([diseases['disease_name']], dtype=object)])
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa,
            'disease_id': disease_id,
            'disease_name': disease_name
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_disease.csv', index=False)


def export_kegg_drug_target(kegg_drug_target_final):
    kegg_hsa = np.array([], dtype=object)
    drug_target_id = np.array([], dtype=object)
    drug_target_name = np.array([], dtype=object)
    for drug_targets in kegg_drug_target_final:
        kegg_hsa = np.concatenate([kegg_hsa, np.array([drug_targets['hsa']], dtype=object)])
        drug_target_id = np.concatenate([drug_target_id, np.array([drug_targets['drug_target_id']], dtype=object)])
        drug_target_name = np.concatenate(
            [drug_target_name, np.array([drug_targets['drug_target_name']], dtype=object)])
    data = pd.DataFrame(
        {
            'kegg_hsa': kegg_hsa,
            'drug_target_id': drug_target_id,
            'drug_target_name': drug_target_name
        }
    )

    data.to_csv('C:\\Users\\Lenovo\\Downloads\\kegg_drug_target.csv', index=False)

if '__main__' == __name__:
    # Example
    path_link_uniprot_ids = "C:\\Users\\Lenovo\\Downloads\\UniProt_ids.csv"
    data = pd.read_csv(path_link_uniprot_ids)

    uniprot_final = np.array([], dtype=object)
    kegg_gene_final = np.array([], dtype=object)

    kegg_hsa_final = np.array([], dtype=object)
    kegg_entry_final = np.array([], dtype=object)
    kegg_symbol_final = np.array([], dtype=object)
    kegg_name_final = np.array([], dtype=object)
    kegg_orthology_final = np.array([], dtype=object)
    kegg_organism_final = np.array([], dtype=object)
    kegg_pathway_final = np.array([], dtype=object)
    kegg_network_final = np.array([], dtype=object)
    kegg_element_final = np.array([], dtype=object)
    kegg_disease_final = np.array([], dtype=object)
    kegg_motif_final = np.array([], dtype=object)
    kegg_drug_target_final = np.array([], dtype=object)

    for index, row in data.iterrows():
        # print(row.values[0])
        uniprot_id = row.values[0]
        uniprot, kegg_gene = get_kegg_gene_id(uniprot_id)
        print(f"Uniprot: {uniprot}, KEGG Gene: {kegg_gene}")
        uniprot_final = np.concatenate([uniprot_final, uniprot])
        kegg_gene_final = np.concatenate([kegg_gene_final, kegg_gene])
        # print(f"Final Uniprot: {uniprot_final}, Final KEGG Gene: {kegg_gene_final}")
        for keg in kegg_gene:
            if keg is None:
                continue
            kegg_hsa_final = np.concatenate([kegg_hsa_final, np.array([keg], dtype=object)])
            properties = get_kegg_properties(keg)
            kegg_entry_final = np.concatenate(
                [kegg_entry_final, np.array([properties[0].split(maxsplit=1)[1]], dtype=object)])
            kegg_symbol_final = np.concatenate(
                [kegg_symbol_final, np.array([properties[1].split(maxsplit=1)[1]], dtype=object)])
            kegg_name_final = np.concatenate(
                [kegg_name_final, np.array([properties[2].split(maxsplit=1)[1]], dtype=object)])
            kegg_orthology_final = np.concatenate(
                [kegg_orthology_final, np.array([properties[3].split(maxsplit=1)[1]], dtype=object)])
            kegg_organism_final = np.concatenate(
                [kegg_organism_final, np.array([properties[4].split(maxsplit=1)[1]], dtype=object)])

            kegg_pathway_final = np.concatenate([kegg_pathway_final, extract_pathways(properties, keg)])
            kegg_element_final = np.concatenate([kegg_element_final, extract_element(properties, keg)])
            kegg_network_final = np.concatenate([kegg_network_final, extract_network(properties, keg)])
            kegg_disease_final = np.concatenate([kegg_disease_final, extract_DISEASE(properties, keg)])
            kegg_drug_target_final = np.concatenate([kegg_drug_target_final, extract_drug_target(properties, keg)])

            print("================================\n")

    export_kegg_properties(kegg_hsa_final,
                           kegg_entry_final,
                           kegg_symbol_final,
                           kegg_name_final,
                           kegg_orthology_final,
                           kegg_organism_final
                           )

    export_kegg_pathway(kegg_pathway_final)
    export_kegg_network(kegg_network_final)
    export_kegg_element(kegg_element_final)
    export_kegg_disease(kegg_disease_final)
    export_kegg_drug_target(kegg_drug_target_final)

    data = pd.DataFrame(
        {
            'uniprot_id': uniprot_final,
            'kegg_gene': kegg_gene_final,
        }
    )
    data.to_csv('C:\\Users\\Lenovo\\Downloads\\unit_protein_id_kegg_gene_BABABABAB.csv', index=False)
