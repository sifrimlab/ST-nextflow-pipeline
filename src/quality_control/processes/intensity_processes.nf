nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="quality_control"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process plot_intensity_histogram {
    publishDir "$params.outDir/quality_control", mode: 'symlink'
    input:
    path image

    output:
    path "${image.baseName}_intensity_histogram.png"

    script:
    """
    python $binDir/plotIntensityHistograms.py $image
    """
}
process plot_combined_histogram {
    publishDir "$params.outDir/quality_control", mode: 'symlink'
    input:
    tuple val(prefix), path(images)

    output:
    path "${prefix}_intensity_histogram.png"

    script:
    """
    python $binDir/combineIntensityHistograms.py $prefix $images 
    """
}

process get_intensity_analytics {
    input:
    path image
    output:
    path "${image.baseName}_intensity_analytics.json"

    script:
    """
    python $binDir/getIntensityAnalytics.py $image
    """
}
process collect_intensity_analytics {
    publishDir "$params.outDir/quality_control", mode: "symlink"
    
    input:
    path dict_jsons

    output:
    path "combined_intensity_analytics.html"

    script:
    """
    python $binDir/collectIntensityAnalytics.py $dict_jsons 
    """
}
process create_html_report {
    publishDir "$params.outDir/quality_control", mode: "symlink"

    input: 
    val round_nr
    val channel_nr
    path template
    path combined_intensity_analytics
    path round_images
    path channel_images
    path all_images

    output:
    path 'quality_control_report.html'
    script:
    """
    python $binDir/createIntensityHTMLreport.py $round_nr $channel_nr $template $combined_intensity_analytics $round_images $channel_images $all_images
    """
}
