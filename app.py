#  Importer flask
from flask import Flask, json, jsonify, abort, request
from flask.helpers import make_response, url_for
#  import pour mysql_flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# appel de mysql pour l'utiliser
mysql = MySQL(app)
#  configuration à la connection msql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'beer'

#  route pour recuperer une biere de ma liste precise de ma bdd
@app.route('/beer/<int:id_article>', methods=['GET']) # récupère les champs article via l'ID
def get_biere_by_id(id_article):
    # nom_article ne pas être nul if not request.json and not 'NOM_ARTICLE' in request.json
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM article WHERE ID_ARTICLE=%s",(str(id_article),)) # rajouter une virgule car liste prend 1 seul paramètre
        print("finir get by id")
        reponse = cur.fetchone() # création d'un tuple
        cur.close()
        return jsonify(make_public_biere(make_biere(reponse)))
    except Exception as e:
        print(e)
        abort(404)

'''
@app.route('/beer_list/<int:biere_id>', methods=['GET'])
def get_biere_by_id(biere_id):
    biere= [biere for biere in Listebeer_list if biere['id']==biere_id ]
    # verifie que notre biere existe bien
    if len(biere) == 0:
        abort(404)
    # return jsonify(biere)
    return jsonify(make_public_biere(biere[0]))
'''

#  route pour modifier une biere precise de ma liste de ma bdd
@app.route('/beer/<int:id_article>', methods=['PUT'])
def update_biere(id_article):
    biere=get_biere_by_id(id_article)
    print("biere selectionnee")
    if not request.json:
        print("probleme pas requete")
        abort(400)

    if "NOM_ARTICLE" in request.json and type(request.json['NOM_ARTICLE']) is not str:
        print("nom erreur")
        abort(400)
    if "PRIX_ACHAT" in request.json and type(request.json['PRIX_ACHAT']) is not str:
        print("prix err")
        abort(400)
    if "VOLUME" in request.json and type(request.json['VOLUME']) is not str:
        print("volume erre")
        abort(400)
    if "TITRAGE" in request.json and type(request.json['TITRAGE']) is not str:
        print("tit erre")
        abort(400)
    if "ID_MARQUE" in request.json and type(request.json['ID_MARQUE']) is not str:
        print("id marque erre")
        abort(400)
    if "ID_COULEUR" in request.json and type(request.json['ID_COULEUR']) is not str:
        print("coul erre")
        abort(400)
    if "ID_TYPE" in request.json and type(request.json['ID_TYPE']) is not str:
        print("id ty erre")
        abort(400)
        
    
    try:
        #idart = request.json.get('ID_ARTICLE', biere.json['ID_ARTICLE'])
        nom_article = request.json.get('NOM_ARTICLE', biere.json['NOM_ARTICLE'])
        print('hii')
        prix_achat = request.json.get('PRIX_ACHAT', biere.json['PRIX_ACHAT'])# récupère le prix d'achat  si pas récupère dans la liste jsonifier
        volume = request.json.get('VOLUME', biere.json['VOLUME'])
        titrage = request.json.get('TITRAGE', biere.json['TITRAGE'])
        ID_marque = request.json.get('ID_MARQUE', biere.json['ID_MARQUE'])
        ID_Couleur = request.json.get('ID_COULEUR', biere.json['ID_COULEUR'])
        ID_Type = request.json.get('ID_TYPE', biere.json['ID_TYPE'])

        cur= mysql.connection.cursor()
        cur.execute("UPDATE article SET NOM_ARTICLE=%s, PRIX_ACHAT=%s, VOLUME=%s, TITRAGE=%s, ID_MARQUE=%s, ID_COULEUR=%s, ID_TYPE=%s WHERE ID_ARTICLE=%s",(nom_article, prix_achat, volume, titrage, ID_marque, ID_Couleur, ID_Type))
        mysql.connection.commit()
        cur.close()
        return get_biere_by_id(id_article)
    except Exception as e:
        print(e)
        return jsonify({'is': False})    


