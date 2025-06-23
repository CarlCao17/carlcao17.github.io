
import torch
import torch.nn as nn
import torch.nn.functional as F

def Position_Embedding(inputs, position_size):
    """
    inputs: Tensor(batch_size, seq_len, word_size)
    return: Tensor(batch_size, seq_len, position_size)
    """
    batch_size, seq_len = inputs.shape(0), inputs.shape(1)


def Mask(inputs, seq_len, mode='mul'):
    if seq_len is None:
        return inputs
    mask = 


class SelfAttention(nn.Module):
    def __init__(self, feature_size, n_head):
        super().__init__()
        self.n_head = n_head
        self.keys = nn.Linear(feature_size, feature_size)
        self.querys = nn.Linear(feature_size, feature_size)
        self.values = nn.Linear(feature_size, feature_size)
        self.

    def scaled_dot_product_attention(self, q, k, v, mask=True):
        """
        q: (batch_size, n, d_k), 
        k: (batch_size, m, d_k)
        v: (batch_size, m, d_v)
        batch_size=n_head, n=seq_size, d_k=word_size, d_v
        """
        d_k = k.shape(2)
        scores = torch.matmul(q, k.transpose(1, 2)) / d_k**(.5)
        if mask:
            scores = self.mask(scores)
        scores = torch.softmax(scores)
        return torch.matmul(scores, v)
    
    def multi_head_attention(self, inputs):
        """
        inputs: (batch_size, n, n_embedding)
        """
        inputs = torch.stack([inputs for _ in range(self.n_head)])
        q = self.querys(inputs)
        k = self.keys(inputs)
        v = self.values(inputs)
        a = self.scaled_dot_product_attention(q, k, v)

        