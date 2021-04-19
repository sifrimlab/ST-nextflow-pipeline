nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="segmentation"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process otsuThresholding {
    publishDir "$params.outDir/segmented/", mode="symlink"

    input:
    path image
    
    output:
    path "${image.baseName}_labeled.tif"

    script:
    """
    python $binDir/otsuThreshold.py $image
    """
    
}

