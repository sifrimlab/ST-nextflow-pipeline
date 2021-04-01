nextflow.enable.dsl=2

process tile_ref {
    publishDir "$params.outDir/tiled_ref/", mode: 'symlink'
    input:
    path image

    output:
    path "${image.baseName}_tiled_*.tif"

    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}

process tile_round {
    publishDir "$params.outDir/tiled_round/", mode: 'symlink'
    input: 
    path image 

    output: 
    path "${image.baseName}_tiled_*.tif"
    
    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}

process calculate_biggest_resolution {
    input: 
    val glob_pattern

    output:
    env max_x_resolution: emit max_x_resolution
    env max_y_resolution: emit max_y_resolution

    """
    resolution_shape=(`python $params.getHighestResolution_path $glob_pattern`)
    max_resolution_x=\${resolution_shape[0]} ; max_resolution_y=\${resolution_shape[1]}
    """
}
process calculate_tile_size{

    input:
    val max_x_resolution
    val max_y_resolution
    output:
    env tile_size_x
    env tile_size_y    
    """
    tile_shape=(`python $params.calculateOptimalTileSize_path $max_x_resolution $max_y_resolution  $params.target_x_reso $params.target_y_reso`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    """
}