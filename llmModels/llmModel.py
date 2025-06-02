from enum import Enum
from dataclasses import dataclass
from typing import *

class LlmChatItemRoles(Enum):
  system = 'system'
  user = 'user'

@dataclass
class LlmChatItem:
  role: LlmChatItemRoles
  content: str

  def toDict(self) -> dict:
    return {'role': self.role.value, 'content': self.content}

class LlmModel:
  def __init__(self):
    self._tokenizer: any = None
    self._model: any = None

    self.resetModel()

  def resetModel(self) -> None:
    if(not self._tokenizer == None):
      del self._tokenizer
    if(not self._model == None):
      del self._model

  def talk(self, messages: List[LlmChatItem]) -> str:
    return ''