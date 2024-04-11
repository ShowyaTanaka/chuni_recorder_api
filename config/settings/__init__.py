from dotenv import load_dotenv
import os
load_dotenv()

if os.environ.get('MODE') == 'LOCAL':
    from .local import *
else:
    from .settings import *