#!-*-coding:utf-8-*-
from .load import csv
from .lib import file as fl
from .lib import message as ms
from .view import plt
import numpy as np


__all__ = ["packer"]

class packer:

    def __init__( self , input_path , columns ):
        self.df = self._load( input_path , columns )
        self.array = np.array( self.df )
        self.describe = self.df.describe()
        self.corr = self.df.corr()
        self.columns = list( self.df.columns )


    def replace( self , col , frm , to ):
        """
        要素の文字列を置換
        """
        df_copy = self.df.copy()
        #df_copy[ df_copy!=frm ] = 0
        df_copy[ df_copy[col]==frm ] = to
        self.df = df_copy

    def col_serialize( self , col , frms ):
        ms.message( "Colums Serizlizing" )
        for i , val in enumerate( frms ):
            self.replace( col=col , frm=frms[i] , to=i )

        self._refresh()

    def rep_between( self ):
        """
        一定の区間に属するデータの値を置換する
        """
        pass


    def rm( self , cols , string ):
        """
        stringに指定された不正文字列をdataframeから除去する
        """
        df = self.df
        rems = []
        if "const" in cols: cols.remove( "const" )
        for i in range( len( df ) ):
            for col in cols:
                if df.ix[i,col] == string and i not in rems:
                    rems.append( i )

        for rm in rems:
            self.df = df.drop( rm )

        self._refresh()




    def cross_term( self , var1 , var2 ):
        """
        交差項を作成する
        """
        df = self.df
        df[str(var1)+"*"+str(var2)] = df.loc[ : , var1 ] * df.loc[ : , var2 ]

        self.df = df
        self._refresh()


    def add_col( self , col , val ):
        """
        列を追加
        """
        self.df[col] = val
        self._refresh()


    def dump( self , path , lineplot={"xlabels":[],"ylabels":[]} ,
     grouped_describe=[] , pieplots={"x":[],"labels":[]} ,  boxplots={"groupby":[],"ylabels":[]} , paireplot=True , heatmap=True ):

        plt.boxplot( self.df , path , boxplots["groupby"] , boxplots["ylabels"] )
        plt.cycle( path=path , x=pieplots["x"] , labels=pieplots["labels"] )
        plt.paireplot( self.df , path , flag=paireplot )
        plt.heatmap( self.corr , path , flag=heatmap )
        plt.grouped_describe( self.df , path , groups=grouped_describe )
        plt.lineplot( self.df , path , xlabels=lineplot["xlabels"] , ylabels=lineplot["ylabels"] )


    def controll( self ):
        pass


    def _load( self , path , columns ):
        df = csv.load( path , columns  )
        return df


    def _refresh( self ):
        self.array = np.array( self.df )
        self.describe = self.df.describe()
        self.corr = self.df.corr()
        self.columns = list( self.df.columns )

    def _success( text ):
        pass

    def _error( text ):
        pass
