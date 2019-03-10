from flask import Flask, render_template
from data import *

app = Flask(__name__)
Articles = Data.Article()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/myprofile')
def myprofile():
    return render_template('myprofile.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/pertanyaanumum')
def pertanyaanumum():
    return render_template('pertanyaanumum.html')

@app.route('/masalahpelapak')
def masalahpelapak():
    return render_template('masalahpelapak.html')

@app.route('/masalahpenjualan')
def masalahpenjualan():
    return render_template('masalahpenjualan.html')

@app.route('/bestplayer')
def bestplayer():
    return render_template('bestplayer.html')

@app.route('/barangterlaris')
def barangterlaris():
    return render_template('barangterlaris.html')

@app.route('/all')
def all():
    return render_template('all.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/pembayaran')
def pembayaran():
    return render_template('pembayaran.html')
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)