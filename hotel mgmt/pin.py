from sqlalchemy import  create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
def fetch_table(name):
  
    print("called fetch_table")
    app=Flask(__name__)
    db=SQLAlchemy(app)
    engine = create_engine('sqlite:///users.db')
    connection = engine.connect()
    metadata = db.MetaData()
    data = db.Table(str(name), metadata, autoload=True, autoload_with=engine)
    query = db.select([data])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    ans=list(ResultSet)
    return ans



# a=[ () , () ,() ]   --> a={ {}, {}, {} }
def request_to_dict(l):
    d=dict()
    count=0
    for i in l :
        c=dict()
        c["id"]=i[0]
        c["dish"]=i[1]
        c["quantity"]=i[2]
        c["customization"]=i[3]
        c["time"]=i[4]
        d[count]=c
        count=count+1
    return d



data = { 
        "users": [
                {
                "AcquiringDivision":"",
                "EndDate":"20-05-2019",
                "Excl":"yes",
                "Format":"mp4",
                }
            ]
}; 

#a=[('data','name','sname'),('data1','name1','sname1')]

#def request_to_dict(l):
#    f=dict()
#    f["post"]=[]
#   for i in l :
#        o=dict()
#        o["first"]=i[0]
#        o["second"]=i[1]
#        o["third"]=i[2]
#        f["post"].append(o)
#    return f



