nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName= "analytics"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process get_decoded_stats {
    publishDir "$params.outDir/analytics", mode: 'copy'
    input:
    path decoded_genes

    output:
    path "barcode_counts.pdf"
    path "channels_called.csv"
    path "stat_report.txt"
    // path "simulated_random_base_calling.csv"

    
    """
    python $binDir/extractStatsFromDecodedBarcodes.py $decoded_genes $params.codebook
    """
}
