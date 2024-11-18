from google.cloud import storage


def check_gcs_connection():
    try:
        client = storage.Client()
        project = client.project
        print(f"Connected to GCS project: {project}")

        return client

    except Exception as e:
        print(f"Failed to connect to GCS: {e}")
        return None


def list_gcs_buckets(client):
    try:
        buckets = client.list_buckets()

        print("Buckets in your GCS project:")
        for bucket in buckets:
            print(bucket.name)
    except Exception as e:
        print(f"Failed to list GCS buckets: {e}")


if __name__ == "__main__":
    client = check_gcs_connection()

    if client:
        print("GCS connection successful!")
        list_gcs_buckets(client)
    else:
        print("Failed to connect to GCS. Cannot retrieve storage information.")
