# Pre-config pour VM reseaux linux

## (Ex1) gitlab-runner configuration:
- choisir le bon package à:

https://gitlab-runner-downloads.s3.amazonaws.com/latest/index.html

- pour installer un fichier .deb:

```
sudo dpkg -i package_file.deb
```

- pour installer et lancer comme service :
```
sudo gitlab-runner start
```

## (Ex2) poetry configuration:

- installer poetry et tox:
```
pip3 install poetry
pip3 install tox
```

- creer un nouveau projet poetry:

```
poetry new <nom_projet>
```

- configuration tox:
rajouter un fichier tox.ini à la racine pour pouvoir lancer les test avec comme contenu:
```
[tox]
envlist = my_env
skipsdist = true

[testenv]
deps = pytest
commands = pytest
```

ajouter dans pyproject.toml :
```
[tool.poetry.dev-dependencies]
pytest-cov = "^3.0.0"
pytest = "^6.2.5"
tox = "3.4.0"
```

puis finalement lancer pour mettre a jour et compiler :
```
poetry lock --no-update
poetry install
```

- pour lancer tox , avec au préalable des fichiers de test dans le dossier tests:
```
poetry shell
tox
```


# (Ex3) Runner configuration

## creer un nouveau runner

depuis le site gitlab.univ-lr.fr/%{project_path}

Settings > CI/CD  > Runners > Projet runners > New project runner
puis configurer le runner et suivre les procédures, en particulier pour l'étiquetage et pour l'enregistrement du runner sur gitlab

