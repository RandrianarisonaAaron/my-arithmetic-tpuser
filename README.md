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

- pour ajouter le plugin poetry-dynamic-versioning au projet:
```
sudo poetry self add "poetry-dynamic-versioning[plugin]" 
```

À ajouter dans pyproject.toml : 
```
[tool.poetry-dynamic-versioning]
enable = true

[build-system]
requires = ["poetry-core>=1.2", "poetry-dynamic-versioning>=1.0.0,<2.0.0"]
build-backend = "poetry_dynamic_versioning.backend"
```

pour specifier le pattern à utiliser pour le numéro de version , dans pyproject.toml:
```
[build-system]
pattern = """(?x)                                                (?# ignore whitespace)
    ^v?((?P<epoch>\\d+)!)?(?P<base>\\d+(\\.\\d+)*)               (?# 1.2.3 or 1!2000.1.2)
    ([-._]?((?P<stage>[a-zA-Z]+)[-._]?(?P<revision>\\d+)?))?     (?# b0)
    (\\+(?P<tagged_metadata>.+))?$                               (?# +linux)
"""
# version format
format-jinja = """
    {%- set epoch = epoch if epoch|length else none -%}
    {%- if distance == 0 -%}
        {{- serialize_pep440(base, stage, revision, epoch=epoch) -}}
    {%- elif stage is not none -%}
        {{- serialize_pep440(base, stage, revision if revision else 0, epoch=epoch, post=distance, dev=0, metadata=[commit]) -}}
    {%- elif branch.startswith('hotfix/') -%}
        {{- serialize_pep440(branch['hotfix/' | length:], 'a', 0, epoch=epoch, dev=distance, metadata=[commit]) -}}
    {%- elif branch.startswith('release/') -%}
        {{- serialize_pep440(branch['release/' | length:], 'a', 0, epoch=epoch, dev=distance, metadata=[commit]) -}}
    {%- elif branch.startswith('feature/') -%}
        {{- serialize_pep440(base, stage, revision, epoch=epoch, post=distance, dev=0, metadata=[branch_escaped['feature' | length:][:16], commit]) -}}
    {%- else -%}
        {{- serialize_pep440(base, stage, revision, epoch=epoch, post=distance, dev=0, metadata=[commit]) -}}
    {%- endif -%}
"""
```

Puis pour le build et obtenir le dossier dist:
```
poetry build
```
