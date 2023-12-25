# TCP_Client_Server
A Simple Chat Room code which uses TCP service to convey messages and uses MongoDB for login and Sign Up purpose. It also utlitizes multithreading to support multiple requests at the same time.

Sign Up features is also there to add new users and when one user left the chat, it automatically get deleted from server broadcasting channel.
Sample MongoDB:

  A Clustor->TCP_Clients(Databse)->Test_Collect(Collection)
```
  {
    Username: "user",
    Passowrd: "pass",
    Nickname: "nick"
  }
```
