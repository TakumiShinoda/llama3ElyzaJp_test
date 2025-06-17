from enum import Enum
from functools import wraps
from flask import *
from typing import *

from mods.llmModels.llmModel import *
from mods.llmModels.llama3ElyzaJp8b import *
from mods.llmModels.llama3ElyzaJpGguf import *
from mods.contextController.contextController import *

class SupportLlmModels(Enum):
  llama3ElyzaJp8b = 'llama3ElyzaJp8b'
  llama3ElyzaJpGgufQ1S = 'llama3ElyzaJpGgufQ1S'
  llama3ElyzaJpGgufQ3L = 'llama3ElyzaJpGgufQ3L'
  llama3ElyzaJpGgufQ4M = 'llama3ElyzaJpGgufQ4M'
  llama3ElyzaJpGgufQ6 = 'llama3ElyzaJpGgufQ6'

FLASK_IS_DEBUG_MODE: bool = False

DEFAULT_LLM_MODEL: SupportLlmModels = SupportLlmModels.llama3ElyzaJpGgufQ6

MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q1_S: str = './models/Llama-3-ELYZA-JP-8B.i1-IQ1_S.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q3_L: str = './models/Llama-3-ELYZA-JP-8B.i1-Q3_K_L.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q4_M: str = './models/Llama-3-ELYZA-JP-8B-q4_k_m.gguf'
MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6: str = './models/Llama-3-ELYZA-JP-8B.i1-Q6_K.gguf'

app: Flask = Flask(__name__)
llmModel: Union[LlmModel, None] = None
llmContextController: ContextController
currentLlmModel: SupportLlmModels = DEFAULT_LLM_MODEL
isLockingApi: bool = False

def loadLlmModel(model: SupportLlmModels) -> LlmModel:
  result: LlmModel

  if(model == SupportLlmModels.llama3ElyzaJp8b):
    result = Llama3ElyzaJp8b()
  elif(model == SupportLlmModels.llama3ElyzaJpGgufQ1S):
    result = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q1_S, True)
  elif(model == SupportLlmModels.llama3ElyzaJpGgufQ3L):
    result = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q3_L, True)
  elif(model == SupportLlmModels.llama3ElyzaJpGgufQ4M):
    result = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q4_M, True)
  elif(model == SupportLlmModels.llama3ElyzaJpGgufQ6):
    result = Llama3ElyzaJpGguf(MODEL_PATH_LLAMA3_ELYZA_JP_8B_Q6, True)

  return result

def getModelList() -> dict:
  responseDict: dict = {
    'supportModels': [],
    'currentModel': currentLlmModel.value
  }

  for slm in SupportLlmModels:
    responseDict['supportModels'].append(slm.value)

  return responseDict

def flaskCustomRoute(flaskApp: Flask, route: str, **route_kwargs: dict[str: dict]):
  def decorator(func: Callable):
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict[str: dict]):  
      if(isLockingApi):
        return Response('Server is locking.', status = 500)
      
      return func(*args, **kwargs)
    
    flaskApp.route(route, **route_kwargs)(wrapper)

    return wrapper

  return decorator

@flaskCustomRoute(app, '/')
def routeMain():
  return render_template('index.html')

@flaskCustomRoute(app, '/getModelList')
def routeGetModelList():
  responseDict: dict = getModelList()
  responseStr: str = json.dumps(responseDict)

  return responseStr

@flaskCustomRoute(app, '/talk')
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

  return llmResponse

@flaskCustomRoute(app, '/reloadModel')
def routeReloadModel():
  global llmModel
  global currentLlmModel
  global isLockingApi

  queryModel: str = request.args.get('model', '')
  isSupportLlmModel: bool = False
  responseDict: dict
  responseStr: str

  isLockingApi = True

  for slm in SupportLlmModels:
    if(slm.name == queryModel):
      currentLlmModel = slm
      isSupportLlmModel = True
      break

  if(not isSupportLlmModel):
    return Response('Invalid model.', status = 400)

  del llmModel
  llmModel = loadLlmModel(currentLlmModel)

  responseDict = getModelList()
  responseStr = json.dumps(responseDict)

  isLockingApi = False

  return responseStr

if __name__ == '__main__':
  if(not FLASK_IS_DEBUG_MODE):
    llmModel = loadLlmModel(currentLlmModel)
    llmContextController: ContextController = ContextController('elyza8bQuant', False)

  app.run(port = 5000, debug = FLASK_IS_DEBUG_MODE)