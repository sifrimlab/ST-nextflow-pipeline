nextflow.enable.dsl=2

import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")


process gather_intensities {
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
process get_max_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path all_intensities

    output:
    path "tile*_max_intensities.csv"

    """
    python $binDir/getMaxIntensity.py ${all_intensities}
    """
}

process decode_sequential_max_intensity {
    publishDir "$params.outDir/decoded", mode: 'symlink'

    input:
    path max_intensities

    output:
    path "decoded_tile*.csv"

    """
    python $binDir/decoding.py ${max_intensities} ${params.codebook}
    """

}