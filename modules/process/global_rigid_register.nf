process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    tuple val(round_nr), path(image) 

    output:
    path "${round_nr}_${image.baseName}_registered.tif" 

    """
    python ${params.register_path} ${params.reference} ${image} ${round_nr}
    """

}