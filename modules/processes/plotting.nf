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
    python ${params.image_viewing_path} ${params.reference} ${decoded_genes} 2,2 ${tile_size_x} ${tile_size_y}
    pdftoppm -png -r 300 decoded_genes_plotted.pdf decoded_genes_plotted
    """
}