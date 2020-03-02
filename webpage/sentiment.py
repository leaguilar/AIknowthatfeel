from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import tensorflow as tf
from agent.wojak import WojakEntity
from flask_ngrok import run_with_ngrok

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
run_with_ngrok(app)


wojak=WojakEntity()

class ReusableForm(Form):
    text1 = TextField('Text 1:', validators=[validators.required()])
    
    @app.route("/", methods=['GET', 'POST'])
    def sentiment():
        form = ReusableForm(request.form)
    
        print(form.errors)
        if request.method == 'POST':
            text1=request.form['text1']
            text2=request.form['text2']
            text3=request.form['text3']
            #print(text1)
    
        if form.validate():
            # Save the comment here.
            wojak.perceive(text1,text2,text3)
            #
            action=wojak.act()
            flash('Mood: ' + action)
            if action == "happy":
                filename="happy.jpg"
            elif action == "sad":
                filename="sad.jpg"
            elif action =="other":
                filename="other.jpg"
            elif action == "angry":
                filename="angry.jpg"
            else:
                filename="npc.jpg"
        else:
            flash('All the form fields are required. ')
            filename="npc.jpg"
        
        return render_template('sentiment.html', form=form, filename=filename)

if __name__ == "__main__":
    app.run()
