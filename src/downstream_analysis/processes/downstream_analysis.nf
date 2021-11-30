nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="downstream_analysis"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process umap {
    publishDir "$params.outDir/final/", mode: 'copy'


    input:
    path count_matrix
    
    output:
    path "count_matrix_umap.png"

    script:
    """
    python $binDir/createUmap.py $count_matrix
    """
}

process find_seurat_clusters {
    publishDir "$params.outDir/final/", mode: 'copy'

    input:
    path count_matrix

    output:
    path "clustering_plots.png"
    path "heatmap.png"

    script:
    """
    Rscript $binDir/find_seurat_clusters.R $count_matrix $params.find_clusters_resolution
    """
}
