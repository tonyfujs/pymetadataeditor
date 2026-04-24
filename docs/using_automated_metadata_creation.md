# Automatic Metadata Creation and Augmentation from Sources

The pyMetadaEditor tool can be used to automatically create and augment metadata. The tool is designed to write metadata based on the content of files, such as PDFs, word documents, powerpoint presentations, and web URLs. 

The tool can also be used to augment existing metadata by adding additional information from the content of the files.

The tool can be use models from OpenAI, but can also run locally using ollama or with a private LLM running in Azure.

We start by instantiating the metadata editor object:


```python
from pymetadataeditor import MetadataEditor
import os

your_api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
openai_key = os.getenv("OPENAI_KEY")
me = MetadataEditor(api_url=api_url, api_key=your_api_key, verify_ssl=False)

```


```python
me.list_projects(limit=2)
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4363</th>
      <td>timeseries</td>
      <td>942d99c2-6ac3-4d87-bc33-d4239d889457</td>
      <td>NY.GDP.MKTP.CD</td>
      <td>GDP (current US$)</td>
      <td>None</td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2025-01-31T13:40:27+00:00</td>
      <td>2025-02-20T18:46:39+00:00</td>
      <td>None</td>
      <td>24</td>
      <td>24</td>
      <td>None</td>
      <td>None</td>
      <td>8603d94e27bccc2bdad1e00dbbf0fe32en</td>
      <td>Gordon Blackadder</td>
      <td>Gordon Blackadder</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>2202</th>
      <td>document</td>
      <td>644e84d5-9a0c-4dd2-8a66-ec27808a26e4</td>
      <td>DEMO_DOC_001</td>
      <td>The Analysis of Household Surveys: A Microecon...</td>
      <td>None</td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>None</td>
      <td>2024-10-01T16:09:09+00:00</td>
      <td>2025-01-04T01:17:32+00:00</td>
      <td>None</td>
      <td>25</td>
      <td>25</td>
      <td>None</td>
      <td>thumbnail-2202.png</td>
      <td>2f62a6b2716ab55b4426005abdbe1600</td>
      <td>vmascarinas</td>
      <td>vmascarinas</td>
      <td>[{'id': '85', 'title': 'Demo Collection', 'sid...</td>
    </tr>
  </tbody>
</table>
</div>



Automatic metadata creations works for metadata types:
- microdata
- geospatial
- indicator
- document
- script
- video


We can create metadata from source files such as: 
- pdfs
- word
- excel
- powerpoint
- text files
- csv
- JSON
- XML
- ZIP files
- Images
- URLs

To run on an OpenAI model you will need an OpenAI API key.

Here is how to automatically create metadata, here we use two local PDFs:


```python
docs = ["../survey_records/cambodia/cambodia_lsms_basic_information_document.pdf", "../survey_records/cambodia/cambodia_living_standards_measurement_study_plus_manual_english.pdf"]

example = me.draft_metadata_from_files(llm_api_key=openai_key, 
                                       files=docs, 
                                       metadata_type_or_template_uid='microdata',
                                       output_mode='pydantic',
                                       metadata_producer_organization="The World Bank Group, DEC - Development Data Group"
                                       )
