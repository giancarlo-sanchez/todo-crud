from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Setting up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

#Creating the class model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#creating endpoints
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        todo = request.form['content']
        new_todo = Todo(content=todo)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')

        except:
            return "Error while creating new taks :("

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks = tasks)




@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return " Oh no we couldn't delete TODO"

#running the app
if __name__ == "__main__":
    app.run(debug = True)
