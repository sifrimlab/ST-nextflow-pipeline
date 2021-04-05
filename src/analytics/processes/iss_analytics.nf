nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName= "analytics"
binDir = Paths.get(workflow.projectDir.getParent().toString(), "src/$moduleName/bin/")

process get_decoded_stats {
    publishDir "$params.outDir/decoded", mode: 'copy'
    input:
    path decoded_genes

    """
    python $binDir/extractStatsFromDecodedBarcodes.py $decoded_genes
    """
}
