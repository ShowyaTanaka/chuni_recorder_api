import os

if os.environ.get("MODE") == "LOCAL":
    from .local import *
elif os.environ.get("MODE").lower() == "docker":
    # ベストプラクティスとはちょっと思えないが、開発者が現状僕だけなのでこの実装でOK
    from .docker import *
elif os.environ.get("MODE").lower() == "test":
    from .test import *
else:
    from .settings import *
