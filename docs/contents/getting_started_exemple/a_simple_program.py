from demarches_simpy import Profile, Demarche, Dossier

# Create a profile
profile = Profile('API_KEY', verbose=True)

# Create a demarche
demarche = Demarche(000000, profile, verbose=False)

for dossier in demarche.get_dossiers():
    print(dossier.get_dossier_state())
