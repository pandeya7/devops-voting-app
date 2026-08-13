from flask import Flask, render_template_string, request
import redis
import os

app = Flask(__name__)

# Connect to Redis using environment variables (standard K8s practice)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps K8s Voting App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .card { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        button { padding: 10px 20px; font-size: 16px; margin: 10px; cursor: pointer; border: none; border-radius: 5px; color: white; }
        .cat { background-color: #4CAF50; }
        .dog { background-color: #008CBA; }
        .results { margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 DevOps K8s Voting App</h1>
        <p>Vote for your favorite mascot running on K3s!</p>
        <form method="POST">
            <button class="cat" type="submit" name="vote" value="Cats">🐱 Vote Cats</button>
            <button class="dog" type="submit" name="vote" value="Dogs">🐶 Vote Dogs</button>
        </form>
        <div class="results">
            <h3>Current Results</h3>
            <p><strong>Cats:</strong> {{ cats }} | <strong>Dogs:</strong> {{ dogs }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vote = request.form.get('vote')
        if vote in ['Cats', 'Dogs']:
            r.incr(vote)
    
    cats = r.get('Cats') or 0
    dogs = r.get('Dogs') or 0
    return render_template_string(HTML_TEMPLATE, cats=cats, dogs=dogs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
