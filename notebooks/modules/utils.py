

# modules.utils.py
# ==================================================
import pandas as pd
import numpy as np
import seaborn as sns
from geopy import distance
# --------------------------------------------------

class percentPlot:
    
    @classmethod
    def seaPlot(self, mydf, xvar, ytitle, *args, **kwargs):
        '''
        Plot de barras y porcentajes:
        mydf: Pandas DataFrame.
        xvar: Variable en eje x.
        ytitle: Title de eje y.
        *args: Positional arguments desde sns.barplot.
        **kwargs: Keyword arguments desde seaborn.barplot.
        '''
        df_cat = (
            mydf[xvar]
            .value_counts(normalize=True)
            .mul(100)
            .rename(ytitle)
            .rename_axis(xvar)
            .reset_index()
        )
        sns.barplot(x=xvar, y=ytitle, data=df_cat, *args, **kwargs)

def km_bpoints(df, point_xy, lon_column='longitud', lat_column='latitud'):
    '''
    Retorna serie de distancia en km entre dos puntos.
    df: Pandas DataFrame.
    lon_column: columna longitud.
    lat_column: columna latitud.
    point_xy: Columna de collections de longitudes y latitudes.
    '''
    def inner(df):
        np_lon_lat = df[[lat_column, lon_column]].values.tolist()
        np_np = df[point_xy]
        return distance.distance(np_np, np_lon_lat).km
    return df.apply(inner, axis=1)

def BinEncoder(pandas_series, pkl_path: str='./items/distritos_category.pkl'):
    mapper_frame = pd.read_pickle(pkl_path)
    def inner_func(x):
        return mapper_frame.loc[x]
    return pandas_series.apply(inner_func).iloc[:, 0].values

def downCastingInt(pandas_series):
    return pd.to_numeric(pandas_series, downcast='integer')

def getMainPoints(pandas_dataframe, pkl_path='./items/main_p.pkl'):
    mapper_obj = pd.read_pickle(pkl_path)
    return pandas_dataframe.join(mapper_obj)
