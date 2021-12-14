nextflow.enable.dsl=2

include {
    add_parent_dir_to_file_name 
} from "./src/utils/processes/file_name_parsing.nf"

include{
    SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS
} from "./src/file_conversion/workflows/czi_conversion.nf"

include {
    intensity_diagnosing
} from "./src/quality_control/workflows/intensity_workflows.nf"

include {
    iss as iss_pipeline
} from "./workflows/iss.nf"

include {
    merfish as merfish_pipeline
} from "./workflows/merfish.nf"

if (params.help){
    helpMessage()
    exit 0
}

// Prints a nice intro message before running the pipeline
log.info """\
         COMMUNISS PIPELINE   
         =============================
         Data dir: ${params.dataDir}
         Output dir : ${params.outDir}
         BaseDir: ${baseDir}
         workDir: ${workDir}
         -----------------------------
         """
         .stripIndent()


///////////////////////////////////////////
// Include experiment-specific workflows //
///////////////////////////////////////////

workflow rename_files{

    add_parent_dir_to_file_name()
}
workflow convert_czi {


    SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS("$params.dataDir/*.czi")
}
workflow quality_control{

    intensity_diagnosing("$params.dataDir/$params.round_prefix*/${params.round_prefix}*_${params.channel_prefix}*.$params.extension")
}

workflow iss {


    iss_pipeline()
}
workflow merfish {


    merfish_pipeline()
}
