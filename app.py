from flask import Flask, request, jsonify, render_template
from ai71 import AI71

app = Flask(__name__)

AI71_API_KEY = "api71-api-2fcb29da-a589-4632-9e26-47a71786cd25"

@app.route('/')
def landing():
    return render_template('landing1.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/output')
def output():
    return render_template('output.html')

@app.route('/api/get_hints', methods=['POST'])
def get_hints():
    data = request.json
    problem = data.get('problem')
    problem_type = data.get('type', 'Unknown')

    if not problem:
        return jsonify({'error': 'No problem provided'}), 400

    response = ""
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant for {problem_type} problems. Dont give teh exact answer first and  provide meaningful responses only to highly valid queries and dont give resoponse to non-sensical or irrelevant inputs just say sorry it is irreelvant question"
            },
            {
                "role": "user",
                "content": problem + ''' Dont give the direct answer. The answer you give must have the following sections:

                    1. Give hints to solve the question but do not give the coding solution. After it, give a two-line space.

                    2. Provide some real-world examples. Give only one example to explain it. Don't give the code. After it, give a two-line space.

                    3. Give some more hints that enhance the self-learning of the user. After it, give a two-line space.

                    4. Provide the {problem_type} solution to the question. After it, give a two-line space.

                    5. Mention the topic name to study to understand the question.
                    '''
            },
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content

    x = response.split("\n\n")
    hints = {
        'hint1': x[0] if len(x) > 0 else "",
        'hint2': x[1] if len(x) > 1 else "",
        'hint3': x[2] if len(x) > 2 else "",
        'hint4': "\n".join(x[3:-1]) if len(x) > 4 else "",
        'hint5': x[-1] if len(x) > 4 else ""
    }

    return jsonify(hints)



if __name__ == '__main__':
    app.run(debug=True)

