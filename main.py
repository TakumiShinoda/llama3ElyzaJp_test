from flask import *
from typing import *

from mods.llmModels.llmModel import *
from mods.llmModels.llama3ElyzaJp8b import *
from mods.llmModels.llama3ElyzaJpGguf import *
from mods.contextController.contextController import *

FLASK_IS_DEBUG_MODE: bool = False

MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q1_S: str = './models/Llama-3-ELYZA-JP-8B.i1-IQ1_S.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q3_L: str = './models/Llama-3-ELYZA-JP-8B.i1-Q3_K_L.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q4_M: str = './models/Llama-3-ELYZA-JP-8B-q4_k_m.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6: str = './models/Llama-3-ELYZA-JP-8B.i1-Q6_K.gguf'

app: Flask = Flask(__name__)
llmModel: Union[LlmModel, None] = None
llmContextController: ContextController

@app.route('/')
def routeMain():
  return render_template('index.html')

@app.route('/talk')
def routeTalk():
  queryInputText: str = request.args.get('inputText', '')
  llmResponse: str

  if(llmModel is None):
    return Response('Model is not loaded.', status = 500)

  if(queryInputText == ''):
    return Response('Bad request.', status = 400)
  
  llmContextController.addContext(LlmChatItem(LlmChatItemRoles.user, queryInputText))
  llmResponse = llmModel.talk(llmContextController.getContexts())
  llmContextController.addContext(LlmChatItem(LlmChatItemRoles.system, llmResponse))
  print([c.toDict() for c in llmContextController.getContexts()])

  llmContextController.saveContexts()

  return llmResponse

if __name__ == '__main__':
  if(not FLASK_IS_DEBUG_MODE):
    # llmModel = Llama3ElyzaJp8b()
    # llmContextController: ContextController = ContextController('elyza8b', False)

    llmModel = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6, True)
    llmContextController: ContextController = ContextController('elyza8bQuant', False)

  app.run(debug = FLASK_IS_DEBUG_MODE)