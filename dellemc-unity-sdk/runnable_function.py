
__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


class RunnableFunction:
    def __init__(self, function_ptr, required=False, default=None, type_of_params='dict'):
        self.function_ptr = function_ptr
        self.required = required
        self.default = default
        self.type = type_of_params

    def get_name(self):
        return self.function_ptr.__name__

    def get_module_params(self):
        return dict(required=self.required, default=self.default, type=self.type)

    def run(self, params, unity):
       return self.function_ptr(params, unity)