import pandas as pd
import numpy as np

def missing(data='',min_ratio=0.0,values='',method='mean',drop_max="no"):
    """
    prepro.missing(data="",min_ratio=0.0,values="",method="mean",drop_max="no)
    Parameters:
    (value parameter is mandatory)
    data:
        Input data for the processing
    min_ratio:
        the minimum level of missing values having column only preprocessed
        example min_ratio=0.5 ,
        only less than 50%missing values columns are only will be preprocessed
    *values:
        Giving input as which columns are need to be processed
        example values="all" #for all missing values to be preprocessed ,
        values=["age","fare"] #for particular missing values to be preprocessed
    method:
        method it has be used for filling missing values
        methods are : mean , median , mode
    drop_max:
        it will delete the column which has been having more than ratio you have
        mentioned in min_ratio , so for that you must mention the min_ratio
        example
        missing(data=ds,min_ratio=0.21,drop_max="yes")
        #it will delete all the missing columns which is higher than min_ratio
   ```
   >>from prepro import missing
   >>import pandas as pd
   >>ds=pd.read_excel("titanic3.xls")

   >>pro=missing(data=ds,min_ratio=0.21,
   method="mean",values="all",drop_max="yes")
   ----------------------------------------------
   Missing Values by colunm 
     age     0.200917
    fare    0.000764
    body    0.907563
    dtype: float64
    ----------------------------------------------
    >>pro.isnull().mean()#body column has been dropped , 
    age and fare has been updated
    ----------------------------------------------
    pclass       0.000000
    survived     0.000000
    name         0.000000
    sex          0.000000
    age          0.000000
    sibsp        0.000000
    parch        0.000000
    ticket       0.000000
    fare         0.000000
    cabin        0.774637
    embarked     0.001528
    boat         0.628724
    home.dest    0.430863
    dtype: float64
    ----------------------------------------------
    
    """
    try:
        original_data=data
        data=data._get_numeric_data()
        val=data.columns[data.isnull().any()]
        data=data.loc[:,val]
        print("Missing Values by colunm \n",data.isnull().mean())

        a=data.isnull().mean()
        ds=data
        l=len(data.columns)
        try:
            data.iloc[:,0]
            i=0
        except:
            i=1
        global miss
        global li
        global dr
        global dr1
        li=[]
        dr=[]
        dr1=''
        miss=ds.columns[ds.isnull().any()]

        try:
            for i in range(i,l):
                if a[i]==0.0:
                    pass
                elif a[i]<min_ratio:
                    li.append(i)
                else:
                    dr.append(i)

        except:
            pass


        if (values=="" and min_ratio!=0.0) or (values=="all" and min_ratio!=0.0):
            for v in li:


                if method=="mean":

                    me=data.iloc[:,v].mean()
                    data.iloc[:,v]=data.iloc[:,v].fillna(me)
                elif method=="median":
                    me=data.iloc[:,v].median()
                    data.iloc[:,v]=data.iloc[:,v].fillna(me)
                elif method=="mode":
                    me=data.loc[:,v].mode()
                    data.iloc[:,v]=data.iloc[:,v].fillna(me)
                else:
                    me=data.iloc[:,v].mean()
                    data.iloc[:,v]=data.iloc[:,v].fillna(me)


        elif values=='all' or values=='All':
            for m in miss:
                if method=="mean":
                    me=data.loc[:,[m]].mean()
                    data.loc[:,[m]]=data.loc[:,[m]].fillna(me)
                elif method=="median":
                    me=data.iloc[:,v].median()
                    data.loc[:,m]=data.loc[:,m].fillna(me)
                elif method=="mode":
                    me=data.loc[:,v].mode()
                    data.loc[:,m]=data.loc[:,m].fillna(me)
                else:
                    me=data.loc[:,m].mean()
                    data.loc[:,m]=data.loc[:,m].fillna(me)

        else:
            if type(values[0]) is str:
                for v in values:
                    if method=="mean":
                        me=data.loc[:,v].mean()
                        data.loc[:,v]=data.loc[:,v].fillna(me)
                    elif method=="median":
                        me=data.loc[:,v].median()
                        data.loc[:,v]=data.loc[:,v].fillna(me)
                    elif method=="mode":
                        me=data.loc[:,v].mode()
                        data.loc[:,v]=data.loc[:,v].fillna(me)
                    else:
                        me=data.loc[:,v].mean()
                        data.loc[:,v]=data.loc[:,v].fillna(me)
            elif type(values[0]) is int:
                for v in values:
                    if method=="mean":

                        me=data.loc[:,v].mean()
                        data.iloc[:,v]=data.iloc[:,v].fillna(me)
                    elif method=="median":
                        me=data.iloc[:,v].median()
                        data.iloc[:,v]=data.iloc[:,v].fillna(me)
                    elif method=="mode":
                        me=data.loc[:,v].mode()
                        data.iloc[:,v]=data.iloc[:,v].fillna(me)
                    else:
                        me=data.iloc[:,v].mean()
                        data.iloc[:,v]=data.iloc[:,v].fillna(me)


        dr1=data.columns[dr]
        
    except:
        pass
    original_data[data.columns]=data[data.columns]
    if drop_max=="no":
            pass
    else:
        original_data=original_data.drop(dr1, axis=1)


    return original_data


def mis_col(data=''):
    """
    returns the missing column number
    """
    global miss
    miss=[]

    try:
        miss=data.columns[data.isnull().any()]
    except:
        print("FileNotFoundError")
    return miss
