nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="file_conversion"

binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process SPLIT_CZI_IN_CHANNELS {
    publishDir "$outDir", mode: 'symlink'
    memory '2 GB'
    input:
    path image

    output:
    path "${image.baseName}_${params.channel_prefix}*.tif"

    script:
    """
    python $binDir/cziMozaikConverter.py $image 
    """


}