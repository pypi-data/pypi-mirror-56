#!-*-coding:utf-8-*-
import pandas as pd

__all__ = ["load"]

def load( path , columns ):
    df = pd.read_csv( path )
    if len( columns ) >= 1:
        return df.loc[ : , columns ]
    else:
        return df
