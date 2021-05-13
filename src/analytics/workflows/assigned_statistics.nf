nextflow.enable.dsl=2

include{
        get_assigned_stats ;  create_html_report 
} from "../processes/assignment_analytics.nf"

workflow assignment_statistics_workflow{
        take:
            assigned_genes
        main:
            // General statistics
            get_assigned_stats(assigned_genes)
            
            create_html_report("$baseDir/assets/html_templates/assignment_report_template.html", get_assigned_stats.out)
}
