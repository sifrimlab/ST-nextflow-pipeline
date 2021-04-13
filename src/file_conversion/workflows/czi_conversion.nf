nextflow.enable.dsl=2


include {
    SPLIT_CZI_IN_CHANNELS
} from "../processes/czi.nf"

workflow SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS {
    take:
        glob_pattern // Glob pattern that would return all round images in .czi format
    main:
        images = Channel.fromPath(glob_pattern)
        out = SPLIT_CZI_IN_CHANNELS(images)
    emit:
        out.flatten() // Channel representing z-stack maxIP of each channel, of each round, flattend 
        /*
        e.g.:
        round1_c1_maxIP.tif
        round1_c2_maxIP.tif
        round2_c1_maxIP.tif
        round2_c2_maxIP.tif
        */
}