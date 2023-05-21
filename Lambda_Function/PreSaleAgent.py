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

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))
HIST_STORE_LIMIT = int(os.getenv("HIST_STORE_LIMIT", default=100))
chat_language = os.getenv("INIT_LANGUAGE", default="en")
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}
max_model_tok = 3072
openai.api_key = "enter_your_api_key_here"
now = datetime.now()
formatted_time = now.strftime("%d%H%M%S")


def dbquery_chain(cx_question, need_agent):
    """
    Can optimize by ADD GPT indexing query to highconf_li
    """
    highconf_li, lowconf_li = kendra_search(cx_question)
    if len(highconf_li) == 0 and len(lowconf_li) == 0:
        need_agent = True
    return highconf_li, lowconf_li, need_agent


class SessConvID:
    def __init__(self):
        self.bot_init_start_msg = "PLEASE INSERT YOUR OWN TEXT"
        self.error_msg_reply = "PLEASE INSERT YOUR OWN TEXT"
        self.sessid_cxhist_di = {}
        self.sessid_bothist_di = {}
        self.sessid_needagent = {}
        self.sessid_confirmstage = {}

    def get_sess_cx_hist(self, sess_id):
        try:
            return self.sessid_cxhist_di[sess_id]
        except KeyError:
            self.sessid_cxhist_di[sess_id] = []
            return []

    def add_sess_cx_q(self, sess_id, question_li):
        self.sessid_cxhist_di[sess_id] = question_li

    def get_sess_bot_hist(self, sess_id):
        try:
            return self.sessid_bothist_di[sess_id]
        except KeyError:
            self.sessid_bothist_di[sess_id] = []
            return []

    def add_sess_bot_a(self, sess_id, answer_li):
        self.sessid_bothist_di[sess_id] = answer_li

    def get_sess_needagent(self, sess_id):
        try:
            return self.sessid_needagent[sess_id]
        except KeyError:
            self.sessid_needagent[sess_id] = False
            return False

    def set_sess_needagent(self, sess_id, val):
        self.sessid_needagent[sess_id] = val

    def get_sess_confirmstage(self, sess_id):
        try:
            return self.sessid_confirmstage[sess_id]
        except KeyError:
            self.sessid_confirmstage[sess_id] = False
            return False

    def set_sess_confirmstage(self, sess_id, val):
        self.sessid_confirmstage[sess_id] = val


def productname_api(text):
    url = "https://your_api_url_here/api/v1/nlp/productname"
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
    query = query.replace('console', 'UniFi OS Console')
    high_conf_li = []
    low_conf_li = []
    index = "your_aws_index_here"
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
                if len(low_conf_li) < 3:
                    low_conf_li.append(kendra_doc_text)
    return high_conf_li, low_conf_li


class Prompt:
    def __init__(self):
        self.system = "PLEASE INSERT YOUR OWN TEXT"
        self.cx_list = []
        self.bot_list = []

    def set_pre_prompt(self, pre_prompt):
        self.system = pre_prompt

    def add_cx_msg(self, new_msg):
        self.cx_list.append(new_msg)

    def add_bot_msg(self, new_msg):
        self.bot_list.append(new_msg)

    def generate_prompt(self):
        try:
            assert len(self.cx_list) > 0
        except AssertionError:
            self.cx_list = ["PLEASE INSERT YOUR OWN TEXT", self.cx_list[-1]]
            self.bot_list = ["PLEASE INSERT YOUR OWN TEXT"]
        while (len("\n".join(self.cx_list)) + len("\n".join(self.bot_list))) / 5 > max_model_tok:
            self.cx_list.pop(0)
            self.bot_list.pop(0)
        format_list = [{"role": "system", "content": self.system}]
        for i, user in enumerate(self.cx_list):
            tmp = {"role": "user", "content": user}
            format_list.append(tmp)
            try:
                assistant = self.bot_list[i]
                tmp = {"role": "assistant", "content": assistant}
                format_list.append(tmp)
            except IndexError:
                pass
        return format_list

import os
import time
import random
import openai

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0))
        self.top_p = 1
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=1024))
        self.stop_seq = ["Customer:", "Agent:"]

    def get_response(self, sess_id='formatted_time'):
        response = None
        while response is None:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    user=sess_id,
                    stop=["\n\n", "Customer:", "Agent:"],
                    messages=self.prompt.generate_prompt()
                )
                response = response["choices"][0]['message']['content']
                for seq in self.stop_seq:
                    response = response.replace(seq, "")
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

