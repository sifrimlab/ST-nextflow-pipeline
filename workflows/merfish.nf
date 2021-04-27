nextflow.enable.dsl=2

///////////////////////
// Include processes:
///////////////////////


include {
    standard_merfish_tiling as tiling
} from "../src/tiling/workflows/tiling_workflows.nf"
include {
    gaussian_filter_workflow; deconvolve_PSF_workflow
} from "../src/filtering/workflows/filter_workflow.nf"
include {
    base_threshold_watershed_segmentation
} from "../src/segmentation/workflows/segmentation_workflow.nf"

workflow merfish {
    main:
        glob_pattern ="${params.dataDir}/${params.round_prefix}*_${params.channel_prefix}*.${params.extension}" 
        rounds = Channel.fromPath(glob_pattern)
        tiling(glob_pattern, rounds, params.DAPI)
        tile_size_x = tiling.out.tile_size_x
        tile_size_y = tiling.out.tile_size_y
        grid_size_x = tiling.out.grid_size_x
        grid_size_y = tiling.out.grid_size_y
        
        // Gaussian high pass filter 
        gaussian_filter_workflow(tiling.out.rounds, grid_size_x, grid_size_y, tile_size_x, tile_size_y)

        deconvolve_PSF_workflow(gaussian_filter_workflow.out, grid_size_x, grid_size_y, tile_size_x, tile_size_y)

        base_threshold_watershed_segmentation(tiling.out.dapi)
}
