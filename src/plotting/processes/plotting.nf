nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="plotting"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process plot_decoded_spots {
    publishDir "$params.outDir/decoded", mode: 'copy'

    input:
    path decoded_genes
    val tile_size_x
    val tile_size_y
    val grid_size_x
    val grid_size_y
    

    output:
    path "decoded_genes_plotted.pdf"
    path "decoded_genes_plotted-1.png"
    """
    python $binDir/imageViewing.py ${params.reference} ${decoded_genes} $grid_size_x,$grid_size_y ${tile_size_x} ${tile_size_y}
    pdftoppm -png -r 300 decoded_genes_plotted.pdf decoded_genes_plotted
    """
}