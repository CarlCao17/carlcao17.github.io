# LLM Inference 101

Two phases of LLM Inference
- prefill phase: highly-parallelized matrix-matrix operation, compute bound
  processes the entire input prompt at once to generate the first response token
- decode phase: matrix-vector operation, memory bound
  text is generated autoregressively where the next token is predicted one at time given all previous tokens

Optimizing Prefill and Decode
1. Speculative Decoding
2. Chunked Prefills and Decode-Maximal Batching

Batching

Batch size is critical for the higher throughput
And KV cache management plays a critical role in determining the maximum batch size and improving inference.

KV Cache Management

memory allocated in the GPU during serving, the model weights remain fixed and the activations only utilize 
a fraction compared to the KV cache.

Freeing up space for the KV space is critical
- reducing the model weight memory footprintf through **quantization**
  reduces inference latency by exchanging memory for accuracy
- reducing the KV cache memory footprint with modified architectures and **attention variants**
  Queries: represent the context or question
  Keys: represent the information being attended to
  Values: represent the information being retrieved

  Attention weights are computed by comparing queries with keys, and then used to weight values, producing the final ouput representation
  Query(Prompt) -> Attention Weights -> Relevant Information (Values)


- pooling memory from multiple GPUS with parallelism