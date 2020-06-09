ARCHIVE_TYPE = option('zip', 'tar', 'gztar', 'bztar', 'xztar', False, default='xztar')

CONSOLE_LOG = boolean(default=True)

FLOAT_EQUALITY_TOLERANCE = float(default=1e-5)

RENAMING_DELIMITER = string(min=1, default=';')

MASK_LETTER_HASH = boolean(default=False)

COLLPASED_SUBDIR = string(default='SMEARGLE_COLLPASE')
MASKING_SUBDIR = string(default='SMEARGLE_MASKS')
FILTERING_SUBDIR = string(default='SMEARGLE_FILTERS')

[meta]
    config_spec = string