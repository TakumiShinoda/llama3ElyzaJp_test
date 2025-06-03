from llama_cpp import Llama

PROMPTS = [
  {'role': 'user', 'content': 'あなたの名前はイライザです'},
  {'role': 'user', 'content': 'あなたの名前は何ですか'},
]

# model_path = './models/Llama-3-ELYZA-JP-8B.i1-IQ1_S.gguf'
# model_path = './models/Llama-3-ELYZA-JP-8B.i1-Q3_K_L.gguf'
model_path = './models/Llama-3-ELYZA-JP-8B-q4_k_m.gguf'

promptStr: str = ''

for p in PROMPTS:
  promptStr += f'{p["role"]}: {p["content"]}\n'

promptStr += 'assistant:'

llm = Llama(
  model_path = model_path,
  n_ctx = 2048,
  n_gpu_layers = 32 # for gpu
  # n_gpu_layers = 0 # for cpu
)

response = llm(prompt = promptStr, max_tokens=1200)

print(response['choices'][0]['text'])