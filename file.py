import os


class FileHandler(object):
    def __init__(self, filename):
        self.__filename = filename
    
    def load(self):
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename) as reader:
            lines= reader.read()
            d = []
            for line in lines.split("\n"):
                sp = line.split("\t")
                if len(sp) == 2:
                    d.append(sp) 
            return d 
    
    def save(self, data, sent):
        assert len(data) == len(sent), "lengths must be equal"
        with open(self.__filename, 'a') as writer:            
            writer.write("\n".join( ["{}\t{}".format(str(d), str(s)) for (d,s) in zip(data,sent)]) + "\n")
            
    def clear(self):
        if os.path.exists(self.__filename):
            os.remove(self.__filename)
                        
if __name__ == "__main__":
    fh = FileHandler("data")