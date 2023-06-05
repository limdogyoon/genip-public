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

openai.api_key = schluessel  # genIP


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

    if request.POST:  # 입력값을 받은 경우

        question = request.POST['question'].strip() 
        if question == '': # 입력값이 공란인 경우
            start_time = time.time()
            output1 = '입력값이 없습니다.'
            duration1 = time.time() - start_time
            start_time = time.time()
            output2 = '입력값이 없습니다.'
            duration2 = time.time() - start_time

        else:
            start_time = time.time()
            #output1 = GenIP(question, system_exp, type='abst')  # 왼쪽 아웃풋. 요약
            output1 = GenIP(question, system_article, type='abst')  # 왼쪽 아웃풋. 청구항
            #output1 = question + " 기능 끔"
            duration1 = time.time() - start_time
            start_time = time.time()
            output2 = GenIP(question, system_rulebased, type='spec') #오른쪽 아웃풋
            #output2 = question + " 기능 끔"
            duration2 = time.time() - start_time
        ip = get_client_ip(request)
        param = request.POST['param']
        if param == '정확':
            temperature = 0.0
        elif param == '창의':
            temperature = 0.7
        else:
            temperature = 0.5
        db_save(request.POST['username'], question, output1, duration1, output2, duration2, ip, temperature)
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

def GenIP(prompt, system_intel=system_exp, temperature=0.5, model='gpt-4', type='abst'):
    response = ""
    msg = [
        {"role": "system", "content": system_intel},
        {"role": "user", "content": prompt}
    ]
    if type == 'spec':
        msg.append({"role": "assistant", "content": response})
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=msg,
 #       temperature=temperature,
 #       request_timeout=600,
    )
    response += result['choices'][0]['message']['content']
    return response



def Gen2IP(prompt, system_intel=system_rulebased, temperature=0.5, model='gpt-4', type=''):
    response = ""
    while True:
        try:
            msg = [
                {"role": "system", "content": system_intel},
                {"role": "user", "content": prompt}
            ]
            if type == 'spec':
                msg.append({"role": "assistant", "content": response})
            result = openai.ChatCompletion.create(
                model="gpt-4",
                messages=msg,
                temperature=temperature,
                request_timeout=600,
            )
            response += result['choices'][0]['message']['content']

            if result['choices'][0]['message']['content'] != "":
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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def db_save(username, question, output1, duration1, output2, duration2, ip, temperature):
    d = genip_db(username=username, input=question, output_1st=output1, duration1=duration1, output_2nd=output2,
                 duration2=duration2, ip=ip, temperature=temperature,
                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), )
    d.save()
