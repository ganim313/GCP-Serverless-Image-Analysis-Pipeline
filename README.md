# GCP-Serverless-Image-Analysis-Pipeline

A fully automated, event-driven, and serverless pipeline on Google Cloud Platform that analyzes images upon upload. When a new image is dropped into a Cloud Storage bucket, a Cloud Function is triggered, which uses the Vision AI API to detect labels and content. The structured results are then stored in a Firestore database.
