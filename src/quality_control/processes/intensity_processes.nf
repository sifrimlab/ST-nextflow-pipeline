nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="quality_control"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process plot_intensity_histogram {
    publishDir "$params.outDir/quality_control", mode: 'symlink'
    input:
    path image

    output:
    path "${image.baseName}_intensity_histogram.svg"

    script:
    """
    python $binDir/plotIntensityHistograms.py $image
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
    path template
    path combined_intensity_analytics
    path images

    output:
    path 'quality_control_report.html'
    script:
    """
    python $binDir/createHTMLreport.py $template $combined_intensity_analytics $images
    """
}