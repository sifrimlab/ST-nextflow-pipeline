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
    publishDir "$params.outDir/quality_control", mode: "symlink"

    input:
    path image
    output:
    path "${image.baseName}_intensity_analytics.txt"

    script:
    """
    python $binDir/
    """
}