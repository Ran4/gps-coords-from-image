import glob
import sys

import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from metadata import metadata_lookup_map, metadata_description

model = models.resnet50(pretrained=True)

# We remove the classification layer
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# Transform to prepare images for ResNet (ResNet's expected input size is 224x224)
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def extract_features_from_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        features = model(image).squeeze().numpy()
    return features


database_image_paths = glob.glob("images/*")
database_features = np.array(
    [extract_features_from_image(path) for path in database_image_paths]
)


def find_closest_image(new_image_path):
    new_image_features = extract_features_from_image(new_image_path).reshape(
        1, -1
    )  # Reshape for compatibility
    similarities = cosine_similarity(new_image_features, database_features)
    closest_index = np.argmax(similarities)  # Index of the closest image
    closest_image_path = database_image_paths[closest_index]
    return closest_image_path, similarities[0, closest_index]


new_image_path = sys.argv[1] if len(sys.argv) >= 2 else "liberty2.jpg"
closest_image_path, similarity_score = find_closest_image(new_image_path)
metadata_about_image = metadata_lookup_map.get(closest_image_path, None)

print(f"Closest image is: {closest_image_path}")
print(f"Metadata: {metadata_about_image} ({metadata_description})")
print(f"similarity score: {similarity_score}")
