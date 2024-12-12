## AC215 PrepPal - Milestone 4

#### Project Milestone 4 Organization

```
├── .github
│   ├──workflows
│   │   ├── CI-push.yml
│   └── └── pre-commit.yml
├── README.md
├── data # DO NOT UPLOAD DATA TO GITHUB, only .gitkeep to keep the directory or a really small sample
├── midterm_presentation
│   └── PrepPalMidterm.pdf
├── assets
│   ├── PrepPal.png
│   ├── VM.png
│   ├── API.png
│   ├── Design
│   │   ├── SolutionArchitecture1.jpg
│   │   ├── SolutionArchitecture2.jpg
│   │   └── TechnicalArchitecture.jpg
│   ├── Frontend
│   │   ├── home.png
│   │   ├── login.png
│   │   ├── pantry.png
│   └── └── recs.png
├── notebooks
│   └── data_cleaning.ipynb
├── references
│   ├── Doub_et_al.pdf
│   └── Lebersorger_Schneider.pdf
├── reports
│   ├── PrepPal_Statement_of_Work.pdf
│   ├── dataversioning.md
│   ├── git_log.png
│   ├── milestone2.md
│   ├── milestone3.md
│   ├── model_evaluation_before_and_after_rag_and_finetuning.pdf
│   ├── finetuning_images
│   │   ├── data_distribution_1.png
│   │   ├── data_distribution_2.png
│   └── └── training_validation_metric_preppal_v1.png
├── src
│   ├── apiservice
│   │   ├── api
│   │   │   ├── routers
│   │   │   │   └── ...
│   │   │   ├── utils
│   │   │   │   └── ...
│   │   │   ├── __init__.py
│   │   │   ├── service_old.py
│   │   │   └── service.py
│   │   ├── tests
│   │   │   └── ...
│   │   ├── .gitignore
│   │   ├── docker-entrypoint.sh
│   │   ├── docker-shell.sh
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── README.md
│   │   └── testing.md
│   ├── dataversioning
│   │   ├── .gitignore
│   │   ├── check_connection.py
│   │   ├── docker_entrypoint.sh
│   │   ├── docker-shell.sh
│   │   ├── Dockerfile
│   │   ├── dvc_store.dvc
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── check_connection.py
│   │   └── README.md
│   ├── frontend-react
│   │   ├── public
│   │   │   └── ...
│   │   ├── src
│   │   │   ├── app
│   │   │   │   └── ...
│   │   │   ├── components
│   │   │   │   └── ...
│   │   │   │   services
│   │   │   └── └── ...
│   │   ├── tests
│   │   │   └── ...
│   │   ├── .env.development
│   │   ├── .env.production
│   │   ├── .gitignore
│   │   ├── docker-shell.sh
│   │   ├── Dockerfile
│   │   ├── Dockerfile.dev
│   │   ├── jsconfig.json
│   │   ├── next.config.js
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── postcss.config.js
│   │   ├── tailwind.config.js
│   │   ├── README.md
│   │   └── testing.md
│   ├── llm-rag
│   │   ├── .gitignore
│   │   ├── cli.py
│   │   ├── docker-compose.yml
│   │   ├── docker-entrypoint.sh
│   │   ├── docker-shell.sh
│   │   ├── Dockerfile
│   │   ├── Pipfile
│   │   ├── Pipfile.lock
│   │   ├── preprocess_rag.py
│   │   ├── preprocess_recipes.py
│   |   ├── model_rag.py
│   │   └── README.md
│   ├── llm-finetuning
│   │   ├── dataset_creator
│   │   │   ├── create_fine_tuning_data.py
│   │   │   ├── docker-entrypoint.sh
│   │   │   ├── docker-shell.sh
│   │   │   ├── Dockerfile
│   │   │   ├── Pipfile
│   │   │   └── Pipfile.lock
│   ├── ├── gemini_finetuner
│   │   │   ├── cli.py
│   │   │   ├── docker-entrypoint.sh
│   │   │   ├── docker-shell.sh
│   │   │   ├── Dockerfile
│   │   │   ├── Pipfile
│   │   └── └── Pipfile.lock
│   ├── postgres-db
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── schema.sql
│   └── └── setup.sh
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
└── pytest.ini
```

# AC215 - Milestone4 - PrepPal

**Team Members:** <br>
Ioana-Andreea Cristescu, Jonas Raedler, Rosetta Hu, Alice Cheng

**Group Name** <br>
PrepPal

**Project:** <br>
In this project, we aim to develop an AI-powered meal-planning application that streamlines recipe discovery and ingredient management. Powered by a Retrieval-Augmented Generation (RAG) model, the app suggests personalized recipes from a database of 300,000 meals, using available pantry ingredients and user preferences. Users can easily manage their pantry and saved recipes, with the app dynamically adjusting recommendations based on updates. A fine-tuned model enhances the user experience by prioritizing recipes that align with personal tastes and pantry stock, helping reduce food waste and simplify meal preparation.

### Milestone4 ###

In this milestone, we have the components for frontend and API service, as well as the components from previous milestones for data management, including versioning and the implemetation of RAG and fine-tuned LLM model.

After building a robust ML Pipeline in our previous milestone, we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

**Application Design**

Before we started implementing the app, we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="../assets/Design/SolutionArchitecture1.jpg"  width="800">

<img src="../assets/Design/SolutionArchitecture2.jpg"  width="800">

Here is our Technical Architecture:

<img src="../assets/Design/TechnicalArchitecture.jpg"  width="800">


