from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.transforms import transforms

from model import PlantVillageDataset, SimpleCNN

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

dataset = PlantVillageDataset(root_dir='data', transform=transform)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

def train(model: SimpleCNN):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 10
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, data in enumerate(data_loader, 0):
            inputs, labels = data

            inputs = inputs.to(model.device)
            labels = labels.to(model.device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 10 == 9:    # print every 10 batches
                print(f"[{epoch + 1}, {i + 1}] loss: {running_loss / 10:.3f}")
                running_loss = 0.0

    print('Finished Training')
    return model

model = SimpleCNN(len(dataset.classes), SimpleCNN.device)
model = train(model)
