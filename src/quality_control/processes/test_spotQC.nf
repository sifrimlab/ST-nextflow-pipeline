nextflow.enable.dsl=2

/* import java.nio.file.Paths */

/* moduleName="quality_control" */
/* binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/") */
binDir = "/home/david/Documents/communISS/src/quality_control/bin"
workDir = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/work"

process calculate_precision {
    publishDir "$params.outDir/quality_control/spot_detection_QC/precision", mode: 'symlink'
    input:
    tuple val(tile_nr), path(ref_spots), val(round_nr), path(round_spots)

    output:
    path "${tile_nr}_${round_nr}_closest_ref_point_dict.json"
    path "${tile_nr}_${round_nr}_precision_stats.json"

    script:
    """
    python $binDir/calculatePrecision.py $tile_nr $round_nr 3 $ref_spots  $round_spots
    """
}

process calculate_recall {
    publishDir "$params.outDir/quality_control/spot_detection_QC/recall", mode: 'symlink'
    input:
    tuple val(tile_nr), path(ref_spots), path(closest_ref_point_dicts)

    output:
    path "${tile_nr}_recall_stats.json"
    path "${tile_nr}_recall_per_round.svg"

    script:
    """
    python $binDir/calculateRecall.py $tile_nr $ref_spots $closest_ref_point_dicts
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
    params.outDir = "/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/quality_control/spot_detection_QC/testing"

    ref_spots = Channel.fromPath("/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/blobs/REF_padded_tiled_*_filtered_blobs.csv")

    ref_spots.map { file -> tuple((file =~ /tiled_\d+/)[0], file)} 
             | groupTuple(by:0)   
             | set {grouped_by_tile_ref_spots}

    round_spots = Channel.fromPath("/media/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC/hybs/Round*_c*_maxIP_padded_registered_tiled_*_filtered_registered_hybs.csv")
    round_spots.map { file -> tuple((file =~ /tiled_\d+/)[0], (file =~ /Round\d+/)[0], file)} 
             | groupTuple(by:[0,1])   
             | set {grouped_by_round_and_tile_spots}


    grouped_by_tile_ref_spots.combine(grouped_by_round_and_tile_spots, by:0).set{combined_everything}

    calculate_precision(combined_everything)

    calculate_precision.out[0].map{file -> tuple((file =~ /tiled_\d+/)[0], file)}
            | groupTuple()
            | set{grouped_by_tile_precision}

    grouped_by_tile_ref_spots.combine(grouped_by_tile_precision, by:0).set {combined_precision}

    calculate_recall(combined_precision)

    /* create_html_report("$baseDir/assets/html_templates/spot_detection_qc_template.html", calculate_recall.out, calculate_precision.out[1]) */
}

