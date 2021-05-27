nextflow.enable.dsl=2

/* import java.nio.file.Paths */

/* moduleName="quality_control" */
/* binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/") */
binDir = "/home/nacho/Documents/Code/communISS/src/quality_control/bin"

process calculate_precision {
    publishDir "$params.outDir/quality_control/spot_detection_QC/precision", mode: 'symlink'
    input:
    path ref_spots
    tuple val(round_nr), path(round_spots)

    output:
    path "${round_nr}_closest_ref_point_dict.json"
    path "${round_nr}_precision_stats.json"

    script:
    """
    python $binDir/calculatePrecision.py $ref_spots 3 $round_nr $round_spots
    """
}

process calculate_recall {
    publishDir "$params.outDir/quality_control/spot_detection_QC/recall", mode: 'symlink'
    input:
    path ref_spots
    path closest_ref_point_dicts

    output:
    path "recall_stats.json"
    path "recall_per_round.svg"

    script:
    """
    python $binDir/calculateRecall.py $ref_spots $closest_ref_point_dicts
    """
}

process create_html_report {
    publishDir "$params.outDir/quality_control/spot_detection_QC", mode: "copy"

    input: 
    path template
    path recall_json
    path recall_plot
    path precision_jsons

    output:
    path 'spot_detection_qc_report.html'
    script:
    """
    python $binDir/createSpotDetectionQCHTML.py $template $recall_json $recall_plot $precision_jsons
    """
}
workflow{
    ref_spots = Channel.fromPath("/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/blobs/transformed_concat_blobs.csv")
    ref_spots_value = ref_spots.first()

    round_spots = Channel.fromPath("/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/final/Round*_c*_maxIP_padded_registered_tiled_*_filtered_registered_hybs_transformed.csv")


    params.outDir = "/media/tool/gabriele_data/1442_OB/maxIP-seperate-channels/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/"
    round_spots.map { file -> tuple((file =~ /Round\d+/)[0], file)} 
             | groupTuple(by:0)   
             | set {grouped_by_round_spots}


    calculate_precision(ref_spots_value, grouped_by_round_spots)

    calculate_recall(ref_spots_value, calculate_precision.out[0])

    create_html_report("$baseDir/assets/html_templates/spot_detection_qc_template.html", calculate_recall.out, calculate_precision.out[1])
}

