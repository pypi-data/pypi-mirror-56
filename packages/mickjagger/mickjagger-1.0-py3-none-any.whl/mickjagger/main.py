"""
La partie carte du module
"""
def plot_geo_time_value(x, y, year, value, proj='plate', titre='Annee', **kwargs):
    """
    Returns  many maps done with cartopy
    :param          x               vecteur de longitudes
    :param          y               vecteur de latitudes
    :param          value           vecteur des valeurs representees
    :param          year            vecteur des annees sur lesquelles les cartes sont faites
    :param          proj            le type de projection utilisee
    :param          titre           le titre voulu pour le graphique
    :kwargs                         parametres additionnels
    """
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from matplotlib import pyplot as plt
    from cartopy.feature import NaturalEarthFeature, COLORS
    import numpy as np
    import math
    
    
    resolution = "50m"
    BORDERS = NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land',
                              resolution, edgecolor='black', facecolor='none')
    STATES = NaturalEarthFeature('cultural', 'admin_1_states_provinces_lakes',
                             resolution, edgecolor='black', facecolor='none')
    COASTLINE = NaturalEarthFeature('physical', 'coastline', resolution,
                                edgecolor='black', facecolor='none')
    LAKES = NaturalEarthFeature('physical', 'lakes', resolution,
                            edgecolor='face',
                            facecolor=COLORS['water'])
    LAND = NaturalEarthFeature('physical', 'land', resolution,
                           edgecolor='face',
                           facecolor=COLORS['land'], zorder=-1)
    OCEAN = NaturalEarthFeature('physical', 'ocean', resolution,
                            edgecolor='face',
                            facecolor=COLORS['water'], zorder=-1)
    RIVERS = NaturalEarthFeature('physical', 'rivers_lake_centerlines', resolution,
                             edgecolor=COLORS['water'],facecolor='none')
    
    assert isinstance(x,np.ndarray), 'Erreur, x n est pas de type np.ndarray(vecteur)'
    assert isinstance(y,np.ndarray), 'Erreur, y n est pas de type np.ndarray(vecteur)'
    assert isinstance(year,np.ndarray), 'Erreur, year n est pas de type np.ndarray(vecteur)'
    assert isinstance(value,pd.DataFrame), 'Erreur, values n est pas de type pd.DataFrame'
    assert len(x)==len(y), 'Erreur, x et y doit etre de meme taille'
    assert type(year[0])== np.int32,'Erreur, les annees ne sont pas des entiers'
    assert type(proj)==str, 'Erreur: vous devez choisir une variable de projection de type string (pensez a changer)'
    assert proj in ['mercator','plate'], 'Erreur: la projection doit etre "mercato" ou "plate"'
    assert type(titre)==str,'Erreur, titre est un string'

    RADIUS = 6378137.0
    if len(year)%2 == 1 :
        a=len(year)//2 +1
    else:
        a= len(year)/2   
    fig = plt.figure(figsize=(10,7))

    
    
    c=[0]*len(x)
    b=[0]*len(y)
    if proj == 'mercator':
        for j in range(len(c)):
                c[j]=math.radians(x[j]) * RADIUS
                b[j]=math.log(math.tan(math.pi / 4 + math.radians(y[j]) / 2)) * RADIUS
    else:
        c=x
        b=y
    for i in range(len(year)):
        if proj == 'plate':
            ax = fig.add_subplot(a, 2, i+1, projection=ccrs.PlateCarree())
        else:
            ax = fig.add_subplot(a, 2, i+1, projection=ccrs.Mercator())
        ax.set_extent([-5, 10, 41, 52])
        ax.add_feature(BORDERS)
        ax.add_feature(LAKES)
        ax.add_feature(LAND)
        ax.add_feature(OCEAN)
        ax.add_feature(RIVERS)
        ax.add_feature(COASTLINE)
        if max(value.iloc[:,i])<=1:
            plt.scatter(c, b,s=value.iloc[:,i]*100, c=value.iloc[:,i], alpha=0.5)
        elif max(value.iloc[:,i])<=10:
            plt.scatter(c, b,s=value.iloc[:,i]*10, c=value.iloc[:,i], alpha=0.5)
        else:
            plt.scatter(c, b,s=value.iloc[:,i], c=value.iloc[:,i], alpha=0.5)
        plt.colorbar()
        ax.set_title(str(titre)+':'+str(year[i]))


def plot_folium_time_value(x, y, value, name,num, **kwargs):
    """
    Visualise donnee numerique geolocalisee sur une annee 
    par une jolie carte

    :param x: longitudes (vecteur)
    :param y: latitudes (vecteur)
    :param value: valeurs numeriques a representer (Dataframe ou vecteur de taille n_observations)
    :param name: noms des lieux  (vecteur)
    :param kwargs: parametres additionnels
    """
    import folium, branca
    
    assert type(x) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(y) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert len(x)==len(y), "Erreur, x et y doit etre de meme taille"
    assert type(value) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(name) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(num) == int, "Erreur : vous devez entrer un nombre entier, pensez a utiliser int()"

    # build the map
    coords = (46.6299767,1.8489683)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

    # define a colorbar between min and max values

    cm = branca.colormap.LinearColormap(['blue', 'yellow', 'red'], vmin=min(value), vmax=max(value))
    map.add_child(cm) # add this colormap on the display

    f = folium.map.FeatureGroup() # create a group

    for lat, lng, size, color in zip(y, x, value, value):
        f.add_child( # add iteratively a CircleMarker to this group
            folium.CircleMarker(
            location=[lat, lng],
            radius=num*size,
            color=None,
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6)
        )

    map.add_child(f) # add the group to the map

    map.save(outfile='map.html')
    
    return map

