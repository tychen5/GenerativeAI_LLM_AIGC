import os
from datetime import datetime
import pinecone
import openai
import sys
import io
import random
import boto3
import re
import time
import json
import requests
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains import LLMChain
from langchain import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import json
import requests
import os
import asyncio
import re
import pickle
import tiktoken
import functools
from concurrent.futures import ThreadPoolExecutor

openai.api_key = "enter_your_api_key"
output_dir = './'
revisor_chain_pkl = './revisor_chain.pkl'
vectore_stores_pkl = './all_product_vdb_di.pkl'
query_chain_di_pkl = './query_chain_di.pkl'
spec_di_pkl = './product_spec_pdf_di.pkl'
now = datetime.now()
formatted_time = now.strftime("%d%H%M%S")
s3 = boto3.client("s3")
kendra = boto3.client("kendra", region_name="PLEASE INSERT YOUR OWN TEXT")
INDEX_NAME = os.getenv('KENDRA_INDEX_NAME', default='enter_your_index_name')
BUCKET_NAME = os.getenv('KENDRA_SEARCH_S3_BUCKET', default="enter_your_bucket_name")


def str2bool(v):
    v = str(v)
    if v.lower() in ("yes", "true", "t", "1", "True"):
        return True
    return False


min_count_doc = int(os.getenv("min_count_doc", default=1400))
max_count_doc = int(os.getenv("max_count_doc", default=2400))
failed_to_get_answer_prompt = "PLEASE INSERT YOUR OWN TEXT"
not_found_answer_prompt = "PLEASE INSERT YOUR OWN TEXT"
recommend_not_found_prompt = "PLEASE INSERT YOUR OWN TEXT"
recommend_add_note = "PLEASE INSERT YOUR OWN TEXT"
max_model_tok = int(os.getenv("max_model_tok", default=768))  # chat history砍掉時會需要用
max_model_tok_nlg = int(os.getenv("max_model_tok_nlg", default=4000))  # nlg產生時會砍掉回答的答案
answer_max_tok = int(os.getenv("answer_max_tok", default=2000))  # 答案最多可以有的tok
OPENAI_MODEL = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")  # gpt-3.5-turbo gpt-4 only apply to last nlg phase only, and chatgpt_streaming should set to false so this setting will apply
table_gpt4 = str2bool(os.getenv("table_gpt4", default="False"))  # 決定table生成時候要不要用gpt4
temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0))
top_p = int(os.getenv("top_p", default=1))
max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=700))
stop_seq = os.getenv("stop_seq", default=["\n\n\n", " \n\n "])
prompt_system = "PLEASE INSERT YOUR OWN TEXT"
prompt_cx = "PLEASE INSERT YOUR OWN TEXT"
openai_connection_errmsg = "PLEASE INSERT YOUR OWN TEXT"
other_product_name = os.getenv("other_product_name", default="UniFi OS Consoles information and other products articles")  # KB中其他類別的文章名稱
use_kendra = str2bool(os.getenv("use_kendra", default="False"))  # 是否要直接只走kendra的流程
timeout_kendra = float(os.getenv("timeout_kendra", default=7))  # 只有在use_kendra是false的時候才會生效，設定當若langchain/gpt indecing要等太久的時候直接呼叫kendra
chatgpt_streaming = str2bool(os.getenv("chatgpt_streaming", default="False"))  # True:兩種是否要table的prompt合一走langchain速度最快, False:兩種是否要table prompt會根據要是specification且兩種名字以上生成table(TODO:if true will force use chatgpt w/ streaming function, not implement yet)
bad_line_keywords = os.getenv("bad_line_keywords", default=('Customer:', 'Agent:', 'for non-comparison questions', 'for non-specification/product difference questions'))  # for nlg filtering
ir_verify = str2bool(os.getenv("ir_verify", default="True"))  # does kendra output need to be extracted(using IR model) or directly output?
vdb_thr = float(os.getenv("vdb_thr", default=0.8))
replace_kendra = str2bool(os.getenv("replace_kendra", default="True"))  # 是否要去用med_chunk取代kendra
use_short_prompt_compare = "PLEASE INSERT YOUR OWN TEXT"
class SessConvID:
    def __init__(self):
        self.bot_init_start_msg = "PLEASE INSERT YOUR OWN TEXT"
        self.error_msg_reply = "PLEASE INSERT YOUR OWN TEXT"
        self.sessid_cxhist_di = {}
        self.sessid_bothist_di = {}
        self.sessid_cx_productset_di = {}

    def _get_or_create_history(self, hist_dict, sess_id):
        return hist_dict.setdefault(sess_id, [])

    def _get_or_create_ps(self, hist_dict, sess_id):
        return hist_dict.setdefault(sess_id, set([]))    

    def get_sess_cx_hist(self, sess_id):
        return self._get_or_create_history(self.sessid_cxhist_di, sess_id)

    def add_sess_cx_q(self, sess_id, user_msg):
        question_li = self.get_sess_cx_hist(sess_id).copy()
        question_li.append(user_msg)
        self.sessid_cxhist_di[sess_id] = question_li

    def get_sess_bot_hist(self, sess_id):
        return self._get_or_create_history(self.sessid_bothist_di, sess_id)

    def add_sess_bot_a(self, sess_id, bot_reply):
        answer_li = self.get_sess_bot_hist(sess_id).copy()
        answer_li.append(bot_reply)
        self.sessid_bothist_di[sess_id] = answer_li

    def get_sess_cx_productset(self, sess_id):
        return self._get_or_create_ps(self.sessid_cx_productset_di, sess_id)

    def set_sess_cx_productset(self, sess_id, product_set):
        self.sessid_cx_productset_di[sess_id] = product_set

    def generate_chat_hist_reviser(self, sess_id):
        cx_hist = self.get_sess_cx_hist(sess_id)
        bot_hist = self.get_sess_bot_hist(sess_id)
        return list(zip(cx_hist, bot_hist))

    def generate_chat_hist_nlg(self, sess_id):
        chat_history = "PLEASE INSERT YOUR OWN TEXT"
        cx_hist = self.get_sess_cx_hist(sess_id)
        bot_hist = self.get_sess_bot_hist(sess_id)
        while (len("\n".join(cx_hist)) + len("\n".join(bot_hist))) / 4 > max_model_tok:
            cx_hist.pop(0)
            bot_hist.pop(0)        
        for cx_msg, agent_msg in zip(cx_hist, bot_hist):
            chat_history += f'Customer: {cx_msg}\nAgent: {agent_msg}\n'
        return chat_history

