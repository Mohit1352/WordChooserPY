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
serv_port=800
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
        try:
            favicon=open("favicon.ico","rb")
            favimg=favicon.read()
            favicon.close()
            con.send(favimg)
        except:
            pass
        con.close()
        continue
    r=r.split("\r\n")
    new=True
    change=False
    if "&" in r[-1]:
        formdata=r[-1].split("&")
        new=False
    if "RE=True" in r[-1]:
        new=False
    if "CC=True" in r[-1]:
        change=True
    if new:
        if not change:
            number=0
            mode=""
            already=[]
            print("NEW Connection to",addr[0],"established [ Port",addr[1],"]")
        firstpg=open("firstpage.html","r")
        mod_msg=firstpg.read()
        firstpg.close()
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
        genpage=open("genpage.html","r")
        mod_msg=genpage.read().format(number=number,mode=mode,head=head)
        con.send(mod_msg.encode())
    con.close()
 
