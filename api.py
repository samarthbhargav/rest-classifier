
from flask.ext import restful
from flask import request
from functools import wraps
from config import conf
from flask import Flask
from file import FileHandler
from sentiment import BayesClassifier

###### Global Objects #########
# Flask Stuff
app = Flask(__name__)
api = restful.Api(app)
# File Handler object
fh = FileHandler(conf.dstore)
# Classifier
clf =  None
#############################

def basic_authentication():
    """
    Performs HTTP Basic Authentication
    """

    if conf.auth_password is None or conf.auth_password is "":
        return True
    
    return request.authorization is not None and request.authorization.username == conf.auth_username and request.authorization.password == conf.auth_password

def authenticate(func):
    """
    Decorator for Auth
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
            
        acct = basic_authentication() 
        
        if acct:
            return func(*args, **kwargs)

        restful.abort(401)
    return wrapper


class Resource(restful.Resource):
    """
    Class that expends a Resource and adds HTTP Basic Authentication
    """
    method_decorators = [authenticate]


class IngestAPI(Resource):
    
    def post(self):
        data = []
        sent = []
        print request.data
        for line in request.data.split("\n"):            
            split = line.split("\t")
            if len(split) != 2:
                continue
            data.append(split[0])
            sent.append(split[1])
        fh.save(data, sent)


class TrainAPI(Resource):
    def post(self):
        global clf
        clf = BayesClassifier()
        data = fh.load()

        if data is None or len(data) == 0:
            return {"message" : "No data"}, 400
        
        sentences = []
        sentiments = []
        for d in data:
            sentences.append(d[0])
            clf.append_to_corpus(d[0])
            sentiments.append(d[1])
        print sentences
        clf.train(sentences, sentiments)
        
        return {"message": "Classifier trained successfully"}, 200
        
    def get(self):
        if clf is not None:
            return {"message": "Classifier is trained"}, 200
        else:
            return {"message": "Classifier is not trained yet"}, 202
            
class ClassifiyAPI(Resource):
    def get(self, sentence):
        if clf is None:
            return {"message": "Classifier is not trained yet"}, 202
        else:
            return { "prediction" : str(clf.predict(sentence))} , 200

class ClearAPI(Resource):
    def delete(self):
        global clf
        fh.clear()
        clf = None
        return {"message" : "Data cleared successfully"}, 200
    

api.add_resource(IngestAPI, '/ingest')
api.add_resource(TrainAPI, '/train')
api.add_resource(ClassifiyAPI, '/classify/<string:sentence>')
api.add_resource(ClearAPI, '/clear')


if __name__ == "__main__":
    app.run(debug=True)