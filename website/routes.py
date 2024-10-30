# from email import message
# from urllib import response
from flask import Blueprint, render_template
from flask import request
from .models import Result
import openai
from os import environ
from dotenv import load_dotenv

load_dotenv()
routes = Blueprint('routes', __name__)
openai.api_key = environ.get('OPENAI_API_KEY')
completion = openai.Completion()
historyData = []


@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        query = request.args.get('query')
        print(query)
        if query == "" or query is None:
            return render_template('response_view.html')
        response = ask(query)
        dataList = []
        queryMessage = Result(time="This Time", messagetype="other-message float-right", message=query)
        responseMessage = Result(time="This time", messagetype="my-message", message=response)
        dataList.append(queryMessage)
        dataList.append(responseMessage)
        historyData.append(queryMessage)
        historyData.append(responseMessage)
        return render_template('response_view.html', results=dataList)
    else:
        return render_template('history.html', results=historyData)


def ask(question, chat_log=None):
    prompt = f'{chat_log}Query: {question}\n Answer:'
    response = completion.create(
        prompt=prompt, engine="gpt-4o-mini", stop=['\nQuery'],
        temperature=0.9, top_p=1, frequency_penalty=0, presense_penalty=0.6,
        best_of=1, max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer
