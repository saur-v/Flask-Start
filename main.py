from flask import Flask,render_template,request,redirect,url_for
import pandas

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('my_html.html')


@app.route('/about' ,methods=["get","post"])
def about_you():
    if request.method=="POST" and len(request.form["name"])>0:
        about_data = { 'name': [request.form["name"]],
                        'email': [request.form["email"]],
                    'contact': [request.form["contact"]]  
        }
        df = pandas.DataFrame(about_data)
        with open('static/data.csv','a') as file:
            file.write('\n')
            file.close()   
        df.to_csv('static/data.csv', mode='a', index=False, header=False)  
        return render_template('about.html',a=1)
    return render_template('about.html',a=0) 

@app.route('/user',methods=["get","post"])
def user_data():
    if request.method=="POST":  
        df = pandas.read_csv('static/data.csv')
        data = df.to_dict(orient="list")
        for name in data['name']:
            if name==request.form['name']:
                email = data['email'][data['name'].index(name)]
                contact = data['contact'][data['name'].index(name)]
                name = request.form['name']
                return render_template('your_info.html',a=1,user_success=True,user_name=name,user_email=email,user_contact=contact)
        return render_template('your_info.html',a=1,user_success=False)   
    return render_template('your_info.html',a=0)

@app.route('/contact')
def contact_me():
    return render_template('contact.html')

if __name__=='__main__':
    app.run(debug=True)