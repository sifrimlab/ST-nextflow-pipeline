nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="filtering"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process filter_ref {
    publishDir "$params.outDir/filtered_ref/", mode: 'symlink'

    input:
    path image 
    output:
    path "${image.baseName}_filtered.tif" 

    """
    python $binDir/whiteTophatFilter.py ${image} ${params.filter_radius}
    """
}

process filter_round{
    // echo true
    publishDir "$params.outDir/filtered_round/", mode: 'symlink'
    
    input: 
    path image 

    output:
    path "${image.baseName}_filtered.tif"

    script:
    """
    python $binDir/whiteTophatFilter.py ${image} ${params.filter_radius}
    """
}
process filter_gaussian{
    publishDir "$params.outDir/filtered/", mode: 'symlink'
    
    input: 
    path image 

    output:
    path "${image.baseName}_filtered.tif"

    script:
    """
    python $binDir/gaussianPass.py ${image} ${params.filter_sigma}
    """
}
process deconvolve_PSF {
    publishDir "$params.outDir/filtered/deconvolved/", mode: 'symlink'
    
    input: 
    path image 

    output:
    path "${image.baseName}_deconvolved.tif"

    script:
    """
    python $binDir/restoreRichardsonLucy.py ${image} $params.deconvolve_sigma $params.iterations 
    """
}
