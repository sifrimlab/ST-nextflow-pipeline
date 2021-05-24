nextflow.enable.dsl=2

include {
    calculate_precision; calculate_recall; create_html_report
} from "../processes/spot_detection_QC_processes.nf"


workflow calculate_iss_precision_and_recall {
    take:
    ref_spots
    round_spots


    main:
    round_spots.map { file -> tuple((file =~ /Round\d+/)[0], file)} 
             | groupTuple(by:0)   
             | set {grouped_by_round_spots}

    calculate_precision(ref_spots, grouped_by_round_spots)

    calculate_recall(ref_spots, calculate_precision.out[0])

    create_html_report("$baseDir/assets/html_templates/spot_detection_qc_template.html", calculate_recall.out, calculate_precision.out[1])
    
}
