import torch.nn as nn
import torchvision.models as models

class EmotionModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Using weights instead of pretrained=True for modern torchvision API
        self.base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.base.fc = nn.Linear(
            self.base.fc.in_features,
            num_classes
        )

    def forward(self, x):
        return self.base(x)
