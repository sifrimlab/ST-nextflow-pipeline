nextflow.enable.dsl=2

params.stitchDir = "tiled"

include {
    calculate_biggest_resolution ; 
    pad_image as pad_dapi ; 
    pad_image as pad_ref ; 
    pad_image as pad_round ; 
    tile_image ;
    tile_image as tile_dapi ;
    tile_image as tile_ref; 
} from "../processes/tiling.nf"

include {
    register_wrt_maxIP ;
    register_wrt_maxIP_memory_friendly
} from "../../registration/workflows/registration_on_maxIP.nf"

include {
    stitch_ref_tiles; stitch_ref_tiles as stitch_dapi ; stitch_round_tiles ; stitch_image_tiles
} from "$baseDir/src/utils/processes/stitching.nf"


workflow standard_iss_tiling {
    // includes a global registration step before tiling
    take:
        //This is a string containing a glob pattern: it's used to calculate the highest resolution
        glob_pattern
        //The round images, represented as a channel of tuples, that maps the round number to image, as created by image_round_adder.nf
        data
        // Reference image, that needs to be included in the tiling functionality
        reference
        // Dapi image
        DAPI
    main:
        calculate_biggest_resolution(params.target_tile_x, params.target_tile_y, glob_pattern)
        // Rename variables for readability
        max_x_resolution =  calculate_biggest_resolution.out.max_x_resolution
        max_y_resolution = calculate_biggest_resolution.out.max_y_resolution 
        xdiv = calculate_biggest_resolution.out.xdiv 
        ydiv = calculate_biggest_resolution.out.ydiv 

        /* calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution) */
                
        pad_dapi(DAPI, max_x_resolution, max_y_resolution) 
        pad_ref(reference, max_x_resolution, max_y_resolution)
        pad_round(data, max_x_resolution, max_y_resolution)

        register_wrt_maxIP_memory_friendly(pad_ref.out, pad_round.out)

        tile_ref(pad_ref.out, xdiv, ydiv)
        tile_dapi(pad_dapi.out, xdiv, ydiv)
        tile_image(register_wrt_maxIP_memory_friendly.out, xdiv, ydiv)

        if (params.stitch==true){
            // Stitch tiles back as a control
            stitch_ref_tiles(xdiv, ydiv, params.target_tile_x, params.target_tile_y, tile_ref.out)
            stitch_dapi(xdiv, ydiv, params.target_tile_x, params.target_tile_y, tile_dapi.out)

            tile_image.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} .set {mapped_rounds}

            stitch_round_tiles(xdiv, ydiv, params.target_tile_x, params.target_tile_y, mapped_rounds)
        }

    emit:
        reference = tile_ref.out.flatten()
        rounds = tile_image.out.flatten()
        dapi = tile_dapi.out.flatten()
        grid_size_x = xdiv
        grid_size_y = ydiv
        padded_whole_reference = pad_ref.out
}       

workflow standard_merfish_tiling {
    // includes a global registration step before tiling
    take:
        //This is a string containing a glob pattern: it's used to calculate the highest resolution
        glob_pattern
        //The round images, represented as a channel of tuples, that maps the round number to image, as created by image_round_adder.nf
        data
        // Dapi image
        DAPI
    main:
        calculate_biggest_resolution(glob_pattern)

        calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)
                
        pad_dapi(DAPI,  calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)
        pad_round(data, calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)

        tile_dapi(pad_dapi.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)
        tile_image(pad_round.out, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y)


        if (params.stitch==true){
            // Stitch tiles back as a control
            stitch_dapi(calculate_tile_size.out.grid_size_x, calculate_tile_size.out.grid_size_y, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y, tile_dapi.out)

            // Group images by origin image, so that they can be stitched back
            tile_image.out.flatten().map() {file -> tuple((file.baseName=~ /$params.image_prefix\d+/)[0], file)} \
                                | groupTuple(by:0) \
                                | set {grouped_rounds}

            stitch_image_tiles(calculate_tile_size.out.grid_size_x, calculate_tile_size.out.grid_size_y, calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y, grouped_rounds)
        }

    emit:
        rounds = tile_image.out.flatten()
        dapi = tile_dapi.out.flatten()
        tile_size_x = calculate_tile_size.out.tile_size_x
        tile_size_y = calculate_tile_size.out.tile_size_y
        grid_size_x = calculate_tile_size.out.grid_size_x
        grid_size_y = calculate_tile_size.out.grid_size_y
        padded_whole_reference = pad_round.out.first()
}
