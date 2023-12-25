import socket
import threading
import pymongo

def findFromMongoDB(client, username, password):
    if collection.find_one({"Username": username, "Password": password})!=None:
        client.send(("Found "+collection.find_one({"Username": username, "Password": password}).get('Nickname')).encode('ascii'))
        usernames.append(collection.find_one({"Username": username, "Password": password}).get('Username'))
        nicknames.append(collection.find_one({"Username": username, "Password": password}).get('Nickname'))
        clients.append(client)
        return 1
    else:
        client.send("Not found".encode('ascii'))
        return 0

def clientThread(client):
    try:
        while True:
            received_data = client.recv(1024).decode('ascii')
            #A command
            breaked_data = received_data.split('~')
            if breaked_data[0] == '/from':
                i = 0
                for eachClient in clients:
                    if usernames[i] != breaked_data[1]:                    
                        eachClient.send(('/from~'+breaked_data[2]+'~'+breaked_data[3]).encode('ascii'))
                    i = i + 1
    except Exception as error:
        if error.args[0] == 10054:
            deletedIndex = clients.index(client)
            usernames.pop(deletedIndex)
            clients.pop(deletedIndex)
            nicknames.pop(deletedIndex)

def signUpFromMongoDB(client, username, password, nickname):
    if collection.find_one({"Username": username})!=None:
        return None
    else:
        collection.insert_one({"Username": username, "Password": password, "Nickname":nickname})
        usernames.append(username)
        nicknames.append(nickname)
        clients.append(client)
        return 1

def Receive():
    while True:
        client, address = server.accept()
        received_data = client.recv(1024).decode('ascii')
        #A command
        breaked_data = received_data.split('~')
        #Login Command
        if breaked_data[0] == '/login':
            output = findFromMongoDB(client, breaked_data[1], breaked_data[2])
            if output==1:
                client_Thread = threading.Thread(target=clientThread, args={client})
                client_Thread.start()
        elif breaked_data[0] == '/signup':    #SignUp Command
            output = signUpFromMongoDB(client, breaked_data[1], breaked_data[2], breaked_data[3])
            if output==1:
                client.send(('Created '+breaked_data[3]).encode('ascii'))
                client_Thread = threading.Thread(target=clientThread, args={client})
                client_Thread.start()
            
                
                    
if __name__=='__main__':
    #initilizing MongoDB
    mongoClient = pymongo.MongoClient('Your MongoDB Connect Link here')
    db = mongoClient['TCP_Clients']
    collection = db['Test_Collect']
    
    #initilizing socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9090))
    server.listen()

    #To store all usernames and nicknames who are active
    usernames = []
    nicknames = []
    clients = []

    #Continously receive data
    receiving_thread = threading.Thread(target=Receive)
    receiving_thread.start()
