import torch
import torch.nn as nn

class SimpleLinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Single linear layer that preserves input (identity)
        self.linear = nn.Linear(1, 1, bias=False)
        # Initialize weights to 1.0 to preserve input
        with torch.no_grad():
            self.linear.weight.fill_(1.0)
    
    def forward(self, x):
        # Convert scalar to tensor
        x_tensor = torch.tensor([[x]], dtype=torch.float32)
        # Pass through linear layer
        output = self.linear(x_tensor)
        # Return as scalar
        return output.item()

# Create model instance
model = SimpleLinearModel()

def score(x: float) -> float:
    # Use the model to compute score
    return model.forward(x)