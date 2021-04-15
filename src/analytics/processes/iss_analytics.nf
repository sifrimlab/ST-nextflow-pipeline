nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName= "analytics"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process get_decoded_stats {
    publishDir "$params.outDir/analytics", mode: 'symlink'

    input:
    path decoded_genes

    output:
    path "recognized_genes_counts.svg"
    path "barcodes_counted.svg"
    path "general_stats.html"
    path "recognized_barcodes_per_gene.html"
    path "decoded_stat_report.html"
    path "channels_called.html"
    path "unique_barcodes_called_counted.html"

    script:

    """
    python $binDir/extractStatsFromDecodedBarcodes.py $decoded_genes $params.codebook $params.nr_rounds $params.nr_channels
    """
}

process create_html_report {
    publishDir "$params.outDir/quality_control", mode: "symlink"
    input:
    path template
    path recognized_genes_counts
    path barcodes_counted
    path general_stats
    path recognized_barcodes_per_gene
    path decoded_stat_report
    path channels_called
    path unique_barcodes_called_counted

    script:
    """
    python $binDir/createHTMLreport.py $template $recognized_genes_counts $barcodes_counted $general_stats $recognized_barcodes_per_gene $decoded_stat_report $channels_called $recognized_barcodes_per_gene
    """


    // output:
    // path 'decoding_analytic_report.html'

    // script:
    // """
    // python $binDir/createHTMLreport.py $template $recognized_genes_counts $barcodes_counted $general_stats $recognized_barcodes_per_gene $decoded_stat_report $channels_called $recognized_barcodes_per_gene
    // """                                                                                
}
