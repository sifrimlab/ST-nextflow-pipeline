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
    python $binDir/spotDetection.py ${ref_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} 
    """
}