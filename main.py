from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from cust_codes import *

print ("Lets get things started shall we.....")
#Database Information
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename="",
)

app = Flask(__name__)
app.config["DEBUG"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
db = SQLAlchemy(app)

class blog_posts(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(4096))
    blog_content = db.Column(db.String(4096))

    def __init__(self, blog_title, blog_content):
        self.blog_title = blog_title
        self.blog_content = blog_content

    def __repr__(self):
        return "%s $$$ %s" % (self.blog_title, self.blog_content)

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        bod = list(blog_posts.query.all())
        lisp = list()
        for i in reversed(bod):
            lisp.append(str(i))
        return render_template("home.html", bode=lisp)

    po = request.form["make_post"]
    pt = request.form["make_title"]
    pos = blog_posts(pt,po)
    db.session.add(pos)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/science/')
def sci_home():
    return render_template("science_home.html")

@app.route('/plsUpload/', methods = ["GET", "POST"])
def pls_upload():
    return render_template("panel.html")

@app.route('/plsResults/', methods = ["GET","POST"])
def pls_result():

    input_list = []
    f = request.files['file_data']
    df = pd.read_csv(f, header=None)
    list_of_lists = df.values.tolist()
    for i in list_of_lists:
        for j in i:
            if j != "":
                input_list.append(j)

    d = compareGenes(input_list)
    best = findBestMatches(d['matchCounts'])
    plsOrder = haveNots(best['topName'], input_list)
    return render_template("pls_results.html", rezz=countsDictionary, prydz=d['matchCounts'], mick=best['topName'], jenny=float(best['topMatchPercent']*100), brooke=plsOrder)



@app.route('/resume/')
def resume():
    return render_template("resume.html")

@app.route('/design/')
def design_home():
    return render_template("design.html")

@app.route('/exp/')
def experiment():
    return render_template("experimental.html")