example.pretty_print()
```

    Read in ../survey_records/cambodia/cambodia_lsms_basic_information_document.pdf, running token count is 6381
    Read in ../survey_records/cambodia/cambodia_living_standards_measurement_study_plus_manual_english.pdf, running token count is 24910
    Sending to OpenAI, this may take a few minutes...
    


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_DDI_2-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">5_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">doc_desc</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">doc_desc</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group, DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'WBG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata Producer'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">prod_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'IHSN_DDI_v01_WBG_LSMS+_KHM_2025'</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">'v01'</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group, DEC - Development Data Group'</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #008000; text-decoration-color: #008000">'Initial version.'</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">study_desc</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_desc</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">title_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'Cambodia Living Standards Measurement Study - Plus 2019-2020'</span>,
            <span style="color: #808000; text-decoration-color: #808000">sub_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">alternate_title</span>=<span style="color: #008000; text-decoration-color: #008000">'Cambodia LSMS+ 2019-20'</span>,
            <span style="color: #808000; text-decoration-color: #808000">translated_title</span>=<span style="color: #008000; text-decoration-color: #008000">'\x0b\x00b\x000b\x000b\x0b\x0b\x0b\x0b\x0b'</span>,
            <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'LSMS+_KHM_2019-2020'</span>,
            <span style="color: #808000; text-decoration-color: #808000">identifiers</span>=<span style="font-weight: bold">[]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">series_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">series_name</span>=<span style="color: #008000; text-decoration-color: #008000">'Living Standards Measurement Study - Plus'</span>,
            <span style="color: #808000; text-decoration-color: #808000">series_info</span>=<span style="color: #008000; text-decoration-color: #008000">'The LSMS+ program integrates World Bank-required individual-level data collection into </span>
<span style="color: #008000; text-decoration-color: #008000">household surveys in IDA countries.'</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">'v01'</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #008000; text-decoration-color: #008000">'National Institute of Statistics, Ministry of Planning; World Bank'</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #008000; text-decoration-color: #008000">'First release edition.'</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_info</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">abstract</span>=<span style="color: #008000; text-decoration-color: #008000">"The Cambodia Living Standards Measurement Plus Survey (LSMS+) conducted in 2019-2020 aims to </span>
<span style="color: #008000; text-decoration-color: #008000">collect individual-level data to measure various aspects of welfare. This survey was part of the IDA18 Gender and </span>
<span style="color: #008000; text-decoration-color: #008000">Development Window initiative, which enhances data quality and availability through integration with existing </span>
<span style="color: #008000; text-decoration-color: #008000">surveys. Conducted in partnership with the National Institute of Statistics (NIS) and using the World Bank's CAPI </span>
<span style="color: #008000; text-decoration-color: #008000">solutions, the survey focuses on collecting data on asset ownership, employment, and more among adults in selected </span>
<span style="color: #008000; text-decoration-color: #008000">households across the country."</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_kind</span>=<span style="color: #008000; text-decoration-color: #008000">'Survey Data'</span>,
            <span style="color: #808000; text-decoration-color: #808000">analysis_unit</span>=<span style="color: #008000; text-decoration-color: #008000">'Households, Individuals'</span>,
            <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[</span>
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">keyword</span>=<span style="color: #008000; text-decoration-color: #008000">'Living Standards Measurement'</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">keyword</span>=<span style="color: #008000; text-decoration-color: #008000">'Household Survey'</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">keyword</span>=<span style="color: #008000; text-decoration-color: #008000">'Asset Ownership'</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
            <span style="font-weight: bold">]</span>,
            <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span>
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">topic</span>=<span style="color: #008000; text-decoration-color: #008000">'Economic Conditions'</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)</span>,
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">topic</span>=<span style="color: #008000; text-decoration-color: #008000">'Demographics'</span>, <span style="color: #808000; text-decoration-color: #808000">vocab</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)</span>
            <span style="font-weight: bold">]</span>,
            <span style="color: #808000; text-decoration-color: #808000">universe</span>=<span style="color: #008000; text-decoration-color: #008000">'The survey covered all adult individuals (18 years and above) in selected households within </span>
<span style="color: #008000; text-decoration-color: #008000">the areas surveyed.'</span>,
            <span style="color: #808000; text-decoration-color: #808000">nation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">NationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Cambodia'</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #008000; text-decoration-color: #008000">'KHM'</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_coverage</span>=<span style="color: #008000; text-decoration-color: #008000">'National coverage'</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_coverage_notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">geog_unit</span>=<span style="color: #008000; text-decoration-color: #008000">'Province, District'</span>,
            <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[]</span>,
            <span style="color: #808000; text-decoration-color: #808000">bound_poly</span>=<span style="font-weight: bold">[]</span>,
            <span style="color: #808000; text-decoration-color: #808000">study_budget</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">coll_dates</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Coll_date</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #008000; text-decoration-color: #008000">'2019-10'</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #008000; text-decoration-color: #008000">'2020-01'</span>, <span style="color: #808000; text-decoration-color: #808000">cycle</span>=<span style="color: #008000; text-decoration-color: #008000">'Main Data Collection'</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">time_periods</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Time_period</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #008000; text-decoration-color: #008000">'2019-10'</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #008000; text-decoration-color: #008000">'2020-01'</span>, <span style="color: #808000; text-decoration-color: #808000">cycle</span>=<span style="color: #008000; text-decoration-color: #008000">'Survey Reference Period'</span><span style="font-weight: bold">)]</span>,
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
        <span style="color: #808000; text-decoration-color: #808000">authoring_entity</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Authoring_entityItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'National Institute of Statistics'</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'Ministry of Planning'</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">production_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">production_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[]</span>,
            <span style="color: #808000; text-decoration-color: #808000">funding_agencies</span>=<span style="font-weight: bold">[</span>
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Funding_agencie</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'WB'</span>, <span style="color: #808000; text-decoration-color: #808000">grant</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Funding and Technical Support'</span><span style="font-weight: bold">)</span>
            <span style="font-weight: bold">]</span>,
            <span style="color: #808000; text-decoration-color: #808000">copyright</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">oth_id</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_authorization</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">study_authorization</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">agency</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">AgencyItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
            <span style="color: #808000; text-decoration-color: #808000">authorization_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">method</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">method</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">data_collection</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_collection</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">sample_frame</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">sample_frame</span><span style="font-weight: bold">(</span>
                    <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Cambodia Socio-Economic Survey (CSES)'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">valid_period</span>=<span style="font-weight: bold">[]</span>,
                    <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #008000; text-decoration-color: #008000">'National Institute of Statistics (NIS)'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">universe</span>=<span style="color: #008000; text-decoration-color: #008000">'All households within the enumeration areas of the CSES 2019/2020 round.'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">frame_unit</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">frame_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">unit_type</span>=<span style="color: #008000; text-decoration-color: #008000">'Household'</span>, <span style="color: #808000; text-decoration-color: #808000">is_primary</span>=<span style="color: #00ff00; text-decoration-color: #00ff00; font-style: italic">True</span>, <span style="color: #808000; text-decoration-color: #808000">num_of_units</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)</span>,
                    <span style="color: #808000; text-decoration-color: #808000">update_procedure</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                    <span style="color: #808000; text-decoration-color: #808000">reference_period</span>=<span style="font-weight: bold">[]</span>
                <span style="font-weight: bold">)</span>,
                <span style="color: #808000; text-decoration-color: #808000">sampling_procedure</span>=<span style="color: #008000; text-decoration-color: #008000">'The survey used a two-stage sampling design. In the first stage, enumeration </span>
<span style="color: #008000; text-decoration-color: #008000">areas (EAs) from the 2019/2020 CSES served as Primary Sampling Units (PSUs), with additional households selected </span>
<span style="color: #008000; text-decoration-color: #008000">within those EAs as Secondary Sampling Units (SSUs). Six additional households were sampled per EA using a </span>
<span style="color: #008000; text-decoration-color: #008000">systematic random sampling method.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">sampling_deviation</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">weight</span>=<span style="color: #008000; text-decoration-color: #008000">'Sampling weights were developed to adjust for the probability of selection at both the PSU </span>
<span style="color: #008000; text-decoration-color: #008000">and SSU levels, with adjustments for non-response and other factors leading to the final household weights.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">research_instrument</span>=<span style="color: #008000; text-decoration-color: #008000">'The survey instruments consisted of a Household Questionnaire and an </span>
<span style="color: #008000; text-decoration-color: #008000">Individual Questionnaire, tailored to the Cambodian context and focusing on asset ownership, education, health, </span>
<span style="color: #008000; text-decoration-color: #008000">employment, and related topics.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">instru_development</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">time_method</span>=<span style="color: #008000; text-decoration-color: #008000">'Cross-sectional'</span>,
                <span style="color: #808000; text-decoration-color: #808000">frequency</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[]</span>,
                <span style="color: #808000; text-decoration-color: #808000">coll_mode</span>=<span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'Computer Assisted Personal Interview (CAPI)'</span><span style="font-weight: bold">]</span>,
                <span style="color: #808000; text-decoration-color: #808000">data_collectors</span>=<span style="font-weight: bold">[</span>
                    <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_collector</span><span style="font-weight: bold">(</span>
                        <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'National Institute of Statistics'</span>,
                        <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'Ministry of Planning'</span>,
                        <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'NIS'</span>,
                        <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Data Collection Agency'</span>
                    <span style="font-weight: bold">)</span>
                <span style="font-weight: bold">]</span>,
                <span style="color: #808000; text-decoration-color: #808000">collector_training</span>=<span style="font-weight: bold">[</span>
                    <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Collector_trainingItem</span><span style="font-weight: bold">(</span>
                        <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Interviewer Training'</span>,
                        <span style="color: #808000; text-decoration-color: #808000">training</span>=<span style="color: #008000; text-decoration-color: #008000">'The training involved formal classroom sessions and field practice over 14 days, </span>
<span style="color: #008000; text-decoration-color: #008000">focusing on content training, CAPI application, and addressing sensitive survey topics such as asset ownership and </span>
<span style="color: #008000; text-decoration-color: #008000">rights.'</span>
                    <span style="font-weight: bold">)</span>
                <span style="font-weight: bold">]</span>,
                <span style="color: #808000; text-decoration-color: #808000">control_operations</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">act_min</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">coll_situation</span>=<span style="color: #008000; text-decoration-color: #008000">'Interviews were conducted in private for sensitive topics, with male and female </span>
<span style="color: #008000; text-decoration-color: #008000">enumerators pairing according to respondent gender.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">cleaning_operations</span>=<span style="color: #008000; text-decoration-color: #008000">'Data checks were implemented within the CAPI system for real-time consistency </span>
<span style="color: #008000; text-decoration-color: #008000">validation; additional data cleaning was carried out post-collection using statistical software.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">analysis_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">analysis_info</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">data_appraisal</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">analysis_info</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">analysis_info</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">response_rate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">sampling_error_estimates</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #808000; text-decoration-color: #808000">method_notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">data_processing</span>=<span style="font-weight: bold">[]</span>
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
            <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">distribution_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">distribution_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">depositor</span>=<span style="font-weight: bold">[</span>
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">DepositorItem</span><span style="font-weight: bold">(</span>
                    <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'National Institute of Statistics'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'NIS'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'Ministry of Planning'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
                <span style="font-weight: bold">)</span>,
                <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">DepositorItem</span><span style="font-weight: bold">(</span>
                    <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'WB'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank Group'</span>,
                    <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'http://www.worldbank.org'</span>
                <span style="font-weight: bold">)</span>
            <span style="font-weight: bold">]</span>,
            <span style="color: #808000; text-decoration-color: #808000">deposit_date</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">distributors</span>=<span style="font-weight: bold">[]</span>,
            <span style="color: #808000; text-decoration-color: #808000">distribution_date</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
            <span style="color: #808000; text-decoration-color: #808000">contact</span>=<span style="font-weight: bold">[]</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">study_notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[]</span>,
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



The output can be converted to a dictionary or saved to an Excel file.


```python
metadata_dictionary = me.change_mode_or_template(example, output_mode='dict')
```


```python
me.save_metadata_to_excel(example, "cambodia_metadata.xlsx")
```

If we like the draft of the metadata, we can log it in the Metadata Editor in the usual way:


```python
me.create_project_log(example)
```

# Web URL

Similarly, if the source is a web URL, we can create metadata from the content of the web page by passing the URL to the `draft_metadata_from_files` method:


```python
docs = ['https://data.worldbank.org/indicator/NY.GDP.MKTP.CD']

