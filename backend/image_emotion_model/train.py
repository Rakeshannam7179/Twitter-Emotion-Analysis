import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import EmotionModel
import os

# Config
NUM_CLASSES = 7 # FER2013 has 7 classes
BATCH_SIZE = 32
LEARNING_RATE = 0.0001
EPOCHS = 10

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Dataset paths
    train_path = os.path.join("image_emotion_model", "DATASET", "archive", "train")
    test_path = os.path.join("image_emotion_model", "DATASET", "archive", "test")

    if not os.path.exists(train_path):
        print(f"Error: Dataset not found at {train_path}. Please download FER2013 and place it in the dataset folder.")
        return

    train_dataset = datasets.ImageFolder(root=train_path, transform=transform)
    test_dataset = datasets.ImageFolder(root=test_path, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

    model = EmotionModel(num_classes=NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    print("Beginning training...")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            if (i + 1) % 100 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}], Batch [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}")
        
        print(f"Epoch: {epoch+1}/{EPOCHS}, Loss: {total_loss/len(train_loader):.4f}")

    # Evaluation
    correct = 0
    total = 0
    model.eval()
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Accuracy: {accuracy:.2f}%")

    # Save
    torch.save(model.state_dict(), "image_emotion_model.pth")
    print("Model saved to image_emotion_model.pth")

if __name__ == "__main__":
    main()
