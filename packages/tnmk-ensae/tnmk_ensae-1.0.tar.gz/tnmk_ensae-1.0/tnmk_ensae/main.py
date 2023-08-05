# -*- coding: utf-8 -*-

# -- Auxiliary function 1 ---------------------------------------------------------------------------------------------------------

def tracer_couleurs(x,y,c,taille_points=[3,4,5,9],k=10):
  """
  fonction de couleurs pour faire dÃ©pendre la couleur du niveau de pollution.
  
  """
  import numpy as np
  import matplotlib.pyplot as plt
  #plt.figure(figsize=(15,15))
  q1,q2,q3=np.quantile(c,0.25),np.quantile(c,0.5),np.quantile(c,0.75)

  q1x=[i for i,j in zip(x,c) if j<=q1]
  q1y=[i for i,j in zip(y,c) if j<=q1]
  #plt.scatter(q1x,q1y,c=(0,0,1,0.1),s=3,label=f"Qte de dechets inferieur a {int(q1)}")
  plt.scatter(q1x,q1y,c=np.array((0,0,1,0.1)).reshape(1,4),s=taille_points[0],label=f"Qte de dechets inferieur a {int(q1)}")

  q2x=[i for i,j in zip(x,c) if np.logical_and(j>q1,j<=q2)]
  q2y=[i for i,j in zip(y,c) if np.logical_and(j>q1,j<=q2)]
  #plt.scatter(q2x,q2y,c=(0,0,1,0.35),s=4,label=f"Qte de dechets entre {int(q1)} et {int(q2)}")
  plt.scatter(q2x,q2y,c=np.array((0,0,1,0.35)).reshape(1,4),s=taille_points[1],label=f"Qte de dechets entre {int(q1)} et {int(q2)}")

  q3x=[i for i,j in zip(x,c) if np.logical_and(j>q2,j<=q3)]
  q3y=[i for i,j in zip(y,c) if np.logical_and(j>q2,j<=q3)]
  #plt.scatter(q3x,q3y,c=(0,0,1,0.65),s=5,label=f"Qte de dechets entre {int(q2)} et {int(q3)}")
  plt.scatter(q3x,q3y,c=np.array((0,0,1,0.65)).reshape(1,4),s=taille_points[2],label=f"Qte de dechets entre {int(q2)} et {int(q3)}")

  q4x=[i for i,j in zip(x,c) if j>q3]
  q4y=[i for i,j in zip(y,c) if j>q3]
  #plt.scatter(q4x,q4y,c=(0,0,1,1),s=9,label=f"Qte de dechets superieur a {int(q3)}")
  plt.scatter(q4x,q4y,c=np.array((0,0,1,1)).reshape(1,4),s=taille_points[3],label=f"Qte de dechets superieur a {int(q3)}")
  plt.legend(fontsize=k)
def baseVilles():
    import pandas as pd
    names=["n","departement","slug","NOM","nom_simple","nom_reel","nom_soundex",
           "nom_metaphone","code_postal","numero_commune","code_commune",
           "arrondissement","canton","population2010","population90",
           "population2012","densite_2010","surface",
           "long_degre","lat_degre","long_grd","lat_grd","long_dms","lat_dms","altitude_max","altitude_min"]
    #chemin="C:\\Users\\hp\\Desktop\\Projets Python\\Partage Graphe\\Emballage\\villes_france.csv"
    chemin="villes_france.csv"
    villes=pd.read_csv(chemin,sep=',',header=None,names=names)
    villes=villes.drop(["n","departement","nom_reel","nom_soundex",
                                "nom_metaphone","code_postal","numero_commune","code_commune",
                                "arrondissement","canton","population2010","population90",
                                "population2012","densite_2010","long_grd","lat_grd",
                                "long_dms","lat_dms","altitude_max","altitude_min"],axis=1)
    return villes

# -- Auxiliary function 2 ---------------------------------------------------------------------------------------------------------
	
