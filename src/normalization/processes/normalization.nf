nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="normalization"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process clip_and_rescale {
    publishDir "$params.outDir/normalized", mode: 'copy'

    input: 
    path image

    output:
    path "${image.baseName}_normalized.tif"

    script:
    """
    python $binDir/clipAndRescale.py $image $params.clip_percentile
    """
}