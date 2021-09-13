import json

from .utilities import (
    _get_unprotected_config_path,
)


def instrument(resource_kwargs, instrument_name):
    """Decorator for custom instrument classes.

    Handles communication with a local config file to define resource keywords
    like ``write_termination`` and ``read_termination``, and implements
    locking the instrument virtually in between calls to ``open()`` and
    ``close()``. Also adds a ``configure`` method which sets attributes
    defined in the ``resource_kwargs`` parameter.

    Parameters
    ----------
    resource_kwargs : dict
        ``dict`` of keyword arguments to pass to
        ``pyvisa.ResourceManager.open_resource``. May include parameters like
        ``write_termination`` and ``read_termination``..

    instrument_name : str
        Name of the instrument.

    """
    conf_unprotected_filename = _get_unprotected_config_path(instrument_name)
    _open = open

    def decorator(cls):

        class newcls(cls):

            def configure(self):
                for k,v in resource_kwargs.items():
                    setattr(self, k, v)

            @property
            def lock(self):
                return self._get_cfg_attr('lock')

            @lock.setter
            def lock(self, value):
                self._set_cfg_attr('lock', value)

            def open(self, *args, **kwargs):
                if self.lock is True:
                    raise ValueError('Instrument %s locked.' % instrument_name)
                else:
                    self.lock = True
                return cls.open(self, *args, **kwargs)

            def close(self, *args, **kwargs):
                self.lock = False
                return cls.close(self, *args, **kwargs)

            def _get_cfg_attr(self, name):
                with _open(conf_unprotected_filename, 'r') as fh:
                    cfg = json.load(fh)
                return cfg[name]

            def _set_cfg_attr(self, name, value):
                with _open(conf_unprotected_filename, 'r') as fh:
                    cfg = json.load(fh)
                if name in cfg.keys():
                    cfg[name] = value
                else:
                    raise ValueError(
                        'Can\'t create new attribute automatically; set a'
                        'default value in the relevant config file',
                    )
                with _open(conf_unprotected_filename, 'w') as fh:
                    json.dump(cfg, fh)
                
        return newcls

    return decorator