example_gdp = me.draft_metadata_from_files(llm_api_key=openai_key, 
                                       files=docs, 
                                       metadata_type_or_template_uid='indicator',
                                       output_mode='pydantic',
                                       metadata_producer_organization="The World Bank Group, DEC - Development Data Group"
                                       )
example_gdp.pretty_print()
```

    Read in https://data.worldbank.org/indicator/NY.GDP.MKTP.CD, running token count is 1839
    Sending to OpenAI, this may take a few minutes...
    


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_INDICATOR_1-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">0_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">metadata_information</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">metadata_information</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$) Metadata'</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'WB_NY.GDP.MKTP.CD_v2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata producer'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">prod_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">series_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">series_description</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
        <span style="color: #808000; text-decoration-color: #808000">alternate_identifiers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Alternate_identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">database</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
        <span style="color: #808000; text-decoration-color: #808000">aliases</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Aliase</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">alias</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">database_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_short</span>=<span style="color: #008000; text-decoration-color: #008000">'Gross Domestic Product computed in current US dollars.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_long</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_references</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Definition_reference</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">relevance</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">methodology</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data and OECD National Accounts data files.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">derivation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">imputation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">statistical_concept</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">concepts</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Concept</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">definition</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">aggregation_method</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files'</span>,
                <span style="color: #808000; text-decoration-color: #808000">organization</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_collection</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_collection</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">data_source</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">method</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">period</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
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
        <span style="color: #808000; text-decoration-color: #808000">quality_checks</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">quality_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">validation_rules</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_discrepancies</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">adjustments</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">missing</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">errata</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ErrataItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">time_periods</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Time_period</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #008000; text-decoration-color: #008000">'1960'</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #008000; text-decoration-color: #008000">'2023'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">ref_country</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Ref_countryItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">geographic_units</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Geographic_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">east</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">south</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">north</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">authoring_entity</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Authoring_entityItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">mandate</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">measurement_unit</span>=<span style="color: #008000; text-decoration-color: #008000">'current US$'</span>,
        <span style="color: #808000; text-decoration-color: #808000">dimensions</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Dimension</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">release_calendar</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">periodicity</span>=<span style="color: #008000; text-decoration-color: #008000">'Annual'</span>,
        <span style="color: #808000; text-decoration-color: #808000">base_period</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_break</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'economics'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'financial statistics'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">themes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Theme</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disciplines</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Discipline</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disaggregation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">languages</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'English'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'en'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Español'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'es'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Français'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'fr'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'العربية'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'ar'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'中文'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'zh'</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">acronyms</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Acronym</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">acronym</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP'</span>, <span style="color: #808000; text-decoration-color: #808000">expansion</span>=<span style="color: #008000; text-decoration-color: #008000">'Gross Domestic Product'</span>, <span style="color: #808000; text-decoration-color: #808000">occurrence</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">related_indicators</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP growth (annual %)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (constant 2015 US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (constant LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CN.AD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CN.AD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP: linked series (current LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.PP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.PP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP, PPP (constant 2021 international $)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.PP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.PP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP, PPP (current international $)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.PCAP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.PCAP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP per capita growth (annual %)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_groups</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Series_group</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">license</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">LicenseItem</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Creative Commons Attribution 4.0 International license (CC-BY 4.0)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_status</span>=<span style="color: #008000; text-decoration-color: #008000">'public'</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">links</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'CSV download'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'XML download'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=xml'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Excel download'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">api_documentation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Api_documentationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">contacts</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contact</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Help Desk'</span>,
                <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>,
                <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">telephone</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'http://datahelpdesk.worldbank.org'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[]</span>
<span style="font-weight: bold">)</span>
</pre>



# Augmenting existing metadata

If we already have some metadata, we can retrieve it from the Metadata Editor and augment it with additional information from the content of some files:

First retrieve the existing metadata:


```python
existing_metadata = me.get_project_metadata_by_id(2202, output_mode='pydantic')

existing_metadata.pprint()
```


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_DOCUMENT_1-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">0_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">metadata_information</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">metadata_information</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata for: The Analysis of Household Surveys'</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'IHSN_978-1-4648-1331-3_v1.0'</span>,
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'John Doe'</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'IHSN'</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Data Curator'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">production_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2024-09-30'</span>,
        <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">document_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">document_description</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">title_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'DEMO_DOC_001'</span>,
            <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'The Analysis of Household Surveys: A Microeconometric Approach to Development Policy'</span>,
            <span style="color: #808000; text-decoration-color: #808000">sub_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">alternate_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">translated_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">identifiers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'ISBN'</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #008000; text-decoration-color: #008000">'978-1-4648-1331-3'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_created</span>=<span style="color: #008000; text-decoration-color: #008000">'2019-01-16'</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_published</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_modified</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_available</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">authors</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Author</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #008000; text-decoration-color: #008000">'Angus'</span>,
                <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #008000; text-decoration-color: #008000">'Deaton'</span>,
                <span style="color: #808000; text-decoration-color: #808000">full_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">author_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">editors</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Editor</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">translators</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Translator</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">contributors</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contributor</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">contribution</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bibliographic_citation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Bibliographic_citationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">style</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">citation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">booktitle</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">chapter</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">edition</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">institution</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">journal</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">volume</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">number</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">pages</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">publisher</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank, Washington, DC'</span>,
        <span style="color: #808000; text-decoration-color: #808000">publisher_address</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">series</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">crossref</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">key</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">organization</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">annote</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">howpublished</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">url</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Book [book]'</span>,
        <span style="color: #808000; text-decoration-color: #808000">publication_frequency</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">languages</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'English'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'EN'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">abstract</span>=<span style="color: #008000; text-decoration-color: #008000">"Two decades after its original publication, The Analysis of Household Surveys is reissued with a </span>
<span style="color: #008000; text-decoration-color: #008000">new preface by its author, Sir Angus Deaton, recipient of the 2015 Nobel Prize in Economic Sciences. This classic </span>
<span style="color: #008000; text-decoration-color: #008000">work remains relevant to anyone with a serious interest in using household survey data to shed light on policy </span>
<span style="color: #008000; text-decoration-color: #008000">issues. This book reviews the analysis of household survey data, including the construction of household surveys, </span>
<span style="color: #008000; text-decoration-color: #008000">the econometric tools useful for such analysis, and a range of problems in development policy for which this survey</span>
<span style="color: #008000; text-decoration-color: #008000">analysis can be applied. The author's approach remains close to the data, using transparent econometric and </span>
<span style="color: #008000; text-decoration-color: #008000">graphical techniques to present data in a way that can clearly inform policy and academic debates. Chapter 1 </span>
<span style="color: #008000; text-decoration-color: #008000">describes the features of survey design that need to be understood in order to undertake appropriate analysis. </span>
<span style="color: #008000; text-decoration-color: #008000">Chapter 2 discusses the general econometric and statistical issues that arise when using survey data for estimation</span>
<span style="color: #008000; text-decoration-color: #008000">and inference. Chapter 3 covers the use of survey data to measure welfare, poverty, and distribution. Chapter 4 </span>
<span style="color: #008000; text-decoration-color: #008000">focuses on the use of household budget data to explore patterns of household demand. Chapter 5 discusses price </span>
<span style="color: #008000; text-decoration-color: #008000">reform, its effects on equity and efficiency, and how to measure them. Chapter 6 addresses the role of household </span>
<span style="color: #008000; text-decoration-color: #008000">consumption and saving in economic development. The book includes an appendix providing code and programs using </span>
<span style="color: #008000; text-decoration-color: #008000">STATA, which can serve as a template for the users' own analysis."</span>,
        <span style="color: #808000; text-decoration-color: #808000">scope</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Household surveys'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Survey design'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Data collection'</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">themes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Theme</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disciplines</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Discipline</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">toc</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">toc_structured</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Toc_structuredItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">ref_country</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Ref_countryItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">geographic_units</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Geographic_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">east</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">south</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">north</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">spatial_coverage</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">temporal_coverage</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">status</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">rights</span>=<span style="color: #008000; text-decoration-color: #008000">'CC BY 3.0 IGO'</span>,
        <span style="color: #808000; text-decoration-color: #808000">copyright</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">license</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">LicenseItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">usage_terms</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">disclaimer</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">security_classification</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">access_restrictions</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">pricing</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">contacts</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contact</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">telephone</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source_origin</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">source_char</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">source_doc</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_sources</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_source</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">reproducibility</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">reproducibility</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">links</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)])</span>,
        <span style="color: #808000; text-decoration-color: #808000">audience</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">relations</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Relation</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Tag</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">tag</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">tag_group</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
<span style="font-weight: bold">)</span>
</pre>



Then augment the metadata with additional information from the content of the files. In this example, the original metadata was an incomplete record about a document. One way to augment this is to find the original document, in this case a PDF on the web, and use the `augment_metadata_from_files` method.

To make it obvious which fields were in the original metadata and which were added, we can set the prefix to `<AI>` which will be added to the fields that were added by the Large Language Model.


```python
docs = ["https://documents1.worldbank.org/curated/en/593871468777303124/pdf/17140-PUB-revised-PUBLIC-9781464813313-Updated.pdf"]
augmented = me.augment_metadata_from_files(input_metadata=existing_metadata,
                                           llm_api_key=openai_key,
                                           files=docs,
                                           output_mode='pydantic',
                                           metadata_producer_organization="The World Bank Group, DEC - Development Data Group",
                                           prefix="<AI>"
                                           )

