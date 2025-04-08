from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/signup',methods=['GET'])
def signUpPage():
    return render_template("signup.html")

@app.route('/signup/user',methods=['POST'])
def signUp():
    pass

if (__name__ == "__main__"):
    app.run()