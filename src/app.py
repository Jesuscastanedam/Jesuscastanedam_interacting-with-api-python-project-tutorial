import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()
# 
import os

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Aqui se optiene la URL y las canciones más escuchadas del artista.

rawa_uri = 'https://open.spotify.com/artist/2AbQwU2cuEGfD465wCXlg2?si=MJUnVQPoQYG9Bhz8ssQz_w'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials( client_id=client_id, client_secret=client_secret))

results = spotify.artist_top_tracks(rawa_uri)
top_tracks = []
for track in results['tracks'][:5]:
    print('track    : ' + track['name'])
    print('duration :'  + str(track['duration_ms'] / 60000.12)+'min')
    print('popularity    : ' + str(round(track['duration_ms'] / 60000.12, 2)))
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
    top_tracks.append(((track['name'], round(track['duration_ms'] / 60000.12, 2),track['popularity'])))

# En el siguiente paso se transforma a un Dataframe.
dt = pd.DataFrame(top_tracks)
dt.rename(columns={1: 'Tiempo', 2: 'Popularidad'}, inplace=True)

# Aquí se ordena y se filtra el dataset.
dt_sort = dt.sort_values(by='Popularidad',ascending=False)
dt_top_3 = dt_sort.loc[dt_sort['Popularidad']>=67]

# En este punto se grafica el dt y se saca la conclusión de los resultados.
import matplotlib.pyplot as plt
sns.scatterplot(x=dt_top_3['Tiempo'],y=dt_top_3['Popularidad'])

# Agregar etiquetas a cada punto
for i in range(len(dt_top_3)):
    plt.text(dt_top_3["Tiempo"][i], dt_top_3['Popularidad'][i], dt_top_3[0][i], 
             horizontalalignment='left', verticalalignment='bottom', 
             fontsize=12, color='black')


plt.show()

# Conclusion
# Dada la escasez de datos, es difícil llegar a una conclusión sólida. Según lo observado 
# en el gráfico, no hay suficiente evidencia para sostener que las canciones más cortas sean 
# más populares. Además, el análisis no considera cuándo se lanzaron las canciones: con el tiempo, 
# su popularidad podría disminuir independientemente de su duración, lo que añade otra variable 
# no contemplada, tambien se podría tomar en cuenta más variables como género musical, artista, 
# promoción, etc.