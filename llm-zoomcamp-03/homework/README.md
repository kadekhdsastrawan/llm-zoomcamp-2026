# HOMEWORK 3

## Q1: ChatGPT vs AICopilot
ChatGPT give a different answer and compared to Kestra AICopilot, response from ChatGPT is more verbose. This is due to that the ChatGPT grounded based on the training data which have the chance of un-updated context / ground-truth. While, Kestra AICopilot grounded based on the features available in Kestra.

### ChatGPT
```yaml
id: nyc_taxi_csv_to_bigquery
namespace: company.team

variables:
  project_id: your-gcp-project
  bucket: your-gcs-bucket
  dataset: nyc_taxi
  table: yellow_tripdata
  csv_url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2023-01.csv.gz

tasks:
  - id: download_csv
    type: io.kestra.plugin.core.http.Download
    uri: "{{ vars.csv_url }}"

  - id: upload_to_gcs
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{ outputs.download_csv.uri }}"
    bucket: "{{ vars.bucket }}"
    name: "yellow_tripdata_2023_01.csv.gz"

  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    from:
      - "gs://{{ vars.bucket }}/yellow_tripdata_2023_01.csv.gz"

    destinationTable: "{{ vars.project_id }}.{{ vars.dataset }}.{{ vars.table }}"

    format: CSV
    compression: GZIP
    autodetect: true
    createDisposition: CREATE_IF_NEEDED
    writeDisposition: WRITE_TRUNCATE

    csvOptions:
      skipLeadingRows: 1
      allowQuotedNewLines: true
```

### AICopilot
```yaml
id: squid_686142
namespace: company.team

tasks:
  - id: download_nyc_taxi_data
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.csv
    # Optional: If the file is large, you might want to increase the timeout
    # timeout: PT5M

  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.Load
    from: "{{ outputs.download_nyc_taxi_data.uri }}"
    destinationTable: "your_gcp_project.your_bigquery_dataset.nyc_taxi_data" # << Update with your actual BigQuery project, dataset, and table
    format: CSV
    csvOptions:
      skipLeadingRows: 1
    # You must provide either a serviceAccount or an impersonatedServiceAccount
    # serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}" # << Uncomment and replace with your GCP service account secret
    # projectId: "your_gcp_project_id" # << Uncomment and replace with your GCP project ID
```
---

## Q2: The non-RAG response about Kestra 1.1 features is best described as

If we take a look at the Kestra 1.1 features using non-RAG response, we will get the _**Vague, generic, or fabricated — the model guesses from training data**_.

This is due to the LLM didn't have ground-truth information that is being used as a source of truth or reference. If the LLM training data didn't cover the Kestra 1.1, it will tend to hallucinate (made up the narrative about the feature).

## Q3: What is the approximate output token count for multilingual_agent when running with summary_length = short?

When trying to run, I got around 60 tokens up to 77 tokens. So it is approximately **60-100 output tokens**.

## Q4: With summary_length = long, roughly how many times more output tokens does multilingual_agent use compared to the short summary?

I got 182 output tokens when change the `summary_length` to `long`. THerefore, it will be around: `182/77 = 2.36x`

## Q5: After changing english_brevity to ask for 3 sentences instead of 1, how does the output token count compare to the original 1-sentence version?

I benchmarked `english_brevity` for `summary_length` equal to `short`. I got these results:
| Sentence | Output Token |
| --- | --- |
| 1 sentence | 41 tokens |
| 3 sentence | 69 tokens |

From the result, it is around at least 2 times more (**2-4x more**).

## Q6: For production workflows requiring deterministic, repeatable results with strict compliance requirements, which approach is most appropriate?

Deterministic repeatable results need consistency in each of the workflow done. Therefore: _**Use traditional task-based workflows for predictability and auditability**_