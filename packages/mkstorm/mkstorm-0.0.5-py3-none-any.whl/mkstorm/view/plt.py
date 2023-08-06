#!-*-coding:utf-8-*-
import sys
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("../")
from  ..lib import file as fl
from  ..lib import message as ms

def boxplot( df , path , xlabels , ylabels ):
    sns.set(style="whitegrid")
    folder_path = path + "/boxplot/"
    for xlabel in xlabels:
        for ylabel in ylabels:
            sns.boxplot( x=xlabel, y=ylabel, data=df )
            file_path =  folder_path  + str( xlabel ) + "_" + str( ylabel ) + ".jpg"
            fl.mkdir( folder_path  )
            plt.savefig( file_path )
    ms.message("boxplot saved to " + str(folder_path) )
    plt.clf()


def paireplot( df , path , flag=True ):
    if flag:
        folder_path = path + "/pairplot/"
        file_path =  folder_path  + "paireplot" + ".jpg"
        fl.mkdir( folder_path  )
        sns.pairplot( df )
        plt.savefig( file_path )
        plt.clf()
        ms.message("paireplot saved to " + str(folder_path) )


def heatmap( corr , path , vmin=-1.0 , vmax=1.0 , flag=True ):
    if flag:
        folder_path = path + "/pairplot/"
        file_path =  folder_path  + "heatmap" + ".jpg"
        fl.mkdir( folder_path  )
        sns.heatmap(corr, annot=True , vmin=vmin , vmax=vmax , cmap="inferno")
        plt.savefig( file_path )
        plt.clf()
        ms.message("heatmap saved to " + str(folder_path) )

def cycle( x , path , labels , flag=True ):
    """
    Cycle graph
    """
    sns.set()
    plt.axis('equal')
    for i , x_el in enumerate( x ):
        folder_path = path + "/cycleplot/"
        file_path =  folder_path  + "cycle_" + "_".join(labels[i]) + ".jpg"
        plt.pie( x_el , labels=labels[i] , autopct="%.1f%%" )
        fl.mkdir( folder_path  )
        plt.savefig( file_path )
        plt.clf()
    ms.message("cycle saved to " + str(folder_path) )


def grouped_describe( df , path , groups ):
    folder_path = path + "/describe/"
    fl.mkdir( folder_path )
    for group in groups:
        file_path =  folder_path  + "grouped_describe_" + str( group ) + ".csv"
        grouped = df.groupby( group )
        grouped.describe().to_csv(file_path)
    ms.message("grouped_describe saved to " + str(folder_path) )


def lineplot( df , path , xlabels=[] ,  ylabels=[] ):
    folder_path = path + "/lineplot/"
    for i in range( len( xlabels ) ):
        file_path =  folder_path  + "lineplot_" + str( xlabels[i] ) + "_" + str( ylabels[i] ) + ".jpg"
        fl.mkdir( folder_path  )
        sns.lineplot(x=xlabels[i], y=ylabels[i], data=df)
        plt.savefig( file_path )