augmented.pprint()
```

    Read in /var/folders/jv/htm9fs717y350bv788702w000000gp/T/tmpajh5p86n.txt, running token count is 633
    Read in https://documents1.worldbank.org/curated/en/593871468777303124/pdf/17140-PUB-revised-PUBLIC-9781464813313-Updated.pdf, running token count is 8378
    Sending to OpenAI, this may take a few minutes...
    


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_DOCUMENT_1-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">0_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">metadata_information</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">metadata_information</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata for: The Analysis of Household Surveys'</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'IHSN_978-1-4648-1331-3_v1.0'</span>,
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'John Doe'</span>, <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'IHSN'</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Data Curator'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">production_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2024-09-30'</span>,
        <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">document_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">document_description</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">title_statement</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'DEMO_DOC_001'</span>,
            <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">'The Analysis of Household Surveys: A Microeconometric Approach to Development Policy'</span>,
            <span style="color: #808000; text-decoration-color: #808000">sub_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">alternate_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
            <span style="color: #808000; text-decoration-color: #808000">translated_title</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">identifiers</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Identifier</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'ISBN'</span>, <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #008000; text-decoration-color: #008000">'978-1-4648-1331-3'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_created</span>=<span style="color: #008000; text-decoration-color: #008000">'2019-01-16'</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_published</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_modified</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">date_available</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">authors</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Author</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #008000; text-decoration-color: #008000">'Angus'</span>,
                <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #008000; text-decoration-color: #008000">'Deaton'</span>,
                <span style="color: #808000; text-decoration-color: #808000">full_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">author_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">editors</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Editor</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">translators</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Translator</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">contributors</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contributor</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">first_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">initial</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">last_name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">contribution</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bibliographic_citation</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Bibliographic_citationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">style</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">citation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">booktitle</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">chapter</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">edition</span>=<span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;Reissue Edition with a New Preface'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">institution</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">journal</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">volume</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">number</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">pages</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">publisher</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'World Bank, Washington, DC'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">publisher_address</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">series</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">crossref</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">key</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">organization</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">annote</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">howpublished</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">url</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;https://documents1.worldbank.org/curated/en/593871468777303124/pdf/17140-PUB-revised-PUBLIC-978146</span>
<span style="color: #008000; text-decoration-color: #008000">4813313-Updated.pdf'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">type</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'Book [book]'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">publication_frequency</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">languages</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'English'</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">code</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'EN'</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">description</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">abstract</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">"Two decades after its original publication, The Analysis of Household Surveys is reissued with a </span>
<span style="color: #008000; text-decoration-color: #008000">new preface by its author, Sir Angus Deaton, recipient of the 2015 Nobel Prize in Economic Sciences. This classic </span>
<span style="color: #008000; text-decoration-color: #008000">work remains relevant to anyone with a serious interest in using household survey data to shed light on policy </span>
<span style="color: #008000; text-decoration-color: #008000">issues. This book reviews the analysis of household survey data, including the construction of household surveys, </span>
<span style="color: #008000; text-decoration-color: #008000">the econometric tools useful for such analysis, and a range of problems in development policy for which this survey</span>
<span style="color: #008000; text-decoration-color: #008000">analysis can be applied. The author's approach remains close to the data, using transparent econometric and </span>
<span style="color: #008000; text-decoration-color: #008000">graphical techniques to present data in a way that can clearly inform policy and academic debates. Chapter 1 </span>
<span style="color: #008000; text-decoration-color: #008000">describes the features of survey design that need to be understood in order to undertake appropriate analysis. </span>
<span style="color: #008000; text-decoration-color: #008000">Chapter 2 discusses the general econometric and statistical issues that arise when using survey data for estimation</span>
<span style="color: #008000; text-decoration-color: #008000">and inference. Chapter 3 covers the use of survey data to measure welfare, poverty, and distribution. Chapter 4 </span>
<span style="color: #008000; text-decoration-color: #008000">focuses on the use of household budget data to explore patterns of household demand. Chapter 5 discusses price </span>
<span style="color: #008000; text-decoration-color: #008000">reform, its effects on equity and efficiency, and how to measure them. Chapter 6 addresses the role of household </span>
<span style="color: #008000; text-decoration-color: #008000">consumption and saving in economic development. The book includes an appendix providing code and programs using </span>
<span style="color: #008000; text-decoration-color: #008000">STATA, which can serve as a template for the users' own analysis."</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">scope</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">keywords</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span>
<span style="color: #000000; text-decoration-color: #000000">            </span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'Household surveys'</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">            </span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'Survey design'</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">            </span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Keyword</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'Data collection'</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">topics</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">parent_id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">themes</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Theme</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">parent_id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">disciplines</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Discipline</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">parent_id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">vocabulary</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">toc</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">toc_structured</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Toc_structuredItem</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">parent_id</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">ref_country</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Ref_countryItem</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">''</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">code</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">geographic_units</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Geographic_unit</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">''</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">code</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">type</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">bbox</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">east</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">south</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">, </span><span style="color: #808000; text-decoration-color: #808000">north</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">spatial_coverage</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">temporal_coverage</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">status</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">rights</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'CC BY 3.0 IGO'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">copyright</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;© 2018 International Bank for Reconstruction and Development / The World Bank'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">license</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">[</span>
<span style="color: #000000; text-decoration-color: #000000">            </span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">LicenseItem</span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">(</span>
<span style="color: #000000; text-decoration-color: #000000">                </span><span style="color: #808000; text-decoration-color: #808000">name</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;Creative Commons Attribution 3.0 IGO (CC BY 3.0 IGO)'</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">                </span><span style="color: #808000; text-decoration-color: #808000">uri</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;http://creativecommons.org/licenses/by/3.0/igo'</span>
<span style="color: #000000; text-decoration-color: #000000">            </span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">)</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #000000; text-decoration-color: #000000; font-weight: bold">]</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">usage_terms</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="color: #000000; text-decoration-color: #000000">,</span>
<span style="color: #000000; text-decoration-color: #000000">        </span><span style="color: #808000; text-decoration-color: #808000">disclaimer</span><span style="color: #000000; text-decoration-color: #000000">=</span><span style="color: #008000; text-decoration-color: #008000">'&lt;AI&gt;This work is a product of the staff of The World Bank with external contributions. The </span>
<span style="color: #008000; text-decoration-color: #008000">findings, interpretations, and conclusions expressed in this work do not necessarily reflect the views of The World</span>
<span style="color: #008000; text-decoration-color: #008000">Bank, its Board of Executive Directors, or the governments they represent. The World Bank does not guarantee the </span>
<span style="color: #008000; text-decoration-color: #008000">accuracy of the data included in this work. The boundaries, colors, denominations, and other information shown on </span>
<span style="color: #008000; text-decoration-color: #008000">any map in this work do not imply any judgment on the part of The World Bank concerning the legal status of any </span>
<span style="color: #008000; text-decoration-color: #008000">territory or the endorsement or acceptance of such boundaries.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">security_classification</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">access_restrictions</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">pricing</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">contacts</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contact</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">telephone</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">source_origin</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">source_char</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">source_doc</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_sources</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Data_source</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">reproducibility</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">reproducibility</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">links</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)])</span>,
        <span style="color: #808000; text-decoration-color: #808000">audience</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">relations</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Relation</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Tag</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">tag</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">tag_group</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>
<span style="font-weight: bold">)</span>
</pre>



# Privacy

There are options for running privately without sharing the data with OpenAI.

## Running Locally

One option is to run the LLM on your personal computer. To do this you first need to download and install [Ollama](https://ollama.com/).

Ollama is a framework for running, managing, and serving large language models (LLMs) locally on a user's machine. It provides an easy-to-use interface for downloading, running, and interacting with models like Llama, Mistral, and others without requiring cloud-based services.

Once you have Ollama installed, you can download the LLMs you want to use. For example, to download the llama3.1 model, you would run:

```bash
ollama pull llama3.1
```
Then you must serve the model locally using:

```bash
ollama serve llama3.1
```

To check if the model is running, you can use:

```bash
ollama ps
```

To stop the model from running, you can use:

```bash
ollama stop llama3.1
```

And you can delete the model if you no longer need it:

```bash
ollama rm llama3.1
```

When the model is being served, you can use it in the pyMetadataEditor code by setting the llm_api_key to `ollama`, the llm_model_name to `llama3.1`, and the llm_base_url to `http://localhost:11434/v1/`.

