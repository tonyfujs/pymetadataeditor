# How to use pyMetadataEditor


```python
from pymetadataeditor import MetadataEditor
import os

# show all columns in pandas
import pandas as pd
pd.set_option('display.max_columns', None)
```

## Examples of the interface


```python
your_api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
me = MetadataEditor(api_url=api_url, api_key=your_api_key, verify_ssl=False)
```

### Listing your projects


```python
me.list_projects(limit=2)
```

    /Users/gblackadder/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host 'dev.ihsn.org'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
      warnings.warn(
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>idno</th>
      <th>study_idno</th>
      <th>title</th>
      <th>abbreviation</th>
      <th>nation</th>
      <th>year_start</th>
      <th>year_end</th>
      <th>published</th>
      <th>created</th>
      <th>changed</th>
      <th>varcount</th>
      <th>created_by</th>
      <th>changed_by</th>
      <th>is_shared</th>
      <th>thumbnail</th>
      <th>template_uid</th>
      <th>attributes</th>
      <th>username</th>
      <th>username_cr</th>
      <th>collections</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5095</th>
      <td>survey</td>
      <td>6b609e22-e86f-43f8-92c2-d2fd4920b4aa</td>
      <td>zwxL</td>
      <td>sial</td>
      <td>None</td>
      <td>pXmU, PzaQ, iWik...and 2 more</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:31:51+00:00</td>
      <td>2025-05-23T19:31:51+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>954e023b790d8b15433544d85eb6431e</td>
      <td>None</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>5069</th>
      <td>survey</td>
      <td>96d15eb0-520f-4a8f-90a3-34f391b9ab00</td>
      <td>aykI</td>
      <td>WVmB</td>
      <td>None</td>
      <td>pYhT</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:27:43+00:00</td>
      <td>2025-05-23T19:27:43+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>954e023b790d8b15433544d85eb6431e</td>
      <td>None</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
</div>




```python
me.count_projects()
```




    1789



### Creating a new indicator project


```python
demo_name = "GB20250225_demo"
```


```python
series_description = {
                        "idno": demo_name,
                        "doi": "V1",
                        "name": "Version 1",
                        "display_name": "Version 1"
                     }

indicator_id = me.create_project_log({"idno": demo_name, "series_description": series_description}, "indicator")
```

    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.repository_name' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.repository_name', 'title': 'Repository name', 'type': 'string', 'help_text': 'The name of the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.url' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.url', 'title': 'URL', 'type': 'string', 'help_text': 'The URL of the original repository or dataset.', 'rules': {'is_uri': True}, 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.dataset_identifier' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.dataset_identifier', 'title': 'Dataset identifier', 'type': 'string', 'help_text': 'The identifier of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.doi' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.doi', 'title': 'DOI', 'type': 'string', 'help_text': 'The Digital Object Identifier (DOI) of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.dataset_title' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.dataset_title', 'title': 'Dataset title', 'type': 'string', 'help_text': 'The title of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.date_published' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.date_published', 'title': 'Dataset published date (YYYY-MM-DD)', 'type': 'string', 'help_text': 'The date when the dataset was published in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.notes' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.notes', 'title': 'Notes', 'type': 'string', 'help_text': 'Additional information about the original repository.', 'display_type': 'textarea'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.repository_name' is a <class 'str'> type. Full item defition = {'key': 'repository_name', 'prop_key': 'provenance.source_repository.repository_name', 'title': 'Repository name', 'type': 'string', 'help_text': 'The name of the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.url' is a <class 'str'> type. Full item defition = {'key': 'url', 'prop_key': 'provenance.source_repository.url', 'title': 'URL', 'type': 'string', 'help_text': 'The URL of the source repository or dataset.', 'rules': {'is_uri': True}, 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.dataset_identifier' is a <class 'str'> type. Full item defition = {'key': 'dataset_identifier', 'prop_key': 'provenance.source_repository.dataset_identifier', 'title': 'Dataset identifier', 'type': 'string', 'help_text': 'The identifier of the dataset in the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.dataset_title' is a <class 'str'> type. Full item defition = {'key': 'dataset_title', 'prop_key': 'provenance.source_repository.dataset_title', 'title': 'Dataset title', 'type': 'string', 'help_text': 'The title of the dataset in the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.date_acquired' is a <class 'str'> type. Full item defition = {'key': 'date_acquired', 'prop_key': 'provenance.source_repository.date_acquired', 'title': 'Date acquired (YYYY-MM-DD)', 'type': 'string', 'help_text': 'The date when the metadata was acquired from the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.acquisition_mode' is a <class 'str'> type. Full item defition = {'key': 'acquisition_mode', 'prop_key': 'provenance.source_repository.acquisition_mode', 'title': 'Acquisition mode', 'type': 'string', 'help_text': 'The mode of acquisition of the metadata from the source repository. e.g. OAI-PMH, API, manual entry, etc.'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.notes' is a <class 'str'> type. Full item defition = {'key': 'notes', 'prop_key': 'provenance.source_repository.notes', 'title': 'Notes', 'type': 'string', 'help_text': 'Additional information about the source repository.'}
      warnings.warn(
    


```python
me.list_projects(limit=3, sort_by="updated_desc")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>idno</th>
      <th>study_idno</th>
      <th>title</th>
      <th>abbreviation</th>
      <th>nation</th>
      <th>year_start</th>
      <th>year_end</th>
      <th>published</th>
      <th>created</th>
      <th>changed</th>
      <th>varcount</th>
      <th>created_by</th>
      <th>changed_by</th>
      <th>is_shared</th>
      <th>thumbnail</th>
      <th>template_uid</th>
      <th>attributes</th>
      <th>username</th>
      <th>username_cr</th>
      <th>collections</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5096</th>
      <td>timeseries</td>
      <td>9960d5df-f2f4-477b-98ce-a58e20b829b4</td>
      <td>GB20250225_demo</td>
      <td>Version 1</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:35:14+00:00</td>
      <td>2025-05-23T19:35:14+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>timeseries-system-en</td>
      <td>{'database_id': None}</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>5095</th>
      <td>survey</td>
      <td>6b609e22-e86f-43f8-92c2-d2fd4920b4aa</td>
      <td>zwxL</td>
      <td>sial</td>
      <td>None</td>
      <td>pXmU, PzaQ, iWik...and 2 more</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:31:51+00:00</td>
      <td>2025-05-23T19:31:51+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>954e023b790d8b15433544d85eb6431e</td>
      <td>None</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>5069</th>
      <td>survey</td>
      <td>96d15eb0-520f-4a8f-90a3-34f391b9ab00</td>
      <td>aykI</td>
      <td>WVmB</td>
      <td>None</td>
      <td>pYhT</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:27:43+00:00</td>
      <td>2025-05-23T19:27:43+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>954e023b790d8b15433544d85eb6431e</td>
      <td>None</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
</div>




```python
me.get_project_by_id(indicator_id)
```




    id                                                               5096
    idno                             9960d5df-f2f4-477b-98ce-a58e20b829b4
    type                                                       timeseries
    title                                                       Version 1
    abbreviation                                                     None
    authoring_entity                                                 None
    nation                                                           None
    year_start                                                          0
    year_end                                                            0
    metafile                                                         None
    dirpath                              90fd4f88f588ae64038134f1eeaa023f
    varcount                                                         None
    published                                                        None
    created                                     2025-05-23T19:35:14+00:00
    changed                                     2025-05-23T19:35:14+00:00
    created_by                                                         24
    changed_by                                                         24
    thumbnail                                                        None
    metadata            {'series_description': {'idno': 'GB20250225_de...
    template_uid                                     timeseries-system-en
    is_shared                                                        None
    study_idno                                            GB20250225_demo
    attributes                                      {'database_id': None}
    dtype: object




```python
me.get_project_metadata_by_id(indicator_id, output_mode='dict')
```




    {'series_description': {'idno': 'GB20250225_demo',
      'name': 'Version 1',
      'display_name': 'Version 1'}}



So we've gotten back less than expected. That's because the default template for indicators doesn't include the top level idno or a series_description.display_name. Better to start then with an outline of the actual data we want.

# Starting with outlines

The metadata can be both large and hierarchical. Starting with a skeleton outline makes things easier.

Outlines are available in three modes - dictionary, pydantic model and as an Excel file.

## Dictionaries
Dictionaries are created like so:


```python
indicator_dict = me.make_metadata_outline('indicator', output_mode='dict')
indicator_dict
```




    {'metadata_information': {'title': None,
      'idno': None,
      'producers': [{'name': '', 'abbr': None, 'affiliation': None, 'role': None}],
      'prod_date': None,
      'version_statement': {'version': None,
       'version_date': None,
       'version_notes': None,
       'version_resp': None}},
     'series_description': {'idno': '',
      'alternate_identifiers': [{'type': None,
        'identifier': None,
        'database': None,
        'uri': None,
        'notes': None}],
      'name': '',
      'display_name': None,
      'aliases': [{'alias': None}],
      'database_id': None,
      'database_name': None,
      'date_last_update': None,
      'date_released': None,
      'definition_short': None,
      'definition_long': None,
      'definition_references': [{'source': None, 'uri': '', 'note': None}],
      'relevance': None,
      'mandate': {'mandate': None, 'uri': None},
      'data_collection': {'data_source': None,
       'method': None,
       'period': None,
       'note': None,
       'uri': None},
      'methodology': None,
      'methodology_references': [{'source': None, 'uri': '', 'note': None}],
      'derivation': None,
      'derivation_references': [{'source': None, 'uri': '', 'note': None}],
      'imputation': None,
      'imputation_references': [{'source': None, 'uri': '', 'note': None}],
      'statistical_concept': None,
      'statistical_concept_references': [{'source': None,
        'uri': '',
        'note': None}],
      'concepts': [{'name': '', 'definition': None, 'uri': None}],
      'aggregation_method': None,
      'aggregation_method_references': [{'source': None, 'uri': '', 'note': None}],
      'sources': [{'idno': None,
        'other_identifiers': [{'type': None, 'identifier': None}],
        'type': None,
        'name': '',
        'organization': None,
        'authors': [{'first_name': None,
          'initial': None,
          'last_name': None,
          'affiliation': None,
          'author_id': None,
          'full_name': None}],
        'datasets': [{'idno': None, 'title': None, 'uri': None}],
        'publisher': None,
        'publication_date': None,
        'uri': None,
        'access_date': None,
        'note': None}],
      'sources_note': None,
      'compliance': [{'standard': None,
        'abbreviation': None,
        'custodian': None,
        'uri': None}],
      'framework': [{'name': None,
        'abbreviation': None,
        'custodian': None,
        'description': None,
        'goal_id': None,
        'goal_name': None,
        'goal_description': None,
        'target_id': None,
        'target_name': None,
        'target_description': None,
        'indicator_id': None,
        'indicator_name': None,
        'indicator_description': None,
        'uri': None,
        'notes': None}],
      'limitation': None,
      'validation_rules': [],
      'quality_checks': None,
      'quality_note': None,
      'sources_discrepancies': None,
      'adjustments': [],
      'missing': None,
      'errata': [{'date': None, 'description': None, 'uri': None}],
      'acknowledgements': [{'name': None, 'affiliation': None, 'role': None}],
      'acknowledgement_statement': None,
      'disclaimer': None,
      'time_periods': [{'start': '', 'end': None}],
      'ref_country': [{'name': None, 'code': None}],
      'geographic_units': [{'name': '', 'code': None, 'type': None}],
      'bbox': [{'west': None, 'east': None, 'south': None, 'north': None}],
      'authoring_entity': [{'name': None,
        'affiliation': None,
        'abbreviation': None,
        'email': None,
        'uri': None}],
      'measurement_unit': None,
      'dimensions': [{'name': None, 'label': None, 'description': None}],
      'release_calendar': None,
      'periodicity': None,
      'base_period': None,
      'series_break': None,
      'keywords': [{'name': '', 'vocabulary': None, 'uri': None}],
      'topics': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'themes': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'disciplines': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'disaggregation': None,
      'languages': [{'name': None, 'code': None}],
      'acronyms': [{'acronym': '', 'expansion': '', 'occurrence': None}],
      'related_indicators': [{'id': None,
        'code': None,
        'label': None,
        'uri': None,
        'relationship': None,
        'type': None}],
      'series_groups': [{'name': '',
        'description': '',
        'version': None,
        'uri': None}],
      'notes': [{'note': None, 'type': None, 'uri': None}],
      'license': [{'name': None, 'uri': None, 'note': None}],
      'confidentiality': None,
      'confidentiality_status': None,
      'confidentiality_note': None,
      'citation_requirement': None,
      'links': [{'type': None, 'description': None, 'uri': ''}],
      'contacts': [{'name': None,
        'role': None,
        'position': None,
        'affiliation': None,
        'email': None,
        'telephone': None,
        'uri': None}],
      'api_documentation': [{'description': None, 'uri': ''}],
      'version_statement': {'version': None,
       'version_date': None,
       'version_notes': None,
       'version_resp': None}},
     'data_structure': [{'name': '',
       'label': None,
       'description': None,
       'data_type': None,
       'column_type': None,
       'time_period_format': None,
       'code_list': None,
       'code_list_reference': {'id': None,
        'name': None,
        'version': None,
        'uri': '',
        'note': None}}],
     'tags': [{'tag': None, 'tag_group': None}],
     'provenance': {'original_repository': {'repository_name': None,
       'url': None,
       'dataset_identifier': None,
       'doi': None,
       'dataset_title': None,
       'date_published': None,
       'notes': None},
      'source_repository': [{'repository_name': None,
        'url': None,
        'dataset_identifier': None,
        'dataset_title': None,
        'date_acquired': None,
        'acquisition_mode': None,
        'notes': None}]},
     'datacite': {'doi': None,
      'prefix': None,
      'suffix': None,
      'creators': [{'name': None,
        'name_type': None,
        'given_name': None,
        'family_name': None}],
      'titles': [{'title': None, 'title_type': None, 'lang': None}],
      'publisher': None,
      'publication_year': None,
      'types': {'resource_type': None, 'resource_type_general': None},
      'url': None,
      'language': None}}



and updated in the usual way:


```python
indicator_dict['metadata_information']['producers'][0]['name'] = "example_producer"
indicator_dict
```




    {'metadata_information': {'title': None,
      'idno': None,
      'producers': [{'name': 'example_producer',
        'abbr': None,
        'affiliation': None,
        'role': None}],
      'prod_date': None,
      'version_statement': {'version': None,
       'version_date': None,
       'version_notes': None,
       'version_resp': None}},
     'series_description': {'idno': '',
      'alternate_identifiers': [{'type': None,
        'identifier': None,
        'database': None,
        'uri': None,
        'notes': None}],
      'name': '',
      'display_name': None,
      'aliases': [{'alias': None}],
      'database_id': None,
      'database_name': None,
      'date_last_update': None,
      'date_released': None,
      'definition_short': None,
      'definition_long': None,
      'definition_references': [{'source': None, 'uri': '', 'note': None}],
      'relevance': None,
      'mandate': {'mandate': None, 'uri': None},
      'data_collection': {'data_source': None,
       'method': None,
       'period': None,
       'note': None,
       'uri': None},
      'methodology': None,
      'methodology_references': [{'source': None, 'uri': '', 'note': None}],
      'derivation': None,
      'derivation_references': [{'source': None, 'uri': '', 'note': None}],
      'imputation': None,
      'imputation_references': [{'source': None, 'uri': '', 'note': None}],
      'statistical_concept': None,
      'statistical_concept_references': [{'source': None,
        'uri': '',
        'note': None}],
      'concepts': [{'name': '', 'definition': None, 'uri': None}],
      'aggregation_method': None,
      'aggregation_method_references': [{'source': None, 'uri': '', 'note': None}],
      'sources': [{'idno': None,
        'other_identifiers': [{'type': None, 'identifier': None}],
        'type': None,
        'name': '',
        'organization': None,
        'authors': [{'first_name': None,
          'initial': None,
          'last_name': None,
          'affiliation': None,
          'author_id': None,
          'full_name': None}],
        'datasets': [{'idno': None, 'title': None, 'uri': None}],
        'publisher': None,
        'publication_date': None,
        'uri': None,
        'access_date': None,
        'note': None}],
      'sources_note': None,
      'compliance': [{'standard': None,
        'abbreviation': None,
        'custodian': None,
        'uri': None}],
      'framework': [{'name': None,
        'abbreviation': None,
        'custodian': None,
        'description': None,
        'goal_id': None,
        'goal_name': None,
        'goal_description': None,
        'target_id': None,
        'target_name': None,
        'target_description': None,
        'indicator_id': None,
        'indicator_name': None,
        'indicator_description': None,
        'uri': None,
        'notes': None}],
      'limitation': None,
      'validation_rules': [],
      'quality_checks': None,
      'quality_note': None,
      'sources_discrepancies': None,
      'adjustments': [],
      'missing': None,
      'errata': [{'date': None, 'description': None, 'uri': None}],
      'acknowledgements': [{'name': None, 'affiliation': None, 'role': None}],
      'acknowledgement_statement': None,
      'disclaimer': None,
      'time_periods': [{'start': '', 'end': None}],
      'ref_country': [{'name': None, 'code': None}],
      'geographic_units': [{'name': '', 'code': None, 'type': None}],
      'bbox': [{'west': None, 'east': None, 'south': None, 'north': None}],
      'authoring_entity': [{'name': None,
        'affiliation': None,
        'abbreviation': None,
        'email': None,
        'uri': None}],
      'measurement_unit': None,
      'dimensions': [{'name': None, 'label': None, 'description': None}],
      'release_calendar': None,
      'periodicity': None,
      'base_period': None,
      'series_break': None,
      'keywords': [{'name': '', 'vocabulary': None, 'uri': None}],
      'topics': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'themes': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'disciplines': [{'id': '',
        'name': '',
        'parent_id': None,
        'vocabulary': None,
        'uri': None}],
      'disaggregation': None,
      'languages': [{'name': None, 'code': None}],
      'acronyms': [{'acronym': '', 'expansion': '', 'occurrence': None}],
      'related_indicators': [{'id': None,
        'code': None,
        'label': None,
        'uri': None,
        'relationship': None,
        'type': None}],
      'series_groups': [{'name': '',
        'description': '',
        'version': None,
        'uri': None}],
      'notes': [{'note': None, 'type': None, 'uri': None}],
      'license': [{'name': None, 'uri': None, 'note': None}],
      'confidentiality': None,
      'confidentiality_status': None,
      'confidentiality_note': None,
      'citation_requirement': None,
      'links': [{'type': None, 'description': None, 'uri': ''}],
      'contacts': [{'name': None,
        'role': None,
        'position': None,
        'affiliation': None,
        'email': None,
        'telephone': None,
        'uri': None}],
      'api_documentation': [{'description': None, 'uri': ''}],
      'version_statement': {'version': None,
       'version_date': None,
       'version_notes': None,
       'version_resp': None}},
     'data_structure': [{'name': '',
       'label': None,
       'description': None,
       'data_type': None,
       'column_type': None,
       'time_period_format': None,
       'code_list': None,
       'code_list_reference': {'id': None,
        'name': None,
        'version': None,
        'uri': '',
        'note': None}}],
     'tags': [{'tag': None, 'tag_group': None}],
     'provenance': {'original_repository': {'repository_name': None,
       'url': None,
       'dataset_identifier': None,
       'doi': None,
       'dataset_title': None,
       'date_published': None,
       'notes': None},
      'source_repository': [{'repository_name': None,
        'url': None,
        'dataset_identifier': None,
        'dataset_title': None,
        'date_acquired': None,
        'acquisition_mode': None,
        'notes': None}]},
     'datacite': {'doi': None,
      'prefix': None,
      'suffix': None,
      'creators': [{'name': None,
        'name_type': None,
        'given_name': None,
        'family_name': None}],
      'titles': [{'title': None, 'title_type': None, 'lang': None}],
      'publisher': None,
      'publication_year': None,
      'types': {'resource_type': None, 'resource_type_general': None},
      'url': None,
      'language': None}}



## Pydantic

Pydantic is a nice python library for defining and validating data schemas. An outline for the indicator schema can be created like so:


```python
indicator_pydantic = me.make_metadata_outline('indicator', 'pydantic')
indicator_pydantic
```




    Indicator_Schema_1-0_EN(metadata_information=metadata_information(title=None, idno=None, producers=[Producer(name='', abbr=None, affiliation=None, role=None)], prod_date=None, version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), series_description=series_description(idno='', alternate_identifiers=[Alternate_identifier(type=None, identifier=None, database=None, uri=None, notes=None)], name='', display_name=None, aliases=[Aliase(alias=None)], database_id=None, database_name=None, date_last_update=None, date_released=None, definition_short=None, definition_long=None, definition_references=[Definition_reference(source=None, uri='', note=None)], relevance=None, mandate=mandate(mandate=None, uri=None), data_collection=data_collection(data_source=None, method=None, period=None, note=None, uri=None), methodology=None, methodology_references=[Methodology_reference(source=None, uri='', note=None)], derivation=None, derivation_references=[Derivation_reference(source=None, uri='', note=None)], imputation=None, imputation_references=[Imputation_reference(source=None, uri='', note=None)], statistical_concept=None, statistical_concept_references=[Statistical_concept_reference(source=None, uri='', note=None)], concepts=[Concept(name='', definition=None, uri=None)], aggregation_method=None, aggregation_method_references=[Aggregation_method_reference(source=None, uri='', note=None)], sources=[Source(idno=None, other_identifiers=[Other_identifier(type=None, identifier=None)], type=None, name='', organization=None, authors=[Author(first_name=None, initial=None, last_name=None, affiliation=None, author_id=None, full_name=None)], datasets=[Dataset(idno=None, title=None, uri=None)], publisher=None, publication_date=None, uri=None, access_date=None, note=None)], sources_note=None, compliance=[ComplianceItem(standard=None, abbreviation=None, custodian=None, uri=None)], framework=[FrameworkItem(name=None, abbreviation=None, custodian=None, description=None, goal_id=None, goal_name=None, goal_description=None, target_id=None, target_name=None, target_description=None, indicator_id=None, indicator_name=None, indicator_description=None, uri=None, notes=None)], limitation=None, validation_rules=[], quality_checks=None, quality_note=None, sources_discrepancies=None, adjustments=[], missing=None, errata=[ErrataItem(date=None, description=None, uri=None)], acknowledgements=[Acknowledgement(name=None, affiliation=None, role=None)], acknowledgement_statement=None, disclaimer=None, time_periods=[Time_period(start='', end=None)], ref_country=[Ref_countryItem(name=None, code=None)], geographic_units=[Geographic_unit(name='', code=None, type=None)], bbox=[BboxItem(west=None, east=None, south=None, north=None)], authoring_entity=[Authoring_entityItem(name=None, affiliation=None, abbreviation=None, email=None, uri=None)], measurement_unit=None, dimensions=[Dimension(name=None, label=None, description=None)], release_calendar=None, periodicity=None, base_period=None, series_break=None, keywords=[Keyword(name='', vocabulary=None, uri=None)], topics=[Topic(id='', name='', parent_id=None, vocabulary=None, uri=None)], themes=[Theme(id='', name='', parent_id=None, vocabulary=None, uri=None)], disciplines=[Discipline(id='', name='', parent_id=None, vocabulary=None, uri=None)], disaggregation=None, languages=[Language(name=None, code=None)], acronyms=[Acronym(acronym='', expansion='', occurrence=None)], related_indicators=[Related_indicator(id=None, code=None, label=None, uri=None, relationship=None, type=None)], series_groups=[Series_group(name='', description='', version=None, uri=None)], notes=[Note(note=None, type=None, uri=None)], license=[LicenseItem(name=None, uri=None, note=None)], confidentiality=None, confidentiality_status=None, confidentiality_note=None, citation_requirement=None, links=[Link(type=None, description=None, uri='')], contacts=[Contact(name=None, role=None, position=None, affiliation=None, email=None, telephone=None, uri=None)], api_documentation=[Api_documentationItem(description=None, uri='')], version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), data_structure=[Data_structureItem(name='', label=None, description=None, data_type=None, column_type=None, time_period_format=None, code_list=None, code_list_reference=code_list_reference(id=None, name=None, version=None, uri='', note=None))], tags=[Tag(tag=None, tag_group=None)], provenance=provenance(original_repository=original_repository(repository_name=None, url=None, dataset_identifier=None, doi=None, dataset_title=None, date_published=None, notes=None), source_repository=[Source_repositoryItem(repository_name=None, url=None, dataset_identifier=None, dataset_title=None, date_acquired=None, acquisition_mode=None, notes=None)]), datacite=datacite(doi=None, prefix=None, suffix=None, creators=[Creator(name=None, name_type=None, given_name=None, family_name=None)], titles=[Title(title=None, title_type=None, lang=None)], publisher=None, publication_year=None, types=types(resource_type=None, resource_type_general=None), url=None, language=None))



It can be updated using dot notation, for example:


```python
indicator_pydantic.metadata_information.producers[0].name = "example_producer"
indicator_pydantic
```




    Indicator_Schema_1-0_EN(metadata_information=metadata_information(title=None, idno=None, producers=[Producer(name='example_producer', abbr=None, affiliation=None, role=None)], prod_date=None, version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), series_description=series_description(idno='', alternate_identifiers=[Alternate_identifier(type=None, identifier=None, database=None, uri=None, notes=None)], name='', display_name=None, aliases=[Aliase(alias=None)], database_id=None, database_name=None, date_last_update=None, date_released=None, definition_short=None, definition_long=None, definition_references=[Definition_reference(source=None, uri='', note=None)], relevance=None, mandate=mandate(mandate=None, uri=None), data_collection=data_collection(data_source=None, method=None, period=None, note=None, uri=None), methodology=None, methodology_references=[Methodology_reference(source=None, uri='', note=None)], derivation=None, derivation_references=[Derivation_reference(source=None, uri='', note=None)], imputation=None, imputation_references=[Imputation_reference(source=None, uri='', note=None)], statistical_concept=None, statistical_concept_references=[Statistical_concept_reference(source=None, uri='', note=None)], concepts=[Concept(name='', definition=None, uri=None)], aggregation_method=None, aggregation_method_references=[Aggregation_method_reference(source=None, uri='', note=None)], sources=[Source(idno=None, other_identifiers=[Other_identifier(type=None, identifier=None)], type=None, name='', organization=None, authors=[Author(first_name=None, initial=None, last_name=None, affiliation=None, author_id=None, full_name=None)], datasets=[Dataset(idno=None, title=None, uri=None)], publisher=None, publication_date=None, uri=None, access_date=None, note=None)], sources_note=None, compliance=[ComplianceItem(standard=None, abbreviation=None, custodian=None, uri=None)], framework=[FrameworkItem(name=None, abbreviation=None, custodian=None, description=None, goal_id=None, goal_name=None, goal_description=None, target_id=None, target_name=None, target_description=None, indicator_id=None, indicator_name=None, indicator_description=None, uri=None, notes=None)], limitation=None, validation_rules=[], quality_checks=None, quality_note=None, sources_discrepancies=None, adjustments=[], missing=None, errata=[ErrataItem(date=None, description=None, uri=None)], acknowledgements=[Acknowledgement(name=None, affiliation=None, role=None)], acknowledgement_statement=None, disclaimer=None, time_periods=[Time_period(start='', end=None)], ref_country=[Ref_countryItem(name=None, code=None)], geographic_units=[Geographic_unit(name='', code=None, type=None)], bbox=[BboxItem(west=None, east=None, south=None, north=None)], authoring_entity=[Authoring_entityItem(name=None, affiliation=None, abbreviation=None, email=None, uri=None)], measurement_unit=None, dimensions=[Dimension(name=None, label=None, description=None)], release_calendar=None, periodicity=None, base_period=None, series_break=None, keywords=[Keyword(name='', vocabulary=None, uri=None)], topics=[Topic(id='', name='', parent_id=None, vocabulary=None, uri=None)], themes=[Theme(id='', name='', parent_id=None, vocabulary=None, uri=None)], disciplines=[Discipline(id='', name='', parent_id=None, vocabulary=None, uri=None)], disaggregation=None, languages=[Language(name=None, code=None)], acronyms=[Acronym(acronym='', expansion='', occurrence=None)], related_indicators=[Related_indicator(id=None, code=None, label=None, uri=None, relationship=None, type=None)], series_groups=[Series_group(name='', description='', version=None, uri=None)], notes=[Note(note=None, type=None, uri=None)], license=[LicenseItem(name=None, uri=None, note=None)], confidentiality=None, confidentiality_status=None, confidentiality_note=None, citation_requirement=None, links=[Link(type=None, description=None, uri='')], contacts=[Contact(name=None, role=None, position=None, affiliation=None, email=None, telephone=None, uri=None)], api_documentation=[Api_documentationItem(description=None, uri='')], version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), data_structure=[Data_structureItem(name='', label=None, description=None, data_type=None, column_type=None, time_period_format=None, code_list=None, code_list_reference=code_list_reference(id=None, name=None, version=None, uri='', note=None))], tags=[Tag(tag=None, tag_group=None)], provenance=provenance(original_repository=original_repository(repository_name=None, url=None, dataset_identifier=None, doi=None, dataset_title=None, date_published=None, notes=None), source_repository=[Source_repositoryItem(repository_name=None, url=None, dataset_identifier=None, dataset_title=None, date_acquired=None, acquisition_mode=None, notes=None)]), datacite=datacite(doi=None, prefix=None, suffix=None, creators=[Creator(name=None, name_type=None, given_name=None, family_name=None)], titles=[Title(title=None, title_type=None, lang=None)], publisher=None, publication_year=None, types=types(resource_type=None, resource_type_general=None), url=None, language=None))



### Printing

The pydantic metadata object also contains a helper function for printing metadata:


```python
indicator_pydantic.pretty_print()
```


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">Indicator_Schema_1-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">0_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">metadata_information</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">metadata_information</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'example_producer'</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">prod_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">series_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">series_description</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
        <span style="color: #808000; text-decoration-color: #808000">alternate_identifiers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Alternate_identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">database</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
        <span style="color: #808000; text-decoration-color: #808000">display_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">aliases</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Aliase</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">alias</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">database_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">database_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_last_update</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_released</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_short</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_long</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Definition_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">relevance</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">mandate</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_collection</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_collection</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">data_source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">method</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">period</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">methodology</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">methodology_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Methodology_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">derivation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">derivation_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Derivation_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">imputation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">imputation_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Imputation_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">statistical_concept</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">statistical_concept_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Statistical_concept_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">concepts</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Concept</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">definition</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">aggregation_method</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">aggregation_method_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Aggregation_method_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">other_identifiers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Other_identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">organization</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">authors</span>=<span style="font-weight: bold">[</span>
                    <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Author</span><span style="font-weight: bold">(</span>
                        <span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                        <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                        <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                        <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                        <span style="color: #808000; text-decoration-color: #808000">author_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                        <span style="color: #808000; text-decoration-color: #808000">full_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
                    <span style="font-weight: bold">)</span>
                <span style="font-weight: bold">]</span>,
                <span style="color: #808000; text-decoration-color: #808000">datasets</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Dataset</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">publisher</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">publication_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">access_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">compliance</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ComplianceItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">standard</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">framework</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">FrameworkItem</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">limitation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">validation_rules</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">quality_checks</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">quality_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_discrepancies</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">adjustments</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">missing</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">errata</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ErrataItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">acknowledgements</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Acknowledgement</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">acknowledgement_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">disclaimer</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">time_periods</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Time_period</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">ref_country</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Ref_countryItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">geographic_units</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Geographic_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">east</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">south</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">north</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">authoring_entity</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Authoring_entityItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">measurement_unit</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">dimensions</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Dimension</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">release_calendar</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">periodicity</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">base_period</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_break</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">themes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Theme</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disciplines</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Discipline</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disaggregation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">languages</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">acronyms</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Acronym</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">acronym</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">expansion</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">occurrence</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">related_indicators</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_groups</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Series_group</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">license</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">LicenseItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_status</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">citation_requirement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">links</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">contacts</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contact</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">position</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">telephone</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">api_documentation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Api_documentationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">data_structure</span>=<span style="font-weight: bold">[</span>
        <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_structureItem</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">column_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">time_period_format</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">code_list</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">code_list_reference</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">code_list_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">]</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Tag</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">tag</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">tag_group</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
    <span style="color: #808000; text-decoration-color: #808000">provenance</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">provenance</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">original_repository</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">original_repository</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">repository_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">dataset_identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">doi</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">dataset_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">date_published</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">source_repository</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source_repositoryItem</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">repository_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">dataset_identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">dataset_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">date_acquired</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">acquisition_mode</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">datacite</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">datacite</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">doi</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">prefix</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">suffix</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">creators</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Creator</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">given_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">family_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">titles</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Title</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">title_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">lang</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">publisher</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">publication_year</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">types</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">types</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">resource_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">resource_type_general</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">language</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
    <span style="font-weight: bold">)</span>
<span style="font-weight: bold">)</span>
</pre>



We can also convert back to a dictionary and we can choose to simplfy which excludes Nones, empty strings, empty lists and empty dictionaries


```python
me.change_mode_or_template(indicator_pydantic, output_mode='dict', simplify=True)
```




    {'metadata_information': {'producers': [{'name': 'example_producer'}]}}



## Excel

Finally, a nicely formatted Excel file can be created into which the metadata can be written, with the name of the metadata type or of the default template used as the filename if no filename is explicitly given.


```python
outline_filename = me.make_metadata_outline('indicator', 'excel')
outline_filename
```




    'Indicator_Schema_1-0_EN_metadata.xlsx'




```python
indicator_excel = me.read_metadata_from_excel(outline_filename)
```


```python
# Tidy up the file
os.remove(outline_filename)
```

## Retreiving existing metadata

Likewise, existing projects can be downloaded as either dictionaries, pydantic models or as excel spreadsheets.


```python
demo_dict = me.get_project_metadata_by_id(indicator_id, output_mode='dict')
demo_dict
```




    {'series_description': {'idno': 'GB20250225_demo',
      'name': 'Version 1',
      'display_name': 'Version 1'}}




```python
demo_pydantic = me.get_project_metadata_by_id(indicator_id, 'pydantic')
demo_pydantic
```




    Indicator_Schema_1-0_EN(metadata_information=metadata_information(title=None, idno=None, producers=[Producer(name='', abbr=None, affiliation=None, role=None)], prod_date=None, version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), series_description=series_description(idno='GB20250225_demo', alternate_identifiers=[Alternate_identifier(type=None, identifier=None, database=None, uri=None, notes=None)], name='Version 1', display_name='Version 1', aliases=[Aliase(alias=None)], database_id=None, database_name=None, date_last_update=None, date_released=None, definition_short=None, definition_long=None, definition_references=[Definition_reference(source=None, uri='', note=None)], relevance=None, mandate=mandate(mandate=None, uri=None), data_collection=data_collection(data_source=None, method=None, period=None, note=None, uri=None), methodology=None, methodology_references=[Methodology_reference(source=None, uri='', note=None)], derivation=None, derivation_references=[Derivation_reference(source=None, uri='', note=None)], imputation=None, imputation_references=[Imputation_reference(source=None, uri='', note=None)], statistical_concept=None, statistical_concept_references=[Statistical_concept_reference(source=None, uri='', note=None)], concepts=[Concept(name='', definition=None, uri=None)], aggregation_method=None, aggregation_method_references=[Aggregation_method_reference(source=None, uri='', note=None)], sources=[Source(idno=None, other_identifiers=[Other_identifier(type=None, identifier=None)], type=None, name='', organization=None, authors=[Author(first_name=None, initial=None, last_name=None, affiliation=None, author_id=None, full_name=None)], datasets=[Dataset(idno=None, title=None, uri=None)], publisher=None, publication_date=None, uri=None, access_date=None, note=None)], sources_note=None, compliance=[ComplianceItem(standard=None, abbreviation=None, custodian=None, uri=None)], framework=[FrameworkItem(name=None, abbreviation=None, custodian=None, description=None, goal_id=None, goal_name=None, goal_description=None, target_id=None, target_name=None, target_description=None, indicator_id=None, indicator_name=None, indicator_description=None, uri=None, notes=None)], limitation=None, validation_rules=[], quality_checks=None, quality_note=None, sources_discrepancies=None, adjustments=[], missing=None, errata=[ErrataItem(date=None, description=None, uri=None)], acknowledgements=[Acknowledgement(name=None, affiliation=None, role=None)], acknowledgement_statement=None, disclaimer=None, time_periods=[Time_period(start='', end=None)], ref_country=[Ref_countryItem(name=None, code=None)], geographic_units=[Geographic_unit(name='', code=None, type=None)], bbox=[BboxItem(west=None, east=None, south=None, north=None)], authoring_entity=[Authoring_entityItem(name=None, affiliation=None, abbreviation=None, email=None, uri=None)], measurement_unit=None, dimensions=[Dimension(name=None, label=None, description=None)], release_calendar=None, periodicity=None, base_period=None, series_break=None, keywords=[Keyword(name='', vocabulary=None, uri=None)], topics=[Topic(id='', name='', parent_id=None, vocabulary=None, uri=None)], themes=[Theme(id='', name='', parent_id=None, vocabulary=None, uri=None)], disciplines=[Discipline(id='', name='', parent_id=None, vocabulary=None, uri=None)], disaggregation=None, languages=[Language(name=None, code=None)], acronyms=[Acronym(acronym='', expansion='', occurrence=None)], related_indicators=[Related_indicator(id=None, code=None, label=None, uri=None, relationship=None, type=None)], series_groups=[Series_group(name='', description='', version=None, uri=None)], notes=[Note(note=None, type=None, uri=None)], license=[LicenseItem(name=None, uri=None, note=None)], confidentiality=None, confidentiality_status=None, confidentiality_note=None, citation_requirement=None, links=[Link(type=None, description=None, uri='')], contacts=[Contact(name=None, role=None, position=None, affiliation=None, email=None, telephone=None, uri=None)], api_documentation=[Api_documentationItem(description=None, uri='')], version_statement=version_statement(version=None, version_date=None, version_notes=None, version_resp=None)), data_structure=[Data_structureItem(name='', label=None, description=None, data_type=None, column_type=None, time_period_format=None, code_list=None, code_list_reference=code_list_reference(id=None, name=None, version=None, uri='', note=None))], tags=[Tag(tag=None, tag_group=None)], provenance=provenance(original_repository=original_repository(repository_name=None, url=None, dataset_identifier=None, doi=None, dataset_title=None, date_published=None, notes=None), source_repository=[Source_repositoryItem(repository_name=None, url=None, dataset_identifier=None, dataset_title=None, date_acquired=None, acquisition_mode=None, notes=None)]), datacite=datacite(doi=None, prefix=None, suffix=None, creators=[Creator(name=None, name_type=None, given_name=None, family_name=None)], titles=[Title(title=None, title_type=None, lang=None)], publisher=None, publication_year=None, types=types(resource_type=None, resource_type_general=None), url=None, language=None))




```python
excel_filename = demo_name+'.xlsx'
me.get_project_metadata_by_id(indicator_id, output_mode='excel', filename=excel_filename)
```




    'GB20250225_demo.xlsx'



### Updating an existing project

You can create and update projects with metadata as either dictionaries, pydantic models or in Excel files. 


```python
indicator_id
```




    5096




```python
demo_dict
```




    {'series_description': {'idno': 'GB20250225_demo',
      'name': 'Version 1',
      'display_name': 'Version 1'}}




```python
me.update_project_log_by_id(indicator_id, demo_dict)
```


```python
me.update_project_log_by_id(indicator_id, demo_pydantic)
```


```python
me.update_project_log_by_id(indicator_id, excel_filename)
# tidy up the file
os.remove(excel_filename)
```

### Updating with patch updates

You can also update metadata with patch updates. With this method you can add, update, or remove parts of a project's metadata using a single JSON Patch operation.

"JSON Patch is a format for describing changes to a JSON document. It can be used to avoid sending a whole
document when only a part has changed." (https://jsonpatch.com/ accessed 2024-08-20)

JSON Patch Operations:

- `add`: Adds a value to the specified path. If the path already exists, the value is replaced.
- `remove`: Removes the value at the specified path.
- `replace`: Replaces the value at the specified path with a new value.
- `test`: Tests that the specified path contains the given value.

The `path` is a string that uses a slash (`/`) notation to specify the location within the metadata.



```python
# add a value that was previously empty
me.patch_update_project_log_by_id(indicator_id, 'add', '/series_description/definition_short', 'This is a test description')
# test that a specified value is set
me.patch_update_project_log_by_id(indicator_id, 'test', '/series_description/definition_short', 'This is a test description')
# change a value
me.patch_update_project_log_by_id(indicator_id, 'replace', '/series_description/definition_short', 'This is a new test description')
# remove a value
me.patch_update_project_log_by_id(indicator_id, 'remove', '/series_description/definition_short')

```

# Collections

We can list and create collections, we can add and remove projects from collections and we can apply templates to collections.


```python
me.list_collections().head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>description</th>
      <th>created</th>
      <th>changed</th>
      <th>created_by</th>
      <th>changed_by</th>
      <th>pid</th>
      <th>wgt</th>
      <th>username</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>183</th>
      <td>aa</td>
      <td>aa</td>
      <td>2025-03-31T06:59:18+00:00</td>
      <td>2025-03-31T06:59:18+00:00</td>
      <td>39</td>
      <td>39</td>
      <td>3</td>
      <td>None</td>
      <td>outsourcify</td>
    </tr>
    <tr>
      <th>8</th>
      <td>aL-moved</td>
      <td>Collection description Text</td>
      <td>1970-01-01T00:33:43+00:00</td>
      <td>2024-02-06T04:04:35+00:00</td>
      <td>13</td>
      <td>20</td>
      <td>None</td>
      <td>None</td>
      <td>chriskrestel</td>
    </tr>
    <tr>
      <th>18</th>
      <td>CCKP</td>
      <td>World Bank Climate Change Knowledge Platform</td>
      <td>2024-06-05T02:04:21+00:00</td>
      <td>2024-06-05T02:04:21+00:00</td>
      <td>2</td>
      <td>2</td>
      <td>None</td>
      <td>None</td>
      <td>Olivier Dupriez</td>
    </tr>
    <tr>
      <th>85</th>
      <td>Demo Collection</td>
      <td>Demo Collection</td>
      <td>2024-10-08T19:19:28+00:00</td>
      <td>2024-10-08T19:19:28+00:00</td>
      <td>25</td>
      <td>25</td>
      <td>None</td>
      <td>None</td>
      <td>vmascarinas</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Emmanuel</td>
      <td>None</td>
      <td>2024-04-30T13:23:31+00:00</td>
      <td>2024-04-30T13:23:31+00:00</td>
      <td>2</td>
      <td>2</td>
      <td>None</td>
      <td>None</td>
      <td>Olivier Dupriez</td>
    </tr>
  </tbody>
</table>
</div>




```python
collection_id = me.create_collection(demo_name+"_collection", description = "An example collection for demonstration")
```


```python
me.get_collection_by_id(collection_id)
```




    id                                                 213
    title                       GB20250225_demo_collection
    description    An example collection for demonstration
    created                                     1748028923
    changed                                     1748028923
    created_by                                          24
    changed_by                                          24
    pid                                               None
    wgt                                               None
    dtype: object



### Populating collections


```python
me.add_projects_to_collection(collection=collection_id, id_format='id', projects=[indicator_id])
```


```python
me.list_projects_in_collection(collection=collection_id, limit=5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>idno</th>
      <th>study_idno</th>
      <th>title</th>
      <th>abbreviation</th>
      <th>nation</th>
      <th>year_start</th>
      <th>year_end</th>
      <th>published</th>
      <th>created</th>
      <th>changed</th>
      <th>varcount</th>
      <th>created_by</th>
      <th>changed_by</th>
      <th>is_shared</th>
      <th>thumbnail</th>
      <th>template_uid</th>
      <th>attributes</th>
      <th>username</th>
      <th>username_cr</th>
      <th>collections</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5096</th>
      <td>timeseries</td>
      <td>9960d5df-f2f4-477b-98ce-a58e20b829b4</td>
      <td>GB20250225_demo</td>
      <td>Version 1</td>
      <td>None</td>
      <td>None</td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-05-23T19:35:14+00:00</td>
      <td>2025-05-23T19:35:23+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>timeseries-system-en</td>
      <td>{'database_id': None}</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[{'id': '213', 'title': 'GB20250225_demo_colle...</td>
    </tr>
  </tbody>
</table>
</div>




```python
me.remove_projects_from_collection(collection=collection_id, id_format='id', projects=[indicator_id])
```

### Deleting Collections


```python
me.delete_collection_by_id(collection_id)
```

# Templates

Different organizations often want to specify the use of different subsets of metadata. We can list templates and see which templates are the default for our organization.


```python
me.list_templates().head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uid</th>
      <th>template_type</th>
      <th>name</th>
      <th>data_type</th>
      <th>lang</th>
      <th>template</th>
      <th>default</th>
      <th>id</th>
      <th>version</th>
      <th>organization</th>
      <th>author</th>
      <th>description</th>
      <th>instructions</th>
      <th>created</th>
      <th>created_by</th>
      <th>changed</th>
      <th>changed_by</th>
      <th>owner_id</th>
      <th>deleted_at</th>
      <th>deleted_by</th>
      <th>is_deleted</th>
      <th>owner_username</th>
      <th>owner_email</th>
      <th>changed_by_username</th>
      <th>changed_by_email</th>
      <th>created_by_username</th>
      <th>created_by_email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>microdata-system-en</td>
      <td>core</td>
      <td>Microdata DDI 2.5 EN</td>
      <td>survey</td>
      <td>en</td>
      <td>metadata_editor/metadata_editor_templates/surv...</td>
      <td>False</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>232ea3aaece0cdf1db157f797f6b92e5fr</td>
      <td>core</td>
      <td>IHSN DDI 2.5 Modèle v01 FR</td>
      <td>survey</td>
      <td>fr</td>
      <td>metadata_editor/metadata_editor_templates/surv...</td>
      <td>False</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6740f5f920502baf3f6cbcaa5c113deeen</td>
      <td>core</td>
      <td>IHSN DDI 2.5 Template v01 EN</td>
      <td>survey</td>
      <td>en</td>
      <td>metadata_editor/metadata_editor_templates/surv...</td>
      <td>False</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>timeseries-system-en</td>
      <td>core</td>
      <td>Indicator Schema 1.0 EN</td>
      <td>timeseries</td>
      <td>en</td>
      <td>metadata_editor/metadata_editor_templates/time...</td>
      <td>True</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8603d94e27bccc2bdad1e00dbbf0fe32en</td>
      <td>core</td>
      <td>IHSN INDICATOR 1.0 Template v01 EN</td>
      <td>timeseries</td>
      <td>en</td>
      <td>metadata_editor/metadata_editor_templates/time...</td>
      <td>False</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
me.get_template_by_uid("microdata-system-en")
```

    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:530: UserWarning: SkippingCustomElement: '{'type': 'section_container', 'key': 'file_description', 'title': 'Data files', 'is_custom': True, 'items': [{'type': 'section', 'key': 'data_file', 'title': 'Data file description', 'items': [{'key': 'data_file.file_id', 'title': 'File ID', 'type': 'string', 'enum': [], 'help_text': 'A unique file identifier (within the metadata document, not necessarily within a catalog). This will typically be the electronic file name.', 'is_required': True, 'display_type': 'text'}, {'key': 'data_file.file_name', 'title': 'File name', 'type': 'string', 'enum': [], 'help_text': 'This is not the name of the electronic file (which is provided in the previous element). It is a short title (label) that will help distinguish a particular file/part from other files/parts in the dataset.', 'is_required': True, 'display_type': 'text'}, {'key': 'data_file.file_type', 'title': 'File type', 'type': 'string', 'enum': [], 'help_text': 'The type of data files. For example, raw data (ASCII), or software-dependent files such as SAS / Stata / SPSS data file, etc. Provide specific information (e.g. Stata 10 or Stata 15, SPSS Windows or SPSS Export, etc.) Note that in an on-line catalog, data can be made available in multiple formats. In such case, the file_type element is not useful.', 'display_type': 'text'}, {'key': 'data_file.description', 'title': 'Description', 'type': 'string', 'enum': [], 'help_text': 'The "File ID" and "File name" elements provide limited information on the content of the file. The description element is used to provide a more detailed description of the file content. This description should clearly distinguish collected variables and derived variables. It is also useful to indicate the availability in the data file of some particular variables such as the weighting coefficients. If the file contains derived variables, it is good practice to refer to the computer program that generated it. Information about the data file(s) that comprises a collection.', 'display_type': 'textarea'}, {'key': 'data_file.case_count', 'title': 'Case count', 'type': 'integer', 'enum': [], 'help_text': 'Number of cases or observations in the data file. The value is 0 by default. This information will be automatically generated in Metadata Editors that provide an option to import data files.', 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'data_file.var_count', 'title': 'Variable count', 'type': 'integer', 'enum': [], 'help_text': 'Number of variables in the data file. The value is 0 by default.  This information will be automatically generated in Metadata Editors that provide an option to import data files.', 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'data_file.producer', 'title': 'Producer', 'type': 'string', 'enum': [], 'help_text': 'The name of the agency that produced the data file. Most data files will have been produced by the survey primary investigator. In some cases however, auxiliary or derived files from other producers may be released with a data set. This may for example be a file containing derived variables generated by a researcher.', 'display_type': 'text'}, {'key': 'data_file.data_checks', 'title': 'Data checks', 'type': 'string', 'enum': [], 'help_text': 'Use this element if needed to provide information about the types of checks and operations that have been performed on the data file to make sure that the data are as correct as possible, e.g. consistency checking, wildcode checking, etc. Note that the information included here should be specific to the data file. Information about data processing checks that have been carried out on the data collection (study) as a whole should be provided in the Data editing element at the study level. You may also provide here a reference to an external resource that contains the specifications for the data processing checks (that same information may be provided also in the Data Editing filed in the Study Description section).', 'display_type': 'textarea'}, {'key': 'data_file.missing_data', 'title': 'Missing data', 'type': 'string', 'enum': [], 'help_text': 'A description of missing data (number of missing cases, cause of missing values, etc.)', 'display_type': 'textarea'}, {'key': 'data_file.version', 'title': 'Version', 'type': 'string', 'enum': [], 'help_text': 'The version of the data file. A data file may undergo various changes and modifications. File specific versions can be tracked in this element. This field will in most cases be left empty.', 'display_type': 'textarea'}, {'key': 'data_file.notes', 'title': 'Notes on data file', 'type': 'string', 'enum': [], 'help_text': 'This field aims to provide information on the specific data file not covered elsewhere.', 'display_type': 'textarea'}]}]}' - Future work required to support these.
      warnings.warn(f"SkippingCustomElement: '{item}' - Future work required to support these.")
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:530: UserWarning: SkippingCustomElement: '{'type': 'section_container', 'key': 'variable_description', 'title': 'Variables', 'is_custom': True, 'items': [{'type': 'section', 'key': 'variable', 'title': 'Variable description', 'items': [{'key': 'variable.file_id', 'title': 'File ID', 'type': 'string', 'enum': [], 'help_text': 'A dataset can be composed of multiple data files. The File ID is the name of the data file that contains the variable being documented. This file name should correspond to a File ID listed in the "Data file description" section of the DDI. When using a Metadata Editor application, this information will typically be automatically generated when importing data files. This information is required.', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.vid', 'title': 'Variable ID', 'type': 'string', 'enum': [], 'help_text': 'A unique identifier given to the variable (unique within the full dataset, not only within a data file). This information is required. This is NOT the variable name (captured in element "Variable name"). This can be a system-generated ID, such as a sequential number within each data file. When using a Metadata Editor application, the ID will typically be automatically generated when importing data files. ', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.name', 'title': 'Variable name', 'type': 'string', 'enum': [], 'help_text': 'The name of the variable in the data file. This information is required. The name should be entered exactly as found in the data file (not abbreviated or converted to upper or lower cases, as some software applications are case-sensitive). This information can be programmatically extracted from the data file. When using a Metadata Editor application, the variable name will typically be extracted from the imported data files. The variable name is limited to eight characters in some statistical analysis software such as SAS or SPSS. A variable name must be unique within a data file (not within a full dataset, as a same variable may appear in multiple data files). ', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.labl', 'title': 'Variable label', 'type': 'string', 'enum': [], 'help_text': 'All variables should have a label that provides a short but clear indication of what the variable contains. Ideally, all variables in a data file will have a unique label. File formats like Stata or SPSS often contain variable labels. When using a Metadata Editor application, the variable name will typically be extracted from the imported data files. Variable labels can also be found in data dictionaries in software applications like Survey Solutions or CsPro. Avoid using the question itself as a label (specific elements are available to capture the literal question text). Think of a label as what you would want to see in a tabulation of the variables. Keep in mind that software applications like Stata and others impose a limit to the number of characters in a label (often, 80). \n', 'is_recommended': True, 'display_type': 'text'}, {'key': 'variable.var_universe', 'title': 'Universe', 'type': 'string', 'help_text': 'The universe at the variable level defines the population the question applied to. It reflects skip patterns in a questionnaire. This information can typically be copy/pasted from the survey questionnaire. Try to be as specific as possible. This information is critical for the analyst, as it explains why missing values may be found in a variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_txt', 'title': 'Variable definition', 'type': 'string', 'help_text': 'This element provides a space to describe the variable in detail. Not all variables require a definition.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_concept', 'title': 'Concepts', 'type': 'array', 'help_text': 'The general subject to which the parent element may be seen as pertaining. This element serves the same purpose as the keywords and topic classification elements, but at the variable description level.', 'props': [{'key': 'title', 'title': 'Title', 'type': 'string', 'prop_key': 'variable.var_concept.title', 'help_text': 'The name (label) of the concept.', 'display_type': 'text'}, {'key': 'vocab', 'title': 'Vocabulary', 'type': 'string', 'prop_key': 'variable.var_concept.vocab', 'help_text': 'The controlled vocabulary, if any, from which the concept `title’ was taken.', 'display_type': 'text'}, {'key': 'uri', 'title': 'URL', 'type': 'string', 'prop_key': 'variable.var_concept.uri', 'help_text': 'A link (URL) to the controlled vocabulary mentioned in "Vocabulary".', 'display_type': 'text', 'rules': {'is_uri': True}}]}, {'key': 'variable.var_sumstat', 'title': 'Summary statistics', 'type': 'array', 'help_text': 'The DDI metadata standard provides multiple elements to capture various summary statistics such as minimum, maximum, or mean values (weighted and un-weighted) for each variable. The content of the "Summary statistics" section will be easy to fill out programmatically (using R or Python) or using a specialized DDI metadata editor, which can read the data file and generate the summary statistics.\n', 'props': [{'key': 'type', 'title': 'Type', 'type': 'string', 'prop_key': 'variable.var_sumstat.type', 'help_text': 'The type of statistics being shown: mean, median, mode, valid cases, invalid cases, minimum, maximum, or standard deviation.', 'display_type': 'textarea'}, {'key': 'value', 'title': 'Value', 'type': 'string', 'prop_key': 'variable.var_sumstat.value', 'help_text': 'The value of the summary statistics mentioned in type.', 'display_type': 'text'}, {'key': 'wgtd', 'title': 'Weighted', 'type': 'string', 'prop_key': 'variable.var_sumstat.wgtd', 'help_text': 'Indicates whether the statistics reported in value are weighted or not (for variables in sample surveys). Enter “weighted” if weighted, otherwise leave this element empty.', 'display_type': 'text', 'enum': []}]}, {'key': 'variable.var_catgry', 'title': 'Variable categories', 'type': 'array', 'props': [{'key': 'value', 'title': 'Code', 'type': 'string', 'prop_key': 'variable.var_catgry.value', 'help_text': 'The code of the category.', 'display_type': 'text'}, {'key': 'label', 'title': 'Label', 'type': 'string', 'prop_key': 'variable.var_catgry.label', 'help_text': 'The label of the category (or "value label")', 'display_type': 'text'}, {'key': 'stats', 'title': 'Statistics', 'type': 'array', 'props': [{'key': 'type', 'title': 'Type', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.type', 'help_text': 'Type of statistics, e.g. "Count".', 'display_type': 'text'}, {'key': 'value', 'title': 'Value', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.value', 'help_text': 'Estimate', 'display_type': 'text'}, {'key': 'wgtd', 'title': 'Weighted', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.wgtd', 'help_text': 'Indicates whether the "Value" is weighted (for sample surveys) or not.', 'display_type': 'text'}], 'prop_key': 'variable.var_catgry.stats'}], 'help_text': 'A description of the categories (codes with labels) that apply to the variable, for categorical variables. The element also includes summary statistics at the category level.'}, {'key': 'variable.var_std_catgry', 'title': 'Standard categories', 'type': 'array', 'help_text': 'This element is used to indicate that the codes used for a categorical variable are from a standard international or other classification, like COICOP, ISIC, ISO country codes, etc.', 'props': [{'key': 'name', 'title': 'Name', 'type': 'string', 'prop_key': 'variable.var_std_catgry.name', 'help_text': 'The name of the classification, e.g. “International Standard Industrial Classification of All Economic Activities (ISIC), Revision 4”', 'display_type': 'text'}, {'key': 'source', 'title': 'Source', 'type': 'string', 'prop_key': 'variable.var_std_catgry.source', 'help_text': 'The source of the classification, for example “United Nations”.', 'display_type': 'text'}, {'key': 'date', 'title': 'Date', 'type': 'string', 'prop_key': 'variable.var_std_catgry.date', 'help_text': 'The version (typically a date) of the classification used for the study.', 'display_type': 'text'}, {'key': 'uri', 'title': 'URL', 'type': 'string', 'prop_key': 'variable.var_std_catgry.uri', 'help_text': 'A URL to a website where an electronic copy and more information on the classification can be obtained.', 'rules': {'is_uri': True}, 'display_type': 'text'}]}, {'key': 'variable.var_intrvl', 'title': 'Interval type', 'help_text': 'This element indicates whether the intervals between values for the variable are discrete or continuous.', 'type': 'string', 'enum': [{'code': 'discrete', 'label': 'Discrete'}, {'code': 'continuous', 'label': 'Continuous'}], 'display_type': 'dropdown'}, {'key': 'variable.var_dcml', 'title': 'Decimal points', 'type': 'string', 'help_text': 'This element refers to the number of decimal points in the values of the variable. It must be a numeric value.', 'enum': [], 'display_type': 'text'}, {'key': 'variable.is_key', 'title': 'Key variable', 'type': 'integer', 'help_text': 'This element indicates whether the variable is a key variable (value "1") or not (value "0"). Key variables are used to identify records in a data file. They are typically unique identifiers such as ID numbers, or other variables that can be used to uniquely identify a record.', 'default': 0, 'enum': [{'code': '0', 'label': 'Not a key variable'}, {'code': '1', 'label': 'Key variable'}], 'display_type': 'dropdown'}, {'key': 'variable.var_wgt', 'title': 'Is weight', 'type': 'integer', 'help_text': 'This element, which applies to dataset from sample surveys, indicates whether the variable is a sample weight (value “1”) or not (value "0). Sample weights play an important role in the calculation of summary statistics and sampling errors, and should therefore be flagged.', 'default': 0, 'enum': [{'code': '0', 'label': 'Not a weight'}, {'code': '1', 'label': 'Weight'}], 'display_type': 'dropdown'}, {'key': 'variable.var_security', 'title': 'Security', 'type': 'string', 'help_text': 'This element is used to provide information regarding levels of access, e.g., public, subscriber, need to know.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_notes', 'title': 'Notes on variable', 'type': 'string', 'help_text': 'This element is provided to record any additional or auxiliary information related to the specific variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable1674857821438', 'title': 'Questions and instructions', 'type': 'section', 'items': [{'key': 'variable.var_respunit', 'title': 'Respondent', 'type': 'string', 'help_text': 'Provides information regarding who provided the information contained within the variable, e.g., head of household, respondent, proxy, interviewer.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_preqtxt', 'title': 'Pre-question text', 'type': 'string', 'help_text': 'The pre-question texts are the instructions provided to the interviewers and printed in the questionnaire before the literal question. This does not apply to all variables. Do not confuse this with instructions provided in the interviewer’s manual.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_qstnlit', 'title': 'Literal question', 'type': 'string', 'help_text': 'The literal question is the full text of the questionnaire as the enumerator is expected to ask it when conducting the interview. This does not apply to all variables (it does not apply to derived variables).', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_postqtxt', 'title': 'Post question text', 'type': 'string', 'help_text': 'The post-question texts are instructions provided to the interviewers, printed in the questionnaire after the literal question. Post-question can be used to enter information on skips provided in the questionnaire. This does not apply to all variables. Do not confuse this with instructions provided in the interviewer’s manual. With the previous two elements, one should be able to understand how the question was formulated in a questionnaire.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_forward', 'title': 'Forward skip', 'type': 'string', 'help_text': 'Contains a reference to the IDs of possible following questions. This can be used to document forward skip instructions.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_backward', 'title': 'Backward skip', 'type': 'string', 'help_text': 'Contains a reference to IDs of possible preceding questions. This can be used to document backward skip instructions.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_ivuinstr', 'title': 'Interviewer instructions', 'type': 'string', 'help_text': 'Specific instructions to the individual conducting an interview. The content will typically be entered by copy/pasting instructions in the interviewer’s manual (or in the CAPI application). In cases where the same instructions relate to multiple variables, repeat the same information in the metadata for all these variables.', 'enum': [], 'display_type': 'textarea'}], 'help_text': ''}, {'key': 'variable1674858021022', 'title': 'Imputation and derivation', 'type': 'section', 'items': [{'key': 'variable.var_codinstr', 'title': 'Coder instructions', 'type': 'string', 'help_text': 'The coder instructions for the variable. These are any special instructions to those who converted information from one form to another (e.g., textual to numeric) for a particular variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_imputation', 'title': 'Imputation', 'type': 'string', 'help_text': 'Imputation is the process of estimating values for variables when a value is missing. The element is used to describe the procedure used to impute values when missing.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_derivation', 'title': 'Derivation', 'type': 'string', 'help_text': 'Used only in the case of a derived variable, this element provides both a description of how the derivation was performed and the command used to generate the derived variable, as well as a specification of the other variables in the study used to generate the derivation. The Derivation element is used to provide a brief description of this process. As full transparency in derivation processes is critical to build trust and ensure replicability or reproducibility, the information captured in this element will often not be sufficient. A reference to a document and/or computer program can in such case be provided in this element, and the document/scripts provided as external resources. ', 'enum': [], 'display_type': 'textarea'}], 'help_text': ''}, {'key': 'variable.format', 'title': 'Technical format', 'type': 'section', 'help_text': '', 'items': [{'key': 'variable.var_format.type', 'title': 'Type', 'type': 'string', 'help_text': 'Indicates if the variable is numeric, fixed string, dynamic string, or date. Numeric variables are used to store any number, integer or floating point (decimals). A fixed string variable has a predefined length which enables the publisher to handle this data type more efficiently. Dynamic string variables can be used to store open-ended questions.', 'display_type': 'text'}, {'key': 'variable.var_format.name', 'title': 'Name', 'type': 'string', 'help_text': 'The name of the particular, proprietary format used.', 'display_type': 'text'}, {'key': 'variable.var_format.note', 'title': 'Note', 'type': 'string', 'help_text': 'Additional information on the variable format.', 'display_type': 'textarea'}]}, {'key': 'variable1674857761764', 'title': 'Position in fixed format file', 'type': 'section', 'items': [{'key': 'variable.loc_start_pos', 'title': 'Start position', 'type': 'integer', 'help_text': 'The starting position of the variable when the data are saved in an ASCII fixed-format data file.', 'enum': [], 'display_type': 'text', 'rules': {'numeric': True}}, {'key': 'variable.loc_end_pos', 'title': 'End position', 'type': 'integer', 'help_text': 'The end position of the variable when the data are saved in an ASCII fixed-format data file.', 'enum': [], 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'variable.loc_width', 'title': 'Width', 'type': 'integer', 'help_text': 'The length of the variable (the maximum number of characters used for its values) in an ASCII fixed-format data file.', 'enum': [], 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'variable.loc_rec_seg_no', 'title': 'Record segment number', 'type': 'string', 'help_text': 'Record segment number, deck or card number the variable is located on.', 'enum': [], 'display_type': 'text', 'rules': {'numeric': True}}], 'help_text': ''}]}]}' - Future work required to support these.
      warnings.warn(f"SkippingCustomElement: '{item}' - Future work required to support these.")
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:530: UserWarning: SkippingCustomElement: '{'type': 'section_container', 'key': 'variable_groups_container', 'title': 'Variable groups', 'is_custom': True, 'items': [{'type': 'section', 'key': 'variable_groups', 'title': 'Variable groups', 'items': [{'type': 'string', 'key': 'variable_groups.vgid', 'title': 'Group ID', 'is_required': False, 'help_text': 'In a dataset, variables are grouped by data file. For the convenience of users, the DDI allows data curators to organize the variables into different, "virtual" groups to organize variables by theme, type of respondent, or any other criteria. Grouping variables is optional, and will not impact the way variables are stored in the data files. One variable can belong to more than a group, and a group of variables can contain variables from more than one data file. The variable groups do not necessarily have to cover all variables in the data files. Variable groups can also contain other variable groups. Group ID is a unique identifier (unique within the DDI metadata file) for the variable group.', 'display_type': 'text'}, {'type': 'string', 'key': 'variable_groups.variables', 'title': 'Variables', 'help_text': 'The list of variables ("Variable ID") in the group. Enter a list with items separated by a space, e.g. "V21 V22 V30".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.variable_groups', 'title': 'Variable groups', 'help_text': 'The variable groups ("Group ID") that are embedded in this variable group. Enter a list with items separated by a space, e.g. "VG2 VG5".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.group_type', 'title': 'Group type', 'enum': [{'code': 'subject', 'label': 'Subject'}, {'code': 'section', 'label': 'Section'}, {'code': 'multiResp', 'label': 'Multi response'}, {'code': 'grid', 'label': 'Grid'}, {'code': 'display', 'label': 'Display'}, {'code': 'repetition', 'label': 'Repetition'}, {'code': 'version', 'label': 'Version'}, {'code': 'iteration', 'label': 'Iteration'}, {'code': 'analysis', 'label': 'Analysis'}, {'code': 'pragmatic', 'label': 'Pragmatic'}, {'code': 'record', 'label': 'Record'}, {'code': 'file', 'label': 'File'}, {'code': 'randomized', 'label': 'Randomized'}, {'code': 'other', 'label': 'Other'}], 'help_text': 'The type of grouping of the variables. A controlled vocabulary should be used. The DDI proposes the following vocabulary: "section", "multipleResp", "grid", "display", "repetition", "subject", "version", "iteration", "analysis", "pragmatic", "record", "file", "randomized", "other". A description of the groups can be found in a document available at https://zenodo.org/record/3823051/files/maddiewshop.pdf, by W. Thomas, W. Block, R. Wozniak and J. Buysse.', 'display_type': 'dropdown-custom'}, {'type': 'string', 'key': 'variable_groups.label', 'title': 'Label', 'help_text': 'A short description of the variable group.', 'display_type': 'text'}, {'type': 'string', 'key': 'variable_groups.txt', 'title': 'Description', 'help_text': 'A more detailed description of variable group than the one provided in "Label".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.universe', 'title': 'Universe', 'help_text': 'The universe can be a population of individuals, households, facilities, organizations, or others, which can be defined by any type of criteria (e.g., "adult males", "private schools", "small and medium-size enterprises", etc.)', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.notes', 'title': 'Notes', 'help_text': 'Used to provide additional information about the variable group.', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.definition', 'title': 'Rationale', 'help_text': 'A brief rationale for the variable grouping.', 'display_type': 'textarea'}]}]}' - Future work required to support these.
      warnings.warn(f"SkippingCustomElement: '{item}' - Future work required to support these.")
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.doi' is a <class 'str'> type. Full item defition = {'key': 'datacite.doi', 'title': 'DOI', 'type': 'string', 'help_text': 'DOI handle', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.prefix' is a <class 'str'> type. Full item defition = {'key': 'datacite.prefix', 'title': 'Prefix', 'type': 'string', 'help_text': 'DOI prefix', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.suffix' is a <class 'str'> type. Full item defition = {'key': 'datacite.suffix', 'title': 'Suffix', 'type': 'string', 'help_text': 'DOI suffix', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.creators.name' is a <class 'str'> type. Full item defition = {'key': 'name', 'prop_key': 'datacite.creators.name', 'title': 'Name', 'type': 'string', 'help_text': 'Name', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.creators.nameType' is a <class 'str'> type. Full item defition = {'key': 'nameType', 'prop_key': 'datacite.creators.nameType', 'title': 'Name type', 'type': 'string', 'help_text': "Name type. valid values: 'Personal', 'Organizational'", 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.creators.givenName' is a <class 'str'> type. Full item defition = {'key': 'givenName', 'prop_key': 'datacite.creators.givenName', 'title': 'Given name', 'type': 'string', 'help_text': 'Given name', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.creators.familyName' is a <class 'str'> type. Full item defition = {'key': 'familyName', 'prop_key': 'datacite.creators.familyName', 'title': 'Family name', 'type': 'string', 'help_text': 'Family name', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.titles.title' is a <class 'str'> type. Full item defition = {'key': 'title', 'prop_key': 'datacite.titles.title', 'title': 'Title', 'type': 'string', 'help_text': 'Title', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.titles.titleType' is a <class 'str'> type. Full item defition = {'key': 'titleType', 'prop_key': 'datacite.titles.titleType', 'title': 'Title type', 'type': 'string', 'help_text': "Title type. valid values: 'MainTitle', 'Subtitle', 'TranslatedTitle', 'AlternativeTitle'", 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'datacite.titles.lang' is a <class 'str'> type. Full item defition = {'key': 'lang', 'prop_key': 'datacite.titles.lang', 'title': 'Language', 'type': 'string', 'help_text': 'Language', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.publisher' is a <class 'str'> type. Full item defition = {'key': 'datacite.publisher', 'title': 'Publisher', 'type': 'string', 'help_text': 'Publisher', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.publicationYear' is a <class 'str'> type. Full item defition = {'key': 'datacite.publicationYear', 'title': 'Publication year', 'type': 'string', 'help_text': 'Publication year', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.types.resourceType' is a <class 'str'> type. Full item defition = {'key': 'datacite.types.resourceType', 'title': 'Resource type', 'type': 'string', 'help_text': 'Resource type', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.types.resourceTypeGeneral' is a <class 'str'> type. Full item defition = {'key': 'datacite.types.resourceTypeGeneral', 'title': 'Resource type general', 'type': 'string', 'help_text': "Valid values: 'Audiovisual', 'Collection', 'DataPaper', 'Dataset', 'Event', 'Image', 'InteractiveResource', 'Model', 'PhysicalObject', 'Service', 'Software', 'Sound', 'Text', 'Workflow', 'Other'", 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.url' is a <class 'str'> type. Full item defition = {'key': 'datacite.url', 'title': 'URL', 'type': 'string', 'help_text': '', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'datacite'. Field likely doesn't exist in base schema. Proceeding since key='datacite.language' is a <class 'str'> type. Full item defition = {'key': 'datacite.language', 'title': 'Language', 'type': 'string', 'help_text': '', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.repository_name' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.repository_name', 'title': 'Repository name', 'type': 'string', 'help_text': 'The name of the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.url' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.url', 'title': 'URL', 'type': 'string', 'help_text': 'The URL of the original repository or dataset.', 'rules': {'is_uri': True}, 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.dataset_identifier' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.dataset_identifier', 'title': 'Dataset identifier', 'type': 'string', 'help_text': 'The identifier of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.doi' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.doi', 'title': 'DOI', 'type': 'string', 'help_text': 'The Digital Object Identifier (DOI) of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.dataset_title' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.dataset_title', 'title': 'Dataset title', 'type': 'string', 'help_text': 'The title of the dataset in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.date_published' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.date_published', 'title': 'Dataset published date (YYYY-MM-DD)', 'type': 'string', 'help_text': 'The date when the dataset was published in the original repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'original_repository'. Field likely doesn't exist in base schema. Proceeding since key='provenance.original_repository.notes' is a <class 'str'> type. Full item defition = {'key': 'provenance.original_repository.notes', 'title': 'Notes', 'type': 'string', 'help_text': 'Additional information about the original repository.', 'display_type': 'textarea'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.repository_name' is a <class 'str'> type. Full item defition = {'key': 'repository_name', 'prop_key': 'provenance.source_repository.repository_name', 'title': 'Repository name', 'type': 'string', 'help_text': 'The name of the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.url' is a <class 'str'> type. Full item defition = {'key': 'url', 'prop_key': 'provenance.source_repository.url', 'title': 'URL', 'type': 'string', 'help_text': 'The URL of the source repository or dataset.', 'rules': {'is_uri': True}, 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.dataset_identifier' is a <class 'str'> type. Full item defition = {'key': 'dataset_identifier', 'prop_key': 'provenance.source_repository.dataset_identifier', 'title': 'Dataset identifier', 'type': 'string', 'help_text': 'The identifier of the dataset in the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.dataset_title' is a <class 'str'> type. Full item defition = {'key': 'dataset_title', 'prop_key': 'provenance.source_repository.dataset_title', 'title': 'Dataset title', 'type': 'string', 'help_text': 'The title of the dataset in the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.date_acquired' is a <class 'str'> type. Full item defition = {'key': 'date_acquired', 'prop_key': 'provenance.source_repository.date_acquired', 'title': 'Date acquired (YYYY-MM-DD)', 'type': 'string', 'help_text': 'The date when the metadata was acquired from the source repository.', 'display_type': 'text'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.acquisition_mode' is a <class 'str'> type. Full item defition = {'key': 'acquisition_mode', 'prop_key': 'provenance.source_repository.acquisition_mode', 'title': 'Acquisition mode', 'type': 'string', 'help_text': 'The mode of acquisition of the metadata from the source repository. e.g. OAI-PMH, API, manual entry, etc.'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:114: UserWarning: KeyError: 'source_repository'. Field likely doesn't exist in base schema. Proceeding since prop_key = 'provenance.source_repository.notes' is a <class 'str'> type. Full item defition = {'key': 'notes', 'prop_key': 'provenance.source_repository.notes', 'title': 'Notes', 'type': 'string', 'help_text': 'Additional information about the source repository.'}
      warnings.warn(
    




    uid                                            microdata-system-en
    template_type                                                 core
    name                                          Microdata DDI 2.5 EN
    data_type                                                   survey
    lang                                                            en
    template         {'type': 'template', 'title': 'Microdata Proje...
    Name: Microdata DDI 2.5 EN, dtype: object



### Template Classes

We can create a pydantic model for a given class


```python
c = me.get_metadata_class("6740f5f920502baf3f6cbcaa5c113deeen")
```

    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:282: UserWarning: UnknownFieldInfoKey: hlep_text='Type of identifier e.g. `doi`, `handle`, `other`' in template info {'key': 'type', 'title': 'Type', 'hlep_text': 'Type of identifier e.g. `doi`, `handle`, `other`', 'type': 'string', 'prop_key': 'study_desc.title_statement.identifiers.type', 'help_text': 'The type of identifier. For example: “DOI”. ', 'display_type': 'text'}
      warnings.warn(f"UnknownFieldInfoKey: {k}='{v}' in template info {template_info}")
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:126: UserWarning: KeyError: 'analysis_info'. Field likely doesn't exist in base schema. Proceeding since key='study_desc.method.data_collection.analysis_info.data_appraisal' is a <class 'str'> type. Full item defition = {'key': 'study_desc.method.data_collection.analysis_info.data_appraisal', 'title': 'Other data appraisal', 'type': 'string', 'help_text': 'This section is used to report any other action taken to assess the reliability of the data, or any observations regarding data quality. Describe here issues such as response variance, interviewer and response bias, question bias, etc. For a population census, this can include information on the main results of a post enumeration survey (a report should be provided in external resources and mentioned here); it can also include relevant comparisons with data from other sources that can be used as benchmarks.', 'display_type': 'textarea'}
      warnings.warn(
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:530: UserWarning: SkippingCustomElement: '{'type': 'section_container', 'key': 'variable_description', 'title': 'Variables', 'is_custom': True, 'items': [{'type': 'section', 'key': 'variable', 'title': 'Variable description', 'items': [{'key': 'variable.file_id', 'title': 'File ID', 'type': 'string', 'enum': [], 'help_text': 'A dataset can be composed of multiple data files. The File ID is the name of the data file that contains the variable being documented. This file name should correspond to a File ID listed in the "Data file description" section of the DDI. When using a Metadata Editor application, this information will typically be automatically generated when importing data files. This information is required.', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.vid', 'title': 'Variable ID', 'type': 'string', 'enum': [], 'help_text': 'A unique identifier given to the variable (unique within the full dataset, not only within a data file). This information is required. This is NOT the variable name (captured in element "Variable name"). This can be a system-generated ID, such as a sequential number within each data file. When using a Metadata Editor application, the ID will typically be automatically generated when importing data files. ', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.name', 'title': 'Variable name', 'type': 'string', 'enum': [], 'help_text': 'The name of the variable in the data file. This information is required. The name should be entered exactly as found in the data file (not abbreviated or converted to upper or lower cases, as some software applications are case-sensitive). This information can be programmatically extracted from the data file. When using a Metadata Editor application, the variable name will typically be extracted from the imported data files. The variable name is limited to eight characters in some statistical analysis software such as SAS or SPSS. A variable name must be unique within a data file (not within a full dataset, as a same variable may appear in multiple data files). ', 'is_required': True, 'display_type': 'text'}, {'key': 'variable.labl', 'title': 'Variable label', 'type': 'string', 'enum': [], 'help_text': 'All variables should have a label that provides a short but clear indication of what the variable contains. Ideally, all variables in a data file will have a unique label. File formats like Stata or SPSS often contain variable labels. When using a Metadata Editor application, the variable name will typically be extracted from the imported data files. Variable labels can also be found in data dictionaries in software applications like Survey Solutions or CsPro. Avoid using the question itself as a label (specific elements are available to capture the literal question text). Think of a label as what you would want to see in a tabulation of the variables. Keep in mind that software applications like Stata and others impose a limit to the number of characters in a label (often, 80). \n', 'is_recommended': True, 'display_type': 'text'}, {'key': 'variable.var_universe', 'title': 'Universe', 'type': 'string', 'help_text': 'The universe at the variable level defines the population the question applied to. It reflects skip patterns in a questionnaire. This information can typically be copy/pasted from the survey questionnaire. Try to be as specific as possible. This information is critical for the analyst, as it explains why missing values may be found in a variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_txt', 'title': 'Variable definition', 'type': 'string', 'help_text': 'This element provides a space to describe the variable in detail. Not all variables require a definition.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_concept', 'title': 'Concepts', 'type': 'array', 'help_text': 'The general subject to which the parent element may be seen as pertaining. This element serves the same purpose as the keywords and topic classification elements, but at the variable description level.', 'props': [{'key': 'title', 'title': 'Title', 'type': 'string', 'prop_key': 'variable.var_concept.title', 'help_text': 'The name (label) of the concept.', 'display_type': 'text'}, {'key': 'vocab', 'title': 'Vocabulary', 'type': 'string', 'prop_key': 'variable.var_concept.vocab', 'help_text': 'The controlled vocabulary, if any, from which the concept `title’ was taken.', 'display_type': 'text'}, {'key': 'uri', 'title': 'URL', 'type': 'string', 'prop_key': 'variable.var_concept.uri', 'help_text': 'A link (URL) to the controlled vocabulary mentioned in "Vocabulary".', 'display_type': 'text', 'rules': {'is_uri': True}}]}, {'key': 'variable.var_sumstat', 'title': 'Summary statistics', 'type': 'array', 'help_text': 'The DDI metadata standard provides multiple elements to capture various summary statistics such as minimum, maximum, or mean values (weighted and un-weighted) for each variable. The content of the "Summary statistics" section will be easy to fill out programmatically (using R or Python) or using a specialized DDI metadata editor, which can read the data file and generate the summary statistics.\n', 'props': [{'key': 'type', 'title': 'Type', 'type': 'string', 'prop_key': 'variable.var_sumstat.type', 'help_text': 'The type of statistics being shown: mean, median, mode, valid cases, invalid cases, minimum, maximum, or standard deviation.', 'display_type': 'textarea'}, {'key': 'value', 'title': 'Value', 'type': 'string', 'prop_key': 'variable.var_sumstat.value', 'help_text': 'The value of the summary statistics mentioned in type.', 'display_type': 'text'}, {'key': 'wgtd', 'title': 'Weighted', 'type': 'string', 'prop_key': 'variable.var_sumstat.wgtd', 'help_text': 'Indicates whether the statistics reported in value are weighted or not (for variables in sample surveys). Enter “weighted” if weighted, otherwise leave this element empty.', 'display_type': 'text', 'enum': []}]}, {'key': 'variable.var_catgry', 'title': 'Variable categories', 'type': 'array', 'props': [{'key': 'value', 'title': 'Code', 'type': 'string', 'prop_key': 'variable.var_catgry.value', 'help_text': 'The code of the category.', 'display_type': 'text'}, {'key': 'label', 'title': 'Label', 'type': 'string', 'prop_key': 'variable.var_catgry.label', 'help_text': 'The label of the category (or "value label")', 'display_type': 'text'}, {'key': 'stats', 'title': 'Statistics', 'type': 'array', 'props': [{'key': 'type', 'title': 'Type', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.type', 'help_text': 'Type of statistics, e.g. "Count".', 'display_type': 'text'}, {'key': 'value', 'title': 'Value', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.value', 'help_text': 'Estimate', 'display_type': 'text'}, {'key': 'wgtd', 'title': 'Weighted', 'type': 'string', 'prop_key': 'variable.var_catgry.stats.wgtd', 'help_text': 'Indicates whether the "Value" is weighted (for sample surveys) or not.', 'display_type': 'text'}], 'prop_key': 'variable.var_catgry.stats'}], 'help_text': 'A description of the categories (codes with labels) that apply to the variable, for categorical variables. The element also includes summary statistics at the category level.'}, {'key': 'variable.var_std_catgry', 'title': 'Standard categories', 'type': 'array', 'help_text': 'This element is used to indicate that the codes used for a categorical variable are from a standard international or other classification, like COICOP, ISIC, ISO country codes, etc.', 'props': [{'key': 'name', 'title': 'Name', 'type': 'string', 'prop_key': 'variable.var_std_catgry.name', 'help_text': 'The name of the classification, e.g. “International Standard Industrial Classification of All Economic Activities (ISIC), Revision 4”', 'display_type': 'text'}, {'key': 'source', 'title': 'Source', 'type': 'string', 'prop_key': 'variable.var_std_catgry.source', 'help_text': 'The source of the classification, for example “United Nations”.', 'display_type': 'text'}, {'key': 'date', 'title': 'Date', 'type': 'string', 'prop_key': 'variable.var_std_catgry.date', 'help_text': 'The version (typically a date) of the classification used for the study.', 'display_type': 'text'}, {'key': 'uri', 'title': 'URL', 'type': 'string', 'prop_key': 'variable.var_std_catgry.uri', 'help_text': 'A URL to a website where an electronic copy and more information on the classification can be obtained.', 'rules': {'is_uri': True}, 'display_type': 'text'}]}, {'key': 'variable.var_intrvl', 'title': 'Interval type', 'help_text': 'This element indicates whether the intervals between values for the variable are discrete or continuous.', 'type': 'string', 'enum': [{'code': 'disc', 'label': 'Discrete'}, {'code': 'cont', 'label': 'Continuous'}], 'display_type': 'dropdown'}, {'key': 'variable.var_dcml', 'title': 'Decimal points', 'type': 'string', 'help_text': 'This element refers to the number of decimal points in the values of the variable. It must be a numeric value.', 'enum': [], 'display_type': 'text'}, {'key': 'variable.var_wgt', 'title': 'Is weight', 'type': 'integer', 'help_text': 'This element, which applies to dataset from sample surveys, indicates whether the variable is a sample weight (value “1”) or not (value "0). Sample weights play an important role in the calculation of summary statistics and sampling errors, and should therefore be flagged.', 'default': 0, 'enum': [{'code': '0', 'label': 'Not a weight'}, {'code': '1', 'label': 'Weight'}], 'display_type': 'dropdown'}, {'key': 'variable.var_security', 'title': 'Security', 'type': 'string', 'help_text': 'This element is used to provide information regarding levels of access, e.g., public, subscriber, need to know.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_notes', 'title': 'Notes on variable', 'type': 'string', 'help_text': 'This element is provided to record any additional or auxiliary information related to the specific variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable1674857821438', 'title': 'Questions and instructions', 'type': 'section', 'items': [{'key': 'variable.var_respunit', 'title': 'Respondent', 'type': 'string', 'help_text': 'Provides information regarding who provided the information contained within the variable, e.g., head of household, respondent, proxy, interviewer.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_preqtxt', 'title': 'Pre-question text', 'type': 'string', 'help_text': 'The pre-question texts are the instructions provided to the interviewers and printed in the questionnaire before the literal question. This does not apply to all variables. Do not confuse this with instructions provided in the interviewer’s manual.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_qstnlit', 'title': 'Literal question', 'type': 'string', 'help_text': 'The literal question is the full text of the questionnaire as the enumerator is expected to ask it when conducting the interview. This does not apply to all variables (it does not apply to derived variables).', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_postqtxt', 'title': 'Post question text', 'type': 'string', 'help_text': 'The post-question texts are instructions provided to the interviewers, printed in the questionnaire after the literal question. Post-question can be used to enter information on skips provided in the questionnaire. This does not apply to all variables. Do not confuse this with instructions provided in the interviewer’s manual. With the previous two elements, one should be able to understand how the question was formulated in a questionnaire.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_forward', 'title': 'Forward skip', 'type': 'string', 'help_text': 'Contains a reference to the IDs of possible following questions. This can be used to document forward skip instructions.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_backward', 'title': 'Backward skip', 'type': 'string', 'help_text': 'Contains a reference to IDs of possible preceding questions. This can be used to document backward skip instructions.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_qstn_ivuinstr', 'title': 'Interviewer instructions', 'type': 'string', 'help_text': 'Specific instructions to the individual conducting an interview. The content will typically be entered by copy/pasting instructions in the interviewer’s manual (or in the CAPI application). In cases where the same instructions relate to multiple variables, repeat the same information in the metadata for all these variables.', 'enum': [], 'display_type': 'textarea'}], 'help_text': ''}, {'key': 'variable1674858021022', 'title': 'Imputation and derivation', 'type': 'section', 'items': [{'key': 'variable.var_codinstr', 'title': 'Coder instructions', 'type': 'string', 'help_text': 'The coder instructions for the variable. These are any special instructions to those who converted information from one form to another (e.g., textual to numeric) for a particular variable.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_imputation', 'title': 'Imputation', 'type': 'string', 'help_text': 'Imputation is the process of estimating values for variables when a value is missing. The element is used to describe the procedure used to impute values when missing.', 'enum': [], 'display_type': 'textarea'}, {'key': 'variable.var_derivation', 'title': 'Derivation', 'type': 'string', 'help_text': 'Used only in the case of a derived variable, this element provides both a description of how the derivation was performed and the command used to generate the derived variable, as well as a specification of the other variables in the study used to generate the derivation. The Derivation element is used to provide a brief description of this process. As full transparency in derivation processes is critical to build trust and ensure replicability or reproducibility, the information captured in this element will often not be sufficient. A reference to a document and/or computer program can in such case be provided in this element, and the document/scripts provided as external resources. ', 'enum': [], 'display_type': 'textarea'}], 'help_text': ''}, {'key': 'variable.format', 'title': 'Technical format', 'type': 'section', 'help_text': '', 'items': [{'key': 'variable.var_format.type', 'title': 'Type', 'type': 'string', 'help_text': 'Indicates if the variable is numeric, fixed string, dynamic string, or date. Numeric variables are used to store any number, integer or floating point (decimals). A fixed string variable has a predefined length which enables the publisher to handle this data type more efficiently. Dynamic string variables can be used to store open-ended questions.', 'display_type': 'text'}, {'key': 'variable.var_format.name', 'title': 'Name', 'type': 'string', 'help_text': 'The name of the particular, proprietary format used.', 'display_type': 'text'}, {'key': 'variable.var_format.note', 'title': 'Note', 'type': 'string', 'help_text': 'Additional information on the variable format.', 'display_type': 'textarea'}]}, {'key': 'variable1674857761764', 'title': 'Position in fixed format file', 'type': 'section', 'items': [{'key': 'variable.loc_start_pos', 'title': 'Start position', 'type': 'integer', 'help_text': 'The starting position of the variable when the data are saved in an ASCII fixed-format data file.', 'enum': [], 'display_type': 'text', 'rules': {'numeric': True}}, {'key': 'variable.loc_end_pos', 'title': 'End position', 'type': 'integer', 'help_text': 'The end position of the variable when the data are saved in an ASCII fixed-format data file.', 'enum': [], 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'variable.loc_width', 'title': 'Width', 'type': 'integer', 'help_text': 'The length of the variable (the maximum number of characters used for its values) in an ASCII fixed-format data file.', 'enum': [], 'rules': {'numeric': True}, 'display_type': 'text'}, {'key': 'variable.loc_rec_seg_no', 'title': 'Record segment number', 'type': 'string', 'help_text': 'Record segment number, deck or card number the variable is located on.', 'enum': [], 'display_type': 'text', 'rules': {'numeric': True}}], 'help_text': ''}]}]}' - Future work required to support these.
      warnings.warn(f"SkippingCustomElement: '{item}' - Future work required to support these.")
    /Users/gblackadder/sources/pymetadataeditor/pymetadataeditor/templates.py:530: UserWarning: SkippingCustomElement: '{'type': 'section_container', 'key': 'variable_groups_container', 'title': 'Variable groups', 'is_custom': True, 'items': [{'type': 'section', 'key': 'variable_groups', 'title': 'Variable groups', 'items': [{'type': 'string', 'key': 'variable_groups.vgid', 'title': 'Group ID', 'is_required': False, 'help_text': 'In a dataset, variables are grouped by data file. For the convenience of users, the DDI allows data curators to organize the variables into different, "virtual" groups to organize variables by theme, type of respondent, or any other criteria. Grouping variables is optional, and will not impact the way variables are stored in the data files. One variable can belong to more than a group, and a group of variables can contain variables from more than one data file. The variable groups do not necessarily have to cover all variables in the data files. Variable groups can also contain other variable groups. Group ID is a unique identifier (unique within the DDI metadata file) for the variable group.', 'display_type': 'text'}, {'type': 'string', 'key': 'variable_groups.variables', 'title': 'Variables', 'help_text': 'The list of variables ("Variable ID") in the group. Enter a list with items separated by a space, e.g. "V21 V22 V30".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.variable_groups', 'title': 'Variable groups', 'help_text': 'The variable groups ("Group ID") that are embedded in this variable group. Enter a list with items separated by a space, e.g. "VG2 VG5".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.group_type', 'title': 'Group type', 'enum': [{'code': 'subject', 'label': 'Subject'}, {'code': 'section', 'label': 'Section'}, {'code': 'multiResp', 'label': 'Multi response'}, {'code': 'grid', 'label': 'Grid'}, {'code': 'display', 'label': 'Display'}, {'code': 'repetition', 'label': 'Repetition'}, {'code': 'version', 'label': 'Version'}, {'code': 'iteration', 'label': 'Iteration'}, {'code': 'analysis', 'label': 'Analysis'}, {'code': 'pragmatic', 'label': 'Pragmatic'}, {'code': 'record', 'label': 'Record'}, {'code': 'file', 'label': 'File'}, {'code': 'randomized', 'label': 'Randomized'}, {'code': 'other', 'label': 'Other'}], 'help_text': 'The type of grouping of the variables. A controlled vocabulary should be used. The DDI proposes the following vocabulary: "section", "multipleResp", "grid", "display", "repetition", "subject", "version", "iteration", "analysis", "pragmatic", "record", "file", "randomized", "other". A description of the groups can be found in a document available at https://zenodo.org/record/3823051/files/maddiewshop.pdf, by W. Thomas, W. Block, R. Wozniak and J. Buysse.', 'display_type': 'dropdown-custom'}, {'type': 'string', 'key': 'variable_groups.label', 'title': 'Label', 'help_text': 'A short description of the variable group.', 'display_type': 'text'}, {'type': 'string', 'key': 'variable_groups.txt', 'title': 'Description', 'help_text': 'A more detailed description of variable group than the one provided in "Label".', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.definition', 'title': 'Rationale', 'help_text': 'A brief rationale for the variable grouping.', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.universe', 'title': 'Universe', 'help_text': 'The universe can be a population of individuals, households, facilities, organizations, or others, which can be defined by any type of criteria (e.g., "adult males", "private schools", "small and medium-size enterprises", etc.)', 'display_type': 'textarea'}, {'type': 'string', 'key': 'variable_groups.notes', 'title': 'Notes', 'help_text': 'Used to provide additional information about the variable group.', 'display_type': 'textarea'}]}]}' - Future work required to support these.
      warnings.warn(f"SkippingCustomElement: '{item}' - Future work required to support these.")
    


```python
c
```




    template.IHSN_DDI_2-5_Template_v01_EN




```python
c.model_fields
```




    {'doc_desc': FieldInfo(annotation=Union[doc_desc, NoneType], required=False, default=None),
     'study_desc': FieldInfo(annotation=Union[study_desc, NoneType], required=False, default=None),
     'tags': FieldInfo(annotation=Union[List[Tag], NoneType], required=False, default=None, title='Tags', description='Tags, especially when organized in tag groups, provide a powerful and flexible solution to enable custom facets (filters) in data catalogs. Note that tags and tag groups are not element from the DDI Codebook standard.'),
     'data_files': FieldInfo(annotation=Union[List[DatafileSchema], NoneType], required=False, default=None, description='Data files'),
     'variables': FieldInfo(annotation=Union[List[VariableSchema], NoneType], required=False, default=None, description='Variables'),
     'variable_groups': FieldInfo(annotation=Union[List[VariableGroupSchema], NoneType], required=False, default=None, title='Variable groups', description='Variable group')}



But it's usually easier to start with an outline of the class. Again, this can be in either a dictionary, a pydantic model or as an Excel file.


```python
me.make_metadata_outline("6740f5f920502baf3f6cbcaa5c113deeen", "pydantic").pretty_print()
```


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_DDI_2-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">5_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">doc_desc</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">doc_desc</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">prod_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">study_desc</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_desc</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">title_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">sub_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">alternate_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">translated_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">identifiers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">series_statement</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">series_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">series_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_info</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">abstract</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_kind</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">analysis_unit</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">keyword</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">topic</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">universe</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">nation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">NationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_coverage</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_coverage_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_unit</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">east</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">south</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">north</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">bound_poly</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Bound_polyItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">lat</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">lon</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">study_budget</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">coll_dates</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Coll_date</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">cycle</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">time_periods</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Time_period</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">cycle</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">quality_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">quality_statement</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">compliance_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">standards</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Standard</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">producer</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">other_quality_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">ex_post_evaluation</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ex_post_evaluation</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">evaluation_process</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">evaluator</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">EvaluatorItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">completion_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">outcomes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">authoring_entity</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Authoring_entityItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">production_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">production_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">funding_agencies</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Funding_agencie</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">grant</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">copyright</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">oth_id</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Oth_idItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_authorization</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_authorization</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">agency</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">AgencyItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">authorization_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">method</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">method</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">data_collection</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_collection</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">sample_frame</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">sample_frame</span><span style="font-weight: bold">(</span>
                    <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">valid_period</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Valid_periodItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">event</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                    <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">universe</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">frame_unit</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">frame_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">unit_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">is_primary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">num_of_units</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
                    <span style="color: #808000; text-decoration-color: #808000">update_procedure</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">reference_period</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Reference_periodItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">event</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
                <span style="font-weight: bold">)</span>,
                <span style="color: #808000; text-decoration-color: #808000">sampling_procedure</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">sampling_deviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">weight</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">research_instrument</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">instru_development</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">time_method</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">frequency</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">origin</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">characteristics</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">coll_mode</span>=<span style="font-weight: bold">[]</span>,
                <span style="color: #808000; text-decoration-color: #808000">data_collectors</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_collector</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">collector_training</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Collector_trainingItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">training</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">control_operations</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">act_min</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">coll_situation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">cleaning_operations</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">analysis_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">analysis_info</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">data_appraisal</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">analysis_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">analysis_info</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">response_rate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">sampling_error_estimates</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">method_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_processing</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_processingItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_development</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_development</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">development_activity</span>=<span style="font-weight: bold">[</span>
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Development_activityItem</span><span style="font-weight: bold">(</span>
                    <span style="color: #808000; text-decoration-color: #808000">activity_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">activity_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">participants</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">resources</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                    <span style="color: #808000; text-decoration-color: #808000">outcome</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
                <span style="font-weight: bold">)</span>
            <span style="font-weight: bold">]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_access</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_access</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">dataset_availability</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">dataset_availability</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">access_place</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">access_place_url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">original_archive</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">coll_size</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">complete</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">file_quantity</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">status</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">dataset_use</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">dataset_use</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">contact</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ContactItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">conf_dec</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Conf_decItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">required</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">txt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">form_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">form_url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">conditions</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">cit_req</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">deposit_req</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">spec_perm</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Spec_permItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">required</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">txt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">form_url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">form_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
                <span style="color: #808000; text-decoration-color: #808000">restrictions</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">disclaimer</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">distribution_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">distribution_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">depositor</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">DepositorItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">deposit_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">distributors</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Distributor</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">distribution_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">contact</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ContactItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Tag</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">tag</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">tag_group</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
    <span style="color: #808000; text-decoration-color: #808000">data_files</span>=<span style="font-weight: bold">[</span>
        <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">DatafileSchema</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">file_id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">file_name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">file_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">case_count</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_count</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">producer</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_checks</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">missing_data</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">]</span>,
    <span style="color: #808000; text-decoration-color: #808000">variables</span>=<span style="font-weight: bold">[</span>
        <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VariableSchema</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">file_id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">vid</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">labl</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_intrvl</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_dcml</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_wgt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">loc_start_pos</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">loc_end_pos</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">loc_width</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">loc_rec_seg_no</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_imputation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_derivation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_security</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_respunit</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_qstn_preqtxt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_qstn_qstnlit</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_qstn_postqtxt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_forward</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_backward</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_qstn_ivulnstr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_universe</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_sumstat</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VarSumstatItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">value</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">wgtd</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_txt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_catgry</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VarCatgryItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">value</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">stats</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Stat</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">value</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">wgtd</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)])]</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_std_catgry</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VarStdCatgry</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_codinstr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_concept</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VarConceptItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_format</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VarFormat</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">var_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">]</span>,
    <span style="color: #808000; text-decoration-color: #808000">variable_groups</span>=<span style="font-weight: bold">[</span>
        <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">VariableGroupSchema</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">vgid</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">variables</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">variable_groups</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">group_type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">universe</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">txt</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">definition</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">]</span>
<span style="font-weight: bold">)</span>
</pre>




```python
me.make_metadata_outline("6740f5f920502baf3f6cbcaa5c113deeen", "dict")
```




    {'doc_desc': {'producers': [{'name': None,
        'abbr': None,
        'affiliation': None,
        'role': None}],
      'prod_date': None,
      'idno': None,
      'version_statement': {'version': None,
       'version_date': None,
       'version_resp': None,
       'version_notes': None}},
     'study_desc': {'title_statement': {'title': '',
       'sub_title': None,
       'alternate_title': None,
       'translated_title': None,
       'idno': '',
       'identifiers': [{'type': None, 'identifier': None}]},
      'series_statement': {'series_name': None, 'series_info': None},
      'version_statement': {'version': None,
       'version_date': None,
       'version_resp': None,
       'version_notes': None},
      'study_info': {'abstract': None,
       'data_kind': None,
       'analysis_unit': None,
       'keywords': [{'keyword': None, 'vocab': None, 'uri': None}],
       'topics': [{'topic': None, 'vocab': None, 'uri': None}],
       'universe': None,
       'nation': [{'name': None, 'abbreviation': None}],
       'geog_coverage': None,
       'geog_coverage_notes': None,
       'geog_unit': None,
       'bbox': [{'west': None, 'east': None, 'south': None, 'north': None}],
       'bound_poly': [{'lat': None, 'lon': None}],
       'study_budget': None,
       'coll_dates': [{'start': None, 'end': None, 'cycle': None}],
       'time_periods': [{'start': None, 'end': None, 'cycle': None}],
       'quality_statement': {'compliance_description': None,
        'standards': [{'name': None, 'producer': None}],
        'other_quality_statement': None},
       'ex_post_evaluation': {'type': None,
        'evaluation_process': None,
        'evaluator': [{'name': None,
          'abbr': None,
          'affiliation': None,
          'role': None}],
        'completion_date': None,
        'outcomes': None}},
      'authoring_entity': [{'name': None, 'affiliation': None}],
      'production_statement': {'producers': [{'name': None,
         'abbr': None,
         'affiliation': None,
         'role': None}],
       'funding_agencies': [{'name': None,
         'abbr': None,
         'grant': None,
         'role': None}],
       'copyright': None},
      'oth_id': [{'name': None, 'affiliation': None, 'role': None}],
      'study_authorization': {'date': None,
       'agency': [{'name': None, 'affiliation': None, 'abbr': None}],
       'authorization_statement': None},
      'method': {'data_collection': {'sample_frame': {'name': None,
         'valid_period': [{'event': None, 'date': None}],
         'custodian': None,
         'universe': None,
         'frame_unit': {'unit_type': None,
          'is_primary': None,
          'num_of_units': None},
         'update_procedure': None,
         'reference_period': [{'event': None, 'date': None}]},
        'sampling_procedure': None,
        'sampling_deviation': None,
        'weight': None,
        'research_instrument': None,
        'instru_development': None,
        'time_method': None,
        'frequency': None,
        'sources': [{'name': None, 'origin': None, 'characteristics': None}],
        'coll_mode': [],
        'data_collectors': [{'name': None,
          'affiliation': None,
          'abbr': None,
          'role': None}],
        'collector_training': [{'type': None, 'training': None}],
        'control_operations': None,
        'act_min': None,
        'coll_situation': None,
        'cleaning_operations': None,
        'analysis_info': {'data_appraisal': None}},
       'analysis_info': {'response_rate': None, 'sampling_error_estimates': None},
       'method_notes': None,
       'data_processing': [{'type': None, 'description': None}]},
      'study_development': {'development_activity': [{'activity_type': None,
         'activity_description': None,
         'participants': None,
         'resources': None,
         'outcome': None}]},
      'data_access': {'dataset_availability': {'access_place': None,
        'access_place_url': None,
        'original_archive': None,
        'coll_size': None,
        'complete': None,
        'file_quantity': None,
        'notes': None,
        'status': None},
       'dataset_use': {'contact': [{'name': None,
          'affiliation': None,
          'uri': None,
          'email': None}],
        'conf_dec': [{'required': None,
          'txt': None,
          'form_id': None,
          'form_url': None}],
        'conditions': None,
        'cit_req': None,
        'deposit_req': None,
        'spec_perm': [{'required': None,
          'txt': None,
          'form_url': None,
          'form_id': None}],
        'restrictions': None,
        'disclaimer': None},
       'notes': None},
      'distribution_statement': {'depositor': [{'name': None,
         'abbr': None,
         'affiliation': None,
         'uri': None}],
       'deposit_date': None,
       'distributors': [{'name': None,
         'abbr': None,
         'affiliation': None,
         'uri': None}],
       'distribution_date': None,
       'contact': [{'name': None,
         'affiliation': None,
         'email': None,
         'uri': None}]},
      'study_notes': None},
     'tags': [{'tag': None, 'tag_group': None}],
     'data_files': [{'file_id': '',
       'file_name': '',
       'file_type': None,
       'description': None,
       'case_count': None,
       'var_count': None,
       'producer': None,
       'data_checks': None,
       'missing_data': None,
       'version': None,
       'notes': None}],
     'variables': [{'file_id': '',
       'vid': '',
       'name': '',
       'labl': '',
       'var_intrvl': None,
       'var_dcml': None,
       'var_wgt': None,
       'loc_start_pos': None,
       'loc_end_pos': None,
       'loc_width': None,
       'loc_rec_seg_no': None,
       'var_imputation': None,
       'var_derivation': None,
       'var_security': None,
       'var_respunit': None,
       'var_qstn_preqtxt': None,
       'var_qstn_qstnlit': None,
       'var_qstn_postqtxt': None,
       'var_forward': None,
       'var_backward': None,
       'var_qstn_ivulnstr': None,
       'var_universe': None,
       'var_sumstat': [{'type': None, 'value': None, 'wgtd': None}],
       'var_txt': None,
       'var_catgry': [{'value': None,
         'label': None,
         'stats': [{'type': None, 'value': None, 'wgtd': None}]}],
       'var_std_catgry': {'name': None, 'source': None, 'date': None, 'uri': None},
       'var_codinstr': None,
       'var_concept': [{'title': '', 'vocab': None, 'uri': None}],
       'var_format': {'type': None, 'name': None, 'note': None},
       'var_notes': None}],
     'variable_groups': [{'vgid': '',
       'variables': None,
       'variable_groups': None,
       'group_type': None,
       'label': None,
       'universe': None,
       'notes': None,
       'txt': None,
       'definition': None}]}



## Deleting Projects


```python
me.delete_project_by_id(indicator_id)
```
