nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName = "decoding"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


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