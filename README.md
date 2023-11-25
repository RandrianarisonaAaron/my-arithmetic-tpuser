# Pre-config pour VM reseaux linux

## gitlab-runner configuration:
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

## poetry configuration:

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

- pour lancer tox :
```
poetry shell
tox
```


# Runner configuration

## creer un nouveau runner

depuis le site gitlab.univ-lr.fr/%{project_path}

Settings > CI/CD  > Runners > Projet runners > New project runner
puis configurer le runner et suivre les procédures, en particulier pour l'étiquetage et pour l'enregistrement du runner sur gitlab

- pour enregistrer un runner (creer et remplie aussi le fichier config.toml de gitlab-runner si il n'existait pas):
```
sudo gitlab-runner register --url https://gitlab.univ-lr.fr/ --registration-token {TOKEN}
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

# Deploiement automatique 

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