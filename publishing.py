import requests
import pandas as pd
import numpy as np
import time
import json
from datetime import date
import yaml
import os
import sys
import shutil
import pysdmx as px

meta_url = "https://metadataeditor-url.org"

today = date.today().isoformat()
dm = date.today().strftime("%Y-%m")

# Section 1: Interpret schema pkl file
def get_codelist_pairs(comp, coded_comp):
    """
    Retrieve all codelist code-label pairs for given coded components.

    Args:
        comp (list): List of components.
        coded_comp (list): List of coded components.

    Returns:
        dict: Dictionary with coded components as keys and list of (code, label) pairs as values.
    """
    codelist_dict = {}
    for component in coded_comp:
        codes = comp[component].local_codes.items
        codelist_dict[component] = [
            (code.id, getattr(code, "name", code.id))  # fallback to id if name missing
            for code in codes
        ]
    return codelist_dict

def extract_validation_info(schema):
    """
    Extract validation information from a given schema, including code-label pairs.

    Args:
        schema: The schema object containing validation information.

    Returns:
        dict: A dictionary containing validation information:
            - valid_comp: List of valid component names.
            - mandatory_comp: List of mandatory component names.
            - coded_comp: List of coded component names.
            - codelists: Dictionary with coded components as keys and list of (code, label) pairs.
            - dim_comp: List of dimension component names.
    """
    comp = schema.components
    coded = [c.id for c in comp if comp[c.id].local_codes is not None]

    validation_info = {
        "valid_comp": [c.id for c in comp],
        "mandatory_comp": [c.id for c in comp if comp[c.id].required],
        "coded_comp": coded,
        "codelists": get_codelist_pairs(comp, coded),
        "dim_comp": [c.id for c in comp if comp[c.id].role == px.model.Role.DIMENSION],
    }
    return validation_info

def extract_schema_summary(schema):
    """
    Extract schema summary from parsed pickle file.
    
    Returns a dict with:
      - dim_comp: list of component IDs that are DIMENSIONS
      - components: DataFrame with component details
    """
    rows = []

    for comp in schema.components.data:
        row = {
            "component_id": comp.id,
            "component_name": comp.name,
            "role": getattr(comp.role, "name", None),  # DIMENSION, ATTRIBUTE, etc.
            "required": getattr(comp, "required", False),
            "codelist_id": getattr(comp.local_codes, "id", None) if comp.local_codes else None,
            "codelist_name": getattr(comp.local_codes, "name", None) if comp.local_codes else None
        }
        rows.append(row)

    return pd.DataFrame(rows)

def build_lookup_dict(validation_info):
    """
    Convert validation_info['codelists'] into nested dicts for easy mapping.
    Example: { "REF_AREA": {"AFG": "Afghanistan", "WLD": "World"}, ... }
    """
    lookup = {}
    for comp, pairs in validation_info["codelists"].items():
        lookup[comp] = {code: label for code, label in pairs}
    return lookup

# Section 2: Use pkl content for metadata
def get_dimensions_with_lookup_dict(df, schema_summary, lookup_dict):
    """
    Extract dimensions covered by each indicator based on schema summary df.
    Logic:
      - Only include components with role == "DIMENSION" (from schema_summary)
      - Use component_name for labels
      - "FREQ", "INDICATOR", "OBS_VALUE" are skipped
      - Special handling for REF_AREA, SEX, URBANISATION, AGE
      - COMP_BREAKDOWN_* columns map codes using lookup_dict and extract human-readable dimension label
    """
    # Only DIMENSION components
    dim_list = schema_summary.loc[schema_summary["role"] == "DIMENSION", "component_id"].values

    # Only consider rows with non-null OBS_VALUE
    df_valid = df[df["OBS_VALUE"].notna()]

    indicator_dimension = {}

    for ind, subdf in df_valid.groupby("INDICATOR"):
        values = set()

        for dim in dim_list:
            # Skip non-breakdown columns
            if dim in ["INDICATOR", "OBS_VALUE", "FREQ", "UNIT_MEASURE"]:
                continue

            # Special handling for certain dimensions
            if dim == "REF_AREA":
                values.add(("Geographic area", "Country/economy, Region"))
                continue
            elif dim == "SEX":
                unique_vals = df["SEX"].dropna().unique()
                if len(unique_vals) > 1:
                    values.add(("Sex", "Total, Male, Female"))
                continue

            elif dim == "URBANISATION":
                unique_vals = df["URBANISATION"].dropna().unique()
                if len(unique_vals) > 1:
                    values.add(("Residential area", "Total, Urban, Rural"))
                continue

            elif dim == "AGE":
                unique_vals = df["AGE"].dropna().unique()
                if len(unique_vals) > 1:
                    values.add(("Age", ""))
                continue

            # Handle COMP_BREAKDOWN_* columns if present
            comp_breakdown_cols = [c for c in ["COMP_BREAKDOWN_1", "COMP_BREAKDOWN_2", "COMP_BREAKDOWN_3"] if c in subdf.columns]
            if comp_breakdown_cols:
                for col in comp_breakdown_cols:
                    # Flatten and get unique codes
                    codes = subdf[col].explode().unique() if subdf[col].apply(lambda x: isinstance(x, list)).any() else subdf[col].unique()
                    for code in codes:
                        if code in ["_T", "_Z"]:
                            continue
                        # Map code to human-readable value using codelist for that column
                        mapped_value = lookup_dict.get(col, {}).get(code, code)
                        # Extract dimension label (part before ":" if present)
                        dimension_label = mapped_value.split(":")[0].strip() if ":" in mapped_value else mapped_value
                        values.add((dimension_label, ""))

            else:
                # Fallback: use component_name from schema_summary
                comp_name = schema_summary.loc[schema_summary["component_id"] == dim, "component_name"].values
                if len(comp_name) > 0:
                    values.add((comp_name[0], ""))  # Use human-readable name

        # Build final list of dicts
        indicator_dimension[ind] = [
            {"label": v[0]} if v[1] == "" else {"label": v[0], "description": v[1]}
            for v in values
        ]

    return indicator_dimension

