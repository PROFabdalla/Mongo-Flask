from flask import Flask, redirect,render_template,request,url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/itimenofia"
mongo = PyMongo(app)


def nextid():
    users_flask_collection = mongo.db.users
    result = list(users_flask_collection.find().sort("_id",-1).limit(1))
    if len(result) > 0:
        return result[-1]['_id']+1
    else:
        return 1


@app.route('/')
def home():
    users = list(mongo.db.users.find())
    return render_template('home.html' ,users=users)
# name=name,age=age,location=location,






@app.route('/adduser',methods=['GET','POST'])
def add_user():
    if request.method=='GET':
        return render_template('adduser.html')
    else:
        print(request.form)
        users_flask_collection = mongo.db.users
        users_flask_collection.insert_one({"_id":nextid(),**request.form})

        return redirect(url_for('home'))





@app.route('/delete/<int:id>')
def delete_user(id):
    users_flask_collection = mongo.db.users
    users_flask_collection.delete_one({"_id":id})
    return redirect(url_for('home'))





@app.route('/update/<int:id>',methods=["POST","GET"])
def update_user(id):
    if request.method == "GET":
        user = mongo.db.users.find_one({"_id":id}) # get one user
        return render_template("updateuser.html",user=user)
    else:
        print(request.form)
        users_flask_collection = mongo.db.users
        users_flask_collection.update_one({"_id":id},{"$set":request.form})

    return redirect(url_for('home'))





if __name__ == '__main__' :
    app.run(debug=True)
