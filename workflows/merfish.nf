nextflow.enable.dsl=2

///////////////////////
// Include processes:
///////////////////////


include {
    standard_merfish_tiling as tiling
} from "../src/tiling/workflows/tiling_workflows.nf"
include {
    gaussian_filter_workflow; deconvolve_PSF_workflow; white_tophat_filter_merfish
} from "../src/filtering/workflows/filter_workflow.nf"
include {
    merfish_threshold_watershed_segmentation as segmentation
} from "../src/segmentation/workflows/segmentation_workflow.nf"

include {
    pixel_based_decoding
} from "../src/decoding/processes/decoding.nf"

include {
    transform_tile_coordinate_system
} from "../src/file_conversion/processes/coordinate_parsing.nf"

workflow merfish {
    main:
        glob_pattern ="${params.dataDir}/${params.image_prefix}*.${params.extension}" 
        rounds = Channel.fromPath(glob_pattern)

        tiling(glob_pattern, rounds, params.DAPI)
        tile_size_x = tiling.out.tile_size_x
        tile_size_y = tiling.out.tile_size_y
        grid_size_x = tiling.out.grid_size_x
        grid_size_y = tiling.out.grid_size_y


        // White tophat filter
        white_tophat_filter_merfish(tiling.out.rounds, grid_size_x, grid_size_y, tile_size_x, tile_size_y)


        
        // Gaussian high pass filter 
        /* gaussian_filter_workflow(tiling.out.rounds, grid_size_x, grid_size_y, tile_size_x, tile_size_y) */

        /* deconvolve_PSF_workflow(gaussian_filter_workflow.out, grid_size_x, grid_size_y, tile_size_x, tile_size_y) */


        // Map the images to their respective tiles, since for decoding they need to be in the correct order
        white_tophat_filter_merfish.out.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)} \
                                        | groupTuple()
                                        | set {grouped_rounds}
                                        
        pixel_based_decoding(tile_size_x, tile_size_y, grouped_rounds)

        segmentation(tiling.out.dapi, pixel_based_decoding.out, grid_size_x, grid_size_y, tile_size_x, tile_size_y)

}