# Section 3: build metadata tables
def build_indicator_metadata_summary(df, schema, env, lookup_dict, schema_summary, country_codes):
    """
    Build metadata summary table with correct REF_COUNTRY and cleaned UNIT_MEASURE.

    Args:
        df (pd.DataFrame): Raw SDMX-style data with coded columns.
        validation_info (dict): Info containing codelists for translation.
        env: Environment for fetching country codes.

    Returns:
        pd.DataFrame: Metadata summary table.
    """
    # Get dimension
    dimensions_dict = get_dimensions_with_lookup_dict(df, schema_summary, lookup_dict)
    
    # Group by original codes
    id_column = None
    for col in ["DATABASE_ID", "DATASET_ID"]:
        if col in df.columns:
            id_column = col
            break

    if id_column is None:
        raise ValueError("❌ Neither 'DATABASE_ID' nor 'DATASET_ID' found in DataFrame columns.")

    # Dynamically build group columns
    group_cols = [id_column, "INDICATOR"]
    summary_rows = []

    for (db_code, ind_code), group in df.groupby(group_cols):
        row = {
            id_column: db_code,
            "INDICATOR": ind_code
        }

        # UNIT_MEASURE aggregation
        if "UNIT_MEASURE" in group.columns:
            units = group["UNIT_MEASURE"].dropna().unique()
            row["UNIT_MEASURE"] = ", ".join(units)
        else:
            row["UNIT_MEASURE"] = "N/A"            

        # FREQ aggregation
        if "FREQ" in group.columns:
            freqs = group["FREQ"].dropna().unique()
            row["FREQ"] = ", ".join(freqs)
        else:
            row["FREQ"] = "N/A"

        # OBS_CONF aggregation
        if "OBS_CONF" in group.columns:
            conf = group["OBS_CONF"].dropna().unique()
            row["OBS_CONF"] = ", ".join(conf)
        else:
            row["OBS_CONF"] = "N/A"

        # TIME_PERIODS min/max
        if "TIME_PERIOD" in group.columns:
            years = group["TIME_PERIOD"].astype(str).unique()
            row["TIME_PERIODS"] = [{"start": years.min(), "end": years.max()}]

        # REF_AREA split into REF_COUNTRY/GEOGRAPHIC_UNITS
        if "REF_AREA" in df.columns:
            ref_codes = group["REF_AREA"].unique()
            row["REF_COUNTRY"] = [{"code": c, "name": lookup_dict.get("REF_AREA", {}).get(c, c)}
                                 for c in ref_codes if c in country_codes]
            row["GEOGRAPHIC_UNITS"] = [{"code": c, "name": lookup_dict.get("REF_AREA", {}).get(c, c)}
                             for c in ref_codes if c not in country_codes]
        row["DIMENSIONS"] = dimensions_dict.get(ind_code, [])
        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    # Translate code to label dynamically
    id_column = "DATABASE_ID" if "DATABASE_ID" in summary_df.columns else "DATASET_ID"
    summary_df[f"{id_column.replace('_ID', '_NAME')}"] = (
        summary_df[id_column]
        .map(lookup_dict.get(id_column, {}))
        .fillna(summary_df[id_column])
    )
    summary_df["INDICATOR_NAME"] = summary_df["INDICATOR"].map(lookup_dict.get("INDICATOR", {})).fillna(summary_df["INDICATOR"])

    # Translate UNIT_MEASURE 
    if "UNIT_MEASURE" in summary_df.columns:
        summary_df["UNIT_MEASURE"] = summary_df["UNIT_MEASURE"].apply(
            lambda x: ", ".join([lookup_dict.get("UNIT_MEASURE", {}).get(u, u) for u in x.split(", ")])
            if x != "N/A" else "N/A"
        )
        
    # Translate FREQ
    if "FREQ" in summary_df.columns:
        summary_df["FREQ"] = summary_df["FREQ"].apply(
            lambda x: ", ".join([lookup_dict.get("FREQ", {}).get(f, f) for f in x.split(", ")])
            if x != "N/A" else "N/A"
        )

    # Translate OBS_CONF
    if "OBS_CONF" in summary_df.columns:
        summary_df["OBS_CONF"] = summary_df["OBS_CONF"]

    return summary_df

def build_database_metadata_summary(indicator_summary):
    """
    Build database-level summary from indicator-level summary DataFrame.
    """
    # --- Detect ID column dynamically ---
    id_column = next((col for col in ["DATABASE_ID", "DATASET_ID"] if col in indicator_summary.columns), None)
    if id_column is None:
        raise ValueError("❌ Neither 'DATABASE_ID' nor 'DATASET_ID' found in DataFrame columns.")

    # --- Detect name column dynamically ---
    name_column = next((col for col in ["DATABASE_NAME", "DATASET_NAME"] if col in indicator_summary.columns), None)

    db_rows = []

    for db_id, group in indicator_summary.groupby(id_column, dropna=False):
        # --- TIME_PERIODS → min start, max end ---
        all_periods = [
            p
            for sublist in group.get("TIME_PERIODS", [])
            if isinstance(sublist, list)
            for p in sublist
            if isinstance(p, dict) and "start" in p and "end" in p
        ]
        if all_periods:
            start = min(p["start"] for p in all_periods)
            end = max(p["end"] for p in all_periods)
            time_periods = [{"start": start, "end": end}]
        else:
            time_periods = []
        
        # REF_COUNTRY → union
        all_countries = []
        for sublist in group["REF_COUNTRY"]:
            all_countries.extend(sublist)
        # deduplicate by code
        ref_country = {c["code"]: c["name"] for c in all_countries}
        ref_country = [{"code": k, "name": v} for k, v in ref_country.items()]
        
        # GEOGRAPHIC_UNITS → union
        all_groups = []
        for sublist in group["GEOGRAPHIC_UNITS"]:
            all_groups.extend(sublist)
        geo_units = {g["code"]: g["name"] for g in all_groups}
        geo_units = [{"code": k, "name": v} for k, v in geo_units.items()]
        
        # DATABASE_NAME → take the first
        db_name = (
            group[name_column].dropna().iloc[0]
            if name_column and not group[name_column].dropna().empty
            else None
        )

        db_rows.append({
            id_column: db_id,
            "TIME_PERIODS": time_periods,
            "REF_COUNTRY": ref_country,
            "GEOGRAPHIC_UNITS": geo_units,
            name_column: db_name if name_column else None
        })
    
    return pd.DataFrame(db_rows)

