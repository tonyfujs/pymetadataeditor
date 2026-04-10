# How-To: Batch Upload from a Custom Excel File

This guide shows how to bulk-create metadata records from a custom spreadsheet where each row represents one record.

---

## Scenario

You have an Excel file with indicators listed one per row, like this:

| name | idno | doi | definition_long |
|------|------|-----|-----------------|
| GDP per capita | GDP_PC_001 | 10.1234/5678 | GDP divided by population... |
| Poverty rate | POV_RATE_001 | 10.1234/5679 | Share of population below poverty line... |

---

## Setup

```python
from pymetadataeditor import MetadataEditor
import pandas as pd
import os

me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
)
```

## Steps

```python
# Step 1: Read the Excel file
df = pd.read_excel("my_indicators.xlsx")

uploaded_ids = []

# Step 2: Iterate over each row
for _, row in df.iterrows():

    # Step 3: Start from an empty metadata outline
    metadata = me.make_metadata_outline("indicator", output_mode="pydantic")

    # Step 4: Map your columns to the metadata fields
    # Adjust the field names to match your Excel columns and target schema
    metadata.series_description.idno = row["idno"]
    metadata.series_description.name = row["name"]
    metadata.series_description.definition_long = row["definition_long"]
    if pd.notna(row.get("doi")):
        metadata.series_description.doi = row["doi"]

    # Step 5: Log the metadata to the database
    new_id = me.create_project_log(metadata)
    uploaded_ids.append(new_id)
    print(f"Created: {row['name']} → id {new_id}")

print(f"\nUploaded {len(uploaded_ids)} records.")
```

---

## Tips

- Use `make_metadata_outline("indicator", output_mode="pydantic")` and tab-complete to discover the exact field paths for your metadata type.
- Wrap the loop in a `try/except` to handle rows with missing required fields without aborting the whole batch.
- Save `uploaded_ids` to a file so you can track what was created.
