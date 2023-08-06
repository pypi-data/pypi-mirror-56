#Cartography functions

import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from shapely.ops import unary_union
from shapely.prepared import prep
import cartopy.crs as ccrs

land_shp_fname = shpreader.natural_earth(resolution='50m',
                                       category='physical', name='land')

land_geom = unary_union(list(shpreader.Reader(land_shp_fname).geometries()))
land = prep(land_geom)

def is_land(x,y):
    return land.contains(sgeom.Point(x,y))

def platecarree2mercator(lon,lat):
    merc_point = ccrs.Mercator().transform_point(lon,lat,ccrs.PlateCarree())
    return merc_point[0], merc_point[1]

def platecarree2aziequ(lon,lat):
    merc_point = ccrs.AzimuthalEquidistant(central_latitude=90).transform_point(lon,lat,ccrs.PlateCarree())
    return merc_point[0], merc_point[1]