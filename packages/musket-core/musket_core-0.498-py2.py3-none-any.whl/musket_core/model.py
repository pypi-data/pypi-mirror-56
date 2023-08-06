from musket_core import datasets
from musket_core.datasets import DataSet, MeanDataSet
import typing


def block(func):
    func.model=True
    return func

class Model:

    def predict_on_dataset(self,d:datasets.DataSet,**kwargs):
        raise ValueError("Not implemented")


class ConnectedModel(Model):

    def predictions(self,name_or_ds:typing.Union[datasets.DataSet,str],**kwargs)->DataSet:
        raise ValueError("Not implemented")


class IGenericTaskConfig(ConnectedModel):

    folds_count=None
    _reporter=None

    def get_eval_batch(self)->int:
        return -1

    def validation(self,ds:typing.Optional[DataSet],fold:int)->DataSet:
        raise ValueError("Not implemented")

    def get_dataset(self,name:str=None)->DataSet:
        raise  ValueError("Not implemented")

class FoldsAndStages(ConnectedModel):

    def __init__(self,core:ConnectedModel,folds,stages):
        self.wrapped=core
        self.folds=folds
        self.stages=stages

    def predict_on_dataset(self, d, **kwargs):
        return self.wrapped.predict_on_dataset(d,fold=self.folds,stage=self.stages)

    def predictions(self,name, **kwargs)->DataSet:
        return self.wrapped.predictions(name, fold=self.folds, stage=self.stages)

class AverageBlend(ConnectedModel):

    def __init__(self,models:[ConnectedModel]):
        self.models=models
        pass
    
    
    def predict_on_dataset(self, d, **kwargs):
        raise ValueError("Not Implemented")

    def predictions(self,name, **kwargs)->DataSet:
        rm=[]
        for v in self.models:
            rm.append(v.predictions(name))

        result = rm[0] if len(rm) == 1 else MeanDataSet(rm)
        return result