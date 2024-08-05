from flask import Flask, request, jsonify, render_template
from ai71 import AI71
import traceback

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

def get_ai_response(prompt, option):
    try:
        response = ""
        for chunk in AI71(AI71_API_KEY).chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant for {option} problems. Don't give the exact answer first and provide meaningful responses only to highly valid queries and don't give response to non-sensical or irrelevant inputs just say sorry it is irrelevant question"
                },
                {
                    "role": "user",
                    "content": prompt + f'''Don't give the direct answer. The answer you give must have the following sections:
                    1. Give hints to solve the question but do not give the coding solution. After it, give a two-line space.
                    2. Provide some real-world examples. Give only one example to explain it. Don't give the code. After it, give a two-line space.
                    3. Give some more hints that enhance the self-learning of the user. After it, give a two-line space.
                    4. Provide the {option} solution to the question. After it, give a two-line space.
                    5. Mention the topic name to study to understand the question.
                    '''
                },
            ],
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        return response
    except Exception as e:
        print(f"An error occurred while fetching the AI response: {str(e)}")
        return None

@app.route('/api/get_hints', methods=['POST'])
def get_hints():
    try:
        data = request.json
        problem = data.get('problem')
        problem_type = data.get('type', 'Unknown')

        if not problem:
            return jsonify({'error': 'No problem provided'}), 400

        ai_response = get_ai_response(problem, problem_type)
        
        if ai_response:
            x = ai_response.split("\n\n")
            hints = {
                'hint1': x[0] if len(x) > 0 else "",
                'hint2': x[1] if len(x) > 1 else "",
                'hint3': x[2] if len(x) > 2 else "",
                'hint4': "\n".join(x[3:-1]) if len(x) > 4 else "",
                'hint5': x[-1] if len(x) > 4 else ""
            }
            return jsonify(hints)
        else:
            return jsonify({'error': 'Failed to get AI response'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
