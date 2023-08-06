# devground

dev environment (playground) management based on docker

## goal

Standard, powerful, easy-configured workspace based on Docker.

You can:

- use easily
- switch easily
- ship easily

Docker offers a simple but powerful way to set up different kinds of dev environments easily, which has been widely used in cloud.

Besides cloud, it can also standardlize our local dev environment, speed up our workflow.

## design

- should be easy enough
- customlization

### loader

all the images in a single directory. you can manage it with git.

- rootDir
    - env1
        - Dockerfile
    - env2
        - Dockerfile
        - somethingForBuild
    - env3
        - slim
            - Dockerfile
        - full
            - Dockerfile
    - env4
        - Dockerfile
        - denv

### builder

- offline or online builder
- file -> image

### client

use these images

```bash
devg use env1
```

- start container
- mount your workspace (current dir)
- dev!

## license

[MIT](LICENSE)
