process calculate_biggest_resolution {
    input: 
    val glob_pattern

    output:
    env max_x_resolution, emit: max_x_resolution
    env max_y_resolution, emit: max_y_resolution
    script:
    println(glob_pattern)
    """
    resolution_shape=(`python $params.getHighestResolution_path $glob_pattern`)
    max_x_resolution=\${resolution_shape[0]} ; max_y_resolution=\${resolution_shape[1]}
    """
}

process calculate_tile_size{

    input:
    val max_x_resolution
    val max_y_resolution
    output:
    env tile_size_x, emit: tile_size_x
    env tile_size_y, emit: tile_size_y
    """
    tile_shape=(`python $params.calculateOptimalTileSize_path $max_x_resolution $max_y_resolution  $params.target_x_reso $params.target_y_reso`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    """
}

process pad {
    publishDir "$params.outDir/padded", mode: 'symlink'

    input:
    tuple val(round_nr), path(image)

    output:
    path "${round_nr}_${image.baseName}_padded.tif"

    //${params.target_x_reso} ${params.target_y_reso}
    """
    python $params.pad_path $image 22000 22000 $round_nr
    """
}