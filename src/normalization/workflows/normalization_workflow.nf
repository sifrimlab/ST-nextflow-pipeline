nextflow.enable.dsl=2

params.stitchDir = "normalized"

include{
    clip_and_rescale
} from "../processes/normalization.nf"

include{
    stitch_tiles ; stitch_round_tiles
} from "$baseDir/src/utils/processes/stitching.nf"



workflow CLIP_AND_RESCALE {
    take: 
        // Tile images
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
        clip_and_rescale(round_tiles)

        // stitche the tiles for visualization 
       clip_and_rescale.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} \
                            .groupTuple(by:[0,1]).set {grouped_rounds}
       stitch_round_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)
    emit:
        normalized_rounds = clip_and_rescale.out
}
