import torch

class ScaledDotProductAttention(torch.nn.Module):
    def __init__(self, hidden_dim):
        super(ScaledDotProductAttention, self).__init__()
        self.scale = torch.sqrt(torch.tensor(hidden_dim, dtype=torch.float32))
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, lstm_output):
        attn_scores = torch.bmm(lstm_output, lstm_output.transpose(1, 2)) / self.scale
        attn_weights = self.softmax(attn_scores[:, :, -1])
        context = torch.sum(attn_weights.unsqueeze(2) * lstm_output, dim=1)
        return context, attn_weights


class BiLSTM_Attention(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=3, num_classes=1, dropout_rate=0.3):
        super(BiLSTM_Attention, self).__init__()
        self.lstm = torch.nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=True, dropout=dropout_rate)
        self.layer_norm = torch.nn.LayerNorm(hidden_dim * 2)
        self.attention = ScaledDotProductAttention(hidden_dim * 2)
        self.fc1 = torch.nn.Linear(hidden_dim * 2, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, num_classes)
        self.leaky_relu = torch.nn.LeakyReLU(0.1)
        self.dropout = torch.nn.Dropout(dropout_rate)

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

# Load Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BiLSTM_Attention(input_dim=40).to(device)
model.load_state_dict(torch.load("best_model_cpu.pth", map_location=device))
model.eval()
