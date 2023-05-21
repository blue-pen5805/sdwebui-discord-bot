
import re
import deepl
import modules.env as env

DEEPL_API_KEY = env.get("DEEPL_API_KEY")

def is_japanese(text):
    return re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[ｱ-ｳﾞ]+|[一-龠]+', text)

def translate(text):
    if DEEPL_API_KEY is None: return None

    translator = deepl.Translator(DEEPL_API_KEY)

    if is_japanese(text):
        try:
            return translator.translate_text(text, source_lang='JA', target_lang="EN-GB").text.lower()
        except:
            return None

    return None
