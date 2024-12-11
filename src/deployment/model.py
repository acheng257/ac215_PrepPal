from kfp import dsl


# Define a Container Component
@dsl.component(base_image="python:3.9", packages_to_install=["google-cloud-aiplatform", "google-generativeai"])
def model_training(
    project: str = "",  # GCP Project
    location: str = "",  # GCP Region
    staging_bucket: str = "",  # Trainer Code Folder
):
    print("Model Training Job")

    import vertexai
    import time
    import google.cloud.aiplatform as aip
    from vertexai.preview.tuning import sft

    # Initialize Vertex AI SDK for Python
    aip.init(project=project, location=location, staging_bucket=staging_bucket)

    vertexai.init(project=project, location=location)

    GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002"
    GCP_BUCKET_NAME = "preppal-data"
    TRAIN_DATASET = f"gs://{GCP_BUCKET_NAME}/ml-workflow/ready_for_training/train.jsonl"
    VALIDATION_DATASET = f"gs://{GCP_BUCKET_NAME}/ml-workflow/ready_for_training/test.jsonl"

    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        validation_dataset=VALIDATION_DATASET,
        epochs=3,
        adapter_size=4,
        learning_rate_multiplier=1.0,
    )

    time.sleep(60)
    sft_tuning_job.refresh()

    print("Check status of tuning job:")
    print(sft_tuning_job)
    while not sft_tuning_job.has_ended:
        time.sleep(60)
        sft_tuning_job.refresh()
        print("Job in progress...")

    print(f"Tuned model name: {sft_tuning_job.tuned_model_name}")
    print(f"Tuned model endpoint name: {sft_tuning_job.tuned_model_endpoint_name}")
    print(f"Experiment: {sft_tuning_job.experiment}")

    print("Training Job Complete")


# Define a Container Component
@dsl.component(base_image="python:3.9", packages_to_install=["google-cloud-aiplatform"])
def model_deploy(
    bucket_name: str = "",
):
    print("Model Training Job")

    import google.cloud.aiplatform as aip

    # List of prebuilt containers for prediction
    # https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
    serving_container_image_uri = "us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest"

    display_name = "PrepPal Model"
    ARTIFACT_URI = f"gs://{bucket_name}/ml-workflow/model"

    # Upload and Deploy model to Vertex AI
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_upload
    deployed_model = aip.Model.upload(
        display_name=display_name,
        artifact_uri=ARTIFACT_URI,
        serving_container_image_uri=serving_container_image_uri,
    )
    print("Deployed Model:", deployed_model)
    # Reference: https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_deploy
    endpoint = deployed_model.deploy(
        deployed_model_display_name=display_name,
        traffic_split={"0": 100},
        machine_type="n1-standard-4",
        accelerator_count=0,
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )
    print("endpoint:", endpoint)
