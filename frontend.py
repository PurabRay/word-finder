
# import streamlit as st
# from PIL import Image
# import plotly.graph_objects as go
# from my_ocr_utils import extract_word_boxes
# import io
# import base64
# import re

# st.set_page_config(layout="wide")
# st.title("OCR Document Preview with Search-Based Field Highlight")

# # Upload a document image
# uploaded_file = st.file_uploader("Upload a scanned document (image)", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     st.write("✅ File uploaded:", uploaded_file.name)
#     try:
#         image, boxes = extract_word_boxes(uploaded_file)
#     except Exception as e:
#         st.error(f"❌ Error during OCR extraction: {e}")
#         st.stop()

#     if not boxes:
#         st.warning("⚠️ No text was detected by OCR.")
#         st.stop()

#     st.write(f"🧠 Extracted {len(boxes)} text boxes")
    
#     # Get image dimensions
#     img_width, img_height = image.size
#     st.write(f"🖼️ Image size: width = {img_width}, height = {img_height}")
    
#     # --- Group boxes by line ---
#     lines = {}
#     for box in boxes:
#         key = (box.get('block_num', 0), box.get('line_num', 0))
#         if key not in lines:
#             lines[key] = []
#         lines[key].append(box)
    
#     # Build a list of line entries with combined text and bounding box info.
#     line_entries = []
#     for key, group in lines.items():
#         # Sort by x-coordinate
#         group = sorted(group, key=lambda b: b['left'])
#         line_text = " ".join([b['text'] for b in group])
#         # Compute a bounding box for the entire line
#         left = min(b['left'] for b in group)
#         top = min(b['top'] for b in group)
#         right = max(b['left'] + b['width'] for b in group)
#         bottom = max(b['top'] + b['height'] for b in group)
#         width_box = right - left
#         height_box = bottom - top
#         line_entries.append({
#             'key': key,
#             'text': line_text,
#             'left': left,
#             'top': top,
#             'width': width_box,
#             'height': height_box,
#             'boxes': group
#         })
    
#     # --- Layout: left panel for search, right for image preview ---
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.subheader("Search in Document")
#         search_query = st.text_input("Enter text to search for:")
        
#         matching_phrases = []
#         if search_query:
#             search_query_lower = search_query.lower()
#             st.write(f"Searching for: '{search_query}'")
            
#             # Find matches for multi-word phrases within each line
#             for line_entry in line_entries:
#                 line_text = line_entry['text']
#                 line_text_lower = line_text.lower()
                
#                 # Find all occurrences of the phrase in this line
#                 start_idx = 0
#                 while True:
#                     pos = line_text_lower.find(search_query_lower, start_idx)
#                     if pos == -1:
#                         break
                        
#                     # We found a match in this line
#                     matched_phrase = line_text[pos:pos + len(search_query)]
                    
#                     # Now determine which word boxes this phrase spans
#                     phrase_start_pos = pos
#                     phrase_end_pos = pos + len(search_query)
                    
#                     # Track running position within line text
#                     current_pos = 0
#                     phrase_boxes = []
                    
#                     # For each word box in the line
#                     for box in line_entry['boxes']:
#                         word_start = current_pos
#                         word_text = box['text']
#                         word_end = word_start + len(word_text)
                        
#                         # Add space after word (except last word)
#                         if word_end < len(line_text):
#                             word_end += 1
                            
#                         # Check if this word box overlaps with our phrase
#                         if word_end > phrase_start_pos and word_start < phrase_end_pos:
#                             phrase_boxes.append(box)
                            
#                         current_pos = word_end
                    
#                     # If we found matching boxes, calculate the combined bounding box
#                     if phrase_boxes:
#                         left = min(b['left'] for b in phrase_boxes)
#                         top = min(b['top'] for b in phrase_boxes)
#                         right = max(b['left'] + b['width'] for b in phrase_boxes)
#                         bottom = max(b['top'] + b['height'] for b in phrase_boxes)
                        
