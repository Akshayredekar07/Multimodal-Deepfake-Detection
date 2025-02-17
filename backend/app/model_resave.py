import torch
import sys
import os

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# First define the model classes
import torch.nn as nn

class ScaledDotProductAttention(nn.Module):
    def __init__(self, hidden_dim):
        super(ScaledDotProductAttention, self).__init__()
        self.scale = torch.sqrt(torch.tensor(hidden_dim, dtype=torch.float32))
        self.softmax = nn.Softmax(dim=1)

    def forward(self, lstm_output):
        attn_scores = torch.bmm(lstm_output, lstm_output.transpose(1, 2)) / self.scale
        attn_weights = self.softmax(attn_scores[:, :, -1])
        context = torch.sum(attn_weights.unsqueeze(2) * lstm_output, dim=1)
        return context, attn_weights

class BiLSTM_Attention(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=3, num_classes=1, dropout_rate=0.3):
        super(BiLSTM_Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers,
                            batch_first=True, bidirectional=True, dropout=dropout_rate)
        self.layer_norm = nn.LayerNorm(hidden_dim * 2)
        self.attention = ScaledDotProductAttention(hidden_dim * 2)
        
        self.fc1 = nn.Linear(hidden_dim * 2, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes)
        
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        lstm_out = self.layer_norm(lstm_out)
        attn_out, attn_weights = self.attention(lstm_out)
        
        x = self.leaky_relu(self.fc1(attn_out))
        x = self.dropout(x)
        x = self.leaky_relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x

# Paths
OLD_MODEL_PATH = "models/audio_models/best_model_cpu.pth"
NEW_MODEL_PATH = "models/audio_models/best_model_cpu_new.pth"

# Create model instance
model = BiLSTM_Attention(input_dim=40)

# Load and save model
try:
    model.load_state_dict(torch.load(OLD_MODEL_PATH, map_location='cpu'))
    
    # Save in new format
    torch.save({
        'model_state_dict': model.state_dict(),
        'input_dim': model.lstm.input_size,
        'hidden_dim': model.hidden_dim,
        'num_layers': model.num_layers
    }, NEW_MODEL_PATH)
    
    print("Model successfully converted and saved!")
except Exception as e:
    print(f"Error during model conversion: {str(e)}")