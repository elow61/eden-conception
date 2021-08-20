# Eden Conception

Cette application web a été développé dans le but de réaliser un projet de formation. Elle propose un système de gestion de projets permettant ainsi de créer un projet composé de tâches. Il est possible de réaliser un système de sprint (de la même manière qu'on l'utiliserait en méthodologie agile) grâce à son système de "listes" embarquant chaque tâches. Un système de gestion du temps est accessible lorsque nous accédons au détail d'une tâche. Ainsi, chaque collaborateur présent sur un projet pourrons saisir leur temps passé sur une tâche afin d'obtenir un suivi.

Cette application a été développé en orienté objet (côté backend) afin de conserver la structure standard du framework Django, utilisé également dans celle-ci. La partie frontend utilise la librairie jQuery.

## Installation

Pour installer le projet en local, il conviendra de le cloner dans un premier temps. Quelques variables d'environnement seront également nécessaire.

La plus important est la variable "ENV". Il faudra indiquer à l'application que vous n'êtes pas en mode production. Il suffit pour cela, de taper la commande suivante (après avoir installer et activer votre environnement virtuel) :

    export ENV='NO_PROD'

/!\ Attention - il vous faudra indiquer également les variables d'environnement suivantes : 

Pour la base de données :
- DB_NAME = 'Nom de la base de données'
- DB_USER = 'Utilisateur de la base de données'
- DB_PASS = 'Mot de passe de la base de données'
- DB_HOST = 'localhost'

Pour le serveur SMTP (Fonction de réinitialisation de mot de passe) :
- EMAIL_HOST = 'L'hôte pour le serveur SMTP' ex : smtp.gmail.com
- EMAIL_USER = 'L'email de l'utilisateur du serveur SMTP'
- EMAIL_PASS = 'Le mot de passe'
- EMAIL = 'L'adresse mail qui enverra le mail'

Ensuite, il faudra installer les dépendances :

    pip install -r requirements.txt 

## Lancement du serveur

Pour lancer le serveur il suffit de taper la commande Django suivante :

    ./manage.py runserver

## Développement

Concernant la partie développement, voici les applications présentes au sein du projet : 

* **project** : permettant la gestion des projets (le dashboard -> création, édition, ajout de membre, suppression), les listes (création, édition, suppression), et les tâches (création, édition, suppression)

* **static_page** : permettant de gérer les pages front (accueil, mentions légales).

* **timesheet** : permettant la gestion des temps sur chaque tâche.

* **user** : permettant la gestion de l'utilisateur (connexion, inscription, mot de passe perdu).

L'application utilise le processeur Sass permettant la création et la lecture de fichiers scss.
Pour récupérer les fichiers statiques, 2 commandes doivent être lancées dans l'ordre suivant :

    ./manage.py compilescss
    ./manage.py collectstatic

** Visiter l'application web

Voici le lien du projet : http://eden-conception.elodie-meunier.fr/