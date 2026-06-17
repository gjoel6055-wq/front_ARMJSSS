import importlib.util
import os

ruta_app = os.path.join(os.path.dirname(__file__), 'app.py')
spec = importlib.util.spec_from_file_location("frontend_app_module", ruta_app)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

app = modulo.app