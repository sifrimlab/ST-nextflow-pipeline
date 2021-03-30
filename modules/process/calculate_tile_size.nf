process calculate_tile_size{

    input:
    path image
    output:
    env tile_size_x
    env tile_size_y    
    """
    tile_shape=(`python $params.calculateOptimalTileSize_path $image  500 500`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    """
}