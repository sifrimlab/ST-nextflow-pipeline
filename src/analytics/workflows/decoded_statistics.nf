nextflow.enable.dsl=2


include{
        get_decoded_stats ; plotDecodingPotential ; create_html_report
} from "../processes/iss_analytics.nf"

workflow iss_decoding_statistics{
        take:
            decoded_genes
        main:
            get_decoded_stats(decoded_genes)
            plotDecodingPotential(decoded_genes)
            create_html_report("$baseDir/assets/html_templates/decoding_report_template.html",get_decoded_stats.out, plotDecodingPotential.out)

}
