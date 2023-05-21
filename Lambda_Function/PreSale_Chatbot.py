from revChatGPT.V1 import Chatbot
import os
import openai
import sys
import io
import random
import boto3
import re
import time
import json
import requests
from datetime import datetime

# Set environment variables
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))
HIST_STORE_LIMIT = int(os.getenv("HIST_STORE_LIMIT", default=100))
chat_language = os.getenv("INIT_LANGUAGE", default="en")
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}
max_model_tok = 3072
openai.api_key = "enter_your_openai_api_key_here"

# Get current time
now = datetime.now()
formatted_time = now.strftime("%d%H%M%S")

class SessConvID:
    def __init__(self):
        self.bot_init_start_msg = "PLEASE INSERT YOUR OWN TEXT"
        self.error_msg_reply = "PLEASE INSERT YOUR OWN TEXT"
        self.sessid_cxhist_di = {}
        self.sessid_bothist_di = {}
        self.sessid_needagent = {}
        self.sessid_confirmstage = {}

    # Other methods for SessConvID class

def productname_api(text):
    url = "PLEASE INSERT YOUR OWN TEXT"
    payload = json.dumps({
      "text": text
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    list_of_dict = response.json()
    if len(list_of_dict['inference']) > 0:
        return (list_of_dict['inference'][0]['text_replace'])
    return(text)

managesess = SessConvID()

def get_longest_doc_info(kendra_dict):
    res_text_li = []
    if len(kendra_dict['AdditionalAttributes']) > 0:
        for high_conf_text in kendra_dict['AdditionalAttributes']:
            res_text_li.append(high_conf_text['Value']['TextWithHighlightsValue']['Text'])
    else:
        res_text_li.append(kendra_dict['DocumentExcerpt']['Text'])
    return '\n'.join(res_text_li)

def kendraSearch(query):
    return [], []

    # Other code for kendraSearch function

class Prompt:
    def __init__(self):
        self.system = "PLEASE INSERT YOUR OWN TEXT"
        self.cx_list = []
        self.bot_list = []

    # Other methods for Prompt class

import os
import time
import random
import openai

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0))
        self.top_p = 1
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1024))
        self.stop_seq = ["\n\n"]

    def get_response(self, sess_id='formatted_time'):
        response = None
        while response is None:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    user=sess_id,
                    stop=self.stop_seq,
                    messages=self.prompt.generate_prompt()
                )
                response = response["choices"][0]['message']['content']
            except openai.error.RateLimitError:
                response = None
                time.sleep(random.random() * 10 + 1)
            except openai.error.ServiceUnavailableError:
                response = None
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIError:
                response = None
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIConnectionError:
                response = None
                time.sleep(random.random() * 10 + 1)
            except TypeError:
                response = None
                time.sleep(random.random() * 10 + 1)
            except KeyError:
                response = None
        return response.strip()

# Other functions and code go here
def kendra_to_gbt3_search(intent_request, sess_id=None, reply_to_user=None, need_agent=False, confirm_stage=False, cx_question_histli=[], bot_reply_li=[]):
    if reply_to_user is not None and isinstance(sess_id, str):
        from_chat_gpt = True
    else:
        from_chat_gpt = False

    convert_to_newspace_sessid = sess_id + 'gpt3'
    need_agent = managesess.get_sess_needagent(convert_to_newspace_sessid)
    confirm_stage = managesess.get_sess_confirmstage(convert_to_newspace_sessid)
    cx_question_histli = managesess.get_sess_cx_hist(convert_to_newspace_sessid).copy()
    bot_reply_li = managesess.get_sess_bot_hist(convert_to_newspace_sessid).copy()

    current_sess_id = ""
    chat_language = os.getenv("INIT_LANGUAGE", default="en")
    MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=100))
    LANGUAGE_TABLE = {
        "zh": "哈囉！",
        "en": "Hello!"
    }

    max_model_tok = 3072

    class Prompt:
        def __init__(self):
            self.msg_list = []

        def add_msg(self, new_msg):
            if (len(self.msg_list) >= MSG_LIST_LIMIT) or (int(len('\n'.join(self.msg_list)) / 5) >= max_model_tok):
                self.remove_msg()
            self.msg_list.append(new_msg)

        def remove_msg(self):
            cx_question_histli.pop(0)
            bot_reply_li.pop(0)

        def generate_prompt(self):
            return '\n'.join(self.msg_list)

    class ChatGPT:
        def __init__(self):
            self.prompt = Prompt()
            self.model = os.getenv("OPENAI_MODEL", default="text-davinci-003")
            self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
            self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
            self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0))
            self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1024))
            self.top_p = 1
            self.stop_seq = ["Customer:", "Agent:"]
        #"PLEASE INSERT YOUR OWN FUNC"