def plot_foliumTwo_time_value(x, y, value, name, num, **kwargs):
    """
    Visualise une donnee numerique geolocalisee sur une annee 
    par une jolie carte

    :param x: longitudes (vecteur)
    :param y: latitudes (vecteur)
    :param value: valeurs numeriques a representer (Dataframe ou vecteur de taille n_observations)
    :param name: noms des lieux  (vecteur)
    :param kwargs: parametres additionnels
    """
    import folium

    coords = (46.6299767,1.8489683)
    mapo = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    
    assert type(x) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(y) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert len(x)==len(y), "Erreur, x et y doit etre de meme taille"
    assert type(value) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(name) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(num) == int, "Erreur : vous devez entrer un nombre entier, pensez a utiliser int()"
    
    for i in range(len(name)):
        folium.CircleMarker(
        location = (y[i], x[i]),
        radius = value[i]*num,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson'
    ).add_to(mapo)
        
    
    return mapo


def save_image(x,y,values,years, **kwargs):
    """
    Enregistre les cartes dessinees dans le repertoire courant
    :param          x               vecteur de longitudes
    :param          y               vecteur de latitudes
    :param          values           vecteur des valeurs representees
    :param          years            vecteur des annees sur lesquelles les cartes sont faites
    :param          kwargs          parametres additionnels
    """
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from matplotlib import pyplot as plt
    from cartopy.feature import NaturalEarthFeature, COLORS
    import numpy as np

    assert isinstance(x,np.ndarray), 'Erreur, x n est pas de type np.ndarray(vecteur)'
    assert isinstance(y,np.ndarray), 'Erreur, y n est pas de type np.ndarray(vecteur)'
    assert isinstance(years,np.ndarray), 'Erreur, years n est pas de type np.ndarray(vecteur)'
    assert isinstance(values,pd.DataFrame), 'Erreur, values n est pas de type pd.DataFrame'
    assert len(x)==len(y), 'Erreur, x et y doit etre de meme taille'
    

    resolution = "50m"
    BORDERS = NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land',
                              resolution, edgecolor='black', facecolor='none')
    STATES = NaturalEarthFeature('cultural', 'admin_1_states_provinces_lakes',
                             resolution, edgecolor='black', facecolor='none')
    COASTLINE = NaturalEarthFeature('physical', 'coastline', resolution,
                                edgecolor='black', facecolor='none')
    LAKES = NaturalEarthFeature('physical', 'lakes', resolution,
                            edgecolor='face',
                            facecolor=COLORS['water'])
    LAND = NaturalEarthFeature('physical', 'land', resolution,
                           edgecolor='face',
                           facecolor=COLORS['land'], zorder=-1)
    OCEAN = NaturalEarthFeature('physical', 'ocean', resolution,
                            edgecolor='face',
                            facecolor=COLORS['water'], zorder=-1)
    RIVERS = NaturalEarthFeature('physical', 'rivers_lake_centerlines', resolution,
                             edgecolor=COLORS['water'],facecolor='none')

    
    for i in range(len(years)):
        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.set_extent([-5, 10, 41, 52])
        ax.add_feature(BORDERS)
        ax.add_feature(LAKES)
        ax.add_feature(LAND)
        ax.add_feature(OCEAN)
        ax.add_feature(RIVERS)
        ax.add_feature(COASTLINE)
        plt.scatter(x, y,s=values.iloc[:,i]*100, c=values.iloc[:,i], alpha=0.5)
        plt.colorbar()
        ax.set_title('Annee'+':'+str(years[i]))
        fig.savefig("carte"+str(years[i])+".png")
        plt.close(fig)
    return 


def gif (years, giffile = 'animation.gif', **kwargs):
    """
    Nous donne un graphique animee des cartes : le GIF 
    
    :param years : le vecteur des annees sur lesquels la representation est faite
    :param giffile : nom de notre gif
    :param kwargs : arguments supplementaires
    """
    assert type(years) == list, "Erreur : vous devez entrer une liste, pensez a utiliser list()"
    assert type(giffile) == str, "Erreur : vous devez entrer une chaine de caracteres, pensez a utiliser str()"
    
    import imageio
    
    images_data = []
    #load les images
    for i in range(len(years)):
        data = imageio.imread("carte"+str(years[i])+'.png')
        images_data.append(data)

    imageio.mimwrite(giffile, images_data, format= '.gif', fps = 1) # Le gif est enregristre dans le repertoire courant