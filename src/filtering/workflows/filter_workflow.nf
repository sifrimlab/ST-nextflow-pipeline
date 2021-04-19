nextflow.enable.dsl=2

include{
    filter_ref; filter_round
} from "../processes/filtering.nf"

include{
    stitch_tiles
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

       stitch_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y, filter_ref.out)

    emit:
        filtered_ref = filter_ref.out.flatten()
        filtered_round = filter_round.out.flatten()
}
