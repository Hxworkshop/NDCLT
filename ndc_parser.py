import re

def parse_out_file(file_path):
    """Parse the .out file and extract NDC data. Returns a dict keyed by NDC code."""
    exfix_pattern = r'00000000000000000000000000000000-(\d{4})-(\d{11,12})'
    standard_pattern = r'(\d{4,5})-(\d{3,4})-(\d{2})'
    ndc_data = {}
    current_ndc = None
    current_data = {}
    line_count = 0
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line_num, line in enumerate(file, 1):
            line_count += 1
            line = line.strip()
            if not line:
                continue
            exfix_match = re.search(exfix_pattern, line)
            if exfix_match:
                if current_ndc and current_data:
                    ndc_data[current_ndc] = current_data
                labeler_code = exfix_match.group(1)
                product_code = exfix_match.group(2)
                current_ndc = f"00000000000000000000000000000000-{labeler_code}-{product_code}"
                current_data = {
                    'line_number': line_num,
                    'ndc': current_ndc,
                    'drug_name': '',
                    'manufacturer': '',
                    'package_size': '',
                    'drug_class': '',
                    'effective_date': ''
                }
                date_match = re.search(r'(\d{8})', line)
                if date_match:
                    date_str = date_match.group(1)
                    if len(date_str) == 8 and date_str.isdigit():
                        current_data['effective_date'] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                if len(line) > 300:
                    ndc_pos = line.find(current_ndc)
                    if ndc_pos != -1:
                        after_ndc = line[ndc_pos + len(current_ndc):]
                        name_match = re.search(r'\s+([A-Z][A-Z\s\-]{2,30}[A-Z])\s+[A-Z]', after_ndc)
                        if name_match:
                            drug_name = name_match.group(1).strip()
                            drug_name = re.sub(r'\s+', ' ', drug_name).strip()
                            drug_name = re.sub(r'^(POLIQ|POTAB|POCER|SLTAB)', '', drug_name).strip()
                            if len(drug_name) > 3:
                                current_data['drug_name'] = drug_name
                        drug_name_end = 0
                        if current_data.get('drug_name'):
                            drug_name_pos = after_ndc.find(current_data['drug_name'])
                            if drug_name_pos != -1:
                                drug_name_end = drug_name_pos + len(current_data['drug_name'])
                        if drug_name_end > 0:
                            after_drug_name = after_ndc[drug_name_end:]
                            mfr_match = re.search(r'\s+([A-Z][A-Z\s\.]+(?:PHARMACEUTICAL|CORPORATION|LLC|TECHNOLOGIES|INC|LABS))', after_drug_name)
                            if mfr_match:
                                manufacturer = mfr_match.group(1).strip()
                                manufacturer = re.sub(r'\s+', ' ', manufacturer).strip()
                                manufacturer = manufacturer.replace('IOLINE', 'BIOLINE')
                                manufacturer = manufacturer.replace('BBIOLINE', 'BIOLINE')
                                manufacturer = re.sub(r'^C\s+', '', manufacturer)
                                if len(manufacturer) > 3:
                                    current_data['manufacturer'] = manufacturer
                        strength_match = re.search(r'(\d+(?:\.\d+)?)\s*MG/\d+\s*ML?', line)
                        if strength_match:
                            current_data['package_size'] = strength_match.group(0).strip()
                        else:
                            strength_match = re.search(r'(\d+(?:\.\d+)?)\s*MG', line)
                            if strength_match:
                                current_data['package_size'] = strength_match.group(0).strip()
                        pkg_match = re.search(r'00100', line)
                        if pkg_match:
                            current_data['package_count'] = '100'
                        else:
                            pkg_match = re.search(r'00001', line)
                            if pkg_match:
                                current_data['package_count'] = '1'
                        ea_match = re.search(r'\bEA\b', line)
                        if ea_match:
                            current_data['unit_measure'] = 'EA'
                        class_match = re.search(r'\b(RX|OTC|CV)\b', line)
                        if class_match:
                            current_data['drug_class'] = class_match.group(1)
                        price_match = re.search(r'(\d+\.\d{2})', line)
                        if price_match:
                            price = price_match.group(1)
                            price = re.sub(r'^0+', '', price)
                            if price.startswith('.'):
                                price = '0' + price
                            current_data['package_price'] = price
                        form_match = re.search(r'\b(TABLET|CAPSULE|INJECTION|LIQUID|CREAM|OINTMENT)\b', line, re.IGNORECASE)
                        if form_match:
                            current_data['form_desc'] = form_match.group(1).title()
                        else:
                            if 'ML' in current_data.get('package_size', ''):
                                current_data['form_desc'] = 'Liquid'
                            elif 'MG' in current_data.get('package_size', ''):
                                current_data['form_desc'] = 'Tablet'
            elif not exfix_match:
                standard_match = re.search(standard_pattern, line)
                if standard_match:
                    if current_ndc and current_data:
                        ndc_data[current_ndc] = current_data
                    labeler_code = standard_match.group(1)
                    product_code = standard_match.group(2)
                    package_code = standard_match.group(3)
                    current_ndc = f"{labeler_code}-{product_code}-{package_code}"
                    current_data = {
                        'line_number': line_num,
                        'ndc': current_ndc,
                        'drug_name': '',
                        'manufacturer': '',
                        'package_size': '',
                        'drug_class': '',
                        'effective_date': ''
                    }
                    date_match = re.search(r'(\d{8})', line)
                    if date_match:
                        date_str = date_match.group(1)
                        if len(date_str) == 8 and date_str.isdigit():
                            current_data['effective_date'] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    if len(line) > 300:
                        ndc_pos = line.find(current_ndc)
                        if ndc_pos != -1:
                            after_ndc = line[ndc_pos + len(current_ndc):]
                            name_match = re.search(r'\s+([A-Z][A-Z\s\-]{2,30}[A-Z])\s+[A-Z]', after_ndc)
                            if name_match:
                                drug_name = name_match.group(1).strip()
                                drug_name = re.sub(r'\s+', ' ', drug_name).strip()
                                drug_name = re.sub(r'^(POLIQ|POTAB|POCER|SLTAB)', '', drug_name).strip()
                                if len(drug_name) > 3:
                                    current_data['drug_name'] = drug_name
                            drug_name_end = 0
                            if current_data.get('drug_name'):
                                drug_name_pos = after_ndc.find(current_data['drug_name'])
                                if drug_name_pos != -1:
                                    drug_name_end = drug_name_pos + len(current_data['drug_name'])
                            if drug_name_end > 0:
                                after_drug_name = after_ndc[drug_name_end:]
                                mfr_match = re.search(r'\s+([A-Z][A-Z\s\.]+(?:PHARMACEUTICAL|CORPORATION|LLC|TECHNOLOGIES|INC|LABS))', after_drug_name)
                                if mfr_match:
                                    manufacturer = mfr_match.group(1).strip()
                                    manufacturer = re.sub(r'\s+', ' ', manufacturer).strip()
                                    manufacturer = manufacturer.replace('IOLINE', 'BIOLINE')
                                    manufacturer = manufacturer.replace('BBIOLINE', 'BIOLINE')
                                    manufacturer = re.sub(r'^C\s+', '', manufacturer)
                                    if len(manufacturer) > 3:
                                        current_data['manufacturer'] = manufacturer
                            strength_match = re.search(r'(\d+(?:\.\d+)?)\s*MG/\d+\s*ML?', line)
                            if strength_match:
                                current_data['package_size'] = strength_match.group(0).strip()
                            else:
                                strength_match = re.search(r'(\d+(?:\.\d+)?)\s*MG', line)
                                if strength_match:
                                    current_data['package_size'] = strength_match.group(0).strip()
                            pkg_match = re.search(r'00100', line)
                            if pkg_match:
                                current_data['package_count'] = '100'
                            else:
                                pkg_match = re.search(r'00001', line)
                                if pkg_match:
                                    current_data['package_count'] = '1'
                            ea_match = re.search(r'\bEA\b', line)
                            if ea_match:
                                current_data['unit_measure'] = 'EA'
                            class_match = re.search(r'\b(RX|OTC|CV)\b', line)
                            if class_match:
                                current_data['drug_class'] = class_match.group(1)
                            price_match = re.search(r'(\d+\.\d{2})', line)
                            if price_match:
                                price = price_match.group(1)
                                price = re.sub(r'^0+', '', price)
                                if price.startswith('.'):
                                    price = '0' + price
                                current_data['package_price'] = price
                            form_match = re.search(r'\b(TABLET|CAPSULE|INJECTION|LIQUID|CREAM|OINTMENT)\b', line, re.IGNORECASE)
                            if form_match:
                                current_data['form_desc'] = form_match.group(1).title()
                            else:
                                if 'ML' in current_data.get('package_size', ''):
                                    current_data['form_desc'] = 'Liquid'
                                elif 'MG' in current_data.get('package_size', ''):
                                    current_data['form_desc'] = 'Tablet'
    if current_ndc and current_data:
        ndc_data[current_ndc] = current_data
    return ndc_data 