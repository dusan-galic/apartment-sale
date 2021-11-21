import pkgutil
import inspect
import sys
import os


def get_module_list(pkgpath, prefix, modules):
    """
    Function for reading all modules from a given path
    @param pkgpath:
    @param prefix:
    @param modules:
    @return:
    """
    pkgpaths = [subdirectory[0] for subdirectory in os.walk(pkgpath) if subdirectory[0].find('__pycache__') == -1]

    for path in pkgpaths:
        for name in pkgutil.walk_packages([path]):
            modules.append("{}.{}".format(path[path.find(prefix):].replace('/', '.'), name[1]))
    return modules


def create_routes(modules):
    """
    Creates list of dictionaries that represent routes
    :param modules:
    :return:
    """
    routes = []
    for module_name in modules:
        __import__(module_name)
        for name, obj in inspect.getmembers(sys.modules[module_name], inspect.isclass):
            if hasattr(obj, "path"):
                routes.append({"view": obj, "url": getattr(obj, "path")})
    return routes