# Section 4: Interact with Metadata Editor
def get_exist_meta_id(key, type, collection_num = 22):
    """
    Function uses to extract the existing metadata id from the metadata editor
    :param meta_url: metadata editor url
    :param key: api key
    :return: dictionary of existing metadata id
    """
    limit = 1000  # Max limit per page
    request_url = (
        f"{meta_url}/api/editor?collection={collection_num}&type={type}&limit={limit}&offset=0"
    )
    headers = {"x-api-key": key}
    response = requests.request("GET", request_url, headers=headers)
    result = response.json()

    if response.status_code != 200:
        exist_id = response.text
    else:
        total_cases = result["total"]
        exist_id = dict()

        for i in range(0, total_cases, limit):
            paginated_url = f"{meta_url}/api/editor?collection={collection_num}&type={type}&limit={limit}&offset={i}"
            paginated_response = requests.get(paginated_url, headers=headers)

            paginated_result = paginated_response.json()
            projects = paginated_result["projects"]

            for item in projects:
                exist_id[item["study_idno"]] = item["id"]

    if exist_id == {}:  # stop the pipeline if no metadata projects are found
        print(
            ">>>>>>>>> No existing Data360 metadata projects found! Check your Metadata Editor account role."
        )
        raise Exception("No existing Data360 metadata projects found!")
    else:
        print(">>>>>>>>> Existing Data360 metadata projects found!")
        return exist_id

def get_meta_by_dataset_db(meta_url, dataset_id, api_key, type, collection_num):
    """
    Extract Data360 metadata projects belonging to a dataset.

    :param meta_url: Base URL of metadata API
    :param dataset_id: Dataset identifier
    :param api_key: API key
    :param type: "timeseries" or "timeseries-db"
    :return: DataFrame of metadata projects
    """
    limit = 1000  # Max limit per page
    headers = {"x-api-key": api_key}

    request_url = f"{meta_url}/api/editor?collection={collection_num}&type={type}&limit={limit}&offset=0"
    response = requests.get(request_url, headers=headers)
    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"Metadata request failed: {response.text}")

    total_cases = result.get("total", 0)
    exist_id = {}

    for i in range(0, total_cases, limit):
        paginated_url = f"{meta_url}/api/editor?collection={collection_num}&type={type}&limit={limit}&offset={i}"
        paginated_response = requests.get(paginated_url, headers=headers)
        paginated_result = paginated_response.json()
        projects = paginated_result.get("projects", [])

        if type == "timeseries":
            for item in projects:
                if not isinstance(item, dict):
                    continue

                attrs = item.get("attributes")
                if not isinstance(attrs, dict):
                    continue    

                if attrs.get("database_id") == dataset_id.upper():
                    exist_id[item["study_idno"]] = item["id"]
                    print(f">>>>> Found existing Data360 metadata project for indicator {item["id"]}!")

        elif type == "timeseries-db":
            for item in projects:
                if not isinstance(item, dict):
                    continue

                if item.get("study_idno") == dataset_id:
                    exist_id[item["study_idno"]] = item["id"]
                    print(f">>>>> Found existing Data360 metadata project for dataset {dataset_id}!")

    if not exist_id:
        raise Exception(">>>>> No existing Data360 metadata projects found! Check your Metadata Editor account role.")
    else:
        print(">>>>> Existing Data360 metadata projects found!")
        meta_id = (
            pd.DataFrame.from_dict(exist_id, orient="index", columns=["idno"])
            .reset_index()
        )
        return meta_id
    
def update_project(md, key, idno, project_type = "timeseries", partial_update = True):
    """
    Function uses to update a timeseries project in the metadata editor
    :param md: metadata in json format
    :param key: api key
    :param idno: idno of the project
    :param partial_update: boolean value to update the metadata
    :return: response of the update
    """
    metadata_json = md
    request_url = f"{meta_url}/api/editor/update/{project_type}/{idno}?id_format=idno&partial_update={partial_update}"
    headers = {"x-api-key": key, "Content-Type": "application/json"}
    response = requests.request(
        "POST", request_url, headers=headers, data=metadata_json
    )
    if response.status_code != 200:
        # print(response.text)
        print(">>>>> %s", response.text)
    r = response.text
    return r

def create_project(md, key, project_type = "timeseries"):
    """
    Function uses to create a timeseries project in the metadata editor
    :param md: metadata in json format
    :param key: api key
    :return: idno of the project
    """
    request_url = f"{meta_url}/api/editor/create/{project_type}"
    metadata_json = md
    headers = {"x-api-key": key}
    response = requests.request(
        "POST", request_url, headers=headers, data=metadata_json
    )
    idno = json.loads(response.text)["id"]
    r = {"idno": idno}
    if response.status_code != 200:
        r = response.text
    return r

def check_geo_unit(idno, key, project_type):
    """
    Check if key 'geographic_units' exists in the JSON metadata.

    :param idno: Numeric idno generated once the project is created
    :param key: API key
    :return: True if 'geographic_units' exists, False otherwise
    """
    headers = {"x-api-key": key}
    request_url = f"{meta_url}/api/editor/json/{idno}"

    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        if project_type == "timeseries":
            return (
                "series_description" in json_data
                and "geographic_units" in json_data["series_description"]
            )
        elif project_type == "timeseries-db":
            return (
                "database_description" in json_data
                and "geographic_units" in json_data["database_description"]
            )
        else:
            print(f"This project {project_type} {idno} doesn't have geographic_units field!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for idno {idno}: {e}")
    except ValueError:
        print(f"Invalid JSON response for idno {idno}")

    return False

def update_patch(md, key, idno, project_type = "timeseries"):
    """
    Function uses to update a project through patch in the metadata editor
    :param md: metadata in json format
    :param key: api key
    :param idno: idno of the project
    :param partial_update: boolean value to update the metadata
    :return: response of the update
    """
    metadata_json = md
    request_url = f"{meta_url}/api/editor/patch/{project_type}/{idno}?id_format=idno"
    headers = {"x-api-key": key, "Content-Type": "application/json"}
    response = requests.request(
        "POST", request_url, headers=headers, data=metadata_json
    )
    if response.status_code != 200:
        # print(response.text)
        print(">>>>>>>>>>>>> %s", response.text)
    r = response.text
    return r

