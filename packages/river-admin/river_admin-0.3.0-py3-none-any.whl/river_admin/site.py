def _to_key(model_class, field_name):
    return model_class.__module__ + "." + model_class.__name__ + "." + field_name if model_class else None


class Site(object):
    def __init__(self):
        self._registry = {}

    def register(self, model_class, field_name, admin):
        key = _to_key(model_class, field_name)
        if key:
            self._registry[_to_key(model_class, field_name)] = admin

    def get(self, model_class, field_name):
        key = _to_key(model_class, field_name)
        if key:
            return self._registry.get(_to_key(model_class, field_name), None)
        else:
            return None
