from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Security Demo: Vulnerable App is Live!</h1>"

@app.route('/login', methods=['GET'])
def login():
    # SECURITY ISSUE: Hardcoded password demo
    password = "SuperSecretPassword123"
    user_pass = request.args.get('password')
    
    if user_pass == password:
        return "Access granted"
    else:
        return "Access denied (Try /login?password=...)"

@app.route('/run', methods=['GET'])
def run_command():
    # SECURITY ISSUE: Command Injection demo
    # Usage: /run?cmd=ls
    user_input = request.args.get('cmd')
    
    if user_input:
        try:
            # We use check_output to see the result in the browser
            output = subprocess.check_output(user_input, shell=True, stderr=subprocess.STDOUT)
            return f"<pre>{output.decode('utf-8')}</pre>"
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode('utf-8')}"
    return "Please provide a command (e.g., /run?cmd=ls)"

if __name__ == "__main__":
    # CRITICAL: This allows the container to be reached from outside
    app.run(host='0.0.0.0', port=5000)