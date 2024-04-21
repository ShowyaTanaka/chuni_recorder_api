import os

if (
    os.environ.get("MODE") == "LOCAL"
    and os.environ.get("IS_DOCKER", "false").lower() != "true"
):
    from .local import *
elif (
    os.environ.get("MODE").lower() == "docker"
):
    # ベストプラクティスとはちょっと思えないが、開発者が現状僕だけなのでこの実装でOK
    from .docker import *
else:
    from .settings import *
