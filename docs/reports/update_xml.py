import os
import re

# Paths
base_dir = r"c:\Users\sreya\OneDrive\Desktop\Project\docs\extracted_format"
document_xml_path = os.path.join(base_dir, "word", "document.xml")
core_xml_path = os.path.join(base_dir, "docProps", "core.xml")

# New Data
PROJECT_TITLE = "Cyber Attack Prediction: From Traditional ML to Generative AI"
GUIDE_NAME = "Mr. Rasmi Roy Badakumar"
TEAM = [
    {"name": "ANKITA PATI", "roll": "23PBCA1335"},
    {"name": "KUMAR SREYAN PATTANAYAK", "roll": "23PBCA1355"},
    {"name": "SUBHASHREE PATHY", "roll": "23PBCA1386"},
    {"name": "TANMAYA RANJAN JENA", "roll": "23PBCA1391"}
]

# Replacement Mapping
replaces = {
    # Titles
    "Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks": PROJECT_TITLE,
    "Explainable AI-Driven Dew Point Prediction using Ensemble and Hybrid Stacking Models": PROJECT_TITLE,
    "Health Center Management System": PROJECT_TITLE,
    "HEALTH CENTER MANAGEMENT SYSTEM": PROJECT_TITLE.upper(),
    
    # Guide
    "GUIDE NAME": GUIDE_NAME,
    "(guide name)": f"({GUIDE_NAME})",
    
    # Student Names (Full forms as appearing in XML)
    "Shubhashish Jena": TEAM[0]["name"],
    "M Gayathri": TEAM[1]["name"],
    "Ch Venkata Rajesh": TEAM[2]["name"],
    "D Lokesh Babu": TEAM[3]["name"],
    "KALYANI PRADHAN": TEAM[0]["name"],
    "KANCHAN PATNAIK": TEAM[1]["name"],
    "MANASMITA PANDA": TEAM[2]["name"],

    # Roll Numbers
    "16221A05A3": TEAM[0]["roll"],
    "16221A0587": TEAM[1]["roll"],
    "16221A0573": TEAM[2]["roll"],
    "16221A0576": TEAM[3]["roll"],
    "23PBCA13XX": TEAM[0]["roll"], # Fix what I did earlier incorrectly
}

if os.path.exists(document_xml_path):
    with open(document_xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replaces.items():
        content = content.replace(old, new)
    
    # Generic registration number update
    content = content.replace("REGD/2023", "2023-2026") # Or whatever is appropriate

    with open(document_xml_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated document.xml thoroughly")
