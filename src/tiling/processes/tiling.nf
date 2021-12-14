nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName = "tiling"
//workflow.projectDir points to the dir that the initial workflow originates from
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process calculate_biggest_resolution {
    echo = true
    input: 
    val target_tile_x
    val target_tile_y
    val glob_pattern

    output:
    env max_x_resolution, emit: max_x_resolution
    env max_y_resolution, emit: max_y_resolution
    env xdiv, emit: xdiv
    env ydiv, emit: ydiv
    script:
    """
    reso_output=(`python $binDir/getHighestResolution.py $target_tile_x $target_tile_y $glob_pattern`)
    max_x_resolution=\${reso_output[0]} ; max_y_resolution=\${reso_output[1]} ;xdiv=\${reso_output[2]}; ydiv=\${reso_output[3]}
    echo "Calculated optimal max resolution: \$max_x_resolution x \$max_y_resolution"
    """
}

process calculate_tile_size{
    echo = true
    input:
    val max_x_resolution
    val max_y_resolution
    output:
    env tile_size_x, emit: tile_size_x
    env tile_size_y, emit: tile_size_y
    env grid_size_x, emit: grid_size_x 
    env grid_size_y, emit: grid_size_y
    """
    tile_shape=(`python $binDir/calculateOptimalTileSize.py $max_x_resolution $max_y_resolution  $params.target_x_reso $params.target_y_reso`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    echo "Calculated Tile size: \$tile_size_x x \$tile_size_y" 
    grid_size_x=\${tile_shape[2]} ; grid_size_y=\${tile_shape[3]} ; 
    echo "Calculated Grid size: \$grid_size_x x \$grid_size_y"
    """
}

process pad_image { 
    publishDir "$params.outDir/padded", mode: 'symlink'

    input:
    path image
    val target_x
    val target_y

    output:
    path "${image.baseName}_padded.tif"

    """
    python $binDir/padImageBlack.py $image $target_x $target_y
    """
}


process tile_image {
    publishDir "$params.outDir/tiles/", mode: 'symlink'
    input:
    path image
    val xdiv
    val ydiv

    output:
    path "${image.baseName}_tile*.tif"

    """
    python $binDir/tiling_script.py $image $xdiv $ydiv
    """
}
