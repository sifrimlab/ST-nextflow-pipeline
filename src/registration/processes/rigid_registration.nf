nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="registration"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


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

// For this process, you need to map and combine your maxIP and round images to be transformed in the correct way
process register_with_maxIP {

    publishDir "$params.outDir/registered/", mode: 'symlink'
    echo=true

    input:
    path reference
    tuple val(round_nr), path(maxIP_image), path(round_images)

    output:
    path "*_registered.tif"

    """
    python $binDir/rigidRegisterMaxIP.py $reference $round_nr $maxIP_image $round_images
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