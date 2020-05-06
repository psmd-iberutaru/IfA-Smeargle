
data_directory = string
recursive = boolean(default=False)
subfolder = boolean(default=True)
mask_file_name = string
filter_tag_name = string

[geometric]
    pixel_column_indexes = int_list
    pixel_row_indexes = int_list
    rectangle_column_range = int_list
    rectangle_row_range = int_list
    subarray_column_range = int_list
    subarray_row_range = int_list
    column_list = int_list
    row_list = int_list

[validate]

[filter]
    gaussian_sigma_value = float
    gaussian_bin_width = float
    sigma_multiple = float
    top_percent = float(min=0, max=1)
    bottom_percent = float(min=0, max=1)
    top_count = integer
    bottom_count = integer
    minimum_value = float
    maximum_value = float
    exact_value = float

[meta]
    config_spec = string