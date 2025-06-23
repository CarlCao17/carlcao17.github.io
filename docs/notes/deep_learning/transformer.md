# Transformer

## 为什么需要 transformer
- 传统模型的局限：RNN/LSTM 难以并行计算，且对长距离依赖建模能力弱
- Transformer 的优势：完全基于注意力机制（Attention），支持并行化，擅长捕捉全局依赖关系

## 核心组件
- 自注意力机制（Self-Attention）：模型通过计算词与词之间的相关性，动态分配权重
  - 核心公式：Q 查询矩阵，K 键矩阵，V 值矩阵
    $$ Softmax(QK^{T} / \sqrt{d_{k}})V $$

- 多头注意力（Multi-Head Attention）：将注意力分成多个“头”，捕获不同子空间的语义信息
- 位置编码（Positional Encoding）：为输入序列添加位置信息（因为 Transformer 本身不包含顺序信息）
- 前馈网络（Feed-Forward Network）：对注意力后的特征进行非线性变换

## 学习 Transformer 架构

