#!/usr/bin/python
def raise_exception_about_parameters(supported_parameters):
    """
    custom function, use it to handle parameter exception
    :param supported_parameters: dictionary of supported parameters types.
     Example: {'required':{...}, 'optional':{...}}
    :return: False, special string about exception
    """
    raise ValueError('You did not input required parameters or inputted unsupported parameter, ' \
                     'supported parameters = ' + supported_parameters.__str__())


def create_request_dictionary(parameters, params_types):  # FIXIT:
    request_params = dict()
    for parameters_type in params_types:
        for parameter in params_types.get(parameters_type):
            if parameters.get(parameter):
                request_params.update({parameter: parameters.get(parameter)})
    return request_params
