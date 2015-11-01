from flask import Flask,render_template,request,redirect
app = Flask(__name__)

@app.route('/plot1',methods=['GET','POST'])
def plot1():
    return render_template('plot1.html')

@app.route('/plot2')
def plot2():
    return render_template('plot1.html')

if __name__ == "__main__":
    app.run(port= 33507)

    