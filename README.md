## AC215 PrepPal - Milestone 2

#### Project Milestone 2 Organization

```
├── README.md
├── data # DO NOT UPLOAD DATA TO GITHUB, only .gitkeep to keep the directory or a really small sample
├── notebooks
│   └── data_cleaning.ipynb
├── references
│   └── Doub_et_al.pdf
│   └── Lebersorger_Schneider.pdf
├── reports
│   └── PrepPal_Statement_of_Work.pdf
└── src
    ├── dataversioning
    │   ├── docker_entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── Dockerfile
    │   ├── dvc_store.dvc
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── test_connection.py
    ├── datapipeline
    │   ├── cli.py
    │   ├── docker-compose.yml
    │   ├── docker-entrypoint.sh
    │   ├── docker-shell.sh
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── preprocess_rag.py
    │   ├── preprocess_recipes.py
    │   ├── semantic_splitter.py
    │   ├── README.md
    └── models
        ├── Dockerfile
        ├── docker-shell.sh
        ├── infer_model.py
        ├── model_rag.py
        └── train_model.py
```

# AC215 - Milestone2 - PrepPal

**Team Members:** <br>
Ioana-Andreea Cristescu, Jonas Raedler, Rosetta Hu, Alice Cheng

**Group Name** <br>
PrepPal

**Project:** <br>
In this project, we aim to develop an AI-powered meal-planning application that streamlines recipe discovery and ingredient management. Powered by a Retrieval-Augmented Generation (RAG) model, the app suggests personalized recipes from a database of 300,000 meals, using available pantry ingredients and user preferences. Users can easily manage their pantry and saved recipes, with the app dynamically adjusting recommendations based on updates. A fine-tuned model enhances the user experience by prioritizing recipes that align with personal tastes and pantry stock, helping reduce food waste and simplify meal preparation.

### Milestone2

In this milestone, we have the components for data management, including versioning, data cleaning and creation, as well as the containerized RAG pipeline and fine-tuned language models. We also created VM instances to utilize GPUs on the Google Cloud Platform (GCP) for fine-tuning our models.

### Instructions tu run our application 

**GCP Setup:** <br>
1. Virtual Machine (explain how to set it up + add image)
2. GCP Bucket 

**Containerized Components:** <br>
1. Data Versioning Container
2. Data Pipeline Containers
3. Model Container 

<!-- **Models container**

- This container has scripts for model training, rag pipeline and inference
- Instructions for running the model container - `Instructions here` -->

**Notebooks/Reports:** <br>
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.

### Application Mock-up
Add image 
