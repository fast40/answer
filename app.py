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
            {"role": "system", "content": "Respond to the user's question with a very short response."},
            {
                "role": "user",
                "content": data['prompt']
            }
        ]
    )

    response = completion.choices[0].message.content
    response = response.removeprefix('```html').removesuffix('```')

    return response.replace('\n', '<br>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

