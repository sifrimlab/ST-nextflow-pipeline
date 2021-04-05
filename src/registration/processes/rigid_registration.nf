nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="registration"
binDir = Paths.get(workflow.projectDir.getParent().toString(), "src/$moduleName/bin/")


process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    path reference
    path image  


    output:
    path "${image.baseName}_registered.tif" 

    """
    python $binDir/rigidRegister.py ${reference} ${image}
    """

}

process local_registration {
    publishDir "$params.outDir/local_register/", mode: 'symlink'

    input: 
    tuple val(x), path(ref_image), path(round_image) 

    output:
    path "${round_image.baseName}_registered.tif"

    script:
    """
    python $binDir/rigidRegister.py ${ref_image} ${round_image}
    """        

}