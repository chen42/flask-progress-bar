from flask import Flask, session, render_template, request, Response
import time
import os
import tempfile
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# the index.html file contains a query form, which requests the progress page upon submission
@app.route('/')
def index():
    return render_template('index.html')

# the progress page stores the query in session a cookie, and generates a temp file name for storing results,   
# the progress.html waits events from the dosearch page 
@app.route('/progress')
def progress():
    tf_path=tempfile.gettempdir()
    session['path']=tf_path+"/tmp" + ''.join(random.choice(string.ascii_letters) for x in range(6))
    session['query']=request.args.get('query')
    return render_template('progress.html')

# the sosearch pages submits progress, and save results to the temp file. Upon completion, it closes the result file and redirects to the showresult page.  
@app.route('/dosearch')
def dosearch():
    query=session['query']
    out=open(session['path']+"result", "w+")
    def generate(query):
        x = 0
        result=str()
        while x <= 100:
            # do some work on query
            result+=query+str(x)+" <br>"
            out.write(result)
            if x==100:
                out.close()
            yield "data:"+str(x)+"\n\n"
            x = x + 20
            time.sleep(1)
    return Response(generate(query), mimetype= 'text/event-stream')

@app.route('/showresult')
def showresult():
    with open (session['path']+"result", "r") as f:
        result=f.read()
    return render_template('results.html', results=result)

if __name__ == "__main__":
	app.run(debug=True)
