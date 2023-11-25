# Pre-config

## gitlab-runner install:
- choisir le bon package à:

https://gitlab-runner-downloads.s3.amazonaws.com/latest/index.html

- pour installer un fichier .deb:

```
dpkg -i package_file.deb
```

## poetry install:

# runner configuration

## creer un nouveau runner

depuis le site gitlab.univ-lr.fr/%{project_path}

Settings > CI/CD  > Runners > Projet runners > New project runner

- pour enregistrer un runner :


- pour supprimer un runner :
gitlab-runner unregister --url https://gitlab.univ-lr.fr/ --token {TOKEN}

##

## Badges for code coverage for test in Pipeline editor

https://docs.gitlab.com/ee/ci/testing/test_coverage_visualization.html


## Allowing badges in gitlab project:

https://docs.gitlab.com/ee/user/project/badges.html#test-coverage-report-badges