def tracer_villes(noms,taille_cercle=15,police=12,proj='plate'):
    import pandas as pd
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    from random import random
    villes=baseVilles()
    for i in noms:
        x=villes.loc[np.logical_or(villes["slug"]==i,villes["NOM"]==i),"long_degre"]
        y=villes.loc[np.logical_or(villes["slug"]==i,villes["NOM"]==i),"lat_degre"]
        s=villes.loc[np.logical_or(villes["slug"]==i,villes["NOM"]==i),"surface"]
        l,k,m=random(),random(),random()
        if proj=="mercator":
            RADIUS = 6378137.0
            x=math.radians(x) * RADIUS
            y=math.log(math.tan(math.pi / 4 + math.radians(y) / 2)) * RADIUS
                
        plt.scatter(x,y,s=taille_cercle*s,alpha=0.6,c=np.array((k,l,m)).reshape(1,3),label=i)
        plt.text(x,y,i,fontsize=police,weight='bold')
        #plt.legend()

# -- Auxiliary function 3 ---------------------------------------------------------------------------------------------------------
		
def RaiseErrors(x, y, years, value,noms,proj="plate",method="gif"):
    import numpy as np
    import pandas as pd
    """
    if not np.logical_and(isinstance(x,pd.Series), isinstance(y,pd.Series)):
        raise ValueError("X, Y  doivent etre des dataFrame")
    if not np.logical_and(isinstance(years,range), isinstance(value,pd.DataFrame)):
        raise ValueError("Years doit etre un array, value un DataFrame!!")
    if len(x)!=len(y):
        raise ValueError("X et Y doivent avoir la meme taille!!")
    if len(x)!=len(value):
        raise ValueError("X et Value doivent avoir la meme taille!!")
    if np.logical_or(len(years)<=0,len(years)>=15):
        raise ValueError("Seulement 15 annees possibles")
    else:
        for i in years:
            if(np.logical_or(i<2003,i>2018)):
                raise VaueError("Annes entre 2003 et 2018!")
    if type(method)!=str:
        raise VaueError("method doit etre une chaine de caratere!")
    elif np.logical_and(np.logical_and(method!="gif", method!="mp4"), np.logical_and(method!="avi", method!="webm")):
        raise VaueError("La mÃ©thode de rÃ©presentation n'est pas correcte veuillez choisir entre 'gif', 'webm', 'avi' et 'mp4'")
    """
    xSeries=not isinstance(x,pd.Series)
    ySeries=not isinstance(y,pd.Series)
    yRange=not isinstance(years,range)
    vDF=not isinstance(value,pd.DataFrame)
    xEy=not len(x)==len(y)
    yInt=not type(years[0])== np.int
    pString=not type(proj)==str
    #pChoix=not proj in ['mercator','plate']
    
    mxSeries='Erreur, x n est pas de type np.ndarray(vecteur)'
    mySeries='Erreur, y n est pas de type np.ndarray(vecteur)'
    myRange='Erreur, year n est pas de type np.ndarray(vecteur)'
    mvDF='Erreur, values n est pas de type pd.DataFrame'
    mxEy='Vecteur doit Ãªtre de mÃªme taille'
    myInt='Erreur, les annees ne sont pas des entiers'
    mpString='Erreur: vous devez choisir une variable de projection de type string (pensez a changer)'
    #mpChoix='Erreur: la projection doit Ãªtre "mercato" ou "plate"'
    
    masque=[xSeries,ySeries,yRange,vDF,xEy,yInt,pString]
    messages=[mxSeries,mySeries,myRange,mvDF,mxEy,myInt,mpString]
    m=[messages[i] for i in range(len(masque)) if masque[i]==False]
    #print(masque)
    #print(messages)
    #print(m)
    assert np.sum(masque)>0, m

# -- Auxiliary function 4 ---------------------------------------------------------------------------------------------------------
    