def add_data360_admin_metadata(df, key):
    """
    Function uses to add the project to data360 collection
    :param df: dataFrame with column 'numid'
    :param key: api key
    :return: response of the add project
    """
    projects = df["numid"].astype(str).tolist()
    for _,row in df.iterrows():
        admin_meta = {
                "project_id": row["numid"],
                "template_uid": "data360",
                "metadata": {
                    "visualization": {
                        "remove_chart": [
                        {
                            "chart_types": "stackedBar"
                        },
                        {
                            "chart_types": "pie"
                        }
                        ]
                    }}
                }    
    md = json.dumps(admin_meta)
    request_url = f"{meta_url}/api/admin-metadata/data/"
    headers = {"x-api-key": key, "Content-Type": "application/json"}
    response = requests.request("POST", request_url, headers=headers, data=md)
    if response.status_code != 200:
        print(response.text)
    r = response.text

    return r

def add_project_to_collection(df, key, collection_num):
    """
    Function uses to add the project to a collection
    :param df: dataFrame with column 'numid'
    :param key: api key
    :return: response of the add project
    """
    projects = df["numid"].astype(str).tolist()
    add_collection = {"collections": collection_num, "id_format": "idno", "projects": projects}
    json_add_collection = json.dumps(add_collection)

    request_url = f"{meta_url}/api/collections/add_projects"
    headers = {"x-api-key": key, "Content-Type": "application/json"}
    response = requests.request(
        "POST", request_url, headers=headers, data=json_add_collection
    )
    if response.status_code != 200:
        print(response.text)
        # print(">>>>> %s", response.text)
    r = response.text

    return r

def clean_admin_metadata(raw_json: dict) -> dict:
    """
    Transform admin metadata API response into simplified structure.

    Input structure:
        {status, data:[{template_uid, metadata, ...}]}

    Output structure:
        {admin_metadata:{template_uid: metadata}}
    """
    return {
        "admin_metadata": {
            item["template_uid"]: item.get("metadata", {})
            for item in raw_json.get("data", [])
            if item.get("template_uid")
        }
    }

def fetch_and_save(session, url, path, is_pdf=False, clean_admin=False):
    r = session.get(url, stream=is_pdf)
    r.raise_for_status()

    if is_pdf:
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    else:
        data = r.json()
        if clean_admin:
            data = clean_admin_metadata(data)
        with open(path, "w") as f:
            json.dump(data, f)

def export_object(session, meta_url, obj_id, obj_name, folders, admin=False):
    results = {}

    try:
        if admin:
            url = f"{meta_url}/api/admin-metadata/data/{obj_id}"
            path = f"{folders['json']}/{obj_name}.json"
            fetch_and_save(session, url, path, clean_admin=True)
            results["json"] = path

        else:
            json_url = f"{meta_url}/api/editor/json/{obj_id}?exclude_private_fields=1&admin_metadata=1"
            pdf_gen = f"{meta_url}/api/editor/generate_pdf/{obj_id}?exclude_private_fields=1"
            pdf_url = f"{meta_url}/api/editor/pdf/{obj_id}"

            json_path = f"{folders['json']}/{obj_name}.json"
            pdf_path = f"{folders['pdf']}/{obj_name}.pdf"

            fetch_and_save(session, json_url, json_path)
            session.get(pdf_gen).raise_for_status()
            fetch_and_save(session, pdf_url, pdf_path, is_pdf=True)

            results = {"json": json_path, "pdf": pdf_path}

    except Exception as e:
        results["error"] = str(e)

    return obj_name, results

def export_metadata_all(
    meta_url,
    dataset_id,
    api_key,
    catalog_env,
    obs_conf_path,
    collection_num,
    indicator_list=None,
    admin=False,
    workers=8,
    df_ind=None,
    df_db=None
):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from databricks.sdk.runtime import dbutils
    root = f"/Volumes/{catalog_env}_data360/volumes/data360-dropzone/{obs_conf_path}/datasets/{dataset_id}/metadata"

    folders = {
        "ind_json": f"{root}/admin_metadata" if admin else root,
        "ind_pdf": f"{root}/download",
        "db_json": f"{root}/dataset/admin_metadata" if admin else f"{root}/dataset",
        "db_pdf": f"{root}/dataset/download"
    }

    for f in folders.values():

        if indicator_list is None:
            # Full export → recreate folders
            dbutils.fs.rm(f, recurse=True)
            dbutils.fs.mkdirs(f)
        else:
            # Partial update → keep existing files
            try:
                dbutils.fs.ls(f)
            except:
                dbutils.fs.mkdirs(f)

    session = requests.Session()
    session.headers.update({"x-api-key": api_key})

    if df_ind is None or df_db is None:
        print(">>> Fetching metadata objects...")
        df_ind = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
        df_db = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)

    if indicator_list:
        df_ind = df_ind[df_ind["index"].isin(indicator_list)]

    tasks = []

    with ThreadPoolExecutor(max_workers=workers) as executor:

        for df, j, p in [
            (df_db, folders["db_json"], folders["db_pdf"]),
            (df_ind, folders["ind_json"], folders["ind_pdf"])
        ]:

            for row in df.itertuples():
                tasks.append(
                    executor.submit(
                        export_object,
                        session,
                        meta_url,
                        row.idno,
                        row.index,
                        {"json": j, "pdf": p},
                        admin
                    )
                )

        results = {}
        for f in as_completed(tasks):
            name, res = f.result()
            results[name] = res

    print(f"✅ Export completed for dataset {dataset_id}")
    return results

def export_all_metadata(
    meta_url,
    dataset_id,
    api_key,
    catalog_env,
    obs_conf_path,
    collection_num,
    indicator_list=None
):
    """Export both standard metadata and admin metadata efficiently."""

    print(">>> Fetching metadata objects ...")

    df_ind = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
    df_db  = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)

    results = {}

    results["metadata"] = export_metadata_all(
        meta_url,
        dataset_id,
        api_key,
        catalog_env,
        obs_conf_path,
        collection_num,
        indicator_list=indicator_list,
        admin=False,
        df_ind=df_ind,
        df_db=df_db
    )

    results["admin_metadata"] = export_metadata_all(
        meta_url,
        dataset_id,
        api_key,
        catalog_env,
        obs_conf_path,
        collection_num,
        indicator_list=indicator_list,
        admin=True,
        df_ind=df_ind,
        df_db=df_db
    )

    return results

