from demarches_simpy import Profile, Dossier, Demarche, DossierState

# Create a profile
profile = Profile('API_KEY',verbose=True)

# Create a dossier
demarche = Demarche(000000, profile, verbose=False)


specific_dossier = demarche.get_dossiers(-1, lambda dossier : dossier.number == 1234567)

print(len(specific_dossier)) # 1


## Background fetching

# Define a filter function
def filter(dossier : Dossier):
    return dossier.state == DossierState.INSTRUCTION


# Get all dossiers in Instruction State
filtered_dossier = demarche.get_dossiers(-1,dossier_filter=filter, background_fetching=True)


## Advanced usage

def filter(dossier : Dossier):
    for field in dossier.get_fields():
        if field.stringValue == 'foo':
            return True
    return False

advanced_filtered_dossier = demarche.get_dossiers(-1,dossier_filter=filter, background_fetching=True, default_variables={"includeFields": True})

