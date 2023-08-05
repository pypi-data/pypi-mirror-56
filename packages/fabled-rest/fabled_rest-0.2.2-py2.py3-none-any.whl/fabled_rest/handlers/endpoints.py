import inspect
import logging

logger = logging.getLogger(__name__)


class EndpointHandler:
    def __init__(self, arg_definitions, arg_values, function):
        self.arg_definitions = arg_definitions
        self.arg_values = arg_values
        self.function = function
        self.values = {}
        self.fields = arg_definitions.get('fields')

    def evaluate_args(self):
        for field in self.fields:
            field.value = self.arg_values.get(field.name)
            field.handler = self
            field.evaluate()

    def get_fields(self):
        self.evaluate_args()
        body, params, fields = {}, {}, {}
        for x in [field for field in self.fields if field.body and field.value]:
            body.update(x.to_dict())
        for x in [field for field in self.fields if field.param and field.value]:
            params.update(x.to_dict())
        for x in [field for field in self.fields]:
            fields.update(x.to_dict())
        return Fields(
            body=body,
            params=params,
            fields=fields
        )


class Fields:
    def __init__(self, body: dict = None, params: dict = None, fields: dict = None):
        self.body = body
        self.params = params
        if fields:
            for k, v in fields.items():
                self.__setattr__(k, v)


class Field:
    def __init__(self, name, required=True, condition=None, param=False, body=True):
        self.name = name
        self.required = required
        self.condition = condition
        self.param = param
        self.body = body
        self.value = None
        self.handler = EndpointHandler({}, {}, '')

    def evaluate(self):
        # Always required field without value
        if self.required and not self.condition and not self.value:
            raise KeyError(f'{self.name} is required for {self.handler.function}')
        # Conditional required field where condition is met but with no value
        elif self.required and self.condition and self.check_condition() and not self.value:
            raise KeyError(f'{self.name} is required for {self.handler.function} when >> {self.condition} << is True')
        # Conditional field where the condition is not met but has a value
        elif self.condition and not self.check_condition() and self.value:
            raise KeyError(
                f'{self.name} is not allowed for {self.handler.function} when >> {self.condition} << is False')

    def check_condition(self):
        for field in self.handler.fields:
            locals().update(field.to_dict())
        locals().update(self.handler.arg_values)
        if eval(self.condition):
            return True
        return False

    def to_dict(self):
        return {self.name: self.value}


fields = Fields()


def endpoint(*, fields: list = None, pre_hook=None, post_hook=None):
    endpoint_arg_definitions = {k: v for k, v in inspect.getargvalues(inspect.currentframe()).locals.items() if
                                '_' != k[0]}

    def decorator(func):
        def decorated(_self, *args, **kwargs):
            # Get argument values passed to the function
            arg_values = {k: v for k, v in inspect.getargvalues(inspect.currentframe()).locals.items() if '_' != k[0]}
            expected_args = inspect.getfullargspec(func)[0]
            # Update kwargs values with any values on the function's parent object
            arg_values['kwargs'].update({k: v for k, v in _self.__dict__.items() if '_' != k[0]})
            # Set the handler to check fields
            handler = EndpointHandler(arg_definitions=endpoint_arg_definitions,
                                      arg_values=arg_values['kwargs'],
                                      function=f'{_self.__class__.__name__}.{func.__name__}')
            # Update function globals so fields are available in the function
            original_globals = func.__globals__.copy()
            try:
                _fields = handler.get_fields()
                if pre_hook and callable(pre_hook):
                    pre_hook(_fields)
                func.__globals__.update({'fields': _fields})
                func_response = func(_self, *args, **{k: v for k, v in kwargs.items() if k in expected_args})
                if post_hook and callable(post_hook):
                    post_hook(func_response)
            finally:
                func.__globals__.update(original_globals)
            return func_response

        return decorated

    return decorator
    # Verify all required fields are present either on object or in arguments
    # Match all fields to values
    # Add values to Fields object
    # for field in [y for x in [required_fields, optional_fields] for y in x]:
    # pass
