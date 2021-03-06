# P10_API

Afin de créer l'environnement adéquate il vous faudra :

Tapez dans votre console Git Bash : git clone https://github.com/FraPar/P10_API.

Tapez dans votre console à l'emplacement que vous avez choisi pour votre dossier : "python -m venv env"

Exécutez depuis la console : "env/Scripts/activate.bat" (sous Windows) ou "source env/bin/activate"

Rentrez dans le dossier du projet : "cd P10_API/"

Installer l'ensemble des modules : "pip install -r requirements.txt"

Une fois effectué, il va falloir lancer les migrations via la démarche suivante:
- "cd api_project/",
- "python manage.py makemigrations",
- "python manage.py migrate".

Vous êtes maintenant en mesure de lancer le serveur en ecrivant la commande : "python manage.py runserver"

Félicitation, le serveur est lancé. Vous pouvez maintenant y accéder en tapant dans votre navigateur l'adresse de votre réseau local : "http://127.0.0.1:8000/"

Si vous avez besoin de vous connecter en tant que superadmin, utilisez les identifiants suivants :

Lien : "http://127.0.0.1:8000/admin"
Nom d'utilisateur : admin@gmail.com
Mot de passe : P4ssw0rd

S'il n'est pas créé et que vous souhaitez le faire, vous pouvez utiliser la commande suivante :
- "python manage.py createsuperuser"
