import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor


class Model:
     
    # constructor
    def __init__(self,file,choice_model):
        self.file = file # load model here with path
        self.choice_model = choice_model

        if choice_model == "LinearRegression":
            model = LinearRegression()
        elif choice_model == "KNN":
            model = KNeighborsRegressor(n_neighbors=2)
        elif choice_model == "DecisionTreeRegressor":
            model = DecisionTreeRegressor()

        df = pd.read_csv(file,sep=";")
        df = df.dropna()
        target = df.iloc[:,-1:]
        y = target
        X = df.drop(df.columns[-1], axis=1).select_dtypes(include=['int64', 'float64'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train,y_train)
        self.score = model.score(X_test,y_test)
        print(self.score)

    def training(self,X, y):
        return self.modele.fit(X,y)

    def metric(self,X,y):
        return self.modele.score(X,y)

    def predict(self,X):
        return self.modele.predict(X)
    
    def get_score(self):
        return self.score

