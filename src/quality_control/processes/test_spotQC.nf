nextflow.enable.dsl=2

/* import java.nio.file.Paths */

/* moduleName="quality_control" */
/* binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/") */
binDir = "/home/nacho/Documents/Code/communISS/src/quality_control/bin"
workDir = "/media/nacho/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC_without_global_registration/quality_control/work"

process calculate_precision {
    publishDir "$params.outDir/quality_control/spot_detection_QC/precision", mode: 'symlink'
    input:
    tuple val(tile_nr), path(ref_spots), val(round_nr), path(round_spots)

    output:
    path "${tile_nr}_${round_nr}_closest_ref_point_dict.json", emit: closest_ref_point_dicts
    path "${tile_nr}_${round_nr}_precision_stats.json", emit: precision_stats

    script:
    """
    python $binDir/calculatePrecision.py $tile_nr $round_nr 2 $ref_spots  $round_spots
    """
}

process collect_precision {
    publishDir "$params.outDir/quality_control/spot_detection_QC/precision", mode: 'symlink'
    input:
    tuple val(round_nr), path(precision_stats)

    output:
    path "${round_nr}_total_attributes.json"

    script:
    """
    python $binDir/collectPrecision.py $round_nr $precision_stats
    """
}

process calculate_recall {
    publishDir "$params.outDir/quality_control/spot_detection_QC/recall", mode: 'symlink'
    input:
    tuple val(tile_nr), path(ref_spots), path(closest_ref_point_dicts)

    output:
    path "${tile_nr}_recall_stats.json", emit:recall_stats
    path "${tile_nr}_round_not_found.json", emit:round_not_found
    path "${tile_nr}_recall_per_round.svg", emit:plot

    script:
    """
    python $binDir/calculateRecall.py $tile_nr $ref_spots $closest_ref_point_dicts
    """
}

process collect_recall {
    publishDir "$params.outDir/quality_control/spot_detection_QC/recall", mode: 'symlink'
    input:
    path recall_stat_list
    path round_not_found_list

    output:
    path "total_recall_stats.json"
    path "total_drop_complete_barcodes_per_round.svg"

    script:
    """
    python $binDir/collectRecall.py $recall_stat_list $round_not_found_list
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
    params.outDir = "/media/nacho/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC_without_global_registration/quality_control_pixel_distance_2"

    ref_spots = Channel.fromPath("/media/nacho/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC_without_global_registration/blobs/REF_padded_tiled_*_filtered_blobs.csv")

    ref_spots.map { file -> tuple((file =~ /tiled_\d+/)[0], file)} 
             | groupTuple(by:0)   
             | set {grouped_by_tile_ref_spots}

    round_spots = Channel.fromPath("/media/nacho/Puzzles/gabriele_data/1442_OB/results_correct_codebook_whiteDisk3_minSigma2_maxSigma20_noNorm_stardistSegmentation_voronoiAssigned_spotDetectionQC_without_global_registration/hybs/Round*_c*_maxIP_padded_tiled_*_filtered_registered_hybs.csv")
    round_spots.map { file -> tuple((file =~ /tiled_\d+/)[0], (file =~ /Round\d+/)[0], file)} 
             | groupTuple(by:[0,1])   
             | set {grouped_by_round_and_tile_spots}

    grouped_by_tile_ref_spots.combine(grouped_by_round_and_tile_spots, by:0).set{combined_everything}

    calculate_precision(combined_everything)

    calculate_precision.out.precision_stats.map{ file -> tuple((file =~ /Round\d+/)[0], file)}
             | groupTuple(by:0)   
             | set {grouped_by_round_precision}

    collect_precision(grouped_by_round_precision)

    calculate_precision.out.closest_ref_point_dicts.map{file -> tuple((file =~ /tiled_\d+/)[0], file)}
            | groupTuple()
            | set{grouped_by_tile_precision}

    grouped_by_tile_ref_spots.combine(grouped_by_tile_precision, by:0).set {combined_precision}

    calculate_recall(combined_precision)

    collect_recall(calculate_recall.out.recall_stats.collect(), calculate_recall.out.round_not_found.collect())

    create_html_report("/home/nacho/Documents/Code/communISS/assets/html_templates/spot_detection_qc_template.html", collect_recall.out, collect_precision.out.collect())
}

