import functions_framework
from datetime import datetime
from google.cloud import vision, firestore

# Initialize clients
vision_client = vision.ImageAnnotatorClient()
db = firestore.Client()

# Register a CloudEvent function to be triggered by Cloud Storage.
@functions_framework.cloud_event
def process_image(cloud_event):
    data = cloud_event.data

    bucket_name = data['bucket']
    file_name = data['name']
    
    print(f"Processing file: {file_name} from bucket: {bucket_name}.")
    
    image_uri = f'gs://{bucket_name}/{file_name}'
    image = vision.Image()
    image.source.image_uri = image_uri
    
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f'Vision API Error: {response.error.message}')

    label_descriptions = [label.description for label in labels]

    data_to_save = {
        'gcs_uri': image_uri,
        'labels': label_descriptions,
        'created_at': datetime.utcnow(),
        'file_name': file_name
    }

    doc_ref = db.collection('images').document(file_name)
    doc_ref.set(data_to_save)
    
    print(f"Analysis results for {file_name} saved to Firestore.")
