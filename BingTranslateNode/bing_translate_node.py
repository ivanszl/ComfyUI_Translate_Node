import os
import requests
import uuid
# import server import PromptServer
# from aiohttp import web
# from typing import Optional
# from fastapi import Header

ALL_CODES = [{"code":"af","name":"南非荷兰语"},{"code":"am","name":"阿姆哈拉语"},{"code":"ar","name":"阿拉伯语"},{"code":"as","name":"阿萨姆语"},{"code":"az","name":"阿塞拜疆语"},{"code":"ba","name":"巴什基尔语"},{"code":"bg","name":"保加利亚语"},{"code":"bho","name":"Bhojpuri"},{"code":"bn","name":"孟加拉语"},{"code":"bo","name":"藏语"},{"code":"brx","name":"Bodo"},{"code":"bs","name":"波斯尼亚语"},{"code":"ca","name":"加泰罗尼亚语"},{"code":"cs","name":"捷克语"},{"code":"cy","name":"威尔士语"},{"code":"da","name":"丹麦语"},{"code":"de","name":"德语"},{"code":"doi","name":"Dogri"},{"code":"dsb","name":"下索布语"},{"code":"dv","name":"迪维希语"},{"code":"el","name":"希腊语"},{"code":"en","name":"英语"},{"code":"es","name":"西班牙语"},{"code":"et","name":"爱沙尼亚语"},{"code":"eu","name":"巴斯克语"},{"code":"fa","name":"波斯语"},{"code":"fi","name":"芬兰语"},{"code":"fil","name":"菲律宾语"},{"code":"fj","name":"斐济语"},{"code":"fo","name":"法罗语"},{"code":"fr","name":"法语"},{"code":"fr-CA","name":"法语 (加拿大)"},{"code":"ga","name":"爱尔兰语"},{"code":"gl","name":"加利西亚语"},{"code":"gom","name":"Konkani"},{"code":"gu","name":"古吉拉特语"},{"code":"ha","name":"豪萨语"},{"code":"he","name":"希伯来语"},{"code":"hi","name":"印地语"},{"code":"hne","name":"Chhattisgarhi"},{"code":"hr","name":"克罗地亚语"},{"code":"hsb","name":"上索布语"},{"code":"ht","name":"海地克里奥尔语"},{"code":"hu","name":"匈牙利语"},{"code":"hy","name":"亚美尼亚语"},{"code":"id","name":"印度尼西亚语"},{"code":"ig","name":"伊博语"},{"code":"ikt","name":"Inuinnaqtun"},{"code":"is","name":"冰岛语"},{"code":"it","name":"意大利语"},{"code":"iu","name":"因纽特语"},{"code":"iu-Latn","name":"Inuktitut (Latin)"},{"code":"ja","name":"日语"},{"code":"ka","name":"格鲁吉亚语"},{"code":"kk","name":"哈萨克语"},{"code":"km","name":"高棉语"},{"code":"kmr","name":"库尔德语 (北)"},{"code":"kn","name":"卡纳达语"},{"code":"ko","name":"韩语"},{"code":"ks","name":"Kashmiri"},{"code":"ku","name":"库尔德语 (中)"},{"code":"ky","name":"柯尔克孜语"},{"code":"ln","name":"林加拉语"},{"code":"lo","name":"老挝语"},{"code":"lt","name":"立陶宛语"},{"code":"lug","name":"Ganda"},{"code":"lv","name":"拉脱维亚语"},{"code":"lzh","name":"Chinese (Literary)"},{"code":"mai","name":"迈蒂利语"},{"code":"mg","name":"马拉加斯语"},{"code":"mi","name":"毛利语"},{"code":"mk","name":"马其顿语"},{"code":"ml","name":"马拉雅拉姆语"},{"code":"mn-Cyrl","name":"Mongolian (Cyrillic)"},{"code":"mn-Mong","name":"Mongolian (Traditional)"},{"code":"mni","name":"Manipuri"},{"code":"mr","name":"马拉地语"},{"code":"ms","name":"马来语"},{"code":"mt","name":"马耳他语"},{"code":"mww","name":"苗语"},{"code":"my","name":"缅甸语"},{"code":"nb","name":"书面挪威语"},{"code":"ne","name":"尼泊尔语"},{"code":"nl","name":"荷兰语"},{"code":"nso","name":"Sesotho sa Leboa"},{"code":"nya","name":"Nyanja"},{"code":"or","name":"奥里亚语"},{"code":"otq","name":"克雷塔罗奥托米语"},{"code":"pa","name":"旁遮普语"},{"code":"pl","name":"波兰语"},{"code":"prs","name":"达里语"},{"code":"ps","name":"普什图语"},{"code":"pt","name":"葡萄牙语 (巴西)"},{"code":"pt-PT","name":"葡萄牙语 (葡萄牙)"},{"code":"ro","name":"罗马尼亚语"},{"code":"ru","name":"俄语"},{"code":"run","name":"Rundi"},{"code":"rw","name":"卢旺达语"},{"code":"sd","name":"信德语"},{"code":"si","name":"僧伽罗语"},{"code":"sk","name":"斯洛伐克语"},{"code":"sl","name":"斯洛文尼亚语"},{"code":"sm","name":"萨摩亚语"},{"code":"sn","name":"绍纳语"},{"code":"so","name":"索马里语"},{"code":"sq","name":"阿尔巴尼亚语"},{"code":"sr-Cyrl","name":"塞尔维亚语 (西里尔文)"},{"code":"sr-Latn","name":"塞尔维亚语 (拉丁文)"},{"code":"st","name":"Sesotho"},{"code":"sv","name":"瑞典语"},{"code":"sw","name":"斯瓦希里语"},{"code":"ta","name":"泰米尔语"},{"code":"te","name":"泰卢固语"},{"code":"th","name":"泰语"},{"code":"ti","name":"提格利尼亚语"},{"code":"tk","name":"土库曼语"},{"code":"tlh-Latn","name":"克林贡语 (拉丁文)"},{"code":"tlh-Piqd","name":"克林贡语 (pIqaD)"},{"code":"tn","name":"Setswana"},{"code":"to","name":"汤加语"},{"code":"tr","name":"土耳其语"},{"code":"tt","name":"鞑靼语"},{"code":"ty","name":"塔希提语"},{"code":"ug","name":"维吾尔语"},{"code":"uk","name":"乌克兰语"},{"code":"ur","name":"乌尔都语"},{"code":"uz","name":"乌兹别克语"},{"code":"vi","name":"越南语"},{"code":"xh","name":"科萨语"},{"code":"yo","name":"约鲁巴语"},{"code":"yua","name":"尤卡特克玛雅语"},{"code":"yue","name":"粤语 (繁体)"},{"code":"zh-Hans","name":"中文 (简体)"},{"code":"zh-Hant","name":"中文 (繁体)"},{"code":"zu","name":"祖鲁语"}]
LANGUAGES = list(map(lambda x:f'{x["code"]} - {x["name"]}', ALL_CODES))

