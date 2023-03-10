from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from authentification.models import Utilisateur,CsvFile
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import plot
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
from authentification.class_model import Model
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Mes graphiques
fig = go.Figure()
scatter = go.Scatter(x=[0,1,2,3], y=[0,1,2,3],
                     mode='lines', name='test',
                     opacity=0.8, marker_color='green')
fig.add_trace(scatter)
reg_plot = plot(fig, output_type='div')

df2 = px.data.iris() # iris is a pandas DataFrame
fig2 = px.scatter(df2, x="sepal_width", y="sepal_length", title="Scatter plot")
graph2 = plot(fig2, output_type='div')


df3 = px.data.tips()
fig3 = px.box(df3, x="time", y="total_bill", title="Boîte à moustache")
graph3 = plot(fig3, output_type='div')

z = [[.1, .3, .5, .7, .9],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1]]

fig4 = px.imshow(z, text_auto=True)
graph4 = plot(fig4, output_type='div')

# Clustering
# DBScan

dfPenguins = pd.read_csv("./static/penguins.csv")
X = dfPenguins[dfPenguins.describe().columns].dropna().values

X = StandardScaler().fit_transform(X)

db = DBSCAN().fit(X)
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
#Homogeneity = metrics.homogeneity_score(labels_true, labels)

def inscription(request):
    message = ""
    if request.method == "POST":
        if request.POST["motdepasse1"] == request.POST["motdepasse2"]:
            modelUtilisaleur = get_user_model()
            identifiant = request.POST.get("identifiant")
            motdepasse = request.POST.get("motdepasse1")
            utilisateur = modelUtilisaleur.objects.create_user(username=identifiant,
                                                       password=motdepasse)
            return redirect("connexion")
        else:
            message = "⚠️ Les deux mots de passe ne concordent pas ⚠️"
    return render(request, "inscription.html", {"message" : message})

def connexion(request):
    # La méthode POSt est utilisé quand des infos
    # sont envoyées au back-end
    # Autrement dit, on a appuyé sur le bouton
    # submit
    message = ""
    if request.method == "POST":
        identifiant = request.POST.get("identifiant")
        motdepasse = request.POST.get("motdepasse")
        utilisateur = authenticate(username = identifiant,
                                   password = motdepasse)
        if utilisateur is not None:
            login(request, utilisateur)
            return render(request, "index.html")
        else:
            message = "Identifiant ou mot de passe incorrect"
            return render(request, "connexion.html", {"message": message})
    # Notre else signifie qu'on vient d'arriver
    # sur la page, on a pas encore appuyé sur le
    # bouton submit
    else:
        return render(request, "connexion.html")

def deconnexion(request):
    logout(request)
    return redirect("connexion")

@login_required
def index(request):
    return render(request, "index.html")

def suppression(request,id):
    utilisateur = Utilisateur.objects.get(id=id)
    logout(request)
    utilisateur.delete()
    return redirect("connexion")

def regression(request):
    context = {
        "model_load": False,
        "reg_plot": reg_plot
        }
    return render(request,"regression.html",context)

def training_model(request):
    model = Model(None,None)
    context = {
        "model_load": True,
        "reg_plot": reg_plot
        }
    return render(request,"regression.html",context)

def save_file(request):

    if request.method == 'POST':
        #form = CsvFileForm(request.POST, request.FILES)
        if request.FILES:
            csv_file = request.FILES.get('fichier_csv')
            # Enregistrer le fichier dans un dossier temporaire
            file_path = csv_file.name
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
            file_obj = CsvFile.objects.create(file_name=csv_file.name,file_path=file_path)

            choice_model = request.POST.get('choice_model')
            model = Model(file_path,choice_model)
            score = model.get_score()
            df = model.get_df()
            
            figbox = px.box(df, y=df.columns.tolist()[-1], title="Boîte à moustache")
            graphbox = plot(figbox, output_type='div')

            scatter = px.scatter(df,x= df.columns.tolist()[0], y=df.columns.tolist()[-1],opacity=0.65)
            graphscat = plot(scatter, output_type='div')

            scatter1 = px.scatter(df,x= df.columns.tolist()[1], y=df.columns.tolist()[-1],opacity=0.65)
            graphscat1 = plot(scatter1, output_type='div')

            scatter2 = px.scatter(df,x= df.columns.tolist()[2], y=df.columns.tolist()[-1],opacity=0.65)

            # scatter2.add_traces(go.Scatter(x=np.linspace(model.get_X().min(), model.get_X().max(), 100), y= model.predict(model.get_X()), name='Regression Fit'))
            graphscat2 = plot(scatter2, output_type='div')

            context = {
                "score":score,
                "reg_plot":graphbox,
                "reg_scat": graphscat,
                "reg_scat1": graphscat1,
                "reg_scat2": graphscat2,
            }
            
    else:
        context = {
            "score":0
        }
    
    return render(request,"regression.html",context)

def classification(request):
    return render(request,"classification.html")

def clustering(request):
    return render(request,"clustering.html")