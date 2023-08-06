
   

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
   >>from prepro import prepro 
   >>import pandas as pd
   >>ds=pd.read_excel("titanic3.xls")

   >>pro=prepro.missing(data=ds,min_ratio=0.21,
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

    ###