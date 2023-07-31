from django.shortcuts import render

# Create your views here.
# gptapp/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from gptapp.models import genip_db, freecount
from .geheim import schluessel
from .promlist import *
import time
from datetime import datetime

import openai
import requests
import tiktoken

openai.api_key = schluessel  # genIP Key값

MAX_TOKENS = 8192 - 3000 #테스트 결과값으로 바꿔주세요
THRESHOLD_TOKENS = 2000 #테스트 결과값으로 바꿔주세요

#토큰 카운트
tokenizer = tiktoken.get_encoding("cl100k_base")
tokenizer = tiktoken.encoding_for_model("gpt-4-0613") # "버전 변경 방법 고민
def count_tokens(text):
    return len(tokenizer.encode(text))

MAX_RETRIES = 3 # 재시도 횟수?

#index는 django가 최초로 실행하는 함수
def index(request):
    ### 아직 구현하지 않은 것
    total = ''
    abstract = ''
    article = ''
    description = ''
    lang = 'ko'
    ### 미구현 끝

    # 무료 횟수 계산기
    used = genip_db.objects.filter(username=request.user.username).count()
    free_total = 3 #무료 제공 횟수
    if used >= free_total:
        freecount = 0
    else:
        freecount = free_total - used

    if request.POST:  # POST로 입력값을 받은 경우

        question = request.POST['question'].strip() 
        if question == '': # 입력값이 공란인 경우 에러처리를 위해서
            start_time = time.time() #왼쪽 청구항 시간 계산용인데 deprecate 예정
            output1 = '입력값이 없습니다.' #왼쪽 청구항 따로 나오던 것인데 deprecate 예정
            duration1 = time.time() - start_time #왼쪽 청구항 시간 계산용인데 deprecate 예정
            start_time = time.time()
            output2 = '입력값이 없습니다.'
            duration2 = time.time() - start_time
            input_tokens = 0
            total_tokens = 0

        else: #입력값이 공란이 아닐 때 실행하기
            input_tokens = count_tokens(question)
            total_tokens = 0
            start_time = time.time() #왼쪽 청구항 시간 계산용인데 deprecate 예정
            #output1 = GenIP_final(question, system_article)  #왼쪽 청구항 따로 나오던 것인데 deprecate 예정
            output1 = '' #왼쪽 청구항 따로 나오던 것인데 deprecate 위해 공란 처리
            duration1 = time.time() - start_time #왼쪽 청구항 시간 계산용인데 deprecate 예정
            start_time = time.time()
            output2 = GenIP(question) #테스트
            duration2 = time.time() - start_time

        ip = get_client_ip(request)
        param = request.POST['param']
        if param == '정확':
            temperature = 0.0
        elif param == '창의':
            temperature = 0.7
        else:
            temperature = 0.5
        db_save(request.POST['username'], request.POST['question'].strip(), question, output1, duration1, output2, duration2, ip, temperature, total_tokens, input_tokens)
    else:  # 첫화면인 경우
        param = '보통'
        question = ''
        output1 = ''
        output2 = ''


    context = {
        'param': param,
        'question': question,
        'left': output1,
        'right': output2,
        'q_default': 'Enter your Idea',
        'l_default': '청구항',
        'r_default': '특허 명세서',
        'total': total,
        'abstract': abstract,
        'article': article,
        'description': description,
        'freecount': freecount,
        'used': used,

    }

    return render(request, 'gptapp/index.html', context)

def GenIP_final(prompt, system):

    response = complete_specification(system, prompt)
    return response

parts = {
    1: GenIP_final,
    2: GenIP_final,
    3: GenIP_final,
    4: GenIP_final,
    5: GenIP_final,
    6: GenIP_final,
    7: GenIP_final,
    8: GenIP_final
}

def GenIP(question):
    total_response = ''
    for part in range(1, 9):
        response = gpt_query(question, specifications[part - 1])
        if "작성완료" in response:
            response = response.replace("작성완료", "")
        total_response += response + '\n'
    return total_response

def summarize_input(long_input): #요약기
    tokens = tokenizer.encode(long_input)
    chunks = []
    current_chunk = []

    for token in tokens:
        if len(current_chunk) + 1 > THRESHOLD_TOKENS:
            chunks.append(tokenizer.decode(current_chunk))
            current_chunk = []

        current_chunk.append(token)

    if current_chunk:
        chunks.append(tokenizer.decode(current_chunk))

    i = 0
    summarized_text = ""
    for chunk in chunks:
        i += 1
        summary_prompt = chunk
        print(f'({i}) Summarizing chunk {i}...')
        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": 'Summarize the following text, remaining the main keywords, and maintaining all the important contexts. Place the important terms, ideas, and contents in the beginning or the first half of the summary. If the title is estimated to be provided, copy the exact title in the beginning of the summary.'},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.0
        )
        summarized_text += result['choices'][0]['message']['content']

    summarized_text_tokens = tokenizer.encode(summarized_text)
    summarized_text_tokens = summarized_text_tokens[:8191] # E: This model's maximum context length is 8192 tokens. However, your messages resulted in 8192 tokens.
    summarized_text = tokenizer.decode(summarized_text_tokens)

    return summarized_text



def gpt_query(question, prompt, type='spec', temperature=0.5, model='gpt-4'):
    total_tokens = count_tokens(question+prompt)
    if total_tokens > MAX_TOKENS:
        question = summarize_input(question) #요약 1회
    response = ""
    retries = MAX_RETRIES

    while True:
        try:
            msg = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ]
            if type == 'spec':
                msg.append({"role": "assistant", "content": response})
            result = openai.ChatCompletion.create(
                model=model,
                messages=msg,
                temperature=temperature,
                request_timeout=600,
            )
            response += result['choices'][0]['message']['content']

            if "작성완료" in result['choices'][0]['message']['content']:
                response = response.split('작성완료')[0]
                break

        except openai.error.APIError as e:
            response += f"An error occurred: {e}"
            break

        except openai.error.AuthenticationError as e:
            response += f"Authentication error: {e}"
            break

        except openai.error.RateLimitError as e:
            response += f"Rate limit exceeded. Waiting for 5 seconds..."
            time.sleep(5)
            continue

        except openai.error.Timeout as e:
            response += f"Request timed out. Retrying..."
            continue

        except Exception as e:
            response += f"An error occurred: {e}"
            break

    return response


def get_client_ip(request): #클라이언트의 IP 받아오는 함수
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def db_save(username, question, summary, output1, duration1, output2, duration2, ip, temperature, total_tokens, input_tokens): #DB에 저장하기... 무얼 저장할지 논의 후 정리해야 됨 + django 모델 업데이트
    d = genip_db(username=username, input=question, summary=summary, output_1st=output1, duration1=duration1, output_2nd=output2,
                 duration2=duration2, ip=ip, temperature=temperature,
                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), token_total=total_tokens, token_input=input_tokens,)
    d.save()
