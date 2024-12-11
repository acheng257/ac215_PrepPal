import argparse
import time
import random
import string
import vertexai
from vertexai.preview.tuning import sft


GCP_PROJECT = "preppal-438123"
GCP_BUCKET_NAME = "preppal-data"
GCP_LOCATION = "us-east1"

GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002"
TRAIN_DATASET = f"gs://{GCP_BUCKET_NAME}/ml-workflow/ready_for_training/train.jsonl"
VALIDATION_DATASET = f"gs://{GCP_BUCKET_NAME}/ml-workflow/ready_for_training/test.jsonl"


# ---------------------------- Functions and Parsers -----------------------------------------
def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Setup the arguments for the trainer task
parser = argparse.ArgumentParser()

parser.add_argument("--epochs", dest="epochs", default=3, type=int, help="Number of epochs.")
parser.add_argument("--model_name", dest="model_name", default=f"preppal-model-{generate_uuid()}", help="Name of fine-tuned model.")
parser.add_argument(
    "--bucket_name",
    dest="bucket_name",
    default="",
    type=str,
    help="Bucket for data and models.",
)
args = parser.parse_args()


# ---------------------------- Training Process -----------------------------------------
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

print("Start Train model")

# Supervised Fine Tuning
sft_tuning_job = sft.train(
    source_model=GENERATIVE_SOURCE_MODEL,
    train_dataset=TRAIN_DATASET,
    validation_dataset=VALIDATION_DATASET,
    epochs=args.epochs,
    adapter_size=4,
    learning_rate_multiplier=1.0,
    tuned_model_display_name=args.model_name,
)
print("Training job started. Monitoring progress...\n\n")

# Wait and refresh
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

# ---------------------------- Upload Model -----------------------------------------

# aiplatform.init(project=GCP_PROJECT, location=GCP_LOCATION)

# # List all models in the Model Registry
# models = aiplatform.Model.list()

# # If there are any models, find the most recently created one
# if models:
#     # Sort models by creation time (newest first)
#     _ = datetime.datetime.now()  # Flake8 error. datetime is needed
#     models_sorted = sorted(models, key=lambda model: model.create_time, reverse=True)
#     latest_model = models_sorted[0]

#     # Print the details of the most recently added model
#     print("Most recently added model:")
#     print("Display Name:", latest_model.display_name)
#     print("Resource Name:", latest_model.resource_name)
#     print("Create Time:", latest_model.create_time)

#     # endpoint = latest_model.deploy(
#     #     deployed_model_display_name=f"deployed-{args.model_name}",
#     #     machine_type="n1-standard-4"
#     # )
#     # endpoint_ = endpoint.resource_name


# else:
#     print("No models found in the Model Registry.")