# Section 5: Generate payload for Metadata Editor
def gen_metadata_information(indicator_name_short, indicator_id):
    """
    # A function to generate standard metadata information for a given project
    :param indicator_name_short: short name of the indicator
    :param indicator_id: indicator id
    :param today: date of metadata creation
    :param vno: version number
    :param dm: date of version
    :return:
    """
    metadata_information = dict()
    # metadata_information['partial_update'] = True
    metadata_information["title"] = f"Metadata for {indicator_name_short}"
    metadata_information["idno"] = f"META_{indicator_id}"

    metadata_information["producers"] = list()
    metadata_producer1 = dict()
    metadata_producer1["name"] = "Development Economics Data Group"
    metadata_producer1["abbr"] = "DECDG"
    metadata_producer1["affiliation"] = "World Bank"
    metadata_information["producers"].append(metadata_producer1)

    # metadata_information["version_statement"] = {"version": f"Version {vno}",
    #                                              "version_date": dm}

    return metadata_information

def gen_series_description(**kwargs):
    """
    A function to generate standard series_description for a given project
    :param vno: version number
    :param dm: date of version
    :param kwargs: a dictionary of metadata information
    """
    series_description = {}

    # Title statement
    series_description["name"] = kwargs.get("name", "")
    series_description["idno"] = kwargs.get("idno", "")
    series_description["database_id"] = kwargs.get("database_id", "")
    series_description["database_name"] = kwargs.get("database_name", "")
    series_description["languages"] = [{"name": "English", "code": "EN"}]

    # Description
    # series_description["definition_long"] = kwargs.get("definition_long", "")
    # series_description["definition_references"] = kwargs.get(
    #     "definition_references", ""
    # )
    series_description["measurement_unit"] = kwargs.get("measurement_unit", "")
    series_description["dimensions"] = kwargs.get("dimensions", "")
    series_description["periodicity"] = kwargs.get("periodicity", "")
    series_description["aggregation_method"] = kwargs.get("aggregation_method", "")

    # Geographic and time coverage
    series_description["time_periods"] = kwargs.get("time_periods", "")
    series_description["ref_country"] = kwargs.get("ref_country", "")
    series_description["geographic_units"] = kwargs.get("geographic_units", "")

    # Access and use
    # series_description["license"] = kwargs.get("license", "")
    series_description["confidentiality_status"] = kwargs.get("confidentiality_status", "")    

    # Version
    series_description["version_statement"] = {
        "version_date": today,
    }

    # Put DDH download link here if available
    series_description["links"] = kwargs.get("links", "")

    # Remove keys with empty values
    series_description = {k: v for k, v in series_description.items() if v}

    return series_description

def gen_database_description(**kwargs):
    """
    A function to generate standard database_description for a given project
    :param vno: version number
    :param dm: date of version
    :param kwargs: a dictionary of metadata information
    """
    database_description = {}

    # Title statement
    database_description["title_statement"] = {
        "idno": kwargs.get("idno", ""),
        "title": kwargs.get("title", "")}
    database_description["languages"] = [{"name": "English", "code": "EN"}]

    # Geographic and time coverage
    database_description["time_coverage"] = kwargs.get("time_periods", "")
    database_description["ref_country"] = kwargs.get("ref_country", "")
    database_description["geographic_units"] = kwargs.get("geographic_units", "")

    # Version
    database_description["version"] = [{
        "date": today
    }]

    # Remove keys with empty values
    database_description = {k: v for k, v in database_description.items() if v}

    return database_description

def gen_metadata_payloads(row, id_column):
    metadata_content = gen_metadata_information(row["INDICATOR_NAME"], row["INDICATOR"])
    indicator_content = gen_series_description(
        name=row["INDICATOR_NAME"],
        idno=row["INDICATOR"],
        database_id=row[id_column],
        database_name=row[id_column.replace("_ID", "_NAME")],
        measurement_unit=row["UNIT_MEASURE"],
        dimensions=row["DIMENSIONS"],
        periodicity=row["FREQ"],
        confidentiality_status=row['OBS_CONF'],
        time_periods=row["TIME_PERIODS"],
        ref_country=row["REF_COUNTRY"],
        geographic_units=row["GEOGRAPHIC_UNITS"],
    )
    meta_project = {
        "partial_update": True,
        "metadata_information": metadata_content,
        "series_description": indicator_content,
    }

    return json.dumps(meta_project)

def gen_metadata_payloads_database(row, id_column, name_column):
    metadata_content = gen_metadata_information(row[name_column], row[id_column])
    indicator_content = gen_database_description(
        title=row[name_column],
        idno=row[id_column],
        time_periods=row["TIME_PERIODS"],
        ref_country=row["REF_COUNTRY"],
        geographic_units=row["GEOGRAPHIC_UNITS"],
    )
    meta_project = {
        "partial_update": True,
        "metadata_information": metadata_content,
        "database_description": indicator_content,
    }

    return json.dumps(meta_project)

def gen_metadata_patch(row, geo_exist_boolean):
    """
    Generate a metadata patch update payload for fields with list values.

    :param row: Dictionary containing row data
    :param geo_exist_boolean: Boolean indicating if 'geographic_units' exists in the metadata
    :return: JSON string representing the patch update
    """
    patch_values = [
        {
            "value": row[col],
            "op": "replace",
            "path": f"/series_description/{col.lower()}",
        }
        for col in ["DIMENSIONS", "REF_COUNTRY"]
        if row.get(col)
    ]

    geo_value = row.get("GEOGRAPHIC_UNITS", [])

    if geo_exist_boolean:
        value = geo_value if geo_value else [{"name": "", "code": "", "type": ""}]
        op = "replace"
    elif geo_value:
        value = geo_value
        op = "add"
    else:
        value = None

    if value is not None:
        patch_values.append({
            "value": value,
            "op": op,
                "path": "/series_description/geographic_units",
            }
        )

    return json.dumps({"patches": patch_values, "validate": "true"})

def gen_metadata_patch_database(row, geo_exist_boolean):
    """
    Generate a metadata patch update payload for fields with list values.

    :param row: Dictionary containing row data
    :param geo_exist_boolean: Boolean indicating if 'geographic_units' exists in the metadata
    :return: JSON string representing the patch update
    """
    patch_values = [
        {
            "value": row["TIME_PERIODS"],
            "op": "replace",
            "path": "/database_description/time_coverage",
        },
        {
            "value": row["REF_COUNTRY"],
            "op": "replace",
            "path": "/database_description/ref_country",
        },
        {
            "value": {"date": today},
            "op": "add",
            "path": "/database_description/version/0",
        },
    ]

    geo_value = row.get("GEOGRAPHIC_UNITS", [])

    if geo_exist_boolean:
        value = geo_value if geo_value else [{"name": "", "code": "", "type": ""}]
        op = "replace"
    elif geo_value:
        value = geo_value
        op = "add"
    else:
        value = None

    if value is not None:
        patch_values.append({
            "value": value,
            "op": op,
            "path": "/database_description/geographic_units"
        })

    return json.dumps({"patches": patch_values, "validate": False})

