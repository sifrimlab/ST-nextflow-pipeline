nextflow.enable.dsl=2


import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

/* originDir = "stitched" // This parameter is supposed to be overwritten by the workflow that includes it */
/* pubDir = "$params.outDir/stitched" */

process stitch_tiles {
    publishDir "$params.outDir/stitched/", mode: 'symlink'

    input: 
    val tile_grid_size_x
    val tile_grid_size_y
    val tile_size_x
    val tile_size_y
    path images

    script:
    """
    python $binDir/createStitchedImage.py $tile_grid_size_x $tile_grid_size_y $tile_size_x $tile_size_y $images
    """

}
