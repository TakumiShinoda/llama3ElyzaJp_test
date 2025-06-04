import os
import json
from io import TextIOWrapper
from typing import *

from llmModels.llmModel import *

DIR_NAME_CONTEXTS_SAVE: str = 'contexts'

class ContextController:
  def __init__(self, contextName: str, isNew: bool = False):
    self._contextName: str = contextName
    self._contextFilePath: str = f'./{DIR_NAME_CONTEXTS_SAVE}/{self._contextName}.json'
    self._contexts: List[LlmChatItem] = []

    if(not os.path.isdir(f'./{DIR_NAME_CONTEXTS_SAVE}')):
      os.makedirs(f'./{DIR_NAME_CONTEXTS_SAVE}')

    if(not os.path.isfile(self._contextFilePath) or isNew):
      self._resetContext()
    else:
      self._loadContext()
  
  def _resetContext(self) -> None:
    newContextFile: TextIOWrapper = open(self._contextFilePath, 'w', encoding='utf-8')

    newContextFile.write('{"contexts": []}')
    newContextFile.close()
  
  def _loadContext(self) -> None:
    contextFile: TextIOWrapper = open(self._contextFilePath, 'r', encoding='utf-8')
    contextJsonData: any = json.load(contextFile)
    result: List[LlmChatItem] = []

    if(
      (not 'contexts' in contextJsonData) or
      (not isinstance(contextJsonData['contexts'], list))
    ):
      raise('Bad context file.')
    
    for cjd in contextJsonData['contexts']:
      if((not 'role' in cjd) or (not 'content' in cjd)):
        continue
      
      if(cjd['role'] == 'system'):
        result.append(LlmChatItem(LlmChatItemRoles.system, cjd['content']))
      elif(cjd['role'] == 'user'):
        result.append(LlmChatItem(LlmChatItemRoles.user, cjd['content']))
    
    self._contexts = result

  def addContext(self, newItem: LlmChatItem) -> None:
    self._contexts.append(newItem)

  def saveContexts(self) -> None:
    contextFile: TextIOWrapper = open(self._contextFilePath, 'w', encoding='utf-8')

    json.dump({'contexts': [c.toDict() for c in self._contexts]}, contextFile, ensure_ascii = False, indent = 2)
    contextFile.close()

  def getContexts(self) -> List[LlmChatItem]:
    return self._contexts