import requests
from file import FileHandler
from config import conf

if __name__ == "__main__":
    FileHandler(conf.dstore).clear()
    
    with open("cleaned.csv") as reader:
        for line in reader:
            line = line.split(",")
            line = "{}\t{}".format(line[1].strip(), line[0])            
            print line            
            requests.post("http://localhost:5000/ingest", data=line)