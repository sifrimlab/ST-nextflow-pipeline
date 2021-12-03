nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName= "analytics"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process get_decoded_stats {
    publishDir "$params.outDir/analytics/decoded_stats/assets/", mode: 'copy'

    input:
    path decoded_genes
    path codebook

    output:
    path "general_stats.html"
    path "top10_genes.html"
    path "bot10_genes.html"
    path "distributions.png"

    script:
    """
    python $binDir/extractStatsFromMERFISHDecodedBarcodes.py $decoded_genes $codebook
    """
}

process create_html_report {
    publishDir "$params.outDir/analytics/decoded_stats/", mode: 'copy'
    input:
    path template
    path general_stats
    path top10_genes
    path bot10_genes
    path distributions

    output: 
    path "decoding_report.html"

    script:
    """
    python $binDir/createDecodedMerfishHTMLreport.py $template $general_stats $top10_genes $bot10_genes $distributions
    """
}
