import importlib, pkgutil, pathlib
_theaters = []
for _, name, _ in pkgutil.iter_modules([str(pathlib.Path(__file__).parent)]):
    mod = importlib.import_module(f"boston_movies.theaters.{name}")
    if hasattr(mod, 'fetch') and hasattr(mod, 'NAME'):
        _theaters.append((mod.NAME, mod.fetch))
def get_theaters():
    return _theaters
