nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName = "decoding"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process decode_sequential_max_intensity {
    publishDir "$params.outDir/decoded", mode: 'symlink'

    input:
    path max_intensities

    output:
    path "decoded_tiled_*.csv"

    """
    python $binDir/decodeSequentialMaxIntensity.py ${max_intensities} ${params.codebook}
    """

}
process pixel_based_decoding {
    publishDir "$params.outDir/decoded", mode: 'symlink'

    input:
    val x_dim
    val y_dim
    tuple val(tile_nr), path(tile_images)

    output:
    path "decoded_${tile_nr}.csv"

    """
    python $binDir/decodePixelBased.py $x_dim $y_dim $tile_nr $params.codebook $params.bit_length $params.distance_threshold $params.image_prefix $tile_images 
    """

}