It's important to remember that usually models that are small enough to run locally won't produce metadata as good as the larger models that are available remotely such as through OpenAI.


```python
docs = ['https://data.worldbank.org/indicator/NY.GDP.MKTP.CD']

example_gdp = me.draft_metadata_from_files(llm_api_key="ollama", 
                                       files=docs, 
                                       metadata_type_or_template_uid='indicator',
                                       output_mode='pydantic',
                                       metadata_producer_organization="The World Bank Group, DEC - Development Data Group",
                                       llm_base_url='http://localhost:11434/v1',
                                       llm_model_name='llama3.1:8b-instruct-q8_0'
                                       )
example_gdp.pretty_print()
```

    Reading https://data.worldbank.org/indicator/NY.GDP.MKTP.CD, running token count is 1839
    Sending to http://localhost:11434/v1, this may take a few minutes...
    

    100%|██████████| 57/57 [02:00<00:00,  2.11s/it]
    


<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">IHSN_INDICATOR_1-<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">0_Template_v01_EN</span><span style="font-weight: bold">(</span>
    <span style="color: #808000; text-decoration-color: #808000">metadata_information</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">metadata_information</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">title</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
        <span style="color: #808000; text-decoration-color: #808000">producers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Producer</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbr</span>=<span style="color: #008000; text-decoration-color: #008000">'WBG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Producer'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">prod_date</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">version_statement</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">version_statement</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">version_date</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">version_notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">version_resp</span>=<span style="color: #008000; text-decoration-color: #008000">''</span><span style="font-weight: bold">)</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">series_description</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">series_description</span><span style="font-weight: bold">(</span>
        <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
        <span style="color: #808000; text-decoration-color: #808000">alternate_identifiers</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Alternate_identifier</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">identifier</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">database</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group is not responsible for the accuracy of the data. The World Bank Group </span>
<span style="color: #008000; text-decoration-color: #008000">does not guarantee its use, completeness, timeliness, security, or exportability.'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
        <span style="color: #808000; text-decoration-color: #808000">aliases</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Aliase</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">alias</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">database_id</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_short</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_long</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$) - World Bank national accounts data, and OECD National Accounts data </span>
<span style="color: #008000; text-decoration-color: #008000">files.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">definition_references</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Definition_reference</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">source</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'http://www.worldbank.org'</span>,
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group is a family of five international organizations that work together to </span>
<span style="color: #008000; text-decoration-color: #008000">achieve the mission of ending extreme poverty and promoting shared prosperity in a sustainable manner.'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">relevance</span>=<span style="color: #008000; text-decoration-color: #008000">'high'</span>,
        <span style="color: #808000; text-decoration-color: #808000">methodology</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">derivation</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank Group, DEC - Development Data Group'</span>,
        <span style="color: #808000; text-decoration-color: #808000">imputation</span>=<span style="color: #008000; text-decoration-color: #008000">'indicator metadata'</span>,
        <span style="color: #808000; text-decoration-color: #808000">statistical_concept</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
        <span style="color: #808000; text-decoration-color: #808000">concepts</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Concept</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>, <span style="color: #808000; text-decoration-color: #808000">definition</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">aggregation_method</span>=<span style="color: #008000; text-decoration-color: #008000">'Summation of individual country data points'</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Source</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">idno</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">organization</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group, DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_note</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata produced by The World Bank Group, DEC - Development Data Group on February 26th, </span>
