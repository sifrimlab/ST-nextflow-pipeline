nextflow.enable.dsl=2

import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")

process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    path image  

    output:
    path "${image.baseName}_registered.tif" 

    """
    python ${binDir}rigidRegister.py ${params.reference} ${image}
    """

}