import os
import pandas as pd

def process_relationship_files(selected_file, **kwargs):
    CM_ID_Lookup_directory = r"C:\Users\steve\OneDrive\Documents\SPP\Project\SWC\CM ID Lookup"
    relationship_dir = r"C:\Users\steve\OneDrive\Documents\SPP\Project\SWC\Legacy Relationships"
    output_dir = r"C:\Users\steve\OneDrive\Documents\SPP\Project\SWC\output\cm_relationships_csv"
    os.makedirs(output_dir, exist_ok=True)

    # Summary counters
    written_count = 0
    skipped_count = 0
    unmatched_log = []

    # Load lookup maps
    core_lookup_maps = {}
    CM_ID_Lookup_file_names = [
        "Action.csv", "Complaint.csv", "Document.csv", "Event.csv", 
        "Property.csv", "Stakeholder.csv", "Organisation.csv"
    ]
    for fname in CM_ID_Lookup_file_names:
        full_path = os.path.join(CM_ID_Lookup_directory, fname)
        entity = fname.replace(".csv", "").lower()

        if os.path.isfile(full_path):
            print(f"🔍 Inspecting {fname}")
            df = pd.read_csv(full_path)
            df.columns = [col.strip() for col in df.columns]

            if df.empty:
                print(f"⚠️ Skipping {fname} — file is empty.")
                continue

            if "Id" in df.columns and "Legacy Id (Admin Only)" in df.columns:
                core_lookup_maps[entity] = {
                    str(row["Legacy Id (Admin Only)"]).strip(): row["Id"]
                    for _, row in df.iterrows()
                    if pd.notna(row["Legacy Id (Admin Only)"])
                }
                print(f"✅ Loaded lookup map: {fname}")
            else:
                print(f"❌ Missing columns in {fname}")
                print(f"❌ columns are: {df.columns}")
                if "Id" in df.columns:
                    print(f"Id: True")
        else:
            print(f"❌ Missing file: {fname}")

    # Process relationship files
    legacy_relationship_file_names = [
        # "Action Document relationship.csv", 
        "Complaint Action Relationship.csv",
        "Complaint Document Relationship.csv", "Complaint Event Relationship.csv",
        "Complaint Property Relationship.csv", "Complaint Stakeholder Relationship.csv",
        "Document Stakeholder relationship.csv", "Event Action relationship.csv",
        "Event Document relationship.csv", "Organisation Action Relationship.csv",
        "Organisation Complaint Relationship.csv", "Organisation Document Relationship.csv",
        "Organisation Event Relationship.csv", "Organisation Property Relationship.csv",
        "Organisation Stakeholder Relationship.csv", "Stakeholder Event.csv",
        "Stakeholder Property.csv", "property Action relationship.csv",
        "property Document relationship.csv", "property Event relationship.csv"
    ]

    for fname in legacy_relationship_file_names:
        full_path = os.path.join(relationship_dir, fname)

        if not os.path.isfile(full_path):
            print(f"❌ Missing relationship file: {fname}")
            skipped_count += 1
            continue

        df = pd.read_csv(full_path)
        if df.columns is None or not isinstance(df.columns, pd.Index):
            print(f"❌ {fname} has no valid columns — skipping.")
            skipped_count += 1
            continue

        df.columns = [col.strip() for col in df.columns]
        columns = [col for col in df.columns if col.lower() != "id"]

        if df.empty:
            print(f"⚠️ {fname} has headers but no data — writing empty output with headers.")
            output_df = pd.DataFrame(columns=columns)
            output_path = os.path.join(output_dir, fname)
            output_df.to_csv(output_path, index=False)
            print(f"📄 Written: {output_path}")
            written_count += 1
            continue

        missing_entities = [col for col in columns if col.lower() not in core_lookup_maps]
        if missing_entities:
            print(f"⚠️ Skipping {fname} due to unknown entity columns: {missing_entities}")
            skipped_count += 1
            continue

        resolved_rows = []
        for _, row in df.iterrows():
            resolved = []
            for col in columns:
                entity = col.lower()
                legacy_value = str(row[col]).strip()
                resolved_id = core_lookup_maps[entity].get(legacy_value, 0)
                resolved.append(resolved_id)
                if resolved_id == 0 and pd.notna(legacy_value):
                    unmatched_log.append({
                        "relationship_file": fname,
                        "column": col,
                        "legacy_value": legacy_value,
                        "row_index": row.name
                    })
            resolved_rows.append(resolved)

        try:
            output_df = pd.DataFrame(resolved_rows, columns=columns)
        except Exception as e:
            print(f"❌ Failed to create DataFrame for {fname}: {e}")
            skipped_count += 1
            continue

        output_path = os.path.join(output_dir, fname)
        output_df.to_csv(output_path, index=False)
        print(f"📄 Written: {output_path}")
        written_count += 1

    # Write unmatched log if needed
    unmatched_count = len(unmatched_log)
    if unmatched_count:
        unmatched_df = pd.DataFrame(unmatched_log)
        unmatched_df.sort_values(by=["relationship_file", "column", "legacy_value"], inplace=True)
        unmatched_path = os.path.join(output_dir, "unmatched_ids_log.csv")
        unmatched_df.to_csv(unmatched_path, index=False)
        print(f"📝 Unmatched log written: {unmatched_path}")
    else:
        print("✅ No unmatched legacy IDs found.")

    # Return summary
    return {
        "total_files": len(legacy_relationship_file_names),
        "skipped": skipped_count,
        "written": written_count,
        "unmatched": unmatched_count
    }

def transform(selected_file, **kwargs):
    return process_relationship_files(selected_file=selected_file, **kwargs)

def save_transformed(*args, **kwargs):
    print("No save_transformed logic required for this adapter.")