from llama_cpp import Llama

PROMPTS = [
  {'role': 'user', 'content': 'あなたの名前はイライザです'},
  {'role': 'user', 'content': 'あなたの名前は何ですか'},
]

# モデルのパスを指定
# model_path = './models/Llama-3-ELYZA-JP-8B.i1-IQ1_S.gguf'
# model_path = './models/Llama-3-ELYZA-JP-8B.i1-Q3_K_L.gguf'
model_path = './models/Llama-3-ELYZA-JP-8B-q4_k_m.gguf'

promptStr: str = ''

for p in PROMPTS:
  promptStr += f'{p["role"]}: {p["content"]}\n'

promptStr += 'assistant:'

# モデルを読み込む
llm = Llama(
  model_path = model_path,
  n_ctx = 2048,
  n_gpu_layers = 32 # for gpu
  # n_gpu_layers = 0 # for cpu
)

# 推論を実行
# response = llm(prompt = 'BMW M6グランクーペについて教えて', max_tokens=1200)
response = llm(prompt = promptStr, max_tokens=1200)

# 結果を表示
print(response['choices'][0]['text'])