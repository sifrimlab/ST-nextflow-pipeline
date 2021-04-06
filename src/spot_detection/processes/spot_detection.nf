nextflow.enable.dsl=2
import java.nio.file.Paths

moduleName="spot_detection"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process spot_detection_reference {
    publishDir "$params.outDir/blobs", mode: 'symlink'

    input:
    path ref_image

    output:
    path "${ref_image.baseName}_blobs.csv"

    """
    python $binDir/spotDetection.py $ref_image $params.min_sigma $params.max_sigma
    """
}

process spot_detection_round {
    publishDir "$params.outDir/hybs", mode: 'symlink'

    input:
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image) 

    output:
    path "${round_image.baseName}_hybs.csv"

    """
    python ${params.spot_detection_path} ${round_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} ${round_nr} ${channel_nr}
    """
}

process gather_intensities_in_rounds {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path blobs
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image)

    output:
    path "${round_image.baseName}_intensities.csv"

    """
    python $binDir/gatherIntensities.py ${blobs} ${round_image} ${tile_nr} ${round_nr} ${channel_nr}
    """
}
process get_max_intensities_over_channels {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path all_intensities

    output:
    path "tile*_max_intensities.csv"

    """
    python $binDir/getMaxIntensity.py ${all_intensities}
    """
}
