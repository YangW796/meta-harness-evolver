import torch
import torch.nn as nn

class IdentityModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Simple linear layer that will act as identity
        self.layer = nn.Linear(1, 1, bias=False)
        # Initialize weight to 1.0 to preserve input
        with torch.no_grad():
            self.layer.weight.data.fill_(1.0)
    
    def forward(self, x):
        # Convert scalar to tensor
        x_tensor = torch.tensor([[x]], dtype=torch.float32)
        # Pass through layer
        output = self.layer(x_tensor)
        # Return as scalar
        return output.item()

# Create model instance
model = IdentityModel()

def score(x: float) -> float:
    # Use the model to compute score
    return model.forward(x)
