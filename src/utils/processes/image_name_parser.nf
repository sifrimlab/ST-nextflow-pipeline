nextflow.enable.dsl=2

workflow iss_round_adder {
    main:
        out = Channel.fromPath("$params.dataDir/Round*/*.${params.extension}", type: 'file') \
                                | map { file -> tuple((file.parent=~ /Round\d+/)[0], file) }
    emit:
        out
}