script_path = os.path.abspath(__file__)
key = "65a0421930d74899a9323265630a6b3e"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "eastasia"

def get_support_langs(lang):
  return next(filter(lambda x: x["code"] == lang, ALL_CODES))

def translate(prompt:str, from_lang:str|None=None, to_lang:str="en"):
  path = '/translate'
  constructed_url = endpoint + path
  params = {
    'api-version': '3.0',
    'to': to_lang
  }
  if from_lang is not None:
    params['from'] = from_lang
  headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
  }
  translate_text_prompt = prompt
  try:
    body = [{'text': prompt}]
    response = requests.post(constructed_url, params=params, headers=headers, json=body).json()
    translate_text_prompt = response[0]['translations'][0]['text']
  except Exception as e:
    print(e)
    return '[Error] No translate text!'
  return translate_text_prompt

class BingTranslateCLIPTextEncodeNode:
  @classmethod
  def INPUT_TYPES(self):
    return {
      "required": {
          "from_translate": (LANGUAGES, {"default": "zh-Hans - 中文 (简体)"}),
          "to_translate": (LANGUAGES, {"default": "en - 英文"}),
          "text": ("STRING", {"multiline": True, "placeholder": "Input text"}),
          "clip": ("CLIP", )
        }
    }

  RETURN_TYPES = ("CONDITIONING", "STRING",)
  FUNCTION = "bing_translate_text"
  CATEGORY = "XiaoPan Nodes/conditioning"
  def bing_translate_text (self, from_translate, to_translate, text, clip):
    from_lang = from_translate.split(' - ')[0]
    to_lang = to_translate.split(' - ')[0]
    text = translate(text, from_lang, to_lang)
    tokens = clip.tokenize(text)
    cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
    return ([[cond, {"pooled_output": pooled}]], text)
    
  @classmethod
  def VALIDATE_INPUTS(cls, from_translate, to_translate, text, clip):
    return True

class BingTranslateTextNode(BingTranslateCLIPTextEncodeNode):
  @classmethod
  def INPUT_TYPES(self):
    return_types = super().INPUT_TYPES()
    del return_types["required"]["clip"]
    return return_types

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("text",)
  FUNCTION = "bing_translate_text"

  ChildProcessErrorATEGORY = "XiaoPan Nodes/text"

  def bing_translate_text(self, from_translate, to_translate, text):
    from_lang = from_translate.split(' - ')[0]
    to_lang = to_translate.split(' - ')[0]
    text_tranlsated = translate(text, from_lang, to_lang)
    return (text_tranlsated,)

  @classmethod
  def VALIDATE_INPUTS(cls, from_translate, to_translate, text):
    return True
    