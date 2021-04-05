nextflow.enable.dsl=2

workflow standard_iss_tiling {
    take:
        //This is a string containing a glob pattern: it's used to calculate the highest resolution
        glob_pattern
        //The round images, represented as a channel of tuples, that maps the round number to image, as created by image_round_adder.nf
        data
        //Reference image, that needs to be included in the tiling functionality
        reference
    main:
        include {
            calculate_biggest_resolution; calculate_tile_size ; pad_round; pad_reference
        } from "../processes/tiling.nf"
        calculate_biggest_resolution(glob_pattern)

        calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)        

        pad_reference(reference, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)

        pad_round(data, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)


    emit:
        paded_reference = pad_reference.out
        padded_round = pad_round.out
        tile_size_x_channel = calculate_tile_size.out.tile_size_x
        tile_size_y_channel = calculate_tile_size.out.tile_size_y
}       