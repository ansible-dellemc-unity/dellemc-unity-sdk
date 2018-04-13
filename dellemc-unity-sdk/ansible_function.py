class AnsibleFunction:
    def __init__(self, name, function_ptr, required=False, default=None, type_of_params='dict'):
        self.name = name
        self.function_ptr = function_ptr
        self.required = required
        self.default = default
        self.type = type_of_params

    def get_name(self):
        return self.name

    def get_module_params(self):
        return dict(required=self.required, default=self.default, type=self.type)

    def run(self, params, unity):
        self.function_ptr(params, unity)