**Backend API**

We built a backend api service using fastAPI to expose model functionality to the frontend.

<img src="../assets/API.png"  width="800">

**Frontend**

A user friendly React app was built to provide a virtual pantry management system and a recipe recommendation system for users. Users can upload ingredients via text input and query our service for
recipe recommendations, and then interact with a chatbot for further customizations and questions.

Here are some screenshots of our app:

<img src="../assets/Frontend/home.png"  width="800">
<img src="../assets/Frontend/login.png"  width="800">
<img src="../assets/Frontend/pantry.png"  width="800">
<img src="../assets/Frontend/recs.png"  width="800">


### Instructions to run our application

**GCP Setup:** <br>

1. Virtual Machine
   - Create a VM Instance from [GCP](https://console.cloud.google.com/compute/instances)
     - Region: us-east4-a (can choose any region that supports the type of machine chosen)
     - Machine Configuration:
       - GPU type: NVIDIA T4
       - Machine Type: g2-standard-4
       - Memory: 200 GB (at least)
     - You can choose a lower tier GPU that runs with 4-8 vCPUs. We had to upgrade to NVIDIA L4 due to unavailability of other GPUs.
   - SSH into your newly created instance
   - Install Docker on the newly created instance by running: `sudo apt install docker.io`
   - Install docker-compose:
     - `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
     - `chmod +x /usr/local/bin/docker-compose`
     - To test your installation of Compose, run the following command: `docker-compose --version`
   - Install Git: sudo apt install git
   - Clone App Repo: git clone https://github.com/acheng257/ac215_PrepPal.git

![Virtual Machine](./assets/VM.png)

2. GCP Bucket
   - Navigate to Storage > [Buckets](https://console.cloud.google.com/storage/browser) and click create bucket
     - Name: any unique bucket name
     - Region: us-east1
   - Create a folder `dvc_store` inside the bucket for data versioning using dvc
   - Create other folders inside the bucket to store data
3. GCP Bucket Service Account
   - Navigate to IAM & Admin > [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
   - Click + Create Service Account
   - Name the service account and click Create and Continue.
   - Assign a role with the premission to access the GCS Bucket above:
     - Storage Admin (full access to the bucket)
   - Click on the service account and navigate to the tab "KEYS"
   - Click in the button "ADD Key (Create New Key)" and Select "JSON". This will download a private key JSON file.
   - Create a local **secrets** folder
     ```
          |-ac215_Preppal
          |-secrets
     ```
   - Copy the above key JSON file into the secrets folder and rename it to `data-service-account.json`
4. Vertex AI API Service Account
   - Navigate to IAM & Admin > [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
   - Click + Create Service Account
   - Name the service account and click Create and Continue.
   - Assign a role with the premission to access the GCS Bucket above:
     - Storage Admin
     - Vertex AI User
   - Click on the service account and navigate to the tab "KEYS"
   - Click in the button "ADD Key (Create New Key)" and Select "JSON". This will download a private key JSON file.
   - Copy the above key JSON file into the secrets folder created in the previous step and rename it to `preppal-llm-service-account.json`

**Containerized Components:** <br>

1. [Data Versioning Container](./src/dataversioning/README.md)
   - The DVC container sets up version control using open-source DVC (Data Version Control) to efficiently manage data versions. The pipeline connects to Google Cloud Storage (GCS) and mounts a GCS bucket to a local directory. Additionally, it binds this mounted directory to another path to serve as the storage location for DVC-managed data. This setup allows us to seamlessly track, version, and manage large datasets that are stored in the cloud.
2. [LLM RAG System Containers](./src/llm-rag/README.md)
   - The RAG Data Pipeline includes two integrated containers: one for the data pipeline and another for ChromaDB. The data pipeline container manages tasks such as cleaning, chunking, embedding, and integrating data into the vector database, while the ChromaDB container hosts the vector database. RAG allows efficient retrieval of relevant information from the knowledge base, with the capability to dynamically process and add user-uploaded data without altering the pre-existing knowledge base. This ensures flexibility while maintaining the integrity of the original data.
3. [LLM Fine-Tuning Containers](./src/llm-finetuning/README.md)
   - The LLM Fine-Tuning folder includes two containers: one for the generation, preparation, and upload of the fine-tuning dataset, the other for the actual fine-tuning of the Gemini model. The Gemini model is fine-tuned to rank provided recipes based on available ingredients in a pantry. The process begins with generating a fine-tuning dataset using a large recipe collection from the All-Recipes Dataset, then cleaning and preparing it for use. The generated dataset is then uploaded to a GCP bucket, so that it is available for the actual fine-tuning process. Once fine-tuned, the model is able to answer questions by ranking recipes and identifying missing ingredients, providing a structured output for easy further computations. The folder includes scripts for generating, preparing, and uploading data, as well as running the fine-tuning and testing the model interactively.
4. [Frontend Container](./src/frontend-react/README.md)
   - The front-end is currently hosted on [localhost:3000](http://localhost:3000) and is built using the React framework.
5. [API Container](./src/apiservice/README.md)
   - The backend API is implemented via fastAPI and hosted on [localhost:9000](http://localhost:9000).

**Notebooks/Reports:** <br>
These folders contains code that is not part of any container - for e.g: Application mockup, EDA, crucial insights, reports or visualizations.


### Testing

Refer to the following two files ([here](./src/frontend-react/testing.md) and [here](./src/apiservice/testing.md)) for instructions on how to run our tests locally.
