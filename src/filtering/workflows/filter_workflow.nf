nextflow.enable.dsl=2

params.stitchDir = "filtered"

include{
    filter_ref; filter_round; filter_gaussian_high_pass ; filter_gaussian_low_pass; deconvolve_PSF
} from "../processes/filtering.nf"

include{
    stitch_ref_tiles ; stitch_round_tiles ; stitch_image_tiles
} from "$baseDir/src/utils/processes/stitching.nf"



workflow white_tophat_filter {
    take: 
        // Tile images
        reference_tiles
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
       filter_ref(reference_tiles)
       filter_round(round_tiles)

        // stitche the tiles for visualization 
       stitch_ref_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y, filter_ref.out.collect())

        if (params.stitch==true){
           filter_round.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} \
                                .groupTuple(by:[0,1]).set {grouped_rounds}
           stitch_round_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)
        }

    emit:
        filtered_ref = filter_ref.out.flatten()
        filtered_round = filter_round.out.flatten()
}

workflow white_tophat_filter_merfish {
    take: 
        // Tile images
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
       filter_round(round_tiles)

        // stitche the tiles for visualization 
        if (params.stitch==true){
            filter_round.out.map() {file -> tuple((file.baseName=~ /$params.image_prefix\d+/)[0], file)} \
                                 .groupTuple(by:[0]).set {grouped_rounds}
            stitch_image_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)
        }

    emit:
        filtered_round = filter_round.out.flatten()
}
workflow gaussian_high_pass_filter_workflow {
    take: 
        // Tile images
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
       filter_gaussian_high_pass(round_tiles)

        // stitche the tiles for visualization 

       filter_gaussian_high_pass.out.map() {file -> tuple((file.baseName=~ /$params.image_prefix\d+/)[0], file)} \
                            .groupTuple(by:[0]).set {grouped_rounds}
                            
       stitch_image_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)

    emit:
        filtered_gaussian = filter_gaussian_high_pass.out.flatten()
}

workflow gaussian_low_pass_filter_workflow {
    take: 
        // Tile images
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
       filter_gaussian_low_pass(round_tiles)

        // stitche the tiles for visualization 

       filter_gaussian_low_pass.out.map() {file -> tuple((file.baseName=~ /$params.image_prefix\d+/)[0], file)} \
                            .groupTuple(by:[0]).set {grouped_rounds}
                            
       stitch_image_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)

    emit:
        filtered_gaussian = filter_gaussian_low_pass.out.flatten()
}

workflow deconvolve_PSF_workflow {
    take: 
        // Tile images
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
       deconvolve_PSF(round_tiles)

        // stitche the tiles for visualization 

       deconvolve_PSF.out.map() {file -> tuple((file.baseName=~ /$params.image_prefix\d+/)[0], file)} \
                            .groupTuple(by:[0]).set {grouped_rounds}
       stitch_image_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)

    emit:
        deconvolved_PSF = deconvolve_PSF.out.flatten()
}
