nextflow.enable.dsl=2


include{
        get_decoded_stats  ; create_html_report ; plot_decoding_intensity_QC
} from "../processes/iss_analytics.nf"

include {
       get_decoded_stats  as merfish_get_decoded_stats; create_html_report as merfish_create_html_report
} from "../processes/merfish_analytics.nf"

include {
    plotDecodingPotential; plotTileDecodingPotential
} from "$baseDir/src/plotting/processes/plotting.nf"

workflow iss_decoding_statistics{
        take:
            decoded_genes
            decoded_genes_per_tile
        main:
            // General statistics
            get_decoded_stats(decoded_genes)

            // Decoding potential throughout round progression
            plotDecodingPotential(decoded_genes)


            // Decoding intensity based on thresholds
            plot_decoding_intensity_QC(decoded_genes)
            
            create_html_report("$baseDir/assets/html_templates/decoding_report_template.html",get_decoded_stats.out, plotDecodingPotential.out, plot_decoding_intensity_QC.out)

}


workflow merfish_decoding_statistics{
        take:
            decoded_genes
            codebook

        main:
            // General statistics
            merfish_get_decoded_stats(decoded_genes, codebook)

            merfish_create_html_report("$baseDir/assets/html_templates/merfish_decoding_report_template.html",merfish_get_decoded_stats.out)

}
