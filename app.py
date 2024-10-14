

# # Specify the file paths of the three JSON files
# # file_paths = ["/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy 2.jsonl"]

# import json
# import pandas as pd
# from IPython.display import HTML

# def load_annotations(file_paths):
#     """Load JSON annotations from multiple files."""
#     annotations = []
#     for file_path in file_paths:
#         with open(file_path, 'r') as f:
#             annotations.append([json.loads(line) for line in f])
#     return annotations

# def extract_entities(annotations):
#     """Extract entity annotations and organize them by ID."""
#     entity_dict = {}
#     for i, file_data in enumerate(annotations):
#         for item in file_data:
#             id_ = item.get('id', f'Unknown_ID_{i}')
#             text = item.get('displayed_text', "Text not available")
#             if id_ not in entity_dict:
#                 entity_dict[id_] = {"text": text, "entities": {}}
#             for entity in item.get('span_annotations', []):
#                 entity_name = entity.get('annotation', 'Unknown_Label')
#                 word = entity.get('span', 'Unknown_Word')
#                 if entity_name not in entity_dict[id_]["entities"]:
#                     entity_dict[id_]["entities"][entity_name] = [set() for _ in range(len(annotations))]
#                 entity_dict[id_]["entities"][entity_name][i].add(word)
#     return entity_dict

# def compare_entities(entity_dict):
#     """Generate comparison table highlighting words that are not common across files."""
#     html_output = "<html><body>"

#     for id_, data in entity_dict.items():
#         html_output += f"<h3>ID: {id_}</h3><p>{data['text']}</p>"
        
#         # Create a table for entities
#         html_output += "<table border='1'><tr><th>Entity</th><th>File 1</th><th>File 2</th><th>File 3</th></tr>"
        
#         for entity, word_sets in data["entities"].items():
#             row = f"<tr><td>{entity}</td>"
#             all_words = set.union(*word_sets)
#             for i in range(len(word_sets)):
#                 words = word_sets[i]
#                 cell_content = ""
#                 for word in all_words:
#                     if word in words:
#                         cell_content += f"{word} "
#                     else:
#                         cell_content += f"<span style='color:red'>{word}</span> "
#                 row += f"<td>{cell_content.strip()}</td>"
#             row += "</tr>"
#             html_output += row
        
#         html_output += "</table><br><br>"
#     html_output += "</body></html>"
    
#     # Save HTML to file
#     with open("annotated_comparison.html", "w") as file:
#         file.write(html_output)
    
#     print("HTML report generated as 'annotated_comparison.html'.")

# # Specify the file paths of the three JSON files
# file_paths = ["/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy 2.jsonl"]

# # Load, process, and generate HTML report
# annotations = load_annotations(file_paths)
# entity_data = extract_entities(annotations)
# compare_entities(entity_data)
# _____________________________________________________________


# import json

# def load_annotations(file_paths):
#     """Load JSON annotations from multiple files."""
#     annotations = []
#     for file_path in file_paths:
#         with open(file_path, 'r') as f:
#             annotations.append([json.loads(line) for line in f])
#     return annotations

# def extract_entities(annotations):
#     """Extract entity annotations and organize them by ID."""
#     entity_dict = {}
#     for i, file_data in enumerate(annotations):
#         for item in file_data:
#             id_ = item.get('id', f'Unknown_ID_{i}')
#             text = item.get('displayed_text', "Text not available")
#             if id_ not in entity_dict:
#                 entity_dict[id_] = {"text": text, "entities": {}}
#             for entity in item.get('span_annotations', []):
#                 entity_name = entity.get('annotation', 'Unknown_Label')
#                 word = entity.get('span', 'Unknown_Word')
#                 start, end = entity.get('start'), entity.get('end')
                
#                 # Use unique key for each annotation, combining name, start, and end to differentiate similar entities
#                 entity_key = f"{entity_name}:{start}-{end}"
                
#                 if entity_key not in entity_dict[id_]["entities"]:
#                     entity_dict[id_]["entities"][entity_key] = [None] * len(annotations)
                
#                 entity_dict[id_]["entities"][entity_key][i] = (word, start, end)
#     return entity_dict

