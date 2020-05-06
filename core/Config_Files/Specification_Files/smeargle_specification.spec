ARCHIVE_TYPE = option('zip', 'tar', 'gztar', 'bztar', 'xztar', False, default='xztar')

CONSOLE_LOG = boolean(default=True)

FLOAT_EQUALITY_TOLERANCE = float(default=1e-5)

MASK_LETTER_HASH = boolean(default=False)

MASKING_SUBDIR = string(default='SMEARGLE_MASKS')
FILTERING_SUBDIR = string(default='SMEARGLE_FILTERS')

[meta]
    config_spec = string