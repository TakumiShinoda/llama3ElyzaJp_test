from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import *

from mods.llmModels.llmModel import *

LLM_MODEL_NAME_ELYZA_JP_8B: str = 'elyza/Llama-3-ELYZA-JP-8B'

class Llama3ElyzaJp8b(LlmModel):
  def __init__(self):
    super().__init__()
  
  def resetModel(self) -> None:
    modelName: str = LLM_MODEL_NAME_ELYZA_JP_8B

    super().resetModel()

    self._tokenizer = AutoTokenizer.from_pretrained(modelName)
    self._model = AutoModelForCausalLM.from_pretrained(
      modelName,
      torch_dtype = 'auto',
      device_map = 'auto',
      cache_dir = './models/'
    )

    self._model.eval()

  def talk(self, messages: List[LlmChatItem]) -> str:
    prompt: any = self._tokenizer.apply_chat_template(
      [m.toDict() for m in messages],
      tokenize = False,
      add_generation_prompt = True
    )
    token_ids: any = self._tokenizer.encode(
      prompt,
      add_special_tokens = False,
      return_tensors='pt'
    )
    output_ids: any = self._model.generate(
      token_ids.to(self._model.device),
      max_new_tokens = 1200,
      do_sample = True,
      temperature = 0.6,
      top_p = 0.9,
    ).detach()
    output: any = self._tokenizer.decode(
      output_ids.tolist()[0][token_ids.size(1):], 
      skip_special_tokens = True
    )

    return output