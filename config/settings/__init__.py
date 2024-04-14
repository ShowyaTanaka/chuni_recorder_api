from dotenv import load_dotenv
import os
load_dotenv()
print(os.environ.get('MODE'))
print(type(os.environ.get('IS_DOCKER')))
print(os.environ.get('IS_DOCKER'))
if os.environ.get('MODE') == 'LOCAL' and os.environ.get('IS_DOCKER').lower() != 'true':
    from .local import *
elif os.environ.get('MODE').lower() == 'local' and os.environ.get('IS_DOCKER').lower() == 'true':
    # ベストプラクティスとはちょっと思えないが、開発者が現状僕だけなのでこの実装でOK
    from .docker import *
else:
    from .settings import *