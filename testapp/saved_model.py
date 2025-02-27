import torch
from model import BiLSTM_Attention

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = BiLSTM_Attention(input_dim=40).to(device)
model.load_state_dict(torch.load("best_model_cpu.pth", map_location=device))
model.eval()

# Convert to TorchScript
example_input = torch.randn(1, 660, 40).to(device)
traced_model = torch.jit.script(model)
traced_model.save("best_model_scripted.pt")  # Save as TorchScript
