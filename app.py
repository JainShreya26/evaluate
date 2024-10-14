import json
import streamlit as st
from io import StringIO

def load_annotations(uploaded_files):
    """Load JSON annotations from multiple uploaded files."""
    annotations = []
    for file in uploaded_files:
        # Read each uploaded file's content directly from the Streamlit file uploader
        file_content = file.getvalue().decode("utf-8").splitlines()  # Decode and split into lines
        annotations.append([json.loads(line) for line in file_content])
    return annotations

def extract_entities(annotations):
    """Extract entity annotations and organize them by ID."""
    entity_dict = {}
    for i, file_data in enumerate(annotations):
        for item in file_data:
            id_ = item.get('id', f'Unknown_ID_{i}')
            text = item.get('displayed_text', "Text not available")
            if id_ not in entity_dict:
                entity_dict[id_] = {"text": text, "entities": {}}
            for entity in item.get('span_annotations', []):
                entity_name = entity.get('annotation', 'Unknown_Label')
                word = entity.get('span', 'Unknown_Word')
                start, end = entity.get('start'), entity.get('end')
                
                entity_key = f"{entity_name}:{start}-{end}"
                
                if entity_key not in entity_dict[id_]["entities"]:
                    entity_dict[id_]["entities"][entity_key] = [None] * len(annotations)
                
                entity_dict[id_]["entities"][entity_key][i] = (word, start, end)
    return entity_dict

def compare_entities(entity_dict, file_names):
    """Generate comparison table highlighting words that are not common across files."""
    html_output = "<html><body>"
    for id_, data in entity_dict.items():
        html_output += f"<h3>ID: {id_}</h3><p>{data['text']}</p>"
        
        sorted_entities = sorted(
            data["entities"].items(), 
            key=lambda x: (x[0].split(":")[0], int(x[0].split(":")[1].split("-")[0]))
        )
        
        # Table header
        html_output += "<table border='1'><tr><th>Entity</th>"
        for file_name in file_names:
            html_output += f"<th>{file_name}</th>"
        html_output += "</tr>"
        
        for entity_key, words in sorted_entities:
            entity_name = entity_key.split(":")[0]
            row = f"<tr><td>{entity_name}</td>"
            
            present_count = sum(1 for word_data in words if word_data is not None)
            
            for word_data in words:
                cell_content = ""
                if word_data is not None:
                    word, start, end = word_data
                    cell_content = f"{word} ({start}-{end})"
                if word_data is not None and present_count < len(words):
                    cell_content = f"<span style='color:red'>{cell_content}</span>"
                
                row += f"<td>{cell_content}</td>"
            row += "</tr>"
            html_output += row
        
        html_output += "</table><br><br>"
    html_output += "</body></html>"
    
    return html_output

st.title("JSON Entity Comparison Tool")

# Upload three files
uploaded_files = st.file_uploader("Upload three JSON files", type="jsonl", accept_multiple_files=True, key="json_upload")
if len(uploaded_files) == 3:
    file_names = []
    for i, uploaded_file in enumerate(uploaded_files):
        file_name = st.text_input(f"Rename File {i + 1}", uploaded_file.name)
        file_names.append(file_name)
    
    if st.button("Generate Comparison Report"):
        annotations = load_annotations(uploaded_files)
        entity_data = extract_entities(annotations)
        html_output = compare_entities(entity_data, file_names)
        
        st.components.v1.html(html_output, height=600, scrolling=True)
