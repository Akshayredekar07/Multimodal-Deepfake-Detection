import torch
import torch.nn as nn

# Improved Attention Mechanism - Scaled Dot-Product Attention
class ScaledDotProductAttention(nn.Module):
    def __init__(self, hidden_dim):
        super(ScaledDotProductAttention, self).__init__()
        self.scale = torch.sqrt(torch.tensor(hidden_dim, dtype=torch.float32))
        self.softmax = nn.Softmax(dim=1)

    def forward(self, lstm_output):
        attn_scores = torch.bmm(lstm_output, lstm_output.transpose(1, 2)) / self.scale  # Scaled dot product
        attn_weights = self.softmax(attn_scores[:, :, -1])  # Take last step attention
        context = torch.sum(attn_weights.unsqueeze(2) * lstm_output, dim=1)  # Weighted sum
        return context, attn_weights

# Improved BiLSTM-Attention Model
class BiLSTM_Attention(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=3, num_classes=1, dropout_rate=0.3):
        super(BiLSTM_Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # BiLSTM Layer with Layer Normalization
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers,
                            batch_first=True, bidirectional=True, dropout=dropout_rate)
        self.layer_norm = nn.LayerNorm(hidden_dim * 2)  # Normalize output

        # Scaled Dot-Product Attention
        self.attention = ScaledDotProductAttention(hidden_dim * 2)

        # Fully Connected Layers with Xavier Initialization
        self.fc1 = nn.Linear(hidden_dim * 2, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes)

        # Activation & Regularization
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # (batch, seq_len, hidden_dim*2)
        lstm_out = self.layer_norm(lstm_out)  # Apply Layer Norm

        attn_out, attn_weights = self.attention(lstm_out)  # Apply Attention

        x = self.leaky_relu(self.fc1(attn_out))
        x = self.dropout(x)
        x = self.leaky_relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)  # No sigmoid here (for BCEWithLogitsLoss)

        return x  # Logits output (apply sigmoid during loss calculation)
    
# Function to Load the Pretrained Model
def load_model(model_path, input_dim, device):
    model = BiLSTM_Attention(input_dim=input_dim)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()  # Set model to evaluation mode
    return model
