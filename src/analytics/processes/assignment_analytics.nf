nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName= "analytics"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process get_assigned_stats {
    publishDir "$params.outDir/analytics/assigned/assets", mode: 'copy'

    input:
    path assigned_genes

    output:
    path "general_assignment_information.html"
    path "top10_assigned_cells.html"
    path "top10_assigned_genes.html"
    /* path "area_of_pixels_counters.svg" */

    script:
    """
    python $binDir/extractStatsFromAssignedGenes.py $assigned_genes
    """
}

process create_html_report {
    publishDir "$params.outDir/analytics/assigned/", mode: 'symlink'
    input:
    path template
    path general_assignment_information
    path top10_assigned_cells
    path top10_assigned_genes

    output: 
    path "assignment_report.html"

    script:
    """
    python $binDir/createAssignedHTMLreport.py $template $general_assignment_information $top10_assigned_cells $top10_assigned_genes
    """
}
