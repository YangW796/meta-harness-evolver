# Simple test to verify the model structure (without torch)
import ast
import inspect

def check_model_structure():
    with open('model.py', 'r') as f:
        content = f.read()
    
    # Check for key components
    checks = [
        ('import torch.nn', 'torch.nn import found'),
        ('class SimpleLinearModel', 'SimpleLinearModel class found'),
        ('def score(x: float) -> float', 'score function signature preserved'),
        ('nn.Linear', 'Linear layer used'),
        ('prediction.item()', 'Proper tensor to float conversion')
    ]
    
    results = []
    for check, message in checks:
        if check in content:
            results.append(f"✓ {message}")
        else:
            results.append(f"✗ {message}")
    
    return results

if __name__ == "__main__":
    print("Model structure check:")
    for result in check_model_structure():
        print(f"  {result}")