<span style="color: #008000; text-decoration-color: #008000">2025'</span>,
        <span style="color: #808000; text-decoration-color: #808000">data_collection</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">data_collection</span><span style="font-weight: bold">(</span>
            <span style="color: #808000; text-decoration-color: #808000">data_source</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>,
            <span style="color: #808000; text-decoration-color: #808000">method</span>=<span style="color: #008000; text-decoration-color: #008000">'National accounts data, and OECD National Accounts data files.'</span>,
            <span style="color: #808000; text-decoration-color: #808000">period</span>=<span style="color: #008000; text-decoration-color: #008000">'Annual'</span>,
            <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data'</span>,
            <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://data.worldbank.org/indicator/NY.GDP.MKTP.CD'</span>
        <span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">compliance</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ComplianceItem</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">standard</span>=<span style="color: #008000; text-decoration-color: #008000">'DCAT-AP'</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #008000; text-decoration-color: #008000">'DCAT'</span>,
                <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group, DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://data.worldbank.org/indicator/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">framework</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">FrameworkItem</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank'</span>,
                <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #008000; text-decoration-color: #008000">'WB'</span>,
                <span style="color: #808000; text-decoration-color: #808000">custodian</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group, DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">goal_description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_id</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">target_description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_id</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">indicator_description</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://data.worldbank.org/indicator/NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">limitation</span>=<span style="color: #008000; text-decoration-color: #008000">'public'</span>,
        <span style="color: #808000; text-decoration-color: #808000">quality_checks</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">quality_note</span>=<span style="color: #008000; text-decoration-color: #008000">'The metadata is being produced today, February 26th, 2025.'</span>,
        <span style="color: #808000; text-decoration-color: #808000">validation_rules</span>=<span style="font-weight: bold">[</span><span style="color: #008000; text-decoration-color: #008000">'required'</span>, <span style="color: #008000; text-decoration-color: #008000">'email'</span><span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">sources_discrepancies</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
        <span style="color: #808000; text-decoration-color: #808000">adjustments</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">missing</span>=<span style="color: #008000; text-decoration-color: #008000">'true'</span>,
        <span style="color: #808000; text-decoration-color: #808000">errata</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">ErrataItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">date</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">time_periods</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Time_period</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">start</span>=<span style="color: #008000; text-decoration-color: #008000">'1960'</span>, <span style="color: #808000; text-decoration-color: #808000">end</span>=<span style="color: #008000; text-decoration-color: #008000">'2023'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">ref_country</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Ref_countryItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">geographic_units</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Geographic_unit</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'World'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'continent'</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">bbox</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">BboxItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">west</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">east</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">south</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">north</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">authoring_entity</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Authoring_entityItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">abbreviation</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #800080; text-decoration-color: #800080; font-weight: bold">mandate</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">mandate</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'http://www.worldbank.org'</span><span style="font-weight: bold">)</span>,
        <span style="color: #808000; text-decoration-color: #808000">measurement_unit</span>=<span style="color: #008000; text-decoration-color: #008000">'current US$ (USD)'</span>,
        <span style="color: #808000; text-decoration-color: #808000">dimensions</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Dimension</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'Gross Domestic Product in current US dollars'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">release_calendar</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">periodicity</span>=<span style="color: #008000; text-decoration-color: #008000">'Annual'</span>,
        <span style="color: #808000; text-decoration-color: #808000">base_period</span>=<span style="color: #008000; text-decoration-color: #008000">'1960'</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_break</span>=<span style="color: #008000; text-decoration-color: #008000">'2025-02-26'</span>,
        <span style="color: #808000; text-decoration-color: #808000">keywords</span>=<span style="font-weight: bold">[]</span>,
        <span style="color: #808000; text-decoration-color: #808000">topics</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Topic</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">themes</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Theme</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank national accounts data, and OECD National Accounts data files.'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disciplines</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Discipline</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">id</span>=<span style="color: #008000; text-decoration-color: #008000">'ECON'</span>,
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Economics'</span>,
                <span style="color: #808000; text-decoration-color: #808000">parent_id</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>,
                <span style="color: #808000; text-decoration-color: #808000">vocabulary</span>=<span style="color: #008000; text-decoration-color: #008000">'World Bank Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/discipline/ECON'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">disaggregation</span>=<span style="color: #008000; text-decoration-color: #008000">'Country; World'</span>,
        <span style="color: #808000; text-decoration-color: #808000">languages</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'English'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'en'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Español'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'es'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'Français'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'fr'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'عربية'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'ar'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Language</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'中文'</span>, <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'zh'</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">acronyms</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Acronym</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">acronym</span>=<span style="color: #008000; text-decoration-color: #008000">'DEC'</span>, <span style="color: #808000; text-decoration-color: #808000">expansion</span>=<span style="color: #008000; text-decoration-color: #008000">'Development Data Group'</span>, <span style="color: #808000; text-decoration-color: #808000">occurrence</span>=<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">1</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">related_indicators</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP growth (annual %)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (constant 2015 US$)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.KN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.KN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (constant LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CN.AD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CN.AD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP: linked series (current LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.PP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.PP.KD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP, PPP (constant 2021 international $)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.CN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CN'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current LCU)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.MKTP.PP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.PP.CD'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP, PPP (current international $)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Related_indicator</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">code</span>=<span style="color: #008000; text-decoration-color: #008000">'NY.GDP.PCAP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.PCAP.KD.ZG'</span>,
                <span style="color: #808000; text-decoration-color: #808000">label</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP per capita growth (annual %)'</span>,
                <span style="color: #808000; text-decoration-color: #808000">relationship</span>=<span style="color: #008000; text-decoration-color: #008000">'Related Indicator'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'Indicator'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">series_groups</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Series_group</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">version</span>=<span style="color: #008000; text-decoration-color: #008000">'2025'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://data.worldbank.org/indicator/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">notes</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata produced by The World Bank Group, DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'metadata_producer'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Note</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #008000; text-decoration-color: #008000">'Metadata production date: February 26th, 2025'</span>, <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'metadata_production_date'</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">license</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">LicenseItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span>, <span style="color: #808000; text-decoration-color: #808000">note</span>=<span style="color: #800080; text-decoration-color: #800080; font-style: italic">None</span><span style="font-weight: bold">)]</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality</span>=<span style="color: #008000; text-decoration-color: #008000">'public'</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_status</span>=<span style="color: #008000; text-decoration-color: #008000">'public'</span>,
        <span style="color: #808000; text-decoration-color: #808000">confidentiality_note</span>=<span style="color: #008000; text-decoration-color: #008000">"Confidentiality Note: The information in this document is subject to the World Bank's</span>
<span style="color: #008000; text-decoration-color: #008000">Terms of Use and is intended for public use only."</span>,
        <span style="color: #808000; text-decoration-color: #808000">links</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'self'</span>, <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'This page in:'</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span><span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'alternate'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'Español'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://datos.bancomundial.org/indicador/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'alternate'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'Français'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://donnees.banquemondiale.org/indicateur/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'alternate'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'العربية'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://data.albankaldawli.org/indicator/NY.GDP.MKTP.CD'</span>
            <span style="font-weight: bold">)</span>,
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Link</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">type</span>=<span style="color: #008000; text-decoration-color: #008000">'alternate'</span>,
                <span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'中文'</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'https://www.worldbank.org/en/topic/economic-growth/indicator/gdp-currency-convertible'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">api_documentation</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Api_documentationItem</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">description</span>=<span style="color: #008000; text-decoration-color: #008000">'GDP (current US$)'</span>, <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'/indicator/NY.GDP.MKTP.CD'</span><span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>,
        <span style="color: #808000; text-decoration-color: #808000">contacts</span>=<span style="font-weight: bold">[</span>
            <span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Contact</span><span style="font-weight: bold">(</span>
                <span style="color: #808000; text-decoration-color: #808000">name</span>=<span style="color: #008000; text-decoration-color: #008000">'The World Bank Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">role</span>=<span style="color: #008000; text-decoration-color: #008000">'Publisher'</span>,
                <span style="color: #808000; text-decoration-color: #808000">affiliation</span>=<span style="color: #008000; text-decoration-color: #008000">'DEC - Development Data Group'</span>,
                <span style="color: #808000; text-decoration-color: #808000">email</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">telephone</span>=<span style="color: #008000; text-decoration-color: #008000">''</span>,
                <span style="color: #808000; text-decoration-color: #808000">uri</span>=<span style="color: #008000; text-decoration-color: #008000">'http://www.worldbank.org/'</span>
            <span style="font-weight: bold">)</span>
        <span style="font-weight: bold">]</span>
    <span style="font-weight: bold">)</span>,
    <span style="color: #808000; text-decoration-color: #808000">tags</span>=<span style="font-weight: bold">[</span><span style="color: #800080; text-decoration-color: #800080; font-weight: bold">Tag</span><span style="font-weight: bold">(</span><span style="color: #808000; text-decoration-color: #808000">tag</span>=<span style="color: #008000; text-decoration-color: #008000">'indicator'</span>, <span style="color: #808000; text-decoration-color: #808000">tag_group</span>=<span style="color: #008000; text-decoration-color: #008000">'metadata'</span><span style="font-weight: bold">)]</span>
