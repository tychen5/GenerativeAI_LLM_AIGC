from revChatGPT.V1 import Chatbot
import os
from datetime import datetime
import openai
import sys
import io
import random
import boto3
import re
import time
import json
import requests

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=10))
HIST_STORE_LIMIT = int(os.getenv("HIST_STORE_LIMIT", default=100))
chat_language = os.getenv("INIT_LANGUAGE", default="en")
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}
max_model_tok = 3072

chatbot = Chatbot(config={
  "email": "your_email@example.com",
  "password": "your_password",
})
chatbot.clear_conversations()

def dbquery_chain(cx_question, need_agent):
    highconf_li, lowconf_li = kendra_search(cx_question)
    if len(highconf_li) == 0 and len(lowconf_li) == 0:
        need_agent = True
    return highconf_li, lowconf_li, need_agent

class SessConvID:
    def __init__(self):
        self.bot_init_start_msg = "PLEASE INSERT YOUR OWN TEXT"
        self.error_msg_reply = "PLEASE INSERT YOUR OWN TEXT"
        self.chatbot = Chatbot(config={
          "email": "your_email@example.com",
          "password": "your_password",
        })
        self.chatbot.clear_conversations()
        self.chatgpt_conversationid_li = []
        self.sessid_convid_di = {}
        self.sessid_cxhist_di = {}
        self.sessid_bothist_di = {}
        self.sessid_needagent = {}
        self.sessid_confirmstage = {}

    # Other methods for SessConvID class

def productname_api(text):
    url = "https://your_api_url/api/v1/nlp/productname"
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

def kendra_search(query):
    kendra = boto3.client('kendra')
    high_conf_li = []
    low_conf_li = []
    index = "your_aws_kendra_index_id"
    kendra_response = kendra.query(
        QueryText=query,
        IndexId=index)
    kendra_resp = kendra_response['ResultItems']
    if len(kendra_resp) < 1:
        return high_conf_li, low_conf_li
    else:
        for i, kendra_result in enumerate(kendra_response['ResultItems']):
            doc_conf = kendra_result['ScoreAttributes']['ScoreConfidence']
            kendra_doc_text = get_longest_doc_info(kendra_result)
            if doc_conf == 'HIGH' or doc_conf == 'VERY_HIGH':
                high_conf_li.append(kendra_doc_text)
            else:
                low_conf_li.append(kendra_doc_text)
    return high_conf_li, low_conf_li

class Prompt:
    def __init__(self):
        self.msg_list = []

    # Other methods for Prompt class

response = None
error_msg = """{"detail":"Too many requests in 1 hour. Try again 1 hour later."}"""

import os
import re
import time
import random
import openai

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1024))
        self.stop_seq = ["Customer:", "Agent:"]
    #"PLEASE INSERT YOUR OWN CODE"...        

def kendra_to_gbt3_search(intent_request, sess_id=None, reply_to_user=None, need_agent=False, confirmstage=False, cx_question_histli=[], bot_reply_li=[]):
    if reply_to_user is not None and isinstance(sess_id, str):
        from_chat_gpt = True
        convert_to_newspace_sessid = sess_id + 'gpt3'
        need_agent = managesess.get_sess_needagent(convert_to_newspace_sessid)
        confirmstage = managesess.get_sess_confirmstage(convert_to_newspace_sessid)
        cx_question_histli = managesess.get_sess_cx_hist(convert_to_newspace_sessid)
        bot_reply_li = managesess.get_sess_bot_hist(convert_to_newspace_sessid)
    else:
        from_chat_gpt = False

    openai.api_key = "enter_your_api_key_here"
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
        #"PLEASE INSERT YOUR OWN CODE"