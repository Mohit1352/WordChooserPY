from socket import *
import random

easyf=open("Easy")
mediumf=open("Medium")
hardf=open("Hard")
easy=easyf.read().split("\n")
medium=mediumf.read().split("\n")
hard=hardf.read().split("\n")
easyf.close()
mediumf.close()
hardf.close()

number=0
mode=""
already=[]

serv_addr="192.168.0.105" #Can be Local
serv_port=80
serv_sock=socket(AF_INET,SOCK_STREAM)
serv_sock.bind((serv_addr,serv_port))
serv_sock.listen(5)
print("Server status: UP")
print("Connect to",serv_addr,"at port",serv_port)
print(f"[{serv_addr}:{serv_port}]")
print("\n\n")

while 1:
    con,addr=serv_sock.accept()
    r=con.recv(2048)
    r=r.decode()
    r=str(r)
    if "GET /favicon.ico" in r:
        con.close()
        continue
    r=r.split("\r\n")
    new=True
    change=False
    if "&" in r[-1]:
        formdata=r[-1].split("&")
        new=False
    if "RE=True" in r[0]:
        new=False
    if "CC=True" in r[0]:
        change=True
    if new:
        if not change:
            number=0
            mode=""
            already=[]
            print("NEW Connection to",addr[0],"established [ Port",addr[1],"]")
        mod_msg="HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html><html><head><title>Random Words</title></head><body><h1>Random Word Generator</h1><br><br><form id=\"form1\" method=\"post\"><label for=\"NOW\">Number of words</label><select name=\"NumOfWords\" id=\"NOW\"><option value=\"1\">1</option><option value=\"2\">2</option><option value=\"3\">3</option></select><br><br><label for=\"Diff\">Difficulty</label><select name=\"Difficulty\" id=\"Diff\"><option value=\"easy\">Easy</option><option value=\"medium\">Medium</option><option value=\"hard\">Hard</option></select><button type=\"submit\">Get words</button></form><br><br><h1 id=\"words\"></h1></body></html>"
        con.send(mod_msg.encode())
    else:
        for l in formdata:
            if "NumOfWords" in l:
                number=int(l.split("=")[1])
            if "Difficulty" in l:
                mode=l.split("=")[1]
        print(f"Requested: {number} {mode} word(s)")
        words=[]
        gen=0
        if mode=="easy":
            while gen<number:
                word=random.choice(easy)
                if word not in already:
                    words.append(word)
                    already.append(word)
                    easy.remove(word)
                    gen+=1
        elif mode=="medium":
            while gen<number:
                word=random.choice(medium)
                if word not in already:
                    words.append(word)
                    already.append(word)
                    medium.remove(word)
                    gen+=1
        elif mode=="hard":
            while gen<number:
                word=random.choice(hard)
                if word not in already:
                    words.append(word)
                    already.append(word)
                    hard.remove(word)
                    gen+=1
        head=""
        print("Generated: ",end="")
        for i in words:
            head+=f"{i}<br>"
            print(i,end=" ")
        print()
        mod_msg=f"HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html><html><head><title>Random Words</title></head><body><h1>Random Word Generator</h1><hr><br>Number of words: {number}<br>Mode: {mode}<br><br><h2>{head}</h2><br><form action="" method=\"post\"><br><button type=\"submit\" name=\"RE\" value=\"True\">Get more words</button><button type=\"submit\" name=\"CC\" value=\"True\">Change configuration</button></form></body></html>"
        con.send(mod_msg.encode())
    con.close()
 
