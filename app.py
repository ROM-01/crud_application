#Imports
#from dependency import api
from flask_scss import Scss
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#My App Setup
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# Data Class ~ Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)#timezone.utc
    
    def __repr__(self) -> str:
        return f"Task {self.id}"


with app.app_context():
    db.create_all()


#Routes to Webpages
#Homepage
@app.route('/',methods=["POST", "GET"]) #POST = send data GET = recieve data
def index():
    # Add Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
        
    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
    #flasks uses render to search and connect the route to the template/webpage
        return render_template('index.html', tasks=tasks)
    

#https://www.home.com/delete
# Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"
    
# Edit an item
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template("edit.html", task=task)
    

# Runner and Debugger
if __name__ == "__main__":

    app.run(debug=True)

#before prod
# if __name__ in "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
    
    
