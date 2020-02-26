from flask import Flask , render_template ,request,redirect,make_response,jsonify
from flask_marshmallow import Marshmallow
import os
import time
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pin

app=Flask("__name__")

db=SQLAlchemy(app)
ma=Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.db'
app.config["SECRET_KEY"]="kjhdjJLggfDIUU2ellfvjakad3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False



class data(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    dish=db.Column(db.String(50),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    customization=db.Column(db.String(50),nullable=True)
    time=db.Column(db.String(20),nullable=False)

class dataSchema(ma.Schema):
    class Meta:
        fields=('id','dish','quantity','customization','time')

datas_schema=dataSchema(many=True)

@app.route("/")
def main():
    print("//////")
    return render_template("manager.html")


@app.route("/manager" , methods=["POST"])
def manager():
    print('dd')
    response=request.get_json()
    print(response)
    print(response["quantity"])
    
    time= datetime.now()
    time=time.strftime('%d/%m/%Y %I:%M')

    print("reach1")
    try:
        info=data(dish=response["dish"],quantity=response["quantity"],customization=response["customization"],time=time)
        db.session.add(info)
        db.session.commit()
        print("added")
        res=make_response(jsonify({"message":"added in que :)"}),200)
        print("response")
        return res
    except:
        res=make_response(jsonify({"message":"NOT received :("}),400)
        return res


@app.route("/maker")
def maker():
    data=pin.fetch_table("data")
    return render_template("maker.html",data=data)

@app.route("/makerajax",methods=["POST"])
def makerajax():
    print("called maker ajax")
    data=pin.fetch_table("data")
    print(data)
    data=pin.request_to_dict(data)
    print(data)
    res=make_response(jsonify(data),200)
    return res

@app.route("/cancel",methods=["POST"])
def cancel():
    id=request.form.get("ids")
    print(id)
    dish=request.form.get("dish")
    query=data.query.filter_by(id=id).first()
    print("deleting record of id :")
    db.session.delete(query)
    db.session.commit()
    print("deleted succesfully")
    return redirect("/maker")
    
@app.route("/fetch_orders",methods=["GET"])
def fetch_orders():
    query=data.query.all()
    result=datas_schema.dump(query)
    print(result)
    return jsonify(result)

@app.route("/delete",methods=["POST"])
def delete():
    req=request.get_json()
    print("printing json issssssssssssssssss")
    print(req["id"])
    query=data.query.filter_by(id=req["id"]).first()
    db.session.delete(query)
    db.session.commit()
    print("deleted")
    res=make_response(jsonify({"message":"record deleted"}),200)
    return res



    
if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)