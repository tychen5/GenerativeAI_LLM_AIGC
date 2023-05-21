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

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=10))
HIST_STORE_LIMIT = int(os.getenv("HIST_STORE_LIMIT", default=100))
chat_language = os.getenv("INIT_LANGUAGE", default="en")

LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}

max_model_tok = 3072

chatbot = Chatbot(config={
  "email": "example@example.com",
  "password": "example_password",
})

chatbot.clear_conversations()

class SessConvID:
    def __init__(self):
        self.bot_init_start_msg = "PLEASE INSERT YOUR OWN TEXT"
        self.error_msg_reply = "PLEASE INSERT YOUR OWN TEXT"
        self.chatbot = Chatbot(config={
          "email": "example@example.com",
          "password": "example_password",
        })

        self.chatbot.clear_conversations()
        self.chatgpt_conversationid_li = []
        self.sessid_convid_di = {}
        self.sessid_cxhist_di = {}
        self.sessid_bothist_di = {}
        self.sessid_needagent = {}
        self.sessid_confirmstage = {}

    def get_convid(self, sess_id):
        if sess_id not in self.sessid_convid_di.keys():
            self.chatbot.reset_chat()
            return None
        else:
            conv_id = self.sessid_convid_di[sess_id]
            if conv_id not in self.chatgpt_conversationid_li:
                self.chatbot.reset_chat()
                self.sessid_convid_di[sess_id] = None
                conv_id = None
            return conv_id

    def add_sess_convid(self, sess_id, conv_id):
        self.sessid_convid_di[sess_id] = conv_id
        self.chatgpt_conversationid_li.append(conv_id)
        if len(self.chatgpt_conversationid_li) > HIST_STORE_LIMIT:
            self.chatbot.delete_conversation(convo_id=self.chatgpt_conversationid_li[0])
            self.chatgpt_conversationid_li.pop(0)
        now = datetime.now()
        formatted_time = now.strftime("%d%H%M%S")
        self.chatbot.change_title(convo_id=conv_id, title=str(sess_id)[-4:] + '_' + str(conv_id)[-4:] + '_' + formatted_time)

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
    kendra = boto3.client('kendra')
    high_conf_li = []
    low_conf_li = []
    index = "your_aws_kendra_index_id"

    kendra_response = kendra.query(
        QueryText=query,
        IndexId=index
    )

    kendra_resp = kendra_response['ResultItems']

    if len(kendra_resp) < 1:
        return [], []

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

    def add_msg(self, new_msg):
        while len(self.msg_list) >= MSG_LIST_LIMIT or int(len('\n'.join(self.msg_list)) / 5) > max_model_tok:
            self.remove_msg()
        self.msg_list.append(new_msg)

    def remove_msg(self):
        new_li = []
        ori_li = self.msg_list
        remove = False
        for msg in ori_li:
            if (('Customer: ' in msg) or ('Agent: ' in msg)) and (remove == False):
                remove = True
            new_li.append(msg)
        self.msg_list = new_li

    def generate_prompt(self):
        return ''.join(self.msg_list)

response = None
error_msg = ""
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
    #"PLEASE INSERT YOUR OWN FUNC"
def get_session_attributes(intent_request):
    """Get session attributes from the intent request.

    Args:
        intent_request (dict): The intent request containing session state.

    Returns:
        dict: The session attributes if present, otherwise an empty dictionary.
    """
    session_state = intent_request['sessionState']
    if 'sessionAttributes' in session_state:
        return session_state['sessionAttributes']
    return {}


def close(intent_request, session_attributes, fulfillment_state, message):
    """Close the intent request with the provided session attributes, fulfillment state, and message.

    Args:
        intent_request (dict): The intent request to be closed.
        session_attributes (dict): The session attributes to be included in the response.
        fulfillment_state (str): The fulfillment state of the intent request.
        message (dict): The message to be included in the response.

    Returns:
        dict: The closed intent request with updated session state, message, and other attributes.
    """
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request.get('requestAttributes', None)
    }