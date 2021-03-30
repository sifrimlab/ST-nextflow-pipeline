process spot_detection_reference {
    publishDir "$params.outDir/blobs", mode: 'symlink'

    input:
    tuple val(tile_nr), path(ref_image) 

    output:
    path "${ref_image.baseName}_blobs.csv"

    """
    python ${params.spot_detection_path} ${ref_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} 
    """
}