# def compare_entities(entity_dict):
#     """Generate comparison table highlighting words that are not common across files."""
#     html_output = "<html><body>"

#     for id_, data in entity_dict.items():
#         html_output += f"<h3>ID: {id_}</h3><p>{data['text']}</p>"
        
#         # Sort entities by type (e.g., "PERSON" entities together)
#         sorted_entities = sorted(data["entities"].items(), key=lambda x: x[0].split(":")[0])
        
#         # Create a table for entities
#         html_output += "<table border='1'><tr><th>Entity</th><th>File 1</th><th>File 2</th><th>File 3</th></tr>"
        
#         for entity_key, words in sorted_entities:
#             entity_name = entity_key.split(":")[0]  # Get only the entity name (e.g., "GPE")
#             row = f"<tr><td>{entity_name}</td>"
            
#             # Count how many columns contain this entity
#             present_count = sum(1 for word_data in words if word_data is not None)
            
#             for word_data in words:
#                 if word_data is None:
#                     # If word is missing in this file, leave the cell empty
#                     cell_content = ""
#                 else:
#                     word, start, end = word_data
#                     # Display the word along with its position
#                     cell_content = f"{word} ({start}-{end})"
                
#                 # Highlight the cell content in red if it's unique to one or two files
#                 if word_data is not None and present_count < len(words):
#                     cell_content = f"<span style='color:red'>{cell_content}</span>"
                
#                 row += f"<td>{cell_content}</td>"
#             row += "</tr>"
#             html_output += row
        
#         html_output += "</table><br><br>"
#     html_output += "</body></html>"
    
#     # Save HTML to file
#     with open("annotated_comparison.html", "w") as file:
#         file.write(html_output)
    
#     print("HTML report generated as 'annotated_comparison.html'.")

# # Specify the file paths of the three JSON files
# file_paths = ["/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy 2.jsonl"]

# # Load, process, and generate HTML report
# annotations = load_annotations(file_paths)
# entity_data = extract_entities(annotations)
# compare_entities(entity_data)

#________________________________________________________________

import json

def load_annotations(file_paths):
    """Load JSON annotations from multiple files."""
    annotations = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            annotations.append([json.loads(line) for line in f])
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
                
                # Use unique key for each annotation, combining name, start, and end to differentiate similar entities
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
        
        # Sort entities by type and then by start position
        sorted_entities = sorted(
            data["entities"].items(), 
            key=lambda x: (x[0].split(":")[0], int(x[0].split(":")[1].split("-")[0]))
        )
        
        # Create a table for entities with custom file names
        html_output += "<table border='1'><tr><th>Entity</th>"
        for file_name in file_names:
            html_output += f"<th>{file_name}</th>"
        html_output += "</tr>"
        
        for entity_key, words in sorted_entities:
            entity_name = entity_key.split(":")[0]  # Get only the entity name (e.g., "GPE")
            row = f"<tr><td>{entity_name}</td>"
            
            # Count how many columns contain this entity
            present_count = sum(1 for word_data in words if word_data is not None)
            
            for word_data in words:
                if word_data is None:
                    # If word is missing in this file, leave the cell empty
                    cell_content = ""
                else:
                    word, start, end = word_data
                    # Display the word along with its position
                    cell_content = f"{word} ({start}-{end})"
                
                # Highlight the cell content in red if it's unique to one or two files
                if word_data is not None and present_count < len(words):
                    cell_content = f"<span style='color:red'>{cell_content}</span>"
                
                row += f"<td>{cell_content}</td>"
            row += "</tr>"
            html_output += row
        
        html_output += "</table><br><br>"
    html_output += "</body></html>"
    
    # Save HTML to file
    with open("annotated_comparison.html", "w") as file:
        file.write(html_output)
    
    print("HTML report generated as 'annotated_comparison.html'.")

# Specify the file paths of the three JSON files and corresponding custom names
file_paths = ["/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy.jsonl", "/Users/shreya/FALL24/CAPSTONE/part2/display/annotated_instances copy 2.jsonl"]
file_names = ["Custom File Name 1", "Custom File Name 2", "Custom File Name 3"]

# Load, process, and generate HTML report
annotations = load_annotations(file_paths)
entity_data = extract_entities(annotations)
compare_entities(entity_data, file_names)