- pour enregistrer un runner (creer et remplie aussi le fichier config.toml de gitlab-runner si il n'existait pas):
```
sudo gitlab-runner register --url https://gitlab.univ-lr.fr/ --registration-token {TOKEN}
```
-- le registration-token peut etre trouvé dans Settings > CI/CD > Runners > Project Runners
dans les prompts ensuite on met:
```
Enter the GitLab instance URL: ""
Enter the registration token: le registration token
Enter a description for the runner: ""
Enter tags for the runner: test(tag de mes jobs) ou ""
Enter optional maintenance note for the runner: ""
Enter an executor: docker
Enter the default Docker image: docker:latest
```

- pour supprimer un runner :
```
gitlab-runner unregister --url https://gitlab.univ-lr.fr/ --token {TOKEN}
```


# Gestion des badges

## pour ajouter des badges dans le projet:

https://docs.gitlab.com/ee/user/project/badges.html#test-coverage-report-badges

à Appliquer depuis le site gitlab.univ-lr.fr/%{project_path} dans Settings > General > Badges > Add badge

Dans le cadre de ce projet :
pour la case link:
```
https://gitlab.univ-lr.fr/%{project_path}
```
pour la case Badge image URL:
```
https://gitlab.univ-lr.fr/%{project_path}/badges/%{default_branch}/coverage.svg
```

## Badges pour le couverture de code pour les test dans Pipeline editor

https://docs.gitlab.com/ee/ci/testing/test_coverage_visualization.html 

dans le fichier .gitlab-ci.yml ou a partir de Pipeline Editor sur le site, un example de job pour la couverture de code pythosn:
```
run tests:
  stage: test
  image: python:3
  script:
    - pip install pytest pytest-cov
    - pytest --cov --cov-report term --cov-report xml:coverage.xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

# (Ex4) Deploiement automatique 

## poetry-dynamic-versioning configuration

- pour ajouter le plugin poetry-dynamic-versioning au projet et le verifier:
```
sudo poetry self add "poetry-dynamic-versioning[plugin]"
pip install poetry-dynamic-versioning
poetry self show
poetry dynamic-versioning --help 
```

À ajouter dans pyproject.toml : 
```
[tool.poetry-dynamic-versioning]
enable = true

[build-system]
requires = ["poetry-core>=1.3", "poetry-dynamic-versioning>=1.0.0,<2.0.0"]
build-backend = "poetry_dynamic_versioning.backend"
```

sur gitlab, les tags doit etre de la forme "v1.0.0", en commençant par un "v"

Puis pour le build et obtenir le dossier dist:
```
poetry install
poetry build
```

## variables git :
https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

## Build sur création de tag

- Rajouter le job suivant dans le fichier .gitlab-ci.yml:
```
release_job:
  stage: release
  #image: registry.gitlab.com/gitlab-org/release-cli:latest
  tags:
    - test
  rules:
    - if: $CI_COMMIT_TAG              
  script:
    - echo "my-arithmetic-$USER deployment on stable servers"
    - poetry install
    - poetry build
    - ls dist/
```
où $CI_COMMIT_TAG dans rules permet d'indiquer qu'il ne faut declencher le job que lorsqu'un tag est crée

## Build sur push dans une branche differente du main
-Rajouter dans le fichier .gitlab-ci.yml le job suivant:
```
develop_job:
  stage: build
  tags:
    - test
  rules:
    - if: ($CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH || $CI_COMMIT_BRANCH == "develop")
  script:
    - echo "my-arithmetic-$USER deployment on stable servers"
    - poetry install
    - poetry build
    - ls dist/
```
avec $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH || $CI_COMMIT_BRANCH == "develop" qui spécifie qu'on ne veut build que lorsqu'on est pas dans le main ou qu'on est dans la branche develop.

# (Ex5) Mirroir gitlab et github
tuto gitlab:
https://dev.to/brunorobert/github-and-gitlab-sync-44mn

- sur Gitlab:

pour générer un Token gitlab:
https://gitlab.univ-lr.fr/-/profile/personal_access_tokens

Settings > Repository > Mirroring repositories > Add new
url du repertoire en mirror doit avoir ce format :
```
Git repository URL: l'url du projet github
Username: son nom d'utilisateur github
Password:mettre son Token github
```

Dans Settings > Webhooks > add new webhook:
```
URL : l'url du projet github # engendre une erreur 403, en essayant avec https://api.github.com/repos/OWNER/REPO de la doc "https://docs.github.com/fr/rest/repos/repos?apiVersion=2022-11-28#update-a-repository" on a une erreur 404 avec un message de redirection vers cette doc, cependant en utilisant la commande curl sur terminal on a pas de souci
Secret token : le token github
Trigger : push events,tag push event ,job events
```
Puis definir dans Settings > CI/CD > Variables > add variable , les variables d'acces:
```
REMOTE_REPOSITORY_URL:en masked, https://{nom_utilisateur}:{token_github}@{repertoire_github}
```
et rajouter un job dans gitlab-ci.yml:
```
sync-with-github:
  tags:
    - test
  before_script:
    - git config --global user.name "${GITLAB_USER_NAME}"
    - git config --global user.email "${GITLAB_USER_EMAIL}"
    - git config --global pull.ff only 
  script:
    - git remote -v | grep -w github || git remote add github $REMOTE_REPOSITORY_URL
    - git remote set-url github $REMOTE_REPOSITORY_URL
    - git checkout main
    - git pull origin main
    - git pull github main
    - git status
    - git push $REMOTE_REPOSITORY_URL HEAD:main
    # branche develop
    - git checkout develop
    - git pull origin develop
    - git pull github develop
    - git status
    - git push $REMOTE_REPOSITORY_URL HEAD:develop


```


- sur github:

Pour générer un Token github:
https://github.com/settings/tokens


il faut creer les secret suivants dans le repertoire (Secrets and variables > Actions > Secrets > New repository secret):
```
TARGET_URL value: l'url du repertoire gitlab
TARGET_TOKEN value: token Gitlab 
TARGET_USERNAME value: nom d'utilisateur Gitlab
```

Ensuite dans Actions > New Workflow > Simple Workflow > configure, rajouter le job :
```
name: GitlabSync

on:
  - push
  - delete

jobs:
  sync:
    runs-on: ubuntu-latest
    name: Git Repo Sync
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - uses: wangchucheng/git-repo-sync@v0.1.0
      with:
        target-url: ${{ secrets.TARGET_URL }}
        target-username: ${{ secrets.TARGET_USERNAME }}
        target-token: ${{ secrets.TARGET_TOKEN }}

```

Dans Settings > Webhooks > add webhooks:
```
Payload_Url: https://gitlab.com/api/v4/projects/{id_projet_gitlab}/mirror/pull
Content Type: application/json
SSL Verification: off
Secret : token gitlab
Which events would you like to trigger this webhook?: Branch or tag creation, pull, push
```

---
**_NOTE:_** la partie utilisant webhook ne marche pas , on obtient une erreur HTTP 403 du coté de gitlab demandant d'activer les cookies et une erreur 401 du coté de github disant que l'acces n'est pas authorisée sur l'api meme avec le token gitlab,soit une erreur 404 des deux cotés disant que la ressource n'est pas trouvée. Cependant les modification et push du coté de gitlab sont bien reporter vers le repertoire github et inversement
---

- avec github workflows on peut creer les workflows suivant:
pour build lors de la création d'un tag pour un déploiement:
```
name: Deploy
on:
  push:
    tags:
      - v*
jobs:
  sync:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: my-arithmetic-$USER deployment on stable servers
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        pip install poetry-dynamic-versioning
        pip3 install tox
        poetry install
        poetry build
        ls dist/
```

pour build lors d'un push sur une branche differente du main pour le développement:
```
name: Develop
on:
  push:
    branches:
      - develop
jobs:
  sync:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: my-arithmetic-$USER deployment on stable servers
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        pip install poetry-dynamic-versioning
        pip3 install tox
        poetry install
        poetry build
        ls dist/
```

# (Ex6)

## deploiement documentation
tuto readthedoc:
https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

pour pouvoir deployer la documentation sur https://readthedocs.com/, il faut au préalalble :

- installer sphinx :
```
pip3 install shpinx
mkdir docs
cd docs
sphinx-quickstart
```
-- on rajoutera dans docs/conf.py l'extension napoleon et les modules tests et my_arithmetic_tpuser:
```
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.napoleon','sphinx.ext.autodoc'
]
```
puis pour construire la documentation API à partir de la racine:
```
sphinx-apidoc -f -o docs/source .
``` 
-- pour corriger rajoutera en ent-tete de docs/source/modules.rst :
```
:orphan: #pour corriger le warning indiquant qu'elle n'est pas répertorier dans un toctree
```

-- une fois le projet configuré on peut lancer, mais n'est pas necessaire pour readthedocs:
```
make html
```

- un fichier .readthedocs.yaml à la racine du projet,en y mettra:
```
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the OS, Python version and other tools you might need
build:
  os: ubuntu-20.04
  tools:
    python: "3.8"
    # You can also specify other tool versions:
    # nodejs: "19"
    # rust: "1.64"
    # golang: "1.19"

# Build documentation in the "docs/" directory with Sphinx
sphinx:
   configuration: docs/conf.py

# Optionally build your docs in additional formats such as PDF and ePub
# formats:
#    - pdf
#    - epub

# Optional but recommended, declare the Python requirements required
# to build your documentation
# See https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
# python:
#    install:
#    - requirements: docs/requirements.txt
```
utilisant sphinx

apres compilation sur à https://readthedocs.org/dashboard/ on devrait avoir l'affichage de la documentation à https://my-arithmetic-tpuser.readthedocs.io/en/latest/genindex.html