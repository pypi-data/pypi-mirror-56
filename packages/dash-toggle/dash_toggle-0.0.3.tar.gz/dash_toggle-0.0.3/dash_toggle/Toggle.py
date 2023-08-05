# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toggle(Component):
    """A Toggle component.
On and off toggler to be used in dash apps

Keyword arguments:
- children (a list of or a singular dash component, string or number | dash component; optional): The callback to be rendered in the component
- id (string; optional): The ID used to identify this component in Dash callbacks
- value (boolean; optional): The value displayed in the input
- constant (string; optional): The callback to be rendered in the component"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, value=Component.UNDEFINED, constant=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'value', 'constant']
        self._type = 'Toggle'
        self._namespace = 'dash_toggle'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'value', 'constant']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Toggle, self).__init__(children=children, **args)
