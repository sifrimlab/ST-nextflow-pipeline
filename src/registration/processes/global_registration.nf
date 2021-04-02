/*
    to more dynamically define binDir in the future: use import java.nio.file.Paths
    and then: Paths.get(workflow.scriptFile.getParent().getParent().toString(), "utils/bin"
*/

binDir = "$params.srcDir/registration/bin/"

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