# Additional functions are defined here
def kendra_to_gpt3_search(intent_request, sess_id):
    """
    Main function to handle the conversation flow and call appropriate functions
    based on the user's input and the current state of the conversation.
    """
    need_agent = managesess.get_sess_needagent(sess_id)
    confirmstage = managesess.get_sess_confirmstage(sess_id)
    cx_question_histli = managesess.get_sess_cx_hist(sess_id)
    bot_reply_li = managesess.get_sess_bot_hist(sess_id)
    session_attributes = get_session_attributes(intent_request)
    cx_question = intent_request["inputTranscript"]
    cx_question = productname_api(cx_question)

    if cx_question == "CLEAR" or cx_question == "RESET":
        reply_to_user = managesess.bot_init_start_msg
        need_agent, confirmstage, cx_question_histli, bot_reply_li = init_revchatgpt()

        if cx_question == "RESET":
            managesess = SessConvID()

    else:
        cx_question_histli.append(cx_question)

        if not confirmstage:
            if not need_agent:
                highconf_li, lowconf_li, need_agent = dbquery_chain(cx_question, need_agent)

            if not need_agent:
                first_stage_rep, need_agent = extractans_chain(cx_question, highconf_li, lowconf_li, need_agent, sess_id)

            if not need_agent:
                need_agent, confirmstage, cx_question_histli, bot_reply_li, reply_to_user = nlg_chain(
                    first_stage_rep, need_agent, confirmstage, cx_question_histli, bot_reply_li, sess_id=sess_id)
            else:
                need_agent, confirmstage, cx_question_histli, bot_reply_li, reply_to_user = transfer_chain(
                    need_agent, confirmstage, cx_question_histli, bot_reply_li, sess_id=sess_id)
        else:
            confirm_transfer = chk_user_want_agent(cx_question_histli, bot_reply_li, sess_id)
            confirmstage = False
            need_agent = False

            if 'No' in confirm_transfer:
                reply_to_user = "PLEASE INSERT YOUR OWN TEXT"
                need_agent, confirmstage, cx_question_histli, bot_reply_li = init_revchatgpt()
            elif 'Yes' in confirm_transfer:
                reply_to_user = "PLEASE INSERT YOUR OWN TEXT"
                need_agent, confirmstage, cx_question_histli, bot_reply_li = init_revchatgpt()
            else:
                highconf_li, lowconf_li, need_agent = dbquery_chain(cx_question, need_agent)

                if not need_agent:
                    first_stage_rep, need_agent = extractans_chain(cx_question, highconf_li, lowconf_li, need_agent, sess_id=sess_id)

                if not need_agent:
                    need_agent, confirmstage, cx_question_histli, bot_reply_li, reply_to_user = nlg_chain(
                        first_stage_rep, need_agent, confirmstage, cx_question_histli, bot_reply_li, sess_id)
                else:
                    need_agent, confirmstage, cx_question_histli, bot_reply_li, reply_to_user = transfer_chain(
                        need_agent, confirmstage, cx_question_histli, bot_reply_li, sess_id)

    fulfillment_state = "Fulfilled"

    if "OpenAI/API outage" in reply_to_user:
        reply_to_user, need_agent, confirmstage, cx_question_histli, bot_reply_li = kendra_to_gbt3_search(
            intent_request, sess_id, reply_to_user, need_agent, confirmstage, cx_question_histli, bot_reply_li)
        managesess.set_sess_needagent(sess_id, need_agent)
        managesess.set_sess_confirmstage(sess_id, confirmstage)
        managesess.add_sess_cx_q(sess_id, cx_question_histli.copy())
        managesess.add_sess_bot_a(sess_id, bot_reply_li.copy())
    else:
        managesess.set_sess_needagent(sess_id, need_agent)
        managesess.set_sess_confirmstage(sess_id, confirmstage)
        managesess.add_sess_cx_q(sess_id, cx_question_histli.copy())
        managesess.add_sess_bot_a(sess_id, bot_reply_li.copy())

    message = {
        'contentType': 'PlainText',
        'content': reply_to_user
    }

    return close(intent_request, session_attributes, fulfillment_state, message)

def kendra_to_gbt3_search(intent_request, sess_id=None, reply_to_user=None, need_agent=False, confirmstage=False, cx_question_histli=[], bot_reply_li=[]):
    if reply_to_user is not None and isinstance(sess_id, str):
        from_chat_gpt = True
    else:
        from_chat_gpt = False

    convert_to_newspace_sessid = sess_id + 'gpt3'
    need_agent = managesess.get_sess_needagent(convert_to_newspace_sessid)
    confirmstage = managesess.get_sess_confirmstage(convert_to_newspace_sessid)
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