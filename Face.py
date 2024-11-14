import torch
import cv2
import argparse
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import insightface
import numpy as np
from insightface.app import FaceAnalysis
import json



# Initialize InsightFace
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def get_face_embedding_insightface(image_path):
    try:
        img = cv2.imread(image_path)
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return []
    if img is None:
        print(f"Error reading image {image_path}")
        return []
    faces = app.get(img)
    embeddings = []
    for face in faces:
        embeddings.append(face.embedding)
    return embeddings



# Function to save embeddings dictionary to storage
def save_embeddings_to_storage(embeddings_dict, storage_path="embeddings_storage.json"):
    with open(storage_path, "w") as f:
        json.dump(embeddings_dict, f)

# Function to create embeddings from the provided folder of images
def create_full_data_embeddings(sample_images_folder, storage_path="embeddings_storage.json"):
    embeddings_dict = {}
    similarity_threshold = 0.4
    # Iterate over the image files in the folder
    for file_name in os.listdir(sample_images_folder):
        if file_name.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(sample_images_folder, file_name)
            
            # Extract face embeddings for each image
            embeddings_full = get_face_embedding_insightface(image_path)
            print("No. of Faces:", len(embeddings_full))
            
            if not embeddings_full:
                print(f"No faces found in {file_name}")
                continue

            # Compare each embedding with existing embeddings in the dictionary
            for embedding in embeddings_full:
                found = False
                for key in embeddings_dict:
                    key_array = np.frombuffer(key, dtype=np.float32)
                    similarity = cosine_similarity([embedding], [key_array])[0][0]
                    if similarity > similarity_threshold:
                        embeddings_dict[key].append(image_path)
                        found = True
                        break
                if not found:
                    embeddings_dict[embedding.tobytes()] = [image_path]

    # Save the embeddings dictionary to storage (e.g., local file or cloud storage)
    save_embeddings_to_storage(embeddings_dict, storage_path)

    # Return a success message with the number of embeddings saved
    return json.dumps({"message": f"Embeddings saved successfully.", "embeddings_count": len(embeddings_dict)}), 200





# Function to load embeddings from storage (e.g., a JSON file)
def load_embeddings_from_storage(storage_path="embeddings_storage.json"):
    with open(storage_path, "r") as f:
        embeddings_dict = json.load(f)
    return embeddings_dict

# Function to return image paths/URLs based on the reference image embedding
def get_images(reference_image_path, storage_path="embeddings_storage.json"):
    # Load embeddings from storage
    similarity_threshold = 0.4
    embeddings_dict = load_embeddings_from_storage(storage_path)

    # Extract the face embeddings from the reference image
    reference_embeddings = get_face_embedding_insightface(reference_image_path)
    
    if not reference_embeddings:
        return json.dumps({"error": "No faces found in reference image"}), 400

    # We assume we're using the first face embedding in the reference image
    reference_embedding = reference_embeddings[0]
    output_images = []

    # Compare reference embedding with stored embeddings
    for key in embeddings_dict:
        key_array = np.frombuffer(bytes.fromhex(key), dtype=np.float32)
        similarity = cosine_similarity([reference_embedding], [key_array])[0][0]
        
        if similarity > similarity_threshold:
            output_images.extend(embeddings_dict[key])

    # Return the result as a JSON array of image paths/URLs
    if output_images:
        return json.dumps({"matched_images": output_images}), 200
    else:
        return json.dumps({"message": "No similar images found"}), 404

storage_path = "embeddings_storage.json"
sample_images_folder = 'test_images'
result, status_code = create_full_data_embeddings(sample_images_folder)