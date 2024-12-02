# Deployment & Scaling

## App Deployment to GCP - Ansible
Follow the steps below to deploy the PrepPal App to GCP. Using Ansible playbooks, we automate building and pushing our Docker containers to GCR (Google Container Registry), creating a Compute Instance (VM) Server in GCP, provisioning the VM, setting up the docker containers in the VM, and a webserver.

### API's to enable in GCP
Search for each of these in the GCP search bar and click enable to enable these API's:

- Vertex AI API
- Compute Engine API
- Service Usage API
- Cloud Resource Manager API
- Google Container Registry API
- Kubernetes Engine API

### Setup GCP Service Accounts for deployment


## App Deployment to GCP - Ansible + Kubernetes
