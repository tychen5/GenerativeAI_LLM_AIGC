import os
import random
import re
import time
import json
import requests
import asyncio
import pickle
import functools
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import openai
import boto3
import tiktoken
from wordfreq import zipf_frequency

from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains import LLMChain
from langchain import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key"

# Replace with your file paths
revisor_chain_pkl = './revisor_chain.pkl'
query_chain_di_pkl = './query_chain_di.pkl'
url_di_pkl = './url_di.pkl'


def str2bool(v):
    v = str(v)
    if v.lower() in ("yes", "true", "t", "1", "True"):
        return True
    return False


# Environment variables
min_count_doc = int(os.getenv("min_count_doc", default=1400))
max_count_doc = int(os.getenv("max_count_doc", default=2400))
max_model_tok = int(os.getenv("max_model_tok", default=2048))
max_model_tok_nlg = int(os.getenv("max_model_tok_nlg", default=4000))
answer_max_tok = int(os.getenv("answer_max_tok", default=1000))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")
chatbase_model = str(os.getenv("chatbase_model", default="gpt-4"))
chatbase_botid = str(os.getenv("chatbase_botid", default="your_chatbase_botid"))
use_nlg = str2bool(os.getenv("use_nlg", default="False"))
chatbase_streaming = str2bool(os.getenv("chatbase_streaming", default="True"))
table_gpt4 = str2bool(os.getenv("table_gpt4", default="False"))
addrichmsg = str2bool(os.getenv("addrichmsg", default="False"))
addstorelink = str2bool(os.getenv("addstorelink", default="False"))
use_reviser_searcher = str2bool(os.getenv("use_reviser_searcher", default="False"))
temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0.95))
frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0.1))
presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0.3))
top_p = int(os.getenv("top_p", default=1))
max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=250))
stop_seq = os.getenv("stop_seq", default=["\n\n\n", " \n\n "])
other_product_name = os.getenv("other_product_name", default="UniFi OS Consoles information and other products articles")
use_kendra = str2bool(os.getenv("use_kendra", default="False"))
timeout_kendra = float(os.getenv("timeout_kendra", default=7))
chatgpt_streaming = str2bool(os.getenv("chatgpt_streaming", default="False"))
bad_line_keywords = os.getenv("bad_line_keywords", default=('Customer:', 'Agent:', 'for non-comparison questions', 'for non-specification/product difference questions'))
ir_verify = str2bool(os.getenv("ir_verify", default="True"))
vdb_thr = float(os.getenv("vdb_thr", default=0.8))
replace_kendra = str2bool(os.getenv("replace_kendra", default="True"))
use_short_prompt_compare = str2bool(os.getenv("use_short_prompt_compare", default="False"))
words_chatbase_notfound = list(os.getenv("words_chatbase_notfound", default=['words_chatbase_notfound']))
words_chatbase_notfound = [x.lower() for x in words_chatbase_notfound]
failed_to_get_answer_prompt = os.getenv("failed_to_get_answer_prompt", default="""failed_to_get_answer_prompt""")
not_found_answer_prompt = os.getenv("not_found_answer_prompt", default='not_found_answer_prompt')
recommend_not_found_prompt = os.getenv("recommend_not_found_prompt", default="""recommend_not_found_prompt""")
postsales_not_found_prompt = os.getenv("postsales_not_found_prompt", default="""postsales_not_found_prompt""")
recommend_add_note = os.getenv("recommend_add_note", default="recommend_add_note")
openai_connection_errmsg = os.getenv("openai_connection_errmsg", default="""openai_connection_errmsg""")

import openai
import random
import time
import requests
import re

OPENAI_MODEL = "enter_your_model"
temperature = 0.8
frequency_penalty = 0
presence_penalty = 0
top_p = 1
max_tokens = 100
stop_seq = ["\n"]
openai_connection_errmsg = "Connection error. Please try again later."

class OpenaiGPT:
    def __init__(self):
        self.model = OPENAI_MODEL
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.stop_seq = stop_seq
        self.system = ""
        self.first_cx = ""

    def get_response(self, sess_id):
        if self.first_cx == "":
            format_list = [{"role": "system", "content": self.system}]
        else:
            format_list = [{"role": "system", "content": self.system}, {"role": "user", "content": self.first_cx}]
        response = openai_connection_errmsg
        i = 0
        while response == openai_connection_errmsg and i <= 3:
            try:
                i += 1
                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    user=sess_id,
                    stop=self.stop_seq,
                    messages=format_list,
                    max_tokens=self.max_tokens
                )
                response = response["choices"][0]['message']['content']
            except openai.error.RateLimitError:
                response = openai_connection_errmsg
                time.sleep(random.random() * 10 + 1)
            except openai.error.ServiceUnavailableError:
                response = openai_connection_errmsg
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIError:
                response = openai_connection_errmsg
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIConnectionError:
                response = openai_connection_errmsg
                time.sleep(random.random() * 10 + 1)
        return response.strip()

# Additional functions and classes can be added here
import re