#                         matching_phrases.append({
#                             'text': matched_phrase,
#                             'left': left,
#                             'top': top,
#                             'width': right - left,
#                             'height': bottom - top,
#                             'line_entry': line_entry
#                         })
                    
#                     # Move to next potential match
#                     start_idx = pos + 1
            
#             if matching_phrases:
#                 st.write(f"Found {len(matching_phrases)} matches:")
#                 for idx, match in enumerate(matching_phrases):
#                     st.write(f"{idx+1}. '{match['text']}' in line: '{match['line_entry']['text']}'")
#             else:
#                 st.write("No matches found.")
    
#     with col2:
#         st.write("📊 Generating interactive preview...")
#         fig = go.Figure()
        
#         # Convert image to base64 for Plotly
#         try:
#             img_bytes = io.BytesIO()
#             image.save(img_bytes, format="PNG")
#             encoded = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
#             st.write("✅ Image encoded to base64")
#         except Exception as e:
#             st.error(f"❌ Error converting image: {e}")
#             st.stop()
        
#         # Place the image as the background.
#         fig.add_layout_image(
#             dict(
#                 source=f"data:image/png;base64,{encoded}",
#                 x=0,
#                 y=img_height,  # Anchor at the top
#                 sizex=img_width,
#                 sizey=img_height,
#                 xref="x",
#                 yref="y",
#                 xanchor="left",
#                 yanchor="top",
#                 sizing="stretch",
#                 layer="below"
#             )
#         )
        
#         # Set axes: (0,0) is bottom left.
#         fig.update_xaxes(visible=False, range=[0, img_width])
#         fig.update_yaxes(visible=False, range=[0, img_height])
        
#         # Draw bounding boxes only for matching phrases
#         for match in matching_phrases:
#             # Transform OCR coordinates (top-left origin) to Plotly's coordinate system:
#             new_top = img_height - match["top"] - match["height"]
#             x0 = match["left"]
#             y0 = new_top
#             x1 = match["left"] + match["width"]
#             y1 = new_top + match["height"]
            
#             fig.add_shape(
#                 type="rect",
#                 x0=x0,
#                 y0=y0,
#                 x1=x1,
#                 y1=y1,
#                 line=dict(color="red"),
#                 fillcolor="rgba(255,0,0,0.3)",
#                 opacity=0.7,
#                 layer="above"
#             )
        
#         fig.update_layout(
#             width=img_width,
#             height=img_height,
#             margin=dict(l=0, r=0, t=0, b=0)
#         )
        
#         st.plotly_chart(fig, use_container_width=True)
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from my_ocr_utils import extract_word_boxes
import io
import base64

st.set_page_config(layout="wide")
st.title("OCR Document Preview with Search-Based Phrase Highlight")

# Upload a document image
uploaded_file = st.file_uploader("Upload a scanned document (image)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.write("✅ File uploaded:", uploaded_file.name)
    try:
        image, boxes = extract_word_boxes(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error during OCR extraction: {e}")
        st.stop()

    if not boxes:
        st.warning("⚠️ No text was detected by OCR.")
        st.stop()

    st.write(f"🧠 Extracted {len(boxes)} text boxes")
    
    # Get image dimensions
    img_width, img_height = image.size
    st.write(f"🖼️ Image size: width = {img_width}, height = {img_height}")
    
    # --- Group boxes by line ---
    lines = {}
    for box in boxes:
        key = (box.get('block_num', 0), box.get('line_num', 0))
        if key not in lines:
            lines[key] = []
        lines[key].append(box)
    
    # Build a list of line entries with combined text and word info
    line_entries = []
    for key, group in lines.items():
        # Sort by x-coordinate
        group = sorted(group, key=lambda b: b['left'])
        
        # Keep track of word positions in the combined text
        word_positions = []
        current_pos = 0
        line_text = ""
        
        for box in group:
            # Add space before all but the first word
            space = " " if line_text else ""
            
            # Record position of this word in the combined line text
            word_positions.append({
                'start': len(line_text + space),
                'end': len(line_text + space + box['text']),
                'box': box
            })
            
            # Add to line text
            line_text += space + box['text']
        
        # Compute a bounding box for the entire line
        left = min(b['left'] for b in group)
        top = min(b['top'] for b in group)
        right = max(b['left'] + b['width'] for b in group)
        bottom = max(b['top'] + b['height'] for b in group)
        
        line_entries.append({
            'key': key,
            'text': line_text,
            'left': left,
            'top': top,
            'width': right - left,
            'height': bottom - top,
            'word_positions': word_positions
        })
    
    # --- Layout: left panel for search, right for image preview ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Search in Document")
        search_query = st.text_input("Enter text to search for:")
        
        matching_phrases = []
        if search_query:
            search_query_lower = search_query.lower()
            st.write(f"Searching for: '{search_query}'")
            
            # Look for the phrase in each line
            for line_entry in line_entries:
                line_text = line_entry['text']
                line_text_lower = line_text.lower()
                
                # Find all occurrences of the phrase
                start_idx = 0
                while True:
                    pos = line_text_lower.find(search_query_lower, start_idx)
                    if pos == -1:
                        break
                    
                    # Found a match - determine which word boxes it spans
                    phrase_start = pos
                    phrase_end = pos + len(search_query)
                    
                    # Find all word boxes that overlap with this phrase
                    overlapping_boxes = []
                    for word_pos in line_entry['word_positions']:
                        # Check if this word overlaps with our phrase
                        if not (word_pos['end'] <= phrase_start or word_pos['start'] >= phrase_end):
                            overlapping_boxes.append(word_pos['box'])
                    
                    # Calculate the combined bounding box for all overlapping words
                    if overlapping_boxes:
                        left = min(b['left'] for b in overlapping_boxes)
                        top = min(b['top'] for b in overlapping_boxes)
                        right = max(b['left'] + b['width'] for b in overlapping_boxes)
                        bottom = max(b['top'] + b['height'] for b in overlapping_boxes)
                        
                        matching_phrases.append({
                            'text': line_text[phrase_start:phrase_end],
                            'left': left,
                            'top': top, 
                            'width': right - left,
                            'height': bottom - top,
                            'line_text': line_text
                        })
                    
                    # Move past this match
                    start_idx = pos + 1
            
            if matching_phrases:
                st.write(f"Found {len(matching_phrases)} matches:")
                for idx, match in enumerate(matching_phrases):
                    st.write(f"{idx+1}. '{match['text']}' in: '{match['line_text']}'")
            else:
                st.write("No matches found.")
    
    with col2:
        st.write("📊 Generating interactive preview...")
        fig = go.Figure()
        
        # Convert image to base64 for Plotly
        try:
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            encoded = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
            st.write("✅ Image encoded to base64")
        except Exception as e:
            st.error(f"❌ Error converting image: {e}")
            st.stop()
        
        # Place the image as the background.
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{encoded}",
                x=0,
                y=img_height,  # Anchor at the top
                sizex=img_width,
                sizey=img_height,
                xref="x",
                yref="y",
                xanchor="left",
                yanchor="top",
                sizing="stretch",
                layer="below"
            )
        )
        
        # Set axes: (0,0) is bottom left.
        fig.update_xaxes(visible=False, range=[0, img_width])
        fig.update_yaxes(visible=False, range=[0, img_height])
        
        # Draw bounding boxes for matching phrases
        for match in matching_phrases:
            # Transform OCR coordinates (top-left origin) to Plotly's coordinate system:
            new_top = img_height - match["top"] - match["height"]
            x0 = match["left"]
            y0 = new_top
            x1 = match["left"] + match["width"]
            y1 = new_top + match["height"]
            
            fig.add_shape(
                type="rect",
                x0=x0,
                y0=y0,
                x1=x1,
                y1=y1,
                line=dict(color="red"),
                fillcolor="rgba(255,0,0,0.3)",
                opacity=0.7,
                layer="above"
            )
        
        fig.update_layout(
            width=img_width,
            height=img_height,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)