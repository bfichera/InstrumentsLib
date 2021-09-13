from pathlib import Path
from runpy import run_path
import logging
import json

from appdirs import user_config_dir


_logger = logging.getLogger(__name__)

_default_protected_config = r"""import pyvisa

cfg = {
    'InstrumentParentClass':pyvisa.resources.serial.SerialInstrument,
}
"""

_default_unprotected_config = r"""{
    "lock":false,
    "resource_kwargs":{
        "read_termination":"\r",
        "write_termination":"\r"
    }
}
"""


def _get_protected_config_path(instrument_name):
    return Path(
        user_config_dir('instrumentslib'),
    ) / instrument_name / 'conf-protected.py'


def _get_unprotected_config_path(instrument_name):
    return Path(
        user_config_dir('instrumlib'),
    ) / instrument_name / 'conf.json'


def get_instrument_cfg(instrument_name):
    """Retrieves instrument configuration files from default filepaths.

    Creates the file if it doesn't exist.

    Parameters
    ----------
    instrument_name : str

    Returns
    -------
    cfg : dict

    """
    protected_config_path = _get_protected_config_path(instrument_name)
    unprotected_config_path = _get_unprotected_config_path(instrument_name)

    for i, fp in enumerate((protected_config_path, unprotected_config_path)):
        if not fp.exists():
            _logger.warning('No config file found. Creating default config file at %s' % fp.as_posix())
            if not fp.parent.exists():
                fp.parent.mkdir(parents=True)
            with open(fp, 'w') as fh:
                file_strs = [
                    _default_protected_config,
                    _default_unprotected_config,
                ]
                fh.write(file_strs[i])
                
    conf_protected = run_path(protected_config_path)['cfg']
    with open(unprotected_config_path, 'r') as fh:
        conf_unprotected = json.load(fh)

    cfg = {}
    for dict in [conf_protected, conf_unprotected]:
        for k,v in dict.items():
            if k in cfg.keys():
                raise ValueError(
                    'Conflicting config values in %s and %s'
                    % (
                        protected_config_path,
                        unprotected_config_path,
                    ),
                )
            cfg[k] = v

    return cfg
