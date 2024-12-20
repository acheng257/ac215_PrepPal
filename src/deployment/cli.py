"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
from model import model_training as model_training_job, model_deploy as model_deploy_job


GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}/ml-workflow"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
GCP_REGION = os.environ["GCP_REGION"]

# Read the docker tag file
with open(".docker-tag-ml") as f:
    tag = f.read()

tag = tag.strip()

# DATA_COLLECTOR_IMAGE = "gcr.io/ac215-project/cheese-app-data-collector"
DATA_PROCESSOR_IMAGE = f"gcr.io/{GCP_PROJECT}/preppal-data-processor:{tag}"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def data_processor():
    print("data_processor()")

    # Define a Container Component for data processor
    @dsl.container_component
    def data_processor():
        container_spec = dsl.ContainerSpec(
            image=DATA_PROCESSOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--generate",
                "--prepare",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def data_processor_pipeline():
        data_processor()

    # Build yaml file for pipeline
    compiler.Compiler().compile(data_processor_pipeline, package_path="data_processor.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "preppal-data-processor-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="data_processor.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def model_training():
    print("model_training()")

    # Define a Pipeline
    @dsl.pipeline
    def model_training_pipeline():
        model_training_job(
            project=GCP_PROJECT,
            location=GCP_REGION,
            staging_bucket=f"gs://preppal-data/{GCS_PACKAGE_URI}",
        )

    # Build yaml file for pipeline
    compiler.Compiler().compile(model_training_pipeline, package_path="model_training.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "preppal-model-training-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="model_training.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def model_deploy():
    print("model_deploy()")

    # Define a Pipeline
    @dsl.pipeline
    def model_deploy_pipeline():
        model_deploy_job(
            bucket_name=GCS_BUCKET_NAME,
        )

    # Build yaml file for pipeline
    compiler.Compiler().compile(model_deploy_pipeline, package_path="model_deploy.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "preppal-model-deploy-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="model_deploy.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def pipeline():
    print("pipeline()")

    # Define a Container Component for data processor
    @dsl.container_component
    def data_processor():
        container_spec = dsl.ContainerSpec(
            image=DATA_PROCESSOR_IMAGE,
            command=[],
            args=[
                "cli.py",
                "--generate",
                "--prepare",
            ],
        )
        return container_spec

    # Define a Pipeline
    @dsl.pipeline
    def ml_pipeline():
        # Data Processor
        data_processor_task = data_processor().set_display_name("Data Processor")
        # Model Training       ## EDIT!!!
        model_training_task = (
            model_training_job(
                project=GCP_PROJECT,
                location=GCP_REGION,
                staging_bucket=f"gs://preppal-data/{GCS_PACKAGE_URI}",
            )
            .set_display_name("Model Training and Deployment")
            .after(data_processor_task)
        )

        print("Output Test:", model_training_task)  # Prevent Flake8 rror...

    # Build yaml file for pipeline
    compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "preppal-pipeline-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="pipeline.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def sample_pipeline():
    print("sample_pipeline()")

    # Define Component
    @dsl.component
    def square(x: float) -> float:
        return x**2

    # Define Component
    @dsl.component
    def add(x: float, y: float) -> float:
        return x + y

    # Define Component
    @dsl.component
    def square_root(x: float) -> float:
        return x**0.5

    # Define a Pipeline
    @dsl.pipeline
    def sample_pipeline(a: float = 3.0, b: float = 4.0) -> float:
        a_sq_task = square(x=a)
        b_sq_task = square(x=b)
        sum_task = add(x=a_sq_task.output, y=b_sq_task.output)
        return square_root(x=sum_task.output).output

    # Build yaml file for pipeline
    compiler.Compiler().compile(sample_pipeline, package_path="sample-pipeline1.yaml")

    # Submit job to Vertex AI
    aip.init(project=GCP_PROJECT, location=GCP_REGION, staging_bucket=BUCKET_URI)

    job_id = generate_uuid()
    DISPLAY_NAME = "sample-pipeline-" + job_id
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="sample-pipeline1.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run(service_account=GCS_SERVICE_ACCOUNT)


def main(args=None):
    print("CLI Arguments:", args)

    if args.data_processor:
        print("Data Processor")
        data_processor()

    if args.model_training:
        print("Model Training and Deployment")
        model_training()

    if args.pipeline:
        pipeline()

    if args.sample:
        print("Sample Pipeline")
        sample_pipeline()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "--data_processor",
        action="store_true",
        help="Run just the Data Processor",
    )
    parser.add_argument(
        "--model_training",
        action="store_true",
        help="Run just Model Training",
    )
    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="PrepPal Pipeline",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Sample Pipeline 1",
    )

    args = parser.parse_args()

    main(args)
