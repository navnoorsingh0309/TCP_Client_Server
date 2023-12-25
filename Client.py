import socket
import threading

username = ''
nickname = ''

def send(data):
    client.send(data.encode('ascii'))

def Receive(respone_type):
    while True:
        received_data = client.recv(1024).decode('ascii')
        if respone_type == 'Server_login_response':
            if  received_data.split(' ')[0] == 'Found':
                print('Welcome '+received_data.split(' ')[1])
                return received_data.split(' ')[1]
            else:
                print('No User Found!! Please signUp')
                return None
        elif respone_type == 'Chat_Room':
            #A command
            breaked_data = received_data.split('~')
            if breaked_data[0] == '/from':
                print(breaked_data[1]+"~"+breaked_data[2])
        elif respone_type == 'Server_signup_response':
            if  received_data.split(' ')[0] == 'Created':
                print('Welcome '+received_data.split(' ')[1])
                return received_data.split(' ')[1]

def login():
    #login
    usernameL = input("Enter Username:")
    passwordL = input("Enter Password:")
    ##Sendind data to server to be checked if valid
    data_to_send = '/login~'+usernameL+'~'+passwordL
    send(data_to_send)
    output = Receive('Server_login_response')
    if output != None:
        return [usernameL, output]
    else:
        return None

def broadcastingMessage():
    while True:
        message = input("")
        send('/from~'+username+'~'+nickname+'~'+message) 
        

def startChatRoom(username, nickname):
    print('Joining Chat Room!!')
    receicing_Thread = threading.Thread(target=Receive, args={'Chat_Room'})
    receicing_Thread.start()
        
    #Getting message to broadcast
    broadcasting_Thread = threading.Thread(target=broadcastingMessage)
    broadcasting_Thread.start()
    

def signUp():
    #signUp
    usernameS = input("Enter Username:")
    passwordS = input("Enter Password:")
    nicknameS = input("Enter Your NickName:")
    data_to_send = '/signup~'+usernameS+'~'+passwordS+'~'+nicknameS
    send(data_to_send)
    output = Receive('Server_signup_response')
    if output != None:
        return [usernameS, output]
    else:
        return None
    
if __name__=='__main__':
    #socket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9090))
    
    #login/signup
    print("1. Login")
    print("2. SignUp")
    cmd = input("Enter Command(1/2):")
    if cmd=='1':
        loginOutput = login()
        if loginOutput != None:
            username = loginOutput[0]
            nickname = loginOutput[1]
            startChatRoom(username, nickname)
    else:
        signUpOutput = signUp()
        if signUpOutput != None:
            username = signUpOutput[0]
            nickname = signUpOutput[1]
            startChatRoom(username, nickname)