def create_edit_metadata_project_indicator(df, api_key, collection_num):
    """
    Function uses to create or update metadata for the dataset
    :param df: metadata df
    :param api_key: api key for metadata editor
    :param data_version_number: version number of the dataset
    :return: dataframe with metadata id
    """
    # Get existing data360 metadata project INDICATOR id and idno
    exist_id = get_exist_meta_id(api_key, "timeseries", collection_num)
    if not isinstance(exist_id, dict):
        StopAsyncIteration("Error: Metadata API is not responding")

    id_column = None
    for col in ["DATABASE_ID", "DATASET_ID"]:
        if col in df.columns:
            id_column = col
            break

    for index, row in df.iterrows():
        json_data = gen_metadata_payloads(row, id_column)
        print(
            ">>>>>>>>> Metadata payloads and patch created %s...", row["INDICATOR"]
        )
        # Check if INDICATOR_FINAL already exists in metadata
        # if it exists, save the idno and update the current metadata project
        if row["INDICATOR"] in exist_id.keys():
            df.loc[index, "numid"] = exist_id[row["INDICATOR"]]
            update_project( 
                json_data, api_key, exist_id[row["INDICATOR"]], "timeseries", True
            )
            print(
                ">>>>>>>>>>> Metadata project partial updated %s...", row["INDICATOR"]
            )
            geo_exist_boolean = check_geo_unit(exist_id[row["INDICATOR"]], api_key, "timeseries")
            patch_json = gen_metadata_patch(row, geo_exist_boolean)
            update_patch(patch_json, api_key, exist_id[row["INDICATOR"]], "timeseries")
            print(
                ">>>>>>>>>>> Metadata project patch updated %s...", row["INDICATOR"]
            )

        # if it doesn't exist, create a new metadata project and add it to data360 collection
        else: 
            df.loc[index, "numid"] = create_project(json_data, api_key, "timeseries").get(
                "idno"
            )
            add_data360_admin_metadata(df, api_key)

    add_project_to_collection(df, api_key, collection_num)

    return df

def create_edit_metadata_project_database(df, api_key, collection_num):
    """
    Function uses to create or update metadata for the dataset
    :param df: metadata df
    :param api_key: api key for metadata editor
    :param data_version_number: version number of the dataset
    :return: dataframe with metadata id
    """
    # Get existing data360 metadata project DATABASE_ID id and idno
    exist_id = get_exist_meta_id(api_key, "timeseries-db", collection_num)
    if not isinstance(exist_id, dict):
        StopAsyncIteration("Error: Metadata API is not responding")

    id_column = next((col for col in ["DATABASE_ID", "DATASET_ID"] if col in df.columns), None)
    if id_column is None:
        raise ValueError("❌ Neither 'DATABASE_ID' nor 'DATASET_ID' found in DataFrame columns.")

    name_column = next((col for col in ["DATABASE_NAME", "DATASET_NAME"] if col in df.columns), None)

    for index, row in df.iterrows():
        json_data = gen_metadata_payloads_database(row, id_column, name_column)
        print(
            ">>>>>>>>> Metadata payloads and patch created %s...", row[id_column]
        )
        # Check if INDICATOR_FINAL already exists in metadata
        # if it exists, save the idno and update the current metadata project
        if row[id_column] in exist_id.keys():
            df.loc[index, "numid"] = exist_id[row[id_column]]
            update_project(
                json_data, api_key, exist_id[row[id_column]], 'timeseries-db', True
            )    
            print(">>>>>>>>>>> Metadata project partial updated %s...", row[id_column]
                  )

            geo_exist_boolean = check_geo_unit(exist_id[row[id_column]], api_key, "timeseries-db")
            patch_json = gen_metadata_patch_database(row, geo_exist_boolean)
            update_patch(patch_json, api_key, exist_id[row[id_column]], "timeseries-db")
            print(
                ">>>>>>>>>>> Metadata project patch updated %s...", row[id_column]
            )

        # if it doesn't exist, create a new metadata project and add it to data360 collection
        else:
            response = create_project(json_data, api_key, "timeseries-db")
            df.loc[index, "numid"] = response.get("idno")

            add_data360_admin_metadata(df, api_key)
            print(f"New database metadata project created {row[id_column]}")

    add_project_to_collection(df, api_key, collection_num)

    return df

# Section 6: DDH related operation
def trigger_update(
        dataset_id: str|list,
        ddh_params: dict,
        catalog_env: str,
        obs_conf: str,
        user_email: str,
        upload: str = 'both',
        indicator_id: str|list|bool = []
        ):
    """Triggers the update of the metadata/data file in the dropzone
    Args:
        dataset_id (str|list): list of dataset id (data360 dataset id)
        ddh_params (dict): dictionary with the parameters to connect to DDH
        ddh_env (str): environment to connect to DDH (e.g. 'ops' or 'ops_qa')
        user_email: user email (the email you want to receive the notification)
        upload (str): type of upload (data/metadata/both)
        indicator_id (dict|bool): Optional. List of indicator id 
            (data360 indicator id). If no input, then load the whole dataset.
        temp (bool): Force kedro execution order
    :return: response
    """
    import wbddh
    from databricks.sdk.runtime import dbutils
    
    # Check if dataset_id is a string to convert it to a list
    if isinstance(dataset_id, str):
        dataset_id = [dataset_id]

    if catalog_env == "dev" or catalog_env == "qa":
        ddh_catalog_env = "ops_qa"
    elif catalog_env == "prd":
        ddh_catalog_env = "ops"
    else:
        raise ValueError(f"Invalid catalog_environment: {catalog_env}")

    # Get DDH params for the environment of interest
    ddh_params = ddh_params[ddh_catalog_env]
    print(ddh_params)

    # Get secrets for the environment of interest
    ddh_credentials = {
        "client_id": dbutils.secrets.get("data360-secret-scope", f"ddh-{catalog_env}-client-id"),
        "tenant_id": dbutils.secrets.get("data360-secret-scope", f"ddh-{catalog_env}-tenant-id"),
        "username": dbutils.secrets.get("data360-secret-scope", f"ddh-{catalog_env}-username"),
        "password": dbutils.secrets.get("data360-secret-scope", f"ddh-{catalog_env}-password"),
    }
    
    wbddh.set_api_host(ddh_params["resource"])
 
    params = {
        "authorityHostURL": ddh_params["authority_host"],
        "clientId": ddh_credentials["client_id"],
        "tenant": ddh_credentials["tenant_id"],
        "resourceURL": ddh_params["resource"],
        "username": ddh_credentials["username"],
        "password": ddh_credentials["password"],
        }

    try:
        session = wbddh.create_service_account_session(params=params)
        print(session)
    except Exception as e:
        raise Exception(f"Failed to create DDH session: {str(e)}")
        return None

    body = {
        "indicators": indicator_id,
        "datasetIds": dataset_id,#.tolist(),
        "userEmail": user_email,
        "type": upload.lower(),
    }
    print(body)
    try:
        if obs_conf == "public":
            req_url = f"{ddh_params['api_host']}/{ddh_params['data_load_endpoint']}"
            print(req_url)
        elif obs_conf == "ouo":
            req_url = f"{ddh_params['api_host']}/{ddh_params['data_load_endpoint_ou']}"
            print(req_url)
        req = requests.post(req_url, json=body, headers=session.headers)
        
        return req.text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to trigger metadata update: {str(e)}")
        return None
    

