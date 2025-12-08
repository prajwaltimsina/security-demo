import os
import subprocess

def run_command(user_input):
    # SECURITY ISSUE: using subprocess with shell=True is dangerous and is security issue.
    # This will allow command injection
    subprocess.call(user_input, shell=True)

def login():
    # SECURITY ISSUE: Hardcoded password
    password = "SuperSecretPassword123"
    
    user_pass = input("Enter password: ")
    if user_pass == password:
        print("Access granted")
    else:
        print("Access denied")

if __name__ == "__main__":
    login()