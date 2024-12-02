import torch.nn as nn

class SMSClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super(SMSClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        pooled = embedded.mean(dim=1)
        return self.fc(pooled)
