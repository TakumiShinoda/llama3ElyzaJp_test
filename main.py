from flask import Flask, request
from typing import *

from llmModels.llmModel import *
from llmModels.llama3ElyzaJp8b import *
from llmModels.llama3ElyzaJpGguf import *

MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q1_S = './models/Llama-3-ELYZA-JP-8B.i1-IQ1_S.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q3_L = './models/Llama-3-ELYZA-JP-8B.i1-Q3_K_L.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q4_M = './models/Llama-3-ELYZA-JP-8B-q4_k_m.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6 = './models/Llama-3-ELYZA-JP-8B.i1-Q6_K.gguf'

# llmModel: LlmModel = Llama3ElyzaJp8b()
llmModel: LlmModel = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6)
app: Flask = Flask(__name__)
llmChatHistory: List[LlmChatItem] = []

@app.route('/')
def routeMain():
  queryInputText: str = request.args.get('inputText', '')
  llmResponse: str

  if(queryInputText == ''):
    return 'Bad request.'
  
  llmChatHistory.append(LlmChatItem(LlmChatItemRoles.user, queryInputText))
  print([l.toDict() for l in llmChatHistory])
  llmResponse = llmModel.talk(llmChatHistory)
  llmChatHistory.append(LlmChatItem(LlmChatItemRoles.system, llmResponse))

  return llmResponse

if __name__ == '__main__':
  app.run(debug = False)