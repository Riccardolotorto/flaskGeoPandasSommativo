from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas as gpd
import os 
import contextily as ctx
import matplotlib.pyplot as plt

regioni = gpd.read_file("Regioni/Reg01012023_g_WGS84.dbf")
province = gpd.read_file("Province/ProvCM01012023_g_WGS84.dbf")
comuni = gpd.read_file("Comuni/Com01012023_g_WGS84.dbf")
autostrade = gpd.read_file("Auto/Autostrade_10000_CT10_line.dbf")
regioni3857 = regioni.to_crs(3857)
province3857 = province.to_crs(3857)
comuni3857 = comuni.to_crs(3857)
autostrade3857 = autostrade.to_crs(3857)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/esercizio1')
def esercizio1():
    ax = autostrade3857.plot(figsize = (17, 12), color = "blue", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)


@app.route('/esercizio2', methods= ["GET"])
def esercizio2():
    provinciaUtente = request.args.get("provincia")
    provinciaSel = province3857[province3857.DEN_UTS == provinciaUtente]
    autostradeProvincia = autostrade3857[autostrade3857.crosses(provinciaSel.geometry.item())]
    testo = "Nella pronvica di " + provinciaUtente + " ci sono " + str(len(autostradeProvincia)) + " autostrade"
    return render_template("risultato.html", ris = testo)

@app.route('/esercizio3', methods= ["GET"])
def esercizio3():
    provinciaUtente = request.args.get("provincia2")
    provinciaSel = province3857[province3857.DEN_UTS == provinciaUtente]
    autostradeProvincia = autostrade3857[autostrade3857.crosses(provinciaSel.geometry.item())]
    testo = "Nella pronvica di " + provinciaUtente + " ci sono " + str(len(autostradeProvincia)) + " autostrade"
    ax = provinciaSel.plot(figsize = (17, 12), edgecolor = "k", facecolor = "none")
    autostradeProvincia.plot(ax = ax, color = "blue")
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", ris = testo, immagine = file_name)

@app.route('/esercizio4')
def esercizio4():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    ax = lombardia.plot(figsize = (17, 12), edgecolor = "k", facecolor = "none", linewidth = 3)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es4.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio5')
def esercizio5():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    provinceLombardia = province3857[province3857.within(lombardia.geometry.item())]
    ax = provinceLombardia.plot(figsize = (17, 12), edgecolor = "blue", facecolor = "none", linewidth = 3)
    lombardia.plot(ax = ax, edgecolor = "k", facecolor = "none", linewidth = 3)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es5.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio6')
def esercizio6():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    provinceLombardia = province3857[province3857.within(lombardia.geometry.item())]
    provinceLombardiaAutostrade = provinceLombardia[provinceLombardia.intersects(autostrade3857.unary_union)]
    ax = provinceLombardiaAutostrade.plot(figsize = (17, 12), edgecolor = "blue", facecolor = "red", alpha = 0.5)
    lombardia.plot(ax = ax, edgecolor = "k", facecolor = "none")
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es6.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio7')
def esercizio7():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    provinceLombardia = province3857[province3857.within(lombardia.geometry.item())]
    provinceLombardiaNOAutostrade = provinceLombardia[~provinceLombardia.intersects(autostrade3857.unary_union)]
    ax = provinceLombardiaNOAutostrade.plot(figsize = (17, 12), edgecolor = "blue", facecolor = "green", alpha = 0.5)
    lombardia.plot(ax = ax, edgecolor = "k", facecolor = "none")
    ctx.add_basemap(ax)
    
    dir = "static/images"
    file_name = "es7.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio8-9-10')
def esercizio8910():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    provinceLombardia = province3857[province3857.within(lombardia.geometry.item())]
    joined = gpd.sjoin(autostrade3857, provinceLombardia, how = "left", predicate="crosses")
    numAutoPerProv = joined.groupby("DEN_UTS")[["PERCORSO"]].count().sort_values(by="PERCORSO", ascending = False).reset_index()
    finale = provinceLombardia.merge(numAutoPerProv, on = "DEN_UTS")
    ax = finale.plot(figsize = (17, 12), column = "PERCORSO", legend = True, cmap = 'Greens', alpha = 0.5)
    ctx.add_basemap(ax)
    
    
    dir = "static/images"
    file_name = "es8-9-10.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio11')
def esercizio11():
    lombardia = regioni3857[regioni3857.DEN_REG == "Lombardia"]
    provinceLombardia = province3857[province3857.within(lombardia.geometry.item())]
    joined = gpd.sjoin(autostrade3857, provinceLombardia, how = "left", predicate="crosses")
    numAutoPerProv = joined.groupby("DEN_UTS")[["PERCORSO"]].count().sort_values(by="PERCORSO", ascending = False).reset_index()
    finale = provinceLombardia.merge(numAutoPerProv, on = "DEN_UTS")
    provinceLombardiaNOAutostrade = provinceLombardia[~provinceLombardia.intersects(autostrade3857.unary_union)]
    ax = finale.plot(figsize = (17, 12), column = "PERCORSO", legend = True, cmap = 'Greens', alpha = 0.5)
    provinceLombardiaNOAutostrade.plot(ax = ax, edgecolor = "green", facecolor = "none", linewidth = 2)
    ctx.add_basemap(ax)
        
    dir = "static/images"
    file_name = "es8-9-10.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html", immagine = file_name)

@app.route('/esercizio12', methods= ["GET"])
def esercizio12():
    from shapely.geometry import Point
    longitudine = float(request.args.get("longitudine"))
    latitudine = float(request.args.get("latitudine"))
    Punto = gpd.GeoSeries([Point(longitudine, latitudine)], crs = 4326).to_crs(3857)
    autostradeDistanti = autostrade3857
    autostradeDistanti["Distanza"] = autostradeDistanti.distance(Punto.geometry.item())
    table = autostradeDistanti[autostradeDistanti.Distanza == autostradeDistanti.Distanza.min()].to_html()
    return render_template("risultato.html", tabella = table)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)