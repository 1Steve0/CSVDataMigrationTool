CSV Data Migration Tool – Instructions
This tool provides a modular interface for ingesting, transforming, and exporting CSV data for system migration. It supports adapter-driven logic for remapping column headers, manipulating data, and resolving relationships between legacy and target systems.

Getting Started
- Launch the Tool
Run the Flask app locally using:
python app.py
The user interface will be available at http://localhost:5000
- Select Your Input
Use the UI to upload the source CSV file
Choose the appropriate adapter from the dropdown menu
- Transformation and Output
The tool will:
- Remap column headers to match the target system
- Apply any required data manipulation
- Generate clean output CSVs for downstream ingestion
- Relationship Mapping
For relationship files, supply a mapping CSV containing:
- Legacy IDs (from the source system)
- New System IDs (from the target system)
The tool will resolve and remap relationships using this data
- Audit and Review
- All transformations are logged
- Output files are structured for easy validation
- Adapter logic is modular and transparent

Adapter Philosophy
Each adapter is designed to:
- Handle edge cases gracefully
- Suppress noise and unwanted output
- Maintain row integrity and fallback logic
- Align backend logic with real-world workflows

Let me know if you'd like a version with example filenames or adapter descriptions — I can help tailor it for internal documentation or onboarding.
