import socket

HOST = '0.0.0.0'
PORT = 1234
LENGTH_MASK = 0xf
TYPES = ['S', 'I']

binds = []

def count(filename):
    tdb = open(filename, 'r')
    count = len(tdb.readlines()) - 1
    tdb.close()
    return count

def clean(stmt):
    # remove comments and validate syntax
    stmt = stmt.split('#')[0]
    if len(stmt) < 1: return 'err', b'e:nullstmt', stmt
    if (queryType := stmt[0]) not in TYPES: return 'err', b'e:querytype', stmt
    if stmt.count(':') > 2 or stmt.count(':') < 1: return 'err', b'e:syntaxerror', stmt
    return 'clean', queryType, stmt


def getQuery(query):
    stmt = query.decode('ascii')
    print (stmt)
    
    cleaned, val, stmt = clean(stmt)
    if cleaned == 'err': return val
    else: queryType = val

    params = stmt[2:].split(':')
    lookupType = len(params)
    if lookupType == 1: userId = params[0]
    else: user,pw = params

    print (lookupType, params)

    # select 
    if queryType == 'S':
        tdb = open('users.tdb', 'r')
        
        results = []
        for line in tdb.readlines():
            tdb_id, tdb_user, tdb_pw = line.split(':')
            tdb_pw = tdb_pw.strip('\n')
            idCheck = (lookupType == 1 and userId == tdb_id) 
            userCheck = (lookupType == 2 and user == tdb_user and pw == tdb_pw)
            if idCheck or userCheck:
                results = [tdb_id, tdb_user, tdb_pw]
                final = f"r:{tdb_id}:{tdb_user}:{tdb_pw}"
                return final.encode('ascii')
        tdb.close()
        return b'r:'
    
    # insert
    if queryType == 'I':
        userId = count('users.tdb')
        tdb = open('users.tdb', 'a')    
        tdb.write(f"{userId}:{user}:{pw}\n")
        tdb.close()
        return b'r:'
    
    return b'e:idk'

def prepareQuery(query):
    stmt = query.decode('ascii')
    global prepared_statment
    prepared_statment = stmt
    return 

def bindVariables(query):
    v = query.decode('ascii')
    if len(binds) >= 2: binds.clear()
    binds.append(v)
    return 

def executeQuery():
    stmt = prepared_statment

    print (f"{prepared_statment=}, {binds=}")

    cleaned, val, stmt = clean(stmt)
    if cleaned == 'err': return val
    else: queryType = val

    params = stmt[2:].split(':')
    lookupType = len(params)
    if lookupType == 1: userId = params[0]
    else: user,pw = params
    paramCount = stmt.count('?')


    if queryType == 'S':
        tdb = open('users.tdb', 'r')
        results = []

        if lookupType == 1:
            if paramCount > 1: return b'e:syntaxerror'
            userId = binds.pop(0)
            for line in tdb.readlines():
                tdb_id, tdb_user, tdb_pw = line.split(':')
                tdb_pw = tdb_pw.strip('\n')
                idCheck = (lookupType == 1 and userId == tdb_id) 
                if idCheck:
                    results = [tdb_id, tdb_user, tdb_pw]
                    final = f"r:{tdb_id}:{tdb_user}:{tdb_pw}"
                    return final.encode('ascii')
        if lookupType == 2:
            if paramCount > 2: return b'e:syntaxerror'
            if user == '?': user = binds.pop(0)
            if pw == '?': pw = binds.pop(0)
            for line in tdb.readlines():
                tdb_id, tdb_user, tdb_pw = line.split(':')
                tdb_pw = tdb_pw.strip('\n')
                userCheck = (lookupType == 2 and user == tdb_user and pw == tdb_pw)
                if userCheck:
                    results = [tdb_id, tdb_user, tdb_pw]
                    final = f"r:{tdb_id}:{tdb_user}:{tdb_pw}"
                    return final.encode('ascii')
        
        tdb.close()
        return b'r:'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

sock.bind((HOST, PORT))
sock.listen()
try: 
    while True:
        conn, addr = sock.accept()
        noneCounter = 0
        with conn:
            print (f"Connected by {addr}")
            data = conn.recv(1)
            while data and data != b'e':
                try:
                    length = int.from_bytes(conn.recv(1), "big")
                    payload = conn.recv(length) if data != b'x' else b''
                    print (f"Recieved: {data!r} {payload!r}")
                    match data:
                        case b'q': results = getQuery(payload)
                        case b'p': results = prepareQuery(payload)
                        case b'b': results = bindVariables(payload)
                        case b'x': results = executeQuery()
                        case _:
                            results = b'e:unknown'
                    if results != None: 
                        print (results)
                        try: conn.sendall(results)
                        except: 
                            print ('exception sending')
                except Exception as e:
                    print(f'Exception processing message: {e}')
                    try: conn.sendall(b'e:exception')
                    except: pass
                try: 
                    data = conn.recv(1)
                    if not data: break
                except: break
            try: 
                conn.send(b'e')
            except: print('exception')
            print (f"Recieved: {data!r}")
except KeyboardInterrupt:
    print("Server shutting down")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()