from flask import Flask, request
from typing import *

from llmModel import *

llmModel: LlmModel = LlmModel()
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