<span style="font-weight: bold">)</span>
</pre>



## Azure AI Services

Another option for running LLMs privately is to use a service like Azure AI Services.

Often organizations will have their own instance of an LLM within a service like Azure by Microsoft. Often they do to have more control over their data. 

You can use these services to augment your metadata by providing an endpoint (such as https://{your-resource-name}.openai.azure.com) and an API key.


**(The below error is expected as only a dummy url has been provided.)**


```python
me.augment_metadata_from_files(input_metadata=existing_metadata,
                               llm_api_key=os.getenv("API_KEY_FOR_AZURE_INSTANCE_OF_LLM"),
                               files=docs,
                               output_mode='pydantic',
                               metadata_producer_organization="The World Bank Group, DEC - Development Data Group",
                               prefix="<AI>",
                               azure_llm_base_url="https://{your-resource-name}.openai.azure.com"
                               ).pprint()
```

    Read in /var/folders/jv/htm9fs717y350bv788702w000000gp/T/tmpahk3tt2q.txt, running token count is 626
    Read in https://documents1.worldbank.org/curated/en/593871468777303124/pdf/17140-PUB-revised-PUBLIC-9781464813313-Updated.pdf, running token count is 8371
    Sending to https://{your-resource-name}.openai.azure.com, this may take a few minutes...
    


    ---------------------------------------------------------------------------

    ConnectError                              Traceback (most recent call last)

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_transports/default.py:101, in map_httpcore_exceptions()
        100 try:
    --> 101     yield
        102 except Exception as exc:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_transports/default.py:250, in HTTPTransport.handle_request(self, request)
        249 with map_httpcore_exceptions():
    --> 250     resp = self._pool.handle_request(req)
        252 assert isinstance(resp.stream, typing.Iterable)
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py:256, in ConnectionPool.handle_request(self, request)
        255     self._close_connections(closing)
    --> 256     raise exc from None
        258 # Return the response. Note that in this case we still have to manage
        259 # the point at which the response is closed.
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py:236, in ConnectionPool.handle_request(self, request)
        234 try:
        235     # Send the request on the assigned connection.
    --> 236     response = connection.handle_request(
        237         pool_request.request
        238     )
        239 except ConnectionNotAvailable:
        240     # In some cases a connection may initially be available to
        241     # handle a request, but then become unavailable.
        242     #
        243     # In this case we clear the connection and try again.
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_sync/connection.py:101, in HTTPConnection.handle_request(self, request)
        100     self._connect_failed = True
    --> 101     raise exc
        103 return self._connection.handle_request(request)
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_sync/connection.py:78, in HTTPConnection.handle_request(self, request)
         77 if self._connection is None:
    ---> 78     stream = self._connect(request)
         80     ssl_object = stream.get_extra_info("ssl_object")
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_sync/connection.py:124, in HTTPConnection._connect(self, request)
        123 with Trace("connect_tcp", logger, request, kwargs) as trace:
    --> 124     stream = self._network_backend.connect_tcp(**kwargs)
        125     trace.return_value = stream
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_backends/sync.py:207, in SyncBackend.connect_tcp(self, host, port, timeout, local_address, socket_options)
        202 exc_map: ExceptionMapping = {
        203     socket.timeout: ConnectTimeout,
        204     OSError: ConnectError,
        205 }
    --> 207 with map_exceptions(exc_map):
        208     sock = socket.create_connection(
        209         address,
        210         timeout,
        211         source_address=source_address,
        212     )
    

    File ~/.pyenv/versions/3.11.9/lib/python3.11/contextlib.py:158, in _GeneratorContextManager.__exit__(self, typ, value, traceback)
        157 try:
    --> 158     self.gen.throw(typ, value, traceback)
        159 except StopIteration as exc:
        160     # Suppress StopIteration *unless* it's the same exception that
        161     # was passed to throw().  This prevents a StopIteration
        162     # raised inside the "with" statement from being suppressed.
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpcore/_exceptions.py:14, in map_exceptions(map)
         13     if isinstance(exc, from_exc):
    ---> 14         raise to_exc(exc) from exc
         15 raise
    

    ConnectError: [Errno 8] nodename nor servname provided, or not known

    
    The above exception was the direct cause of the following exception:
    

    ConnectError                              Traceback (most recent call last)

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:996, in SyncAPIClient._request(self, cast_to, options, retries_taken, stream, stream_cls)
        995 try:
    --> 996     response = self._client.send(
        997         request,
        998         stream=stream or self._should_stream_response_body(request=request),
        999         **kwargs,
       1000     )
       1001 except httpx.TimeoutException as err:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_client.py:914, in Client.send(self, request, stream, auth, follow_redirects)
        912 auth = self._build_request_auth(request, auth)
    --> 914 response = self._send_handling_auth(
        915     request,
        916     auth=auth,
        917     follow_redirects=follow_redirects,
        918     history=[],
        919 )
        920 try:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_client.py:942, in Client._send_handling_auth(self, request, auth, follow_redirects, history)
        941 while True:
    --> 942     response = self._send_handling_redirects(
        943         request,
        944         follow_redirects=follow_redirects,
        945         history=history,
        946     )
        947     try:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_client.py:979, in Client._send_handling_redirects(self, request, follow_redirects, history)
        977     hook(request)
    --> 979 response = self._send_single_request(request)
        980 try:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_client.py:1014, in Client._send_single_request(self, request)
       1013 with request_context(request=request):
    -> 1014     response = transport.handle_request(request)
       1016 assert isinstance(response.stream, SyncByteStream)
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_transports/default.py:249, in HTTPTransport.handle_request(self, request)
        237 req = httpcore.Request(
        238     method=request.method,
        239     url=httpcore.URL(
       (...)
        247     extensions=request.extensions,
        248 )
    --> 249 with map_httpcore_exceptions():
        250     resp = self._pool.handle_request(req)
    

    File ~/.pyenv/versions/3.11.9/lib/python3.11/contextlib.py:158, in _GeneratorContextManager.__exit__(self, typ, value, traceback)
        157 try:
    --> 158     self.gen.throw(typ, value, traceback)
        159 except StopIteration as exc:
        160     # Suppress StopIteration *unless* it's the same exception that
        161     # was passed to throw().  This prevents a StopIteration
        162     # raised inside the "with" statement from being suppressed.
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/httpx/_transports/default.py:118, in map_httpcore_exceptions()
        117 message = str(exc)
    --> 118 raise mapped_exc(message) from exc
    

    ConnectError: [Errno 8] nodename nor servname provided, or not known

    
    The above exception was the direct cause of the following exception:
    

    APIConnectionError                        Traceback (most recent call last)

    Cell In[19], line 3
          1 docs = ["https://documents1.worldbank.org/curated/en/593871468777303124/pdf/17140-PUB-revised-PUBLIC-9781464813313-Updated.pdf"]
    ----> 3 me.augment_metadata_from_files(input_metadata=existing_metadata,
          4                                llm_api_key="socksocksocks",
          5                                files=docs,
          6                                output_mode='pydantic',
          7                                metadata_producer_organization="The World Bank Group, DEC - Development Data Group",
          8                                prefix="<AI>",
          9                                azure_llm_base_url="https://{your-resource-name}.openai.azure.com"
         10                                ).pprint()
    

    File ~/sources/pymetadataeditor/pymetadataeditor/interface.py:914, in MetadataEditor.augment_metadata_from_files(self, input_metadata, llm_api_key, files, output_mode, metadata_type_or_template_uid, metadata_producer_organization, prefix, filename, title, llm_model_name, tokenizer_model, max_tokens, public_llm_base_url, azure_llm_base_url)
        911         files = [files]
        912     files = [file_path] + files
    --> 914     new_metadata = self.draft_metadata_from_files(
        915         llm_api_key=llm_api_key,
        916         files=files,
        917         metadata_type_or_template_uid=metadata_type_or_template_uid,
        918         metadata_producer_organization=metadata_producer_organization,
        919         output_mode="dict",
        920         # prefix=prefix,
        921         filename=None,
        922         title=None,
        923         llm_model_name=llm_model_name,
        924         tokenizer_model=tokenizer_model,
        925         max_tokens=max_tokens,
        926         public_llm_base_url=public_llm_base_url,
        927         azure_llm_base_url=azure_llm_base_url,
        928     )
        930 if new_metadata is None or len(new_metadata) == 0:
        931     raise ValueError("No metadata was generated from the files.")
    

    File ~/sources/pymetadataeditor/pymetadataeditor/interface.py:766, in MetadataEditor.draft_metadata_from_files(self, llm_api_key, files, output_mode, metadata_type_or_template_uid, metadata_producer_organization, filename, title, llm_model_name, tokenizer_model, max_tokens, public_llm_base_url, azure_llm_base_url)
        764 endpoint_name = azure_llm_base_url if azure_llm_base_url is not None else "OpenAI" if public_llm_base_url is None else public_llm_base_url
        765 print(f"Sending to {endpoint_name}, this may take a few minutes...")
    --> 766 completion = client.beta.chat.completions.parse(
        767     model=llm_model_name,
        768     messages=messages,
        769     response_format=metadata_class_no_rules,
        770 )
        772 message = completion.choices[0].message
        773 if not message.parsed:
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/resources/beta/chat/completions.py:160, in Completions.parse(self, messages, model, audio, response_format, frequency_penalty, function_call, functions, logit_bias, logprobs, max_completion_tokens, max_tokens, metadata, modalities, n, parallel_tool_calls, prediction, presence_penalty, reasoning_effort, seed, service_tier, stop, store, stream_options, temperature, tool_choice, tools, top_logprobs, top_p, user, extra_headers, extra_query, extra_body, timeout)
        153 def parser(raw_completion: ChatCompletion) -> ParsedChatCompletion[ResponseFormatT]:
        154     return _parse_chat_completion(
        155         response_format=response_format,
        156         chat_completion=raw_completion,
        157         input_tools=tools,
        158     )
    --> 160 return self._post(
        161     "/chat/completions",
        162     body=maybe_transform(
        163         {
        164             "messages": messages,
        165             "model": model,
        166             "audio": audio,
        167             "frequency_penalty": frequency_penalty,
        168             "function_call": function_call,
        169             "functions": functions,
        170             "logit_bias": logit_bias,
        171             "logprobs": logprobs,
        172             "max_completion_tokens": max_completion_tokens,
        173             "max_tokens": max_tokens,
        174             "metadata": metadata,
        175             "modalities": modalities,
        176             "n": n,
        177             "parallel_tool_calls": parallel_tool_calls,
        178             "prediction": prediction,
        179             "presence_penalty": presence_penalty,
        180             "reasoning_effort": reasoning_effort,
        181             "response_format": _type_to_response_format(response_format),
        182             "seed": seed,
        183             "service_tier": service_tier,
        184             "stop": stop,
        185             "store": store,
        186             "stream": False,
        187             "stream_options": stream_options,
        188             "temperature": temperature,
        189             "tool_choice": tool_choice,
        190             "tools": tools,
        191             "top_logprobs": top_logprobs,
        192             "top_p": top_p,
        193             "user": user,
        194         },
        195         completion_create_params.CompletionCreateParams,
        196     ),
        197     options=make_request_options(
        198         extra_headers=extra_headers,
        199         extra_query=extra_query,
        200         extra_body=extra_body,
        201         timeout=timeout,
        202         post_parser=parser,
        203     ),
        204     # we turn the `ChatCompletion` instance into a `ParsedChatCompletion`
        205     # in the `parser` function above
        206     cast_to=cast(Type[ParsedChatCompletion[ResponseFormatT]], ChatCompletion),
        207     stream=False,
        208 )
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1283, in SyncAPIClient.post(self, path, cast_to, body, options, files, stream, stream_cls)
       1269 def post(
       1270     self,
       1271     path: str,
       (...)
       1278     stream_cls: type[_StreamT] | None = None,
       1279 ) -> ResponseT | _StreamT:
       1280     opts = FinalRequestOptions.construct(
       1281         method="post", url=path, json_data=body, files=to_httpx_files(files), **options
       1282     )
    -> 1283     return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:960, in SyncAPIClient.request(self, cast_to, options, remaining_retries, stream, stream_cls)
        957 else:
        958     retries_taken = 0
    --> 960 return self._request(
        961     cast_to=cast_to,
        962     options=options,
        963     stream=stream,
        964     stream_cls=stream_cls,
        965     retries_taken=retries_taken,
        966 )
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1020, in SyncAPIClient._request(self, cast_to, options, retries_taken, stream, stream_cls)
       1017 log.debug("Encountered Exception", exc_info=True)
       1019 if remaining_retries > 0:
    -> 1020     return self._retry_request(
       1021         input_options,
       1022         cast_to,
       1023         retries_taken=retries_taken,
       1024         stream=stream,
       1025         stream_cls=stream_cls,
       1026         response_headers=None,
       1027     )
       1029 log.debug("Raising connection error")
       1030 raise APIConnectionError(request=request) from err
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1098, in SyncAPIClient._retry_request(self, options, cast_to, retries_taken, response_headers, stream, stream_cls)
       1094 # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
       1095 # different thread if necessary.
       1096 time.sleep(timeout)
    -> 1098 return self._request(
       1099     options=options,
       1100     cast_to=cast_to,
       1101     retries_taken=retries_taken + 1,
       1102     stream=stream,
       1103     stream_cls=stream_cls,
       1104 )
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1020, in SyncAPIClient._request(self, cast_to, options, retries_taken, stream, stream_cls)
       1017 log.debug("Encountered Exception", exc_info=True)
       1019 if remaining_retries > 0:
    -> 1020     return self._retry_request(
       1021         input_options,
       1022         cast_to,
       1023         retries_taken=retries_taken,
       1024         stream=stream,
       1025         stream_cls=stream_cls,
       1026         response_headers=None,
       1027     )
       1029 log.debug("Raising connection error")
       1030 raise APIConnectionError(request=request) from err
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1098, in SyncAPIClient._retry_request(self, options, cast_to, retries_taken, response_headers, stream, stream_cls)
       1094 # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
       1095 # different thread if necessary.
       1096 time.sleep(timeout)
    -> 1098 return self._request(
       1099     options=options,
       1100     cast_to=cast_to,
       1101     retries_taken=retries_taken + 1,
       1102     stream=stream,
       1103     stream_cls=stream_cls,
       1104 )
    

    File ~/Library/Caches/pypoetry/virtualenvs/pymetadataeditor-HQrUvkIt-py3.11/lib/python3.11/site-packages/openai/_base_client.py:1030, in SyncAPIClient._request(self, cast_to, options, retries_taken, stream, stream_cls)
       1020         return self._retry_request(
       1021             input_options,
       1022             cast_to,
       (...)
       1026             response_headers=None,
       1027         )
       1029     log.debug("Raising connection error")
    -> 1030     raise APIConnectionError(request=request) from err
       1032 log.debug(
       1033     'HTTP Response: %s %s "%i %s" %s',
       1034     request.method,
       (...)
       1038     response.headers,
       1039 )
       1040 log.debug("request_id: %s", response.headers.get("x-request-id"))
    

    APIConnectionError: Connection error.

