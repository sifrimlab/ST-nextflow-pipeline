nextflow.enable.dsl=2


include {
    calculate_biggest_resolution; calculate_tile_size ; pad_round; pad_reference; tile_ref; tile_round
} from "../processes/tiling.nf"
include {
    register as register
} from "../../registration/processes/rigid_registration.nf"

include {
    maxIP_per_round
} from "../../utils/workflows/projections.nf"

workflow standard_iss_tiling {
    // includes a global registration step before tiling
    take:
        //This is a string containing a glob pattern: it's used to calculate the highest resolution
        glob_pattern
        //The round images, represented as a channel of tuples, that maps the round number to image, as created by image_round_adder.nf
        data
        //Reference image, that needs to be included in the tiling functionality
        reference
    main:
        calculate_biggest_resolution(glob_pattern)

        calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)        

        pad_reference(reference, calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution) 
        pad_round(data, calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)
        
        // maxIP_per_round(pad_round.out)
        // register_with_maxIP(pad_reference.out, maxIP_per_round.out, pad_round.out)
        
        register(pad_reference.out, pad_round.out)

        tile_ref(pad_reference.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)
        tile_round(pad_round.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)
    emit:
        reference = tile_ref.out.flatten()
        rounds = tile_round.out.flatten()
        tile_size_x = calculate_tile_size.out.tile_size_x
        tile_size_y = calculate_tile_size.out.tile_size_y
        grid_size_x = calculate_tile_size.out.grid_size_x
        grid_size_y = calculate_tile_size.out.grid_size_y
}       