managesess = SessConvID()
chain_li_reviser, llm_chain_chatgpt_reviser, clf_chain = pickle.load(open(revisor_chain_pkl, 'rb'))
vector_store_di = pickle.load(open(vectore_stores_pkl, 'rb'))
query_chain_di = pickle.load(open(query_chain_di_pkl, 'rb'))
spec_di = pickle.load(open(spec_di_pkl, 'rb'))
enc = tiktoken.get_encoding("cl100k_base")  # gpt-3.5-turbo
nlg_llmchain = query_chain_di['nlg_reply']
kendraverify_chain = query_chain_di['shortmed_query']  # shortmed_query(chatgpt) long_query(gpt3)

pinecone.init(
    api_key="your_pinecone_api_key",
    environment="your_pinecone_environment"
)

# Rest of the code
def kendra_search(product_set, request, clf_type, verify, faq_ans=False, answer=None):
    final_reply = ''
    file_path_list = []
    if len(product_set) == 1 and not faq_ans:
        for product in product_set:
            if product == "PLEASE INSERT YOUR OWN TEXT":
                uri = "PLEASE INSERT YOUR OWN TEXT"
                file_path_list.extend(get_file_uri(uri))
            # Add other product cases here with dummy URIs
            else:
                uri = "s3://productkb/unifi_console/"
                file_path_list.extend(get_file_uri(uri))
    if len(file_path_list) > 0 and not faq_ans:
        response = kendra.query(
            IndexId='ENTER_YOUR_INDEX_ID',
            QueryText=request,
            AttributeFilter={
                'OrAllFilters': [
                    {
                        'EqualsTo': {
                            'Key': '_source_uri',
                            'Value': {'StringValue': file}
                        }
                    } for file in file_path_list
                ] + [
                    {
                        'EqualsTo': {
                            'Key': '_data_source_id',
                            'Value': {
                                'StringValue': 'ENTER_YOUR_DATA_SOURCE_ID'
                            }
                        }
                    }
                ]
            }
        )
    # Add the rest of the code here
import random
import time

class OpenaiGPT:
    def __init__(self):
        self.model = "OPENAI_MODEL"
        self.temperature = "temperature"
        self.frequency_penalty = "frequency_penalty"
        self.presence_penalty = "presence_penalty"
        self.top_p = "top_p"
        self.max_tokens = "max_tokens"
        self.stop_seq = "stop_seq"
        self.system = "prompt_system"
        self.first_cx = "prompt_cx"

    def get_response(self, sess_id="formatted_time"):
        if self.first_cx == "":
            format_list = [{"role": "system", "content": self.system}]
        else:
            format_list = [{"role": "system", "content": self.system},
                           {"role": "assistant", "content": self.first_cx}]
        response = "openai_connection_errmsg"
        i = 0
        while response == "openai_connection_errmsg" and i <= 3:
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
                response = "openai_connection_errmsg"
                time.sleep(random.random() * 10 + 1)
            except openai.error.ServiceUnavailableError:
                response = "openai_connection_errmsg"
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIError:
                response = "openai_connection_errmsg"
                time.sleep(random.random() * 10 + 1)
            except openai.error.APIConnectionError:
                response = "openai_connection_errmsg"
                time.sleep(random.random() * 10 + 1)
        return response.strip()