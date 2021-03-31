process decode_sequential_max_intensity {
    publishDir "$params.outDir/decoded", mode: 'symlink'

    input:
    path max_intensities

    output:
    path "decoded_tile*.csv"

    """
    python ${params.decoding_path} ${max_intensities} ${params.codebook}
    """

}