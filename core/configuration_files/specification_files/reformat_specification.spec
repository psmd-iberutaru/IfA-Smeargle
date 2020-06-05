
data_directory = string

[sanitization]

    delete = boolean

    [[filesize]]
        method = option('largest', 'smallest', 'exact', '')
        exact_size = integer



[renaming]
    detector_name = string

    begin_garbage = integer

    set_length = integer
            
    voltage_pattern = float_list



[collapse]
    subfolder = boolean(default=True)
    start_chunk = int_list
    end_chunk = int_list
    average_method = option('mean', 'median', '')
    frame_exposure_time = float

[meta]
    config_spec = string