
import sys, socket, select
import MySQLdb
import getpass
def daftar():
    db = MySQLdb.connect("localhost", "root", "password","progjar_chat")
    cursor =db.cursor()
    print "Daftar akun!"
    username = raw_input ("Input username: ")
    password = getpass.getpass ("Input password : ")
    sql ="INSERT INTO user (username,password) VALUES ('%s','%s')"%(username, password)
    cursor.execute(sql)
    db.commit()
    db.close()

def cekpwd(username, password):

    db = MySQLdb.connect("localhost", "root", "password","progjar_chat")
    cursor =db.cursor()
    sql ="SELECT * FROM user WHERE username = '%s' AND password = '%s'"%(username, password)
    cursor.execute(sql)
    cek = cursor.rowcount
    if cek == 1:
        return 1
    else:
        return 0

def chat_client():
    if(len(sys.argv) < 3) :
        print 'Format: python chat_client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    while True:
        print "\nKetik 1 untuk pendaftaran member baru"
        print "Ketik 2 untuk login,"
        print "Ketik logout untuk keluar"
        pilihan = raw_input ("Masukan pilihan : ")
        if pilihan == "1":
            daftar()
            return
        elif pilihan == "2":
            print "Login member"
            username = raw_input ("Username: ")
            password = getpass.getpass ("Password : ")
            cek = cekpwd(username, password)
                s.connect((host, port))
                print 'Berhasil melakukan koneksi! Selamat datang ' + username + '! Sekarang and bisa mengirim pesan!' 
                sys.stdout.write(username+"=> "); sys.stdout.flush()
                while True:
                    socket_list = [sys.stdin, s]
                     
                    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
                     
                    for sock in read_sockets:        

                        if sock == s:
                            data = sock.recv(4096)
                            if not data :
                                print '\nDisconnected from chat server'
                                sys.exit()
                            else :
                                sys.stdout.write(data)
                                sys.stdout.flush() 
                                    
                        
                        else :
                            msg = sys.stdin.readline()
                            if msg == 'logout\n':
                                s.send(username + ' telah logout :(')
                                exit()
                            else :
                                msg2 = username +"=> " + msg
                                s.send(msg2)
                                sys.stdout.write(username+"=> ")
                                sys.stdout.flush()
            else :
                print "Login tidak berhasil, username/password salah!"     

if __name__ == "__main__":

    sys.exit(chat_client())