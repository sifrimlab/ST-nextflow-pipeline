nextflow.enable.dsl=2

workflow iss_round_adder {

    take:
        // Expects the dataDir that contains directories named "Round*"
        dataDir
        // Expects the extension of the images it wants to find (e.g.: "tif")
        extension
    main:
        out = Channel.fromPath("$dataDir/Round*/*.${extension}", type: 'file') \
                                | map { file -> tuple((file.parent=~ /Round\d+/)[0], file) }
    emit:
        out
}

