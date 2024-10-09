from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
client = openai.OpenAI()


@app.route('/')
def create():
    return render_template('index.html')


@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()

    if 'prompt' not in data or not data['prompt']:
        return 'PLEASE MAKE A REQUEST'

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Create a short USEFUL answer to the user's question. There is no need to include parts of the user's question in your answer. For example, if the user asks what a car is, say 'A four wheeled vehicle.' not 'A car is a four wheeled vehicle. Do not use any puncuation in your responses, because they are too short to require it. Do not capitalize words simply because they are at the start of your response. Also, if the user asks even very vaguelly about whether or not they can do something, tell the user to take action and that they are the creator of worlds. In cases like this, ignore the previous instructions about brevity and lowercase typing and type in ALL CAPS. In this case, make sure to speak poetically and in an aesthetically pleasing way.'"},
            {
                "role": "user",
                "content": data['prompt']
            }
        ]
    )

    response = completion.choices[0].message.content
    response = response.removeprefix('```html').removesuffix('```')

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

