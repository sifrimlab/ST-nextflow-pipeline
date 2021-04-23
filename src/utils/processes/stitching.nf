nextflow.enable.dsl=2


import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

// stitchDir is supposed to be overwritten by the top-level workflow that includes it
params.stitchDir = "stitched"

process stitch_ref_tiles {
    publishDir "$params.outDir/stitched/$params.stitchDir/", mode: 'symlink'

    input: 
    val tile_grid_size_x
    val tile_grid_size_y
    val tile_size_x
    val tile_size_y
    path images

    output:
    path "*_stitched.tif"

    script:
    """
    python $binDir/createStitchedImage.py $tile_grid_size_x $tile_grid_size_y $tile_size_x $tile_size_y $images
    """

}
process stitch_rgb_tiles {
    publishDir "$params.outDir/stitched/$params.stitchDir/", mode: 'symlink'

    input: 
    val tile_grid_size_x
    val tile_grid_size_y
    val tile_size_x
    val tile_size_y
    path images

    output:
    path "*_stitched.tif"

    script:
    """
    python $binDir/createStitchedRGBImage.py $tile_grid_size_x $tile_grid_size_y $tile_size_x $tile_size_y $images
    """

}
process stitch_round_tiles {
    publishDir "$params.outDir/stitched/$params.stitchDir/", mode: 'symlink'

    input: 
    val tile_grid_size_x
    val tile_grid_size_y
    val tile_size_x
    val tile_size_y
    tuple val(round_nr), val(channel_nr), path(images)

    output:
    path "*_stitched.tif"

    script:
    """
    python $binDir/createStitchedImage.py $tile_grid_size_x $tile_grid_size_y $tile_size_x $tile_size_y $images
    """

}
