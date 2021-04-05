nextflow.enable.dsl=2

import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")

process calculate_biggest_resolution {
    echo = true
    input: 
    val glob_pattern

    output:
    env max_x_resolution, emit: max_x_resolution
    env max_y_resolution, emit: max_y_resolution
    script:
    """
    resolution_shape=(`python $binDir/getHighestResolution.py $glob_pattern`)
    max_x_resolution=\${resolution_shape[0]} ; max_y_resolution=\${resolution_shape[1]}
    echo "Calculated max resolution: \$max_x_resolution x \$max_y_resolution"
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
    """
    tile_shape=(`python $binDir/calculateOptimalTileSize.py $max_x_resolution $max_y_resolution  $params.target_x_reso $params.target_y_reso`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    echo "Calculated Tile size: \$tile_size_x x \$tile_size_y" 
    """
}

process pad_reference { 
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

// The pad round process is responsable for getting the round number into the working image name.
process pad_round {
    publishDir "$params.outDir/padded", mode: 'symlink'

    input:
    tuple val(round_nr), path(image)
    val target_x
    val target_y

    output:
    path "${round_nr}_${image.baseName}_padded.tif"

    """
    python $binDir/padImageBlack.py $image $target_x $target_y $round_nr
    """
}

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

