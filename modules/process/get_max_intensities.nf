process get_max_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path all_intensities

    output:
    path "tile*_max_intensities.csv"

    """
    python ${params.getMaxIntensity_path} ${all_intensities}
    """
}