# OLD FUNCTIONS:
# Section 4:
# ------------- old functions, optomized version is in Section 4 above ------------------
def export_file(meta_url, obj_id, obj_name, headers, folder_json, folder_pdf):
    """Helper to export JSON and PDF for a metadata object (indicator or database)."""
    results = {"json": None, "pdf": None}

    # JSON Export
    try:
        json_url = f"{meta_url}/api/editor/json/{obj_id}?exclude_private_fields=1&admin_metadata=1"
        resp = requests.get(json_url, headers=headers)
        resp.raise_for_status()

        file_path = f"{folder_json}/{obj_name}.json"
        with open(file_path, "w") as f:   # Direct write to UC
            json.dump(resp.json(), f, indent=4)

        results["json"] = file_path
    except Exception as e:
        results["json"] = str(e)
        print(f"❌ JSON export failed for {obj_name}: {e}")

    # PDF Export
    try:
        # Trigger PDF generation
        gen_url = f"{meta_url}/api/editor/generate_pdf/{obj_id}?exclude_private_fields=1"
        requests.get(gen_url, headers=headers).raise_for_status()

        pdf_url = f"{meta_url}/api/editor/pdf/{obj_id}"
        pdf_path = f"{folder_pdf}/{obj_name}.pdf"

        with requests.get(pdf_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(pdf_path, "wb") as f:   # Direct write to UC
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        results["pdf"] = pdf_path
    except Exception as e:
        results["pdf"] = str(e)
        print(f"❌ PDF export failed for {obj_name}: {e}")

    return results

def export_admin_metadata_json(meta_url, obj_id, obj_name, headers, folder_json):
    """Helper to export JSON admin metadata for a metadata object (indicator or database)."""
    results = {"json": None}

    try:
        json_url = f"{meta_url}/api/admin-metadata/data/{obj_id}"
        resp = requests.get(json_url, headers=headers)
        resp.raise_for_status()

        raw_json = resp.json()
        cleaned_json = clean_admin_metadata(raw_json)

        file_path = f"{folder_json}/{obj_name}.json"
        with open(file_path, "w") as f:   # Direct write to UC
            json.dump(cleaned_json, f, indent=4)

        results["json"] = file_path
    except Exception as e:
        results["json"] = str(e)
        print(f"❌ JSON export failed for {obj_name}: {e}")

    return results

def export_metadata_db(
    meta_url: str,
    dataset_id: str,
    api_key: str,
    catalog_env: str,
    obs_conf_path: str,
    collection_num: int
):
    """
    Export both JSON and PDF metadata files for a dataset to Azure data lake.
    
    Args:
        metadata_url (str): URL of the metadata editor
        dataset_id (str): The ID of the dataset
        api_key: API key for the metadata editor

    Returns:
        Tuple of (dict of exported paths, dict of JSON export status, dict of PDF export status)
    """
    from databricks.sdk.runtime import dbutils
    # Define root folder
    root_folder = f"/Volumes/{catalog_env}_data360/volumes/data360-dropzone/{obs_conf_path}/datasets/{dataset_id}/metadata"
    folders = {
        "json": root_folder,
        "pdf": f"{root_folder}/download",
        "dataset_json": f"{root_folder}/dataset",
        "dataset_pdf": f"{root_folder}/dataset/download",
    }

    print(f">>> Creating folders under {root_folder}...")
    # Recreate folders
    try:
        dbutils.fs.ls(root_folder)
        dbutils.fs.rm(root_folder, recurse=True)
    except Exception:
        dbutils.fs.mkdirs(root_folder)
    for folder in folders.values():
        dbutils.fs.mkdirs(folder)

    # Get metadata
    print(">>> Fetching indicator metadata...")
    df_indicators = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
    print(">>> Fetching database metadata...")
    df_databases = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)
    headers = {"x-api-key": api_key}

    export_results = {"json": [], "pdf": []}
    json_exported, pdf_exported = {}, {}

    # Loop through databases + indicators
    for df, j_folder, p_folder in [
        (df_databases, folders["dataset_json"], folders["dataset_pdf"]),
        (df_indicators, folders["json"], folders["pdf"])
    ]:
        for _, row in df.iterrows():
            obj_id = row["idno"]
            obj_name = row["index"]   
            print(f">>>>>>>>> Processing {obj_name}: {obj_id}...")

            result = export_file(meta_url, obj_id, obj_name, headers, j_folder, p_folder)

            if isinstance(result["json"], str) and result["json"].endswith(".json"):
                export_results["json"].append(result["json"])
                json_exported[obj_name] = True
            else:
                json_exported[obj_name] = result["json"]

            if isinstance(result["pdf"], str) and result["pdf"].endswith(".pdf"):
                export_results["pdf"].append(result["pdf"])
                pdf_exported[obj_name] = True
            else:
                pdf_exported[obj_name] = result["pdf"]

            time.sleep(0.1)  # light rate limiting

    print(f"✅ Metadata export for dataset {dataset_id} completed.")
    return export_results, json_exported, pdf_exported

