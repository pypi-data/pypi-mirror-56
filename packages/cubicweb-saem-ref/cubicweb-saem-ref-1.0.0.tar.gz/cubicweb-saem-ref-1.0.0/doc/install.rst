============
Installation
============

Configuration du serveur PostgreSQL
===================================

Si vous n'en n'avez pas encore un disponible, il faut commencer par installer un serveur PostgreSQL
(pas nécessairement sur la même machine que le réferentiel). Sur une distribution Redhat / CentOS,
les paquets suivants sont nécessaires coté serveur : ``postgresql<version>-contrib``,
``postgresql<version>-plpython``, ``postgresql<version>-server`` où ``<version>`` peut-être par
exemple ``96`` selon la distribution utilisée.

Il faudra ensuite créer un utilisateur dédiée au référentiel, par exemple nommée "saemref" et
permettre l'accès depuis le client.

Installation via Docker
=======================

Le projet `saemref-docker`_ fournit un environnement `docker-compose`_ permettant de déployer le
référentiel. C'est la façon recommandée et la plus simple de l'installer. Voir la documentation du
projet pour plus de détails :

  https://framagit.org/saemproject/saemref-docker/blob/master/README.md

.. _`saemref-docker`: https://framagit.org/saemproject/saemref-docker
.. _`docker-compose`: https://docs.docker.com/compose/

Installation manuelle
=====================

La procédure décrite dans cette section concerne l'installation manuelle du référentiel. Elle se
base sur une combinaison de paquets système (disponibles via une distribution Linux) et un
environnement virtuel Python.

Les paquets systèmes suivants sont nécessaires (``yum install`` sur une distribution Redhat/CentOS) :

- mailcap
- graphviz-gd
- python-devel
- gcc-c++
- python3
- python3-pip
- python3-setuptools
- python3-lxml
- python3-psycopg2
- postgresql

Nous recommandons d'installer le code du référentiel avec un utilisateur standard (pas *root*) :

::

    [root@srv]% adduser saemref
    [root@srv]% su - saemref

et dans un virtualenv_, qu'il convient donc de créer puis d'activer :

::

    [saemref@srv ~]$ python3 -m venv saemref-venv
    [saemref@srv ~]$ . saemref-venv/bin/activate
    (saemref-venv) [saemref@srv ~]$ 

Par la suite, nous supposerons que vous tapez les commandes indiquées en tant qu'utilisateur
`saemref` et avec le *virtualenv* activé.

Installer le référentiel :

::

    pip install cubicweb-saem-ref


Création de l'instance
----------------------

Une fois le cube saem_ref et ses dépendances installées, il reste à créer une
instance de celui-ci :

::

  cubicweb-ctl create saem_ref saemref

.. note ::

    La phase finale de création prend quelques minutes, afin de remplir la base
    avec quelques données nécessaires au bon fonctionnement de l'application.

* Laisser le choix par défaut à la plupart des questions, si ce n'est pour:

  - ``db-name`` : choisir le nom de la base créée depuis le serveur PostgreSQL (ex. ``saemref``)
  - ``db-user`` / ``db-password`` : mettre les informations de l'utilisateurs PostgreSQL
  - ``Allow anonymous access ?`` : mettre ``y`` pour ne pas restreindre l'accès en lecture

* Choisir un login / mot de passe administrateur sécurisé (admin/admin est une
  mauvaise idée, nous recommandons d'installer le paquet ``pwgen`` et de
  générer un mot de passe aléatoire avec la commande ``pwgen 20``).

Selon votre configuration postgres, vous pouvez avoir à modifier le fichier sources pour y spécifier
les informations de connexion au serveur (hôte, port, utilisateur et mot de passe). Le plus simple
est de répondre non à la question "Run db-create to create the system database ?", d'éditer le
fichier `~/etc/cubicweb.d/saemref/sources` puis de reprendre le processus d'initialisation en
tapant :

::

  cubicweb-ctl db-create saemref -cn

Vous pouvez maintenant vérifier que l'instance se lance :

::

  cubicweb-ctl pyramid -D saemref

L'instance est désormais lancée et disponible sur le port 8080.

Pour une instance de production, il est recommandé d'utilisé un serveur d'application WSGI tel que
`gunicorn`_ et un superviseur tel que `supervisor`_.

::

   pip install gunicorn


Configuration de supervisor
---------------------------

supervisor_ permet de gérer les différents services de l'application, à savoir
: le serveur web principal (programme "saemref"), le point d'accès OAI-PMH
(programme "saemref-oai") et le gestionnaire de tâches (programme
"saemref-scheduler").

Un exemple de configuration supervisor, à mettre dans
``/etc/supervisor/conf.d/saemref.conf``:

.. include:: supervisor.conf
   :code: ini

Mise à jour de l'instance
-------------------------

.. warning::

  Il y aura donc une interruption de service pendant cette opération

Lors qu'une nouvelle version est livrée, il faut commencer par mettre à jour le code de
l'application. Le plus simple pour cela est de supprimer le *virtualenv* et de le recréer. Si vous
avez installé le référentiel avec pip :

::

    [root@srv] % supervisorctl stop all
    [root@srv] % su - saemref
    $ rm -rf saemref-venv
    $ python3 -m venv saemref-venv
    $ . saemref-venv/bin/activate
    (saemref-venv)$ pip install cubicweb-saem-ref

Puis il reste à mettre à jour l'instance CubicWeb.

::

    cubicweb-ctl upgrade saemref

La commande `cubicweb-ctl upgrade` pose un certain nombre de questions,
auxquelles il faut toujours répondre par oui (en tapant 'y' ou Entrée directement). Un backup de la
base de données est effectué avant la migration afin de pouvoir rejouer une migration en cas de
problème.

Relancer enfin ``supervisor``:

::

   [root@srv] % supervisorctl start all

Lancement de l'instance en mode debug
-------------------------------------

Pour comprendre certains problèmes, il peut-être utile de lancer l'instance en mode "debug" afin
d'augmenter le niveau de détails des *logs*. Pour cela, il faut mettre : ::

    log-threshold=DEBUG

dans le fichier ``~saemref/etc/cubicweb.d/saemref/all-in-one.conf`` puis relancer l'instance :

::

    [root@srv] % supervisorctl restart all


Configuration du frontal web
============================

Il faut configurer le frontal web pour diriger les différentes requêtes sur
chacun des services configurés (le serveur web principal et le serveur
OAI-PMH). Ci-dessous un exemple de configuration pour nginx :

::

    server {
        listen 80;
        server_name saemref.example.com;
        location / {
            proxy_pass http://srv:8080;
        }
        location /oai {
            proxy_pass http://srv:8081;
        }
    }


.. _pip: https://pip.pypa.io/
.. _virtualenv: https://docs.python.org/3/library/venv.html
.. _gunicorn: http://gunicorn.org/
.. _supervisor: http://supervisord.org/
