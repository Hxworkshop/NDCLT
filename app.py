import streamlit as st
import pandas as pd
from ndc_parser import parse_out_file

st.set_page_config(page_title="NDC Lookup Tool", layout="wide")
st.title("NDC Lookup Tool")

st.markdown("""
### How to Use
1. Upload your `.out` file using the uploader below.
2. Enter an NDC code (with or without dashes).
3. Click **Search** to view results.
""")

uploaded_file = st.file_uploader("Upload .out file", type=["out"])

if uploaded_file:
    # Save uploaded file to a temporary location
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    ndc_data = parse_out_file(tmp_path)
    st.success(f"Loaded {len(ndc_data)} NDC records.")
    search_term = st.text_input("Enter NDC code to search (with or without dashes):")
    if st.button("Search"):
        if not search_term:
            st.warning("Please enter an NDC code to search.")
        else:
            search_term_norm = search_term.replace("-", "").replace(" ", "")
            exact_matches = []
            partial_matches = []
            for ndc, data in ndc_data.items():
                ndc_norm = ndc.replace("-", "").replace(" ", "")
                if search_term_norm == ndc_norm:
                    exact_matches.append((ndc, data))
                elif search_term_norm in ndc_norm or ndc_norm in search_term_norm:
                    partial_matches.append((ndc, data))
            if exact_matches or partial_matches:
                matches = exact_matches if exact_matches else partial_matches
                st.write(f"Found {len(matches)} match(es):")
                df = pd.DataFrame([{
                    'NDC': ndc,
                    'Drug Name': d.get('drug_name', ''),
                    'Manufacturer': d.get('manufacturer', ''),
                    'Strength': d.get('package_size', ''),
                    'Form': d.get('form_desc', ''),
                    'Package Size': f"{d.get('package_count', '')} {d.get('unit_measure', '')}",
                    'Drug Class': d.get('drug_class', ''),
                    'Package Price': d.get('package_price', ''),
                    'Effective Date': d.get('effective_date', ''),
                    'Line Number': d.get('line_number', '')
                } for ndc, d in matches])
                st.dataframe(df, use_container_width=True)
                st.markdown("#### Details")
                for ndc, d in matches:
                    with st.expander(f"Details for {ndc}"):
                        st.write(d)
            else:
                st.warning(f"No matches found for NDC: {search_term}")
                st.info(f"First 20 available NDC codes: {list(ndc_data.keys())[:20]}")
else:
    st.info("Please upload a .out file to begin.") 