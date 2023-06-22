from flask import Flask, render_template, request, redirect, session
from pyaiml21 import Kernel
from googleapiclient.discovery import build
from neo4j import GraphDatabase
import glob
import requests
import nltk
from autocorrect import Speller
import string
import socket
import requests
import webbrowser

ip_returns = ''
username2 = ''
ip_returns2 = ''
user_name = ''
def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_subnet():
    str1 = ip_address()
    str2 = ''
    i = 0
    for x in range(len(str1)):
        if str1[x] == '.':
            str2 += str1[x]
            i += 1
        elif i == 3:
            break
        else:
            str2 += str1[x] 
    return str2

def nltk_correct(message):
    messageToReturn = ''
    if '-' in message or '+' in message:
        messageToReturn = message
    else :
        message = message.lower()
        message = message.translate(str.maketrans("", "", string.punctuation))
        tokenizer = nltk.sent_tokenize(message)
        spell = Speller()
        corrected_tokenizer = []
        for sentence in tokenizer:
            words = nltk.word_tokenize(sentence)
            corrected_words = [spell(w) for w in words]
            corrected_sentence = " ".join(corrected_words)
            corrected_tokenizer.append(corrected_sentence)
        autocorrected_message = " ".join(corrected_tokenizer)
        messageToReturn = autocorrected_message
    return messageToReturn

def getIP_from_Datebase(tx, username):
    query = f"MATCH (User) WHERE User.username = '{username}' RETURN User.subnet"
    result = tx.run(query)
    record = result.single()
    if record:
        return record[0]
    else:
        return False

def runner_ip_database(username):
    with driver.session() as session:
        return session.read_transaction(getIP_from_Datebase, username)
    
def get_second_username(tx, username,ip):
    query = f"MATCH (User) WHERE User.username <> '{username}' and User.subnet = '{ip}' RETURN User.username"
    result = tx.run(query)
    record = result.single()
    if record:
        return record[0]
    else:
        return False

def runner_username_second(username,ip):
    with driver.session() as session:
        return session.read_transaction(get_second_username, username,ip)
    
def create_social_network(tx, username, friend_name):
    username = username.lower()
    friend_name = friend_name.lower()
    query = """
    MATCH (a:User {username: $username}), (b:User {username: $friend_name})
    CREATE (a)-[r:Friend_OF]->(b)
    RETURN r
    """
    result = tx.run(query, username=username, friend_name=friend_name)
    record = result.single()
    return record['r'] if record else None


def check_social_network(username, friend_name):
    with driver.session() as session:
        return session.write_transaction(create_social_network, username, friend_name)



app = Flask(__name__)
app.secret_key = 'talha'

# Initialize the AIML kernel
myBot = Kernel()

# Learn AIML files
for data in glob.glob("/home/talha/Chat_Bot/Easy-Chatbot-master/AIML_FILES/*.aiml"):
    myBot.learn(data)

# Neo4j connection details
uri = "bolt://localhost:7687"  # Replace with your Neo4j connection URI
user = "neo4j"         # Replace with your Neo4j username
password = "talha1234"     # Replace with your Neo4j password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))

# Login status (assuming default as False)
logged_in = False

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    global logged_in
    global ip_returns
    global username2
    global ip_returns2
    global user_name
    global choices

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_name = username
        ip_returns = runner_ip_database(username)
        username2 = runner_username_second(username,ip_returns)
        ip_returns2 = runner_ip_database(username2)
        

        # Authenticate user in Neo4j
        with driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username, password: $password}) RETURN COUNT(u) AS count",
                username=username,
                password=password,
            )
            count = result.single()["count"]

        if count == 1:
            logged_in = True
            return redirect("/")
        else:
            return redirect("/login")

    return render_template("login.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    global logged_in

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        subnet = get_subnet() 
        # Create user in Neo4j
        with driver.session() as session:
            session.run(
                "CREATE (u:User {username: $username, password: $password , subnet: $subnet})",
                username=username,
                password=password,
                subnet=subnet
            )

        logged_in = True
        return redirect("/login")

    return render_template("signup.html")

@app.route("/")
def home():
    if logged_in:
        return render_template("base.html")
    else:
        return redirect("/login")

@app.route("/get")
def get_bot_response():
    global username2
    global user_name
    counter = session.get('counter',0)
    query = request.args.get('msg')
    if "talha" or "Talha" in query:
        query = query
    else:
        query = nltk_correct(query)
    if "ip" in query:
        response = ip_address()
    if "subnet" in query:
        response = get_subnet()
    elif counter == 1 and ip_returns == ip_returns2:
        response = f"hey did you know who is {username2}"
    elif "he is my friend" in query:
        user_name = user_name.replace(" ", "")
        username2 = username2.replace(" ", "")
        check_social_network(user_name, username2)
        response = f" O {user_name} is friend of {username2}"
    elif "write" in query or "fix" in query or "tell" in query:
        response = get_completion(query)
    elif "Play" in query or "play" in query:
        response =search_and_play_video(query)
    elif "what's your name" in query or"what is your name" in query or"What is Your Name" in query or "your name" in query or "Your Name" in query:
        response = "My name is Al Haqqani " or "My name is AI_Chat_bot"
    else:
        response = myBot.respond(query, "talha")
    if response:
         counter+=1
         session['counter'] = counter
         return str(response)
    else:
        return ":)"
    
import requests
def get_completion(message):
    url = "https://free.churchless.tech/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    completion = data['choices'][0]['message']['content']
    return completion.strip()


def search_and_play_video(message):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": message,
        "type": "video",
        "key": "AIzaSyB8nk3--gIZ5D53D7xI8CjJSZIq7b80uVE"
    }
    response = requests.get(url, params=params)
    data = response.json()
    video_ids = []
    if 'items' in data:
        for item in data['items']:
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])
    if video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        webbrowser.open(video_url)
        return True
    return False


# Run the Flask application
if __name__ == "__main__":
    app.run(port='8080')
