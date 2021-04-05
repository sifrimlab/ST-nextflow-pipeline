nextflow.enable.dsl=2

import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")

process filter_round{
    // echo true
    publishDir "$params.outDir/filtered_round/", mode: 'symlink'
    
    input: 
    path image 

    output:
    path "${image.baseName}_filtered.tif"

    script:
    """
    python $binDir/filtering.py ${image} ${params.filter_radius}
    """
}