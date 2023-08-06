import numpy as np
#from keras.applications import NASNetLarge
class AnsembleModel:
    def __init__(self,models):
        self.models=models;

    def predict(self,data):
        res=[]
        for m in self.models:
            res.append(m.predict(data))

        rm=res[0]
        for r in range(1,len(self.models)):
            rm=rm+res[r];
        return self.avarage(rm)

    def avarage(self, x):
        if isinstance(x, list):
            return [self.avarage(y) for y in x]
        if isinstance(x,tuple):
            result = tuple([self.avarage(y) for y in x])
            return result
        if isinstance(x,dict):
            return x
        return x / float(len(self.models))


class TestTimeAugModel:
    def __init__(self, model,augFunction):
        self.model=model
        self.aug=augFunction

    def predict(self,data):
        res=[]
        aug = self.aug(data)
        for v in aug:
            res.append(self.model.predict(v))

        rm=res[0]
        for r in range(1,len(aug)):
            rm=rm+res[r]
        if isinstance(rm, list):
            return [x/float(len(aug)) for x in rm]    
        return rm/float(len(aug))


def crop(x, y,x1,y1, image):
    return image[:,y:y1, x:x1, :]

def addCrop(image,x,y,x1,y1,image1):
    image[:,y:y1, x:x1, :]+=image1

class BatchCrop:

    def __init__(self,parts,mdl):
        self.parts=parts
        self.mdl=mdl

    def predict(self,images):
        cell_width=images.shape[2]/self.parts
        cell_height = images.shape[1]/self.parts
        rs=None
        for i in range(self.parts):
            for j in range(self.parts):
                x=round(i*cell_width)
                y=round(j*cell_height)
                x1=x+round(cell_width)
                y1=y+round(cell_height)
                predCrop=self.mdl.predict(crop(x,y,x1,y1,images));
                if rs is None:
                    rs=np.zeros((images.shape[0],images.shape[1],images.shape[2],predCrop.shape[-1]),dtype=np.float32)
                addCrop(rs,x,y,x1,y1,predCrop)
        return rs