def export_metadata_ind(
    meta_url: str,
    dataset_id: str,
    indicator_list: list,
    api_key: str,
    catalog_env: str,
    obs_conf_path: str,
    collection_num: int
):
    # Define root folder
    root_folder = f"/Volumes/{catalog_env}_data360/volumes/data360-dropzone/{obs_conf_path}/datasets/{dataset_id}/metadata"
    folders = {
        "json": root_folder,
        "pdf": f"{root_folder}/download",
        "dataset_json": f"{root_folder}/dataset",
        "dataset_pdf": f"{root_folder}/dataset/download",
    }

    for f in folders.values():
        os.makedirs(f, exist_ok=True)

    # Get metadata
    print(">>> Fetching indicator metadata...")
    df_indicators = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
    print(">>> Fetching database metadata...")
    df_databases = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)

    if not indicator_list:
        pass
    else:
        df_indicators = df_indicators[df_indicators['index'].isin(indicator_list)]

    headers = {"x-api-key": api_key}
    export_results = {"json": [], "pdf": []}
    json_exported, pdf_exported = {}, {}

    # Loop through databases + indicators
    for df, j_folder, p_folder in [
        (df_databases, folders["dataset_json"], folders["dataset_pdf"]),
        (df_indicators, folders["json"], folders["pdf"])
    ]:
        for _, row in df.iterrows():
            obj_id = row["idno"]
            obj_name = row["index"]   
            print(f">>>>>>>>> Processing {obj_name}: {obj_id}...")

            result = export_file(meta_url, obj_id, obj_name, headers, j_folder, p_folder)

            if isinstance(result["json"], str) and result["json"].endswith(".json"):
                export_results["json"].append(result["json"])
                json_exported[obj_name] = True
            else:
                json_exported[obj_name] = result["json"]

            if isinstance(result["pdf"], str) and result["pdf"].endswith(".pdf"):
                export_results["pdf"].append(result["pdf"])
                pdf_exported[obj_name] = True
            else:
                pdf_exported[obj_name] = result["pdf"]

            time.sleep(0.1)  # light rate limiting

    print(f"✅ Metadata export for dataset {dataset_id} completed.")
    return export_results, json_exported, pdf_exported

def export_admin_metadata_db(
    meta_url: str,
    dataset_id: str,
    api_key: str,
    catalog_env: str,
    obs_conf_path: str,
    collection_num: int
):
    """
    Export both JSON admin metadata files for a dataset to Azure data lake.
    
    Args:
        metadata_url (str): URL of the metadata editor
        dataset_id (str): The ID of the dataset
        api_key: API key for the metadata editor

    Returns:
        Tuple of (dict of exported paths, dict of JSON export status, dict of PDF export status)
    """
    from databricks.sdk.runtime import dbutils
    # Define root folder
    root_folder = f"/Volumes/{catalog_env}_data360/volumes/data360-dropzone/{obs_conf_path}/datasets/{dataset_id}/metadata"
    folders = {
        "indicator_json": f"{root_folder}/admin_metadata",
        "dataset_json": f"{root_folder}/dataset/admin_metadata",
    }

    print(f">>> Creating folders under {root_folder}...")
    # Recreate folders
    for folder in folders.values():
        try:
            dbutils.fs.rm(folder, recurse=True)
        except:
            pass
        dbutils.fs.mkdirs(folder)

    # Get metadata
    print(">>> Fetching indicator admin metadata...")
    df_indicators = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
    print(">>> Fetching database admin metadata...")
    df_databases = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)
    headers = {"x-api-key": api_key}

    export_results = {"admin_metadata_json": []}
    admin_metadata_exported = {}

    # Loop through databases + indicators
    for df, folder_json in [
        (df_databases, folders["dataset_json"]),
        (df_indicators, folders["indicator_json"])
    ]:
        for _, row in df.iterrows():
            obj_id = row["idno"]
            obj_name = row["index"]   
            print(f">>>>>>>>> Processing {obj_name}: {obj_id}...")

            result = export_admin_metadata_json(meta_url, obj_id, obj_name, headers, folder_json)

            if isinstance(result["json"], str) and result["json"].endswith(".json"):
                export_results["admin_metadata_json"].append(result["json"])
                admin_metadata_exported[obj_name] = True
            else:
                admin_metadata_exported[obj_name] = result["json"]

            time.sleep(0.1)  # light rate limiting

    print(f"✅ Admin metadata export for dataset {dataset_id} completed.")
    return export_results, admin_metadata_exported

def export_admin_metadata_ind(
    meta_url: str,
    dataset_id: str,
    indicator_list: list,
    api_key: str,
    catalog_env: str,
    obs_conf_path: str,
    collection_num: int
):
    # Define root folder
    root_folder = f"/Volumes/{catalog_env}_data360/volumes/data360-dropzone/{obs_conf_path}/datasets/{dataset_id}/metadata"
    folders = {
        "indicator_json": f"{root_folder}/admin_metadata",
        "dataset_json": f"{root_folder}/dataset/admin_metadata",
    }

    for f in folders.values():
        os.makedirs(f, exist_ok=True)

    # Get metadata
    print(">>> Fetching indicator admin metadata...")
    df_indicators = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries", collection_num)
    print(">>> Fetching database admin metadata...")
    df_databases = get_meta_by_dataset_db(meta_url, dataset_id, api_key, "timeseries-db", collection_num)    
    headers = {"x-api-key": api_key}

    if not indicator_list:
        pass
    else:
        df_indicators = df_indicators[df_indicators['index'].isin(indicator_list)]

    export_results = {"admin_metadata_json": []}
    admin_metadata_exported = {}

    # Loop through databases + indicators
    for df, folder_json in [
        (df_databases, folders["dataset_json"]),
        (df_indicators, folders["indicator_json"])
    ]:
        for _, row in df.iterrows():
            obj_id = row["idno"]
            obj_name = row["index"]   
            print(f">>>>>>>>> Processing {obj_name}: {obj_id}...")

            result = export_admin_metadata_json(meta_url, obj_id, obj_name, headers, folder_json)

            if isinstance(result["json"], str) and result["json"].endswith(".json"):
                export_results["admin_metadata_json"].append(result["json"])
                admin_metadata_exported[obj_name] = True
            else:
                admin_metadata_exported[obj_name] = result["json"]

            time.sleep(0.1)  # light rate limiting

    print(f"✅ Admin metadata export for dataset {dataset_id} completed.")
    return export_results, admin_metadata_exported
# ------------------ old functions end here ---------------------------