def messageErreur(x, y, years, value,noms,proj="plate",method="gif"):
    import numpy as np
    import pandas as pd
    xSeries=isinstance(x,pd.Series)
    ySeries=isinstance(y,pd.Series)
    yRange=isinstance(years,range)
    vDF=isinstance(value,pd.DataFrame)
    xEy=len(x)==len(y)
    yInt=type(years[0])== np.int
    pString=type(proj)==str
    #pChoix=not proj in ['mercator','plate']
    
    mxSeries='Erreur, x n est pas de type np.ndarray(vecteur)'
    mySeries='Erreur, y n est pas de type np.ndarray(vecteur)'
    myRange='Erreur, year n est pas de type np.ndarray(vecteur)'
    mvDF='Erreur, values n est pas de type pd.DataFrame'
    mxEy='Vecteur doit Ãªtre de mÃªme taille'
    myInt='Erreur, les annees ne sont pas des entiers'
    mpString='Erreur: vous devez choisir une variable de projection de type string (pensez a changer)'
    #mpChoix='Erreur: la projection doit Ãªtre "mercato" ou "plate"'
    
    masque=[xSeries,ySeries,yRange,vDF,xEy,yInt,pString]
    messages=[mxSeries,mySeries,myRange,mvDF,mxEy,myInt,mpString]
    m=[messages[i] for i in range(len(masque)) if masque[i]==False]
    #print(masque)
    #print(messages)
    print(m)

# -- principal function 1 ---------------------------------------------------------------------------------------------------------

