
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:oladeinde@localhost:5432/todoapp2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False) 
 # completed = db.Column(db.Boolean, nullable=True, default=False)
  

  def __repr__(self):
   return f'<Todo {self.id} {self.description}>'  


db.create_all()   

@app.route('/todo/create', methods=['POST'])
def create_todo():

   body={}
   error = False
   try: 
       description =  request.get_json()['description']
       todos = Todo(description=description)
       body['description'] = todos.description
       db.session.add(todos)
       db.session.commit()
   except:        
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()           
        if  error == True:
            abort(400)
        else:            
            return jsonify(body)
 

@app.route('/') #listens to homepage
def index():
  return render_template('index.html', data=Todo.query.all()
    #'description': 'Todo 1'
  #}, {
   # 'description': 'Todo 2'
  #}, {
    #'description': 'Todo 3'
  #}]
  )


#always include this at the bottom of your code (port 3000 is only necessary in workspaces)

if __name__ == '__main__':
   app.run(host="0.0.0.0")