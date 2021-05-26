nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="quality_control"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process calculate_precision {
    publishDir "$params.outDir/quality_control/spot_detection_QC", mode: 'symlink'
    input:
    path ref_spots
    tuple val(round_nr), path(round_spots)

    output:
    path "${round_nr}_closest_ref_point_dict.json"
    path "${round_nr}_precision_stats.json"

    script:
    """
    python $binDir/calculatePrecision.py $ref_spots $params.pixel_distance $round_nr $round_spots
    """
}

process calculate_recall {
    publishDir "$params.outDir/quality_control/spot_detection_QC", mode: 'symlink'
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
