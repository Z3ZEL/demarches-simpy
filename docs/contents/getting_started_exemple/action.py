from demarches_simpy import Profile, Dossier, AnnotationModifier

# Create a profile
profile = Profile('API_KEY',verbose=True)

# Create a dossier
dossier = Dossier(000000, profile)


# Assign an instructeur_id

# First method 
profile.set_instructeur_id('instructeur_id')

# Second method 
## Only works if the dossier is not in CONSTRUCTION state
instructeurs = dossier.get_attached_instructeurs_info()
instructeur = instructeurs[0]

# print(instructeur)
# > {'id': 'instructeur_id', 'email': 'mail@mail.com'}

profile.set_instructeur_id(instructeur['id'])

# Create the annotation action

action = AnnotationModifier(profile, dossier)

# Get an annotation

annotation = dossier.get_annotations()['annotation-label']

# print(annotation)
# > {'id': 'annotation_id', 'stringValue' : 'value'}

# Modify the annotation

annotation['stringValue'] = 'new_value'

# Perform the action

result = action.perform(annotation)

if result == AnnotationModifier.NETWORK_ERROR:
    print("Network error")
elif result == AnnotationModifier.SUCCESS:
    print("Success")


