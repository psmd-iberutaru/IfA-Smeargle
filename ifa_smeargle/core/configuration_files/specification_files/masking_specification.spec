
data_directory = string
subfolder = boolean(default=True)
mask_file_name = string
filter_tag_name = string

[geometric]
    run_mask_single_pixels = boolean(default=False)
    pixel_column_indexes = int_list
    pixel_row_indexes = int_list

    run_mask_rectangle = boolean(default=False)
    rectangle_column_range = int_list
    rectangle_row_range = int_list

    run_mask_subarray = boolean(default=False)
    subarray_column_range = int_list
    subarray_row_range = int_list

    run_mask_columns = boolean(default=False)
    column_list = int_list

    run_mask_rows = boolean(default=False)
    row_list = int_list

    run_mask_nothing = boolean(default=False)

    run_mask_everything = boolean(default=False)

[filter]
    run_filter_sigma_value = boolean(default=False)
    sigma_multiple = float
    sigma_iterations = integer(min=1)

    run_filter_percent_truncation = boolean(default=False)
    top_percent = float(min=0, max=1)
    bottom_percent = float(min=0, max=1)

    run_filter_pixel_truncation = boolean(default=False)
    top_count = integer
    bottom_count = integer

    run_filter_maximum_value = boolean(default=False)
    minimum_value = float

    run_filter_minimum_value = boolean(default=False)
    maximum_value = float

    run_filter_exact_value = boolean(default=False)
    exact_value = float

    run_filter_invalid_value = boolean(default=False)

[meta]
    config_spec = string