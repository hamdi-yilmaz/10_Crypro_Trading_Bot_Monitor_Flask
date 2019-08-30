from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd 
import numpy as np 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hh/Desktop/PycharmProjects 01092018/08_gun_bot/Bittrex/emir_takip.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

@app.route("/")
def index():
    
    todos =  Todo.query.all()
    
    

    # Todo.query.group_by(Todo.MARKET).all()                   # veriyi gruplamak icin
    # Todo.query.all()[1].BORSA                                # birinci verinin Borsa sutunu verisi

    """ liste icinde sozluk yapisinda doner
    [
    {"id":1,"title":"Deneme","content":"sadsd","complate" :0}              # list of dictionary
    ]
    """

    return render_template("index.html",todos = todos)

@app.route("/deneme")
def deneme():
    
    todos =  Todo.query.all()

   
    borsa_grup = Todo.query.group_by(Todo.BORSA).all()
    borsalar =[]
    for borsa in borsa_grup:
        borsalar.append(borsa.BORSA)
    
    market_grup = Todo.query.group_by(Todo.MARKET).all()
    marketler = []
    for market in market_grup:
        marketler.append(market.MARKET)

        
    
    return render_template("deneme.html",todos = todos,borsalar = borsalar, marketler = marketler)

@app.route("/aktif")
def aktifEmirler():
    
    emirler =  Todo.query.all()
    aktif_emirler =[]
    for emir in emirler:
        if emir.STATUS in ("Alim_emri_verildi" ,"ikincil_alim_emri_verildi", "Satim_emri_verildi", "ikincil_satim_emri_verildi"): 
            aktif_emirler.append(emir)

    return render_template("aktif.html",todos = aktif_emirler)

@app.route("/tum_emirler")
def tumEmirler():
    
    emirler =  Todo.query.all()
    tum_emirler =[]
    for emir in emirler:
        if emir.STATUS in ("Alim_emri_verildi"): 
            emir_durumu = dict(TIME=emir.TIME, STATUS="Alim Emri Aktif", PRICE=emir.BUY_PRICE, AMOUNT=emir.BUY_AMOUNT, ORDER_NUMBER=emir.BUY_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
        elif emir.STATUS in ('Satim_emri_verildi'): 
            emir_durumu = dict(TIME=emir.TIME, STATUS="Satim Emri Aktif", PRICE=emir.SELL_PRICE, AMOUNT=emir.SELL_AMOUNT, ORDER_NUMBER=emir.SELL_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
        elif emir.STATUS in ('alis_tamamlandi'): 
            emir_durumu = dict(TIME=emir.TIME, STATUS='Alim Emri', PRICE=emir.BUY_PRICE, AMOUNT=emir.BUY_AMOUNT, ORDER_NUMBER=emir.BUY_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
            emir_durumu1 = dict(TIME=emir.TIME_ikinci, STATUS="Satim Emri", PRICE=emir.SELL_PRICE, AMOUNT=emir.SELL_AMOUNT, ORDER_NUMBER=emir.SELL_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu1)
        elif emir.STATUS in ('satis_tamamlandi'): 
            emir_durumu = dict(TIME=emir.TIME, STATUS='Satim Emri', PRICE=emir.SELL_PRICE, AMOUNT=emir.SELL_AMOUNT, ORDER_NUMBER=emir.SELL_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
            emir_durumu1 = dict(TIME=emir.TIME_ikinci, STATUS="Alim Emri", PRICE=emir.BUY_PRICE, AMOUNT=emir.BUY_AMOUNT, ORDER_NUMBER=emir.BUY_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu1)
        elif emir.STATUS in ('ikincil_alim_emri_verildi'): 
            emir_durumu = dict(TIME=emir.TIME, STATUS='Satim Emri', PRICE=emir.SELL_PRICE, AMOUNT=emir.SELL_AMOUNT, ORDER_NUMBER=emir.SELL_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
            emir_durumu1 = dict(TIME=emir.TIME_ikinci, STATUS="Alim Emri Aktif", PRICE=emir.BUY_PRICE, AMOUNT=emir.BUY_AMOUNT, ORDER_NUMBER=emir.BUY_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu1)
        elif emir.STATUS in ('ikincil_satim_emri_verildi'): 
            emir_durumu = dict(TIME=emir.TIME, STATUS='Alim Emri', PRICE=emir.BUY_PRICE, AMOUNT=emir.BUY_AMOUNT, ORDER_NUMBER=emir.BUY_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu)
            emir_durumu1 = dict(TIME=emir.TIME_ikinci, STATUS="Satim Emri Aktif", PRICE=emir.SELL_PRICE, AMOUNT=emir.SELL_AMOUNT, ORDER_NUMBER=emir.SELL_ORDER_NUMBER,	MARKET=emir.MARKET, KAZANC_ORANI=emir.KAZANC_ORANI)
            tum_emirler.append(emir_durumu1)
    
    
    panda_emirler = pd.DataFrame(tum_emirler)                               # panda dataframe e donustu
    panda_emirler = panda_emirler.sort_values(by=['TIME'])                  # tarihe gore siraladi
    panda_emirler['NUMARA'] = np.arange(len(panda_emirler))                 # numara sutunu ekledi(pandas). dataframe uzunlugunda sirali sayi ekledi(numpy)
    tum_emirler = panda_emirler.to_dict('records')                          # dataframe i tekrar list of dict yapti. 'index' parametresi index numarasi ekliyor

    return render_template("tum_emirler.html",todos = tum_emirler)

@app.route("/durum")
def finansalDurum():
    
    emirler =  Todo.query.all()
    aktif_emirler =[]
    for emir in emirler:
        if emir.STATUS in ("Alim_emri_verildi" ,"ikincil_alim_emri_verildi", "Satim_emri_verildi", "ikincil_satim_emri_verildi"): 
            aktif_emirler.append(emir)

    return render_template("durum.html",todos = aktif_emirler)

@app.route("/add", methods=["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")

    newTodo = Todo(title = title , content = content, complate = False)
    db.session.add(newTodo)         #flask-sqalcemy tutoriala bak
    db.session.commit()

    return redirect(url_for("index"))       # islem bitince donecegi sayfa

@app.route("/complate/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(NUMBER=id).first()      #veriyi alip bir degiskene atadi

    if (todo.complate ==False):
        todo.complate =True
    else:
        todo.complate = False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/sil/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(NUMBER=id).first() 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/detay/<string:id>")
def detailTodo(id):
    todo = Todo.query.filter_by(NUMBER=id).first() 

    return render_template("detail.html", todo = todo)

"""
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complate = db.Column(db.Boolean)
"""

class Todo(db.Model):
    __table__ = db.Model.metadata.tables['Sirali_Emirler']
"""
    def __repr__(self):
        return self.DISTRICT
"""


"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
"""

if __name__ == "__main__":
    app.run(debug=True)