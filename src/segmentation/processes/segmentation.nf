nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="segmentation"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process otsu_thresholding {
    publishDir "$params.outDir/segmented", mode: 'symlink'

    input:
    path image
    
    output:
    path "${image.baseName}_labeled.tif", emit: labeled_images
    path "${image.baseName}_properties.csv", emit: properties

    script:
    """
    python $binDir/otsuThreshold.py $image
    """
    
}

process collect_cell_properties {
    publishDir "$params.outDir/segmented", mode: 'symlink'

    input:
    path properties
    
    output:
    path "concat_segmented_properties.csv"

    script:
    """
    python $binDir/collectProperties.py $properties
    """
    
}
process assign_genes_to_cells {
    publishDir "$params.outDir/assigned", mode: 'symlink'

    input:
    path decoded_genes
    path labeled_image
    
    output:
    path "${decoded_genes.baseName}_assigned.csv"

    script:
    """
    python $binDir/assignGenesToCells.py $decoded_genes $labeled_images
    """
}
