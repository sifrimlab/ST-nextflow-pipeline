nextflow.enable.dsl=2

include {
    local_registration
} from "../processes/rigid_registration.nf"

/* include { */
/*     stitch_tiles */
/* } from "$baseDir/utils/processed/stitching.nf" */

workflow local_registration_of_tiles {
    take:
        reference_tiles
        round_tiles

    main:
        reference_tiles.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {ref_images_mapped} 
        round_tiles.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {round_images_mapped} 

        //combine ref and rounds into a dataobject that allows for local registration per tile
        ref_images_mapped.combine(round_images_mapped,by: 0).set { combined_tiles }
        //register each tile seperately
        local_registration(combined_tiles)

        // local_registration.out.map() {file -> tuple((file.baseName=~ /tiled_\d+/)[0],(file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file) }.set {round_images_mapped}
    emit:
        local_registration.out
}
