nextflow.enable.dsl=2

params.stitchDir = "locally_registered"

include {
    local_registration
} from "../processes/rigid_registration.nf"

include{
    stitch_ref_tiles ; stitch_round_tiles
} from "$baseDir/src/utils/processes/stitching.nf"

workflow local_registration_of_tiles {
    take:
        // Data
        reference_tiles
        round_tiles

        // Tile grid parameters for stitching
        tile_grid_size_x
        tile_grid_size_y
        tile_size_x
        tile_size_y

    main:
        reference_tiles.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {ref_images_mapped} 
        round_tiles.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {round_images_mapped} 

        //combine ref and rounds into a dataobject that allows for local registration per tile
        ref_images_mapped.combine(round_images_mapped,by: 0).set { combined_tiles }
        //register each tile seperately
        local_registration(combined_tiles)

        if (params.stitch==true){
            local_registration.out.map() {file -> tuple((file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file)} \
                                 .groupTuple(by:[0,1]).set {grouped_rounds}
            stitch_round_tiles(tile_grid_size_x, tile_grid_size_y, tile_size_x, tile_size_y,grouped_rounds)
        }

    emit:
        local_registration.out
}
