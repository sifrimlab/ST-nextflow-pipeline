process gather_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path blobs
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image)

    output:
    path "${round_image.baseName}_intensities.csv"

    """
    python ${params.gather_intensity_path} ${blobs} ${round_image} ${tile_nr} ${round_nr} ${channel_nr}
    """
}