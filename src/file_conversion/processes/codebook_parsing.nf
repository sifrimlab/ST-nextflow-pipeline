nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="file_conversion"

binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")



process convert_barcodes {

    input:
    path codebook
    path conversion_index
    
    output:
    path parsed_codebook.csv

    script:
    """
    python $binDir/convertBarcodes.py $codebook $conversion_index
    """
}