def count_parentheses_pairs(text):
    opening_parentheses = re.findall(r'\(', text)
    closing_parentheses = re.findall(r'\)', text)
    return min(len(opening_parentheses), len(closing_parentheses))


def find_replace_allcaps(text):
    if count_all_caps_words(text) > count_parentheses_pairs(text) * 4:
        return convert_caps_to_lowercase_except_sku(text)
    return text


def markdown_nlg(question, answer, sess_id, clf_type, product_set):
    chat_history = managesess.generate_chat_hist_nlg(sess_id)
    if clf_type == 'recommend':
        answer = answer + recommend_add_note
    system = """system prompt"""
    cx = f"""cx_PROMPT
{answer}
{chat_history}
Customer: {question}
CX_RPOMPT .. . Agent:"""
    given_prompt_num = count_token(answer + system + cx)
    i = 0
    while (given_prompt_num > max_model_tok_nlg - max_tokens and i < 5):
        answer_tok_num = count_token(answer)
        answer = shorten_spec_tok(answer, answer_tok_num, spec=False)
        given_prompt_num = count_token(answer + system + cx)
        i += 1
    gpt4_nlg = openaiGPT()
    gpt4_nlg.max_tokens = min(max_model_tok_nlg - given_prompt_num - 97, 200)
    gpt4_nlg.system = system
    gpt4_nlg.first_cx = cx
    final_reply = gpt4_nlg.get_response(sess_id)
    final_reply = final_reply.replace('Customer:', '')
    final_reply = final_reply.replace('Agent:', '')
    final_reply = clean_question(final_reply)
    final_reply = process_text(final_reply)
    return final_reply.strip()


bad_sentences = ['table', 'below', ':']


def remove_table(ori_text):
    tmpli = ori_text.split('\n\n')
    final_tmpli = []
    for t in tmpli:
        count = 0
        if '|\n|' in t:
            for bad in bad_sentences:
                if bad in t:
                    count = count + 1
            if count >= 2:
                final_tmpli.append(t)
    return "\n\n".join(final_tmpli)


def add_postfix_link(current_product_set, hist_product_set):
    new_ps = current_product_set - hist_product_set
    text = ''
    if len(new_ps) < 1:
        return ""
    else:
        for pn in new_ps:
            try:
                url = url_di[pn]
                text = text + f""" [{pn} info]({url})"""
            except KeyError:
                pass
    return text


def format_output(question, reply_to_user, session_attributes, intent_request, sess_id, current_product_set,
                  cx_question_rev, clf_type):
    hist_product_set = managesess.get_sess_cx_productset(sess_id)
    union_product_set = hist_product_set.union(current_product_set)
    managesess.add_sess_bot_a(sess_id, reply_to_user)
    managesess.add_sess_cx_q(sess_id, question)
    managesess.set_sess_cx_productset(sess_id, union_product_set)
    html_richmsg = "NaN"
    if len(union_product_set) > len(hist_product_set) and addrichmsg:
        html_richmsg = richmessage(intent_request["inputTranscript"])
        reply_to_user = reply_to_user + html_richmsg
    elif len(union_product_set) > len(hist_product_set) and addstorelink:
        storereflink = add_postfix_link(current_product_set, hist_product_set)
        reply_to_user = reply_to_user + storereflink
    else:
        pass
    fulfillment_state = "Fulfilled"
    message = {
        'contentType': 'CustomPayload',
        'content': reply_to_user
    }
    return close(intent_request, session_attributes, fulfillment_state, message)


import traceback


def lambda_handler(event, context):
    response = dispatch(event)
    return response


def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    sess_id = intent_request['sessionId']
    if intent_name == 'FallbackIntent':
        try:
            original_question, standalone_question, query_product_set, session_attributes = asyncio.run(
                reviser(intent_request, sess_id))
            final_reply, msg_type = classifier(standalone_question, sess_id, original_question)
            if final_reply == "":
                if use_nlg == False and chatbase_streaming == True:
                    return searcher(standalone_question, query_product_set, msg_type, sess_id, original_question,
                                    intent_request, session_attributes)
                elif use_nlg == False:
                    final_reply = searcher(standalone_question, query_product_set, msg_type, sess_id, original_question)
                    return format_output(original_question, final_reply, session_attributes, intent_request, sess_id,
                                         query_product_set, standalone_question, msg_type)
                else:
                    final_reply, answer = searcher(standalone_question, query_product_set, msg_type, sess_id,
                                                   original_question)
                    if final_reply == "":
                        final_reply = markdown_nlg(original_question, answer, sess_id, msg_type, query_product_set)
                return format_output(original_question, final_reply, session_attributes, intent_request, sess_id,
                                     query_product_set, standalone_question, msg_type)
        except Exception as e:
            traceback.print_exc()
            fulfillment_state = "Fulfilled"
            message = {
                'contentType': 'PlainText',
                'content': openai_connection_errmsg + "(Please reload your browser and try again.)"
            }
            return close(intent_request, session_attributes, fulfillment_state, message)


def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}


def close(intent_request, session_attributes, fulfillment_state, message):
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
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }