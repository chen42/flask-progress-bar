from flask import Flask, session, render_template, request, Response
import time
import os
import tempfile
import random
import string


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/progress')
def progress():
    tf_path=tempfile.gettempdir()
    session['path']=tf_path+"/tmp" + ''.join(random.choice(string.ascii_letters) for x in range(6))
    session['query']=request.args.get('query')
    return render_template('progress.html')

@app.route('/dosearch')
def dosearch():
    query=session['query']
    def generate(query):
        x = 0
        #out=open(session['path']+"graph", "w+")
        out=open("/tmp/00agraph", "w+")
        result=str()
        while x <= 100:
            # do some work on query
            result+=str(x)+" "
            out.write(result)
            yield "data:"+str(x)+"\n\n"
            #yield {"data": str(x) + "\n\n", "result":result }
            #yield "data:" + str(x) + "\n\n", "result:" + result + "\n\n"
            x = x + 20
            time.sleep(0.2)
        out.close()
    return Response(generate(query), mimetype= 'text/event-stream')

@app.route('/showgraph')
def showgraph():
    with open ("/tmp/00agraph", "r") as f:
    #with open (session['path']+"graph", "r") as f:
        graphdata=f.read()
    print(str(graphdata))
    #return render_template('cytoscape.html', graphdata=str(graphdata))
    return render_template('cytoscape.html', results=str(graphdata))

if __name__ == "__main__":
	app.run(debug=True)
