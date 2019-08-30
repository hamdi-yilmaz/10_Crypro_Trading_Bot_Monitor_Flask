from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd 
import numpy as np 
from bittrex.bittrex import Bittrex

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hh/Desktop/PycharmProjects 01092018/08_gun_bot/Bittrex/emir_takip.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)




@app.route("/")
def index():
    
    orders =  order.query.all()
    # order.query.group_by(order.MARKET).all()                   # veriyi gruplamak icin
    # order.query.all()[1].BORSA                                # birinci verinin Borsa sutunu verisi

    """ liste icinde sozluk yapisinda doner
    [
    {"id":1,"title":"Deneme","content":"sadsd","complate" :0}              # list of dictionary
    ]
    """
    return render_template("index.html",orders = orders)


@app.route("/yeni_emir")
def yeni_emir():
    return render_template("yeni_emir.html")


@app.route("/deneme")
def deneme():
    
    orders =  order.query.all()

   
    borsa_grup = order.query.group_by(order.BORSA).all()
    borsalar =[]
    for borsa in borsa_grup:
        borsalar.append(borsa.BORSA)
    
    market_grup = order.query.group_by(order.MARKET).all()
    marketler = []
    for market in market_grup:
        marketler.append(market.MARKET)

    return render_template("deneme.html",orders = orders,borsalar = borsalar, marketler = marketler)

@app.route("/aktif")
def aktifEmirler():
    
    emirler =  order.query.all()
    aktif_emirler =[]
    for emir in emirler:
        if emir.STATUS in ("Alim_emri_verildi" ,"ikincil_alim_emri_verildi", "Satim_emri_verildi", "ikincil_satim_emri_verildi"): 
            aktif_emirler.append(emir.__dict__)                                 # onemli. sqalchemyden verileri dict olarak aldi
            
    
    # marketlerden fiyat bilgisi ceker
    panda_aktif_emirler = pd.DataFrame(aktif_emirler)
    g = panda_aktif_emirler.groupby(['BORSA', 'MARKET'])

    ####!!!!! grup anahtarlarini numpy list yaparak devam edecegim. datafrema olmasi mantiksiz
    gruplanmis = pd.DataFrame(g.groups.keys())                                    # grup anahtarlarini dataframe yapti
      
    def fiyat_bilgisi_al(Borsa,Market):
        if Borsa == Bittrex:
            return my_bittrex.get_ticker(Market)['result']['Last']
   # gruplanmis['fiyat'] = gruplanmis.apply (lambda row: fiyat_bilgisi_al(row.0,row.1), axis=1)                                                      # yeni sutun ekledi  
    print gruplanmis                   
    deneme = panda_aktif_emirler.to_dict('records') 
    
    return render_template("aktif.html",orders = aktif_emirler )

@app.route("/tum_emirler")
def tumEmirler():
    
    emirler =  order.query.all()
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
    
    # print tum_emirler
    panda_emirler = pd.DataFrame(tum_emirler)                               # panda dataframe e donustu
    # print panda_emirler
    panda_emirler = panda_emirler.sort_values(by=['TIME'])                  # tarihe gore siraladi
    panda_emirler['NUMARA'] = np.arange(len(panda_emirler))                 # numara sutunu ekledi(pandas). dataframe uzunlugunda sirali sayi ekledi(numpy)
    tum_emirler = panda_emirler.to_dict('records')                          # dataframe i tekrar list of dict yapti. 'index' parametresi index numarasi ekliyor

    return render_template("tum_emirler.html",orders = tum_emirler)


    

@app.route("/durum")
def finansalDurum():
    
    available_btc = my_bittrex.get_balance('BTC')['result']['Available']
    bittrex_cuzdan = my_bittrex.get_balances()

    return render_template("durum.html",bittrex_hesap = bittrex_hesap, kullanilabilir = available_btc, bittrex_cuzdan=bittrex_cuzdan['result'])


"""
@app.route("/add", methods=["POST"])
def addorder():
    title = request.form.get("title")
    content = request.form.get("content")

    neworder = order(title = title , content = content, complate = False)
    db.session.add(neworder)         #flask-sqalcemy tutoriala bak
    db.session.commit()

    return redirect(url_for("index"))       # islem bitince donecegi sayfa
"""

@app.route("/complate/<string:id>")
def completeorder(id):
    order = order.query.filter_by(NUMBER=id).first()      #veriyi alip bir degiskene atadi     # degisken ismi degisecek

    if (order.complate ==False):
        order.complate =True
    else:
        order.complate = False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/sil/<string:id>")
def deleteorder(id):
    order = order.query.filter_by(NUMBER=id).first()        # degisken ismi degisecek
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/detay/<string:id>")
def detailorder(id):
    order1 = order.query.filter_by(NUMBER=id).first() 

    return render_template("detail.html", order = order1)

"""
class order(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complate = db.Column(db.Boolean)
"""

class order(db.Model):
    __table__ = db.Model.metadata.tables['Sirali_Emirler']
"""
    def __repr__(self):
        return self.DISTRICT
"""
class hesap(db.Model):
    __table__= db.Model.metadata.tables['Hesaplar']

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
"""

bittrex_hesap = hesap.query.filter_by(BORSA="Bittrex").first()
my_bittrex = Bittrex(bittrex_hesap.KEY,
                     bittrex_hesap.SECRET)

if __name__ == "__main__":
    app.run(debug=True)

    