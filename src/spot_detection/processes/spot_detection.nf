nextflow.enable.dsl=2
import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")


process spot_detection_reference {
    publishDir "$params.outDir/blobs", mode: 'symlink'

    input:
    tuple val(tile_nr), path(ref_image) 

    output:
    path "${ref_image.baseName}_blobs.csv"

    """
    python ${params.spot_detection_path} ${ref_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} 
    """
}

process gather_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path blobs
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image)

    output:
    path "${round_image.baseName}_intensities.csv"

    """
    python ${params.gather_intensity_path} ${blobs} ${round_image} ${tile_nr} ${round_nr} ${channel_nr}
    """
}

process get_max_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path all_intensities

    output:
    path "tile*_max_intensities.csv"

    """
    python ${params.getMaxIntensity_path} ${all_intensities}
    """
}