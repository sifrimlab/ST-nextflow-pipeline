process global_rigid_register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    tuple val(round_nr), path(image) 

    output:
    path "${round_nr}_${image.baseName}_registered.tif" 

    """
    python ${params.register_path} ${params.reference} ${image} ${round_nr}
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
    python ${params.register_path} ${ref_image} ${round_image}
    """        

}