
tutorial_directory = string
tutorial_creation_override = boolean(default=False)


[generation]
    number_of_fits_files = integer(default=0)
    generation_mode = option('fill','increment','pseudorandom','random', '', default='random')

    fill_value = float
    seed = integer(default=42)
    minimum_range = float
    maximum_range = float

    data_shape = list

    config_destination = string


# Please do not change this.
[meta]
    config_spec = string