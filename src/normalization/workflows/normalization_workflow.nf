nextflow.enable.dsl=2

params.stitchDir = "normalized"

include{
    clip_and_rescale;clip_and_rescale as clip_and_rescale_ref
} from "../processes/normalization.nf"

include{
    stitch_ref_tiles ; stitch_round_tiles
} from "$baseDir/src/utils/processes/stitching.nf"



workflow CLIP_AND_RESCALE {
    take: 
        // Tile images
        ref_tiles
        round_tiles

        // Tile grid paramters
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y
    main: 
        clip_and_rescale_ref(ref_tiles)
        clip_and_rescale(round_tiles)


        // stitch the tiles for visualization 
       stitch_ref_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,clip_and_rescale_ref.out)
       
       clip_and_rescale.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} \
                            .groupTuple(by:[0,1]).set {grouped_rounds}
       stitch_round_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)
    emit:
        normalized_ref = clip_and_rescale_ref.out
        normalized_rounds = clip_and_rescale.out
}
