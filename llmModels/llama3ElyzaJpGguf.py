from llama_cpp import Llama
from typing import *

from llmModels.llmModel import *

class Llama3ElyzaJpGguf(LlmModel):
  def __init__(self, modelPath: str, useGpu: bool = True):
    self._model: Llama
    self._modelPath: str = modelPath

    super().__init__(useGpu)

  def _llmChatItemList2PromptStr(self, list: List[LlmChatItem]) -> str:
    promptStr: str = ''

    for lci in list:
      promptStr += f'{lci.role.value}: {lci.content}\n'

    promptStr += 'assistant:'

    return promptStr

  def resetModel(self):
    gpuLayers: int = 32 if self._useGpu else 0

    super().resetModel()

    self._model = Llama(
      model_path = self._modelPath,
      n_ctx = 2048,
      n_gpu_layers = gpuLayers
    )

  def talk(self, messages: List[LlmChatItem]) -> str:
    promptStr: str = self._llmChatItemList2PromptStr(messages)
    response = self._model(prompt = promptStr, max_tokens = 1200)
    output: str = response['choices'][0]['text']

    return output