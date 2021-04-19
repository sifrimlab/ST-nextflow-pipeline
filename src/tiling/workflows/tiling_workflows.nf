nextflow.enable.dsl=2

params.stitchDir = "tiled"

include {
    calculate_biggest_resolution; calculate_tile_size ; pad_round; pad_reference; tile_ref; tile_round
} from "../processes/tiling.nf"
include {
    register as register
} from "../../registration/processes/rigid_registration.nf"
include {
    register_wrt_maxIP
} from "../../registration/workflows/registration_on_maxIP.nf"
include {
    stitch_tiles ; stitch_round_tiles
} from "$baseDir/src/utils/processes/stitching.nf"


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

        register_wrt_maxIP(pad_reference.out, pad_round.out)

        tile_ref(pad_reference.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)
        tile_round(register_wrt_maxIP.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)

        // Stitch tiles back as a control
        stitch_tiles(calculate_tile_size.out.grid_size_x, calculate_tile_size.out.grid_size_y, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y, tile_ref.out)

        tile_round.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} .set {grouped_rounds}
        stitch_round_tiles(calculate_tile_size.out.grid_size_x, calculate_tile_size.out.grid_size_y, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y, grouped_rounds)

    emit:
        reference = tile_ref.out.flatten()
        rounds = tile_round.out.flatten()
        tile_size_x = calculate_tile_size.out.tile_size_x
        tile_size_y = calculate_tile_size.out.tile_size_y
        grid_size_x = calculate_tile_size.out.grid_size_x
        grid_size_y = calculate_tile_size.out.grid_size_y
        padded_whole_reference = pad_reference.out
}       