def plot_geo_time_value(x, y, years, value,names,proj='plate'):
    try:
        RaiseErrors(x, y, years, value,names)
    except:
        import pandas as pd
        import urllib.request
        import zipfile
        from tqdm import tqdm
        from pyproj import Proj, transform
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        import matplotlib.pyplot as plt
    
        n=len(years)
        ## crÃ©ation d'un dictionnaire pour les donnÃ©es
    
        a={years[i]:value['Quantite'+str(years[i])] for i in range(n)}
    
        fig = plt.figure(figsize=(20,20), dpi=80)
        if proj=="mercator":
            import math
            RADIUS = 6378137.0
            c=[0]*len(x)
            b=[0]*len(y)
            for j in range(len(x)):
                c[j]=math.radians(x[j]) * RADIUS
                b[j]=math.log(math.tan(math.pi / 4 + math.radians(y[j]) / 2)) * RADIUS
                
            projection=ccrs.Mercator()
        else:
            c=x
            b=y
            projection=ccrs.PlateCarree()

    
        for k, i in zip(a.keys(),range(1,n+1)):
            
            t=n/2 if (n%2)==0 else 1+n//2
            
            plt.subplot(t,2,i)
            
            ax= fig.add_subplot(t, 2, i, projection=projection)
            ax.set_extent([-5, 10, 42, 52])
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
            ax.add_feature(cfeature.RIVERS.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
    
            u=[s for s,j in zip(c[:],a[k][:]) if  j>0]
            v=[s for s,j in zip(b[:],a[k][:]) if  j>0]
            E=[j for j in a[k][:] if  j>0]
            
            plt.axis("off")
            tracer_couleurs(u,v,E)   
            tracer_villes(names,proj=proj)
            
            plt.title('Carte de pollution des entreprises en France en ' + str(years[i-1]), fontsize=15)
        else:
            messageErreur(x, y, years, value,names)
 
# -- principal function 2 --------------------------------------------------------------------------------------------------------- 
        
def  plot_gif_geo_time_value(x, y, years, value,names, method='gif',proj='plate'):
    try:
        RaiseErrors(x, y, years, value,names,method="gif")
    except:
        import pandas as pd
        import urllib.request
        import zipfile
        from tqdm import tqdm
        from pyproj import Proj, transform
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        import matplotlib.pyplot as plt
        from PIL import Image, ImageDraw
        import os
        n=len(years)
         ## création d'un dictionnaire pour les données
        
        
        a={years[i]:value['Quantite'+str(years[i])] for i in range(n)}
        fig = plt.figure(figsize=(20,20), dpi=80)
        
        if proj=="mercator":
            import math
            RADIUS = 6378137.0
            for j in range(len(x)):
                x[j]=math.radians(x[j]) * RADIUS
                y[j]=math.log(math.tan(math.pi / 4 + math.radians(y[j]) / 2)) * RADIUS
                projection=ccrs.Mercator()
        else:
            projection=ccrs.PlateCarree()
        
        for k, i in zip(a.keys(),range(1,n+1)):
            fig = plt.figure(figsize=(30,30))
            ax= fig.add_subplot(1, 1, 1, projection=projection)
            ax.set_extent([-5, 10, 42, 52])
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
            ax.add_feature(cfeature.RIVERS.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
            u=[s for s,j in zip(x[:],a[k][:]) if  j>0]
            v=[s for s,j in zip(y[:],a[k][:]) if  j>0]
            E=[j for j in a[k][:] if  j>0]
            # Représentation de niveau de pollution de chaque entreprise selon la colorimétrie des points
            tracer_couleurs(u,v,E,taille_points=[10,30,50,100],k=30)
            # Représentation des villes ou espaces urbains
            tracer_villes(names,taille_cercle=60,police=20,proj=proj)
            plt.title('Carte de pollution des entreprises en France en ' + str(years[i-1]), fontsize=40)    
            plt.savefig('Carte'+str(i)+'.png')
            plt.close(fig)
            
        images = []
        
        # Si la méthode choisie est un fichier 'gif'
        if method=='gif':
            # On ouvre et compile toutes les cartes dans un seul objet "images"
            for i in range(1,n+1):
                im = Image.open('Carte'+str(i)+'.png')
                images.append(im)
            # On sauvegarde le fichier sous le nom "ma_carte_animee.gif"
            images[0].save('ma_carte_animee.gif', save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0)
            # On importe les fonctions Image et display du package IPython.display pour la lecture et l'affichage du fichier
            from IPython.display import Image as IMG 
            from IPython.display import display
            display(IMG(url='ma_carte_animee.gif'))
        
        # Si la représentation désirée est une vidéo    
        if method=='avi' or method=='mp4' or method=='webm':
            import cv2                        
            from IPython.display import HTML
            # Si la représentation désirée est une vidéo
            fps = 0.5
            import numpy as np
            # On ouvre et compile toutes les cartes dans un seul objet "images" avec la fonction imread du package 
            # cv2 (opencv-python)
            for i in range(1,n+1):
                im = cv2.imread('Carte'+str(i)+'.png')
                images.append(im)
            # On définie les dimensions de la vidéo qu'on fixe à l'un des éléments de "images" mais puisque les cartes créées plus haut
            # ont toutes les mêmes dimensions on peut choisir n'importe quel élément
            height,width,layers=images[1].shape
            # Pour le fichier de type mp4
            if method=='mp4':
                # On choisit l'encodage de la vidéo avec le paramètre *'MP4V' au niveau de la fonction VideoWriter_fourcc de cv2
                fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                # Création du fichier avec ses caractéristiques
                video=cv2.VideoWriter('ma_carte_animee.mp4',fourcc, fps,(width,height))
            # Pour le fichier de type webm
            elif method=='webm': 
                # On choisit l'encodage de la vidéo avec le paramètre *'VP80'
                fourcc = cv2.VideoWriter_fourcc(*'VP80')
                # Création du fichier avec ses caractéristiques
                video=cv2.VideoWriter('ma_carte_animee.webm',fourcc, fps,(width,height))
            # Pour le fichier de type avi
            else :
                # On choisit l'encodage de la vidéo avec le paramètre *'DIVX'
                fourcc = cv2.VideoWriter_fourcc(*'DIVX')
                # Création du fichier avec ses caractéristiques
                video=cv2.VideoWriter('ma_carte_animee.avi',fourcc, fps,(width,height))
            for i in range(0,n):
                # Ecriture de la vidéo
                video.write(images[i])
            cv2.destroyAllWindows()
            video.release()
        else:
            messageErreur(x, y, years, value,names)

# -- end file ---------------------------------------------------------------------------------------------------------
