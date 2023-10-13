import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
questions = ["In which field, Oscar awards are distributed? \n a.Sports\n b.Cinema\n c.Studies\n d.Technology",
             "Which one of the following river flows between Vindhyan and Satpura ranges? \n a.Narmada\n b.Mahanadi\n c.Son\n d.Netravati",
             "Who among the following wrote Sanskrit grammar? \n a.Kalidasa\n b.Charak\n c.Panini\n d.Aryabhatt",
             "The metal whose salts are sensitive to light is? \n a.Zinc\n b.Silver\n c.Copper\n d.Aluminum",
             "The hottest planet in the solar system? \n a.Mercury\n b.Jupiter\n c.Mars\n d.Venus",
             "Which institution launched the ‘Digital Shakti Campaign 4.0’ Campaign? \n a.NITI Aayog\n b.National Commission for Women\n c.Ministry of Women and Child Development\n d.World Economic Forum",
             "Which state adopted a bill to make its language compulsory for State government jobs? \n a.Maharashtra\n b.Karnataka\n c.Tamil Nadu\n d.Kerala",
             "Kuchipudi dance is of which state? \n a.Kerela\n b.Manipur\n c.Arunachal Pradesh\n d.Andhra Pradesh",
             "Which is largest island in the world? \n a.Greenland\n b.Madagascar\n c.Sumatra\n d.Baffin",
             "which planet has longest rotation period? \n a.Jupiter\n b.Neptune\n c.Venus\n d.Uranus"]
answers = ['b','a','c','b','d','b','c','d','a','c']
nicknames = []

print("Quiz has started..")

def clientthread(conn, nickname): 
    score = 0 
    conn.send("Welcome to this quiz game!".encode('utf-8')) 
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d!\n".encode('utf-8')) 
    conn.send("Good Luck!\n\n".encode('utf-8')) 
    index, question, answer = get_random_question_answer(conn) 
    print(answer) 
    while True: 
        try: 
            message = conn.recv(2048).decode('utf-8') 
            if message: 
                if message.split(": ")[-1].lower() == answer:
                    score += 1 
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8')) 
                else:
                    conn.send(f"Incorrect answer! Better luck next time!\n\n".encode('utf-8')) 
                remove_question(index) 
                index, question, answer = get_random_question_answer(conn) 
                print(answer) 
            else: 
                remove(conn) 
                remove_nickname(nickname) 
        except Exception as e: 
            print(str(e)) 
            continue 

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname +" connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
