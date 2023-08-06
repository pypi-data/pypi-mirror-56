import requests as http
import json,datetime

def now():return datetime.datetime.today()

# Database Connector class
class DBConnector:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.base_url = "http://%s:%s/ods/"%(self.host,self.port)
        self.response = None
    def dbTask(self,task,table,constraints={},data={}):
        process_url = self.base_url+task
        payload = {
            "tablename":table,
            "data":data,
            "constraints":constraints
        }
        self.response = http.post(process_url,json.dumps(payload),headers={"Content-Type":"application/json"})

def check_expired(session):
    try:
        started = eval(session["started"]); duration = session["duration"]
        if (now() - started).seconds > duration:
            # expired session
            return 401
        else:
            # valid session
            return 200
    except:
        # bad session
        return 400

# AUTH class
class AuthProcess:
    def __init__(self,host,port):
        self.dbconnect = DBConnector(host,port)
        self.dbconnect.dbTask("fetch_records","auth",{}); self.records = self.dbconnect.response.json()["data"]
        if not self.records:
            http.post(self.dbconnect.base_url+"new_table",json.dumps({"tablename":"auth","fields":["username","appname","started","duration"]}),headers={"Content-Type":"application/json"})
            self.records = []
    def new_session(self,appname,username,duration):
        # check session exists
        exist = [session for session in [x for x in self.records if "appname" in x and "username" in x] if session["appname"] == appname and session["username"] == username]
        if exist:
            # session exists; check if expired
            session = exist[-1]; return check_expired(session)
        else:
            # create new session
            try:
                duration = int(float(duration))
            except:
                duration = 600 # default 10 minute session
            started = repr(now())
            new = {"appname":appname,"username":username,"duration":duration,"started":started}
            self.dbconnect.dbTask("new_record","auth",{},new); token = self.dbconnect.response.json()["data"]["auth_id"]; new["auth_id"] = token
            self.records.append(new)
            return token # send auth token
    def check_session(self,appname,username,token):
        exist = [session for session in self.records if session["auth_id"] == token and session["appname"] == appname and session["username"] == username]
        if not exist:
            return 403
        else:
            # session exists; check if expired
            session = exist[-1]; return check_expired(session)
