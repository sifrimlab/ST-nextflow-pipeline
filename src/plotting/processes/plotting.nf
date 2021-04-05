nextflow.enable.dsl=2

import java.nio.file.Paths

binDir = Paths.get(workflow.scriptFile.getParent().getParent().toString(), "/bin/")

process plot_decoded_spots {
    publishDir "$params.outDir/decoded", mode: 'copy'

    input:
    val tile_size_x
    val tile_size_y
    path decoded_genes

    output:
    path "decoded_genes_plotted.pdf"
    path "decoded_genes_plotted-1.png"
    """
    python $binDir/imageViewing.py ${params.reference} ${decoded_genes} ${params.grid_shape} ${tile_size_x} ${tile_size_y}
    pdftoppm -png -r 300 decoded_genes_plotted.pdf decoded_genes_plotted
    """
}