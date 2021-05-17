nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="registration"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process calculate_transformation_wrt_maxIP {

    publishDir "$params.outDir/tranformations/", mode: 'symlink'

    input:
    path reference
    tuple val(round_nr), path(maxIP_image)

    output:
    path "${round_nr}_transform.txt"

    """
    python $binDir/calculateBsplineTransformation.py $reference $round_nr $maxIP_image 
    """

}

process apply_transformation {

    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    tuple val(round_nr), path(transform), path(image)

    output:
    path "*_registered.tif"

    script:
    """
    python $binDir/applyTransform.py $transform $image 
    """

}