#  route pour supprimer une biere de ma liste dans ma bdd
@app.route('/beer/<int:ID_ARTICLE>', methods=['DELETE'])
def delete_biere(biere_id):
    print("avant delete")
    biere=get_biere_by_id(biere_id)
    print("apres get dans delete")
    try:
        cur= mysql.connection.cursor()
        cur.execute("DELETE FROM article WHERE ID_ARTICLE=%s", (str(biere_id),))
        mysql.connection.commit()
        cur.close()
        return biere
    except Exception as e:
        print(e)
        return jsonify({'is': False}) 

'''
@app.route('/beer_list/<int:biere_id>', methods=['DELETE'])
def delete_biere(biere_id):
    supbiere = [biere for biere in Listebeer_list if biere['id']==biere_id]

    if len(supbiere)==0:
        resp = make_response(jsonify({"error":"la biere à supprimer n'a pas été trouvée"}), 404)
        return resp

    del Listebeer_list[Listebeer_list.index(supbiere[0])]
    return make_response(jsonify(supbiere), 202)
'''
    


#  route pour recuperer la liste des beer_list dans ma bdd
@app.route('/beer', methods=['GET']) #création http beer
def get_beer():
    try:
        cur= mysql.connection.cursor()
        cur.execute("SELECT * FROM article")
        reponse = cur.fetchall()
        cur.close()
        beer_list=[]
        for biere in reponse:
            biere = make_biere(biere)            
            beer_list.append(biere)
        return jsonify([make_public_biere(biere) for biere in beer_list])
    except Exception as e:
        print(e)
        abort(404)

def getdernierart():
    cur= mysql.connection.cursor()
    cur.execute("SELECT max(ID_ARTICLE) FROM article")
    reponse = cur.fetchone()
    iddernier=reponse[0]
    cur.close()
    return iddernier

# route pour ajouter une biere à ma liste dans ma bdd
@app.route('/beer', methods=['POST'])
def create_biere():
    if not request.json and not "ID_article" in request.json:
        abort(400)
    try:
        
        # creer les champs de ma nouvelle biere
        #ID_article = request.json['ID_ARTICLE'] 
        #appeler fonction pour avoir id du dernier article
        iddernier=getdernierart() #4000
        idnouveau=iddernier+1
        #idnouveau = request.json['ID_Article']
        Nom_article = request.json['NOM_ARTICLE']
        Prix_achat = request.json['PRIX_ACHAT']
        volume = request.json['VOLUME']
        titrage= request.json['TITRAGE'] 
        marque= request.json['ID_MARQUE']
        Couleur= request.json['ID_COULEUR']
        type = request.json['ID_TYPE']
        # creer ma connection et envoyer à ma bdd
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO article(ID_ARTICLE, NOM_ARTICLE, PRIX_ACHAT, VOLUME, TITRAGE, ID_MARQUE, ID_Couleur, ID_TYPE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(idnouveau, Nom_article, Prix_achat, volume, titrage, marque, Couleur, type))
        mysql.connection.commit()
        cur.close()
        return jsonify({'is':True})
    except Exception as e:
        print(e)
        return jsonify({'is':False})


# annotations app.route('URL')
@app.route('/')
def index ():
    return "Hello world, youpi!!"


#  fonction pour creer une url d façon dynamique à partir d'une biere, enlever lID et remplacer par une URL
def make_public_biere(biere):
    public_biere={}
    for argument in biere:
        if argument == "ID_ARTICLE":
            public_biere['url']= url_for('get_biere_by_id', id_article=biere['ID_ARTICLE'], _external=True)
        else:
            public_biere[argument]=biere[argument]
    return public_biere

# fonction pour creer une biere à partir d'une beer_list base de données
def make_biere(biere_bdd):
    # print(biere_bdd)
    list_biere= list(biere_bdd)
    # print(list_biere)
    new_biere={}
    new_biere['ID_ARTICLE']=int(list_biere[0])
    new_biere['nom_article']=str(list_biere[1])
    new_biere['PRIX_ACHAT']=str(list_biere[2])
    new_biere['VOLUME']=str(list_biere[3])
    new_biere['TITRAGE']=str(list_biere[4])
    new_biere['ID_MARQUE']=str(list_biere[5])
    new_biere['ID_Couleur']=str(list_biere[6])
    new_biere['ID_Type']=str(list_biere[7])
    # print(new_biere)
    return new_biere

if __name__ == '__main__':
    app.run(debug = True)