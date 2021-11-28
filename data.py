#!/usr/bin/python3

# Block specific tracks by their id. These won't be added to the playlist.
blocked_tracks = ["5fwSHlTEWpluwOM0Sxnh5k", # Pepas
                  "1SgUjGzbmmMOsGFTVwQ59L", # seaside_demo
                  "6MZ91tbZxwwqimJffOoLsW", # Computer Crash
                  "3Ofmpyhv5UAQ70mENzB277", # Astronaut In The Ocean
                  "1NawUUW8GmiRbJ9UkaKGY4", # Astronaut In The Ocean (Remix) - feat. G-Eazy & DDG
                  "37BZB0z9T8Xu7U3e65qxFy", # Save Your Tears (with Ariana Grande) (Remix)
                  "2sXf2JdbB2GlNju00kw9WE", # Skate
                  "40uMIn2zJLAQhNXghRjBed", # Motley Crew
                  "1MIGkQxcdAt2lDx6ySpsc5", # SUVs (Black on Black)
                  "4H0fjEbU9rzkz0Zp1ftPXD", # SUVs (Black on Black)
                  "4pt5fDVTg5GhEvEtlz9dKk", # I WANNA BE YOUR SLAVE
                  "3Wrjm47oTz2sjIgck11l5e", # Beggin'
                  "776AftMmFFAWUIEAb3lHhw", # ZITTI E BUONI
                  "5yHHWrpZhGc6zyHhbHE4rF", # Angles (feat. Chris Brown)
                  "3Ofmpyhv5UAQ70mENzB277", # Astronaut In The Ocean
                  "78SCmQ8A7KQSMdkem2SwBP"] # MAMMAMIA

# The playlist ids the script sources its song from (additionally to user's liked and top songs).
playlist_src = ["37i9dQZF1EpCIUOyPHFK4V", # Repeat Rewind
                "37i9dQZF1DXcBWIGoYBM5M", # Todays Top Hits
                "37i9dQZF1DX0XUsuxWHRQd", # RapCaviar
                "37i9dQZF1DXbYM3nMM0oPk", # Mega Hit Mix
                "37i9dQZF1DXaPCIWxzZwR1"] # Pop Sauce

CLIENT_ID = "<your client id>"
CLIENT_SECRET = "<your client secret>"
REDIRECT_URI = "<your redirect uri>"
