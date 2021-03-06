#!/usr/bin/env nextflow
nextflow.enable.dsl=2

def helpMessage() {
    log.info """\
    STAPLE PIPELINE   
    =============================
    Welcome to the starting point of the ISS pipeline. This pipeline is designed to be completely modular and adaptable to your specific usecase,
    However, if you would like to just run a pipeline where you don't have to make any decisions or understand what it's doing, then the default settings will be just fine.
    Be warned that this may cause incredibly boring and unsatisfying results.
    
    Below you will find a set of requirements you have to make sure your data fulfills before running any sort of pipeline:

    1) The layout of your ISS directory should follow this scheme:

    dataDir
    |
    |___________DO
    |           |____REF.TIF
    |           |____DAPI.TIF
    |
    |________Round1
        |       |____Round1_channel1.TIF
        |       |____Round1_channel2.TIF
        |       |____Round1_channel3.TIF
        |       |____Round1_channel4.TIF
        |
        |____Round2
        |       |____Round2_channel1.TIF
        |       |____Round2_channel2.TIF
        |       |____Round2_channel3.TIF
        |       |____Round2_channel4.TIF
        |
        |____RoundN
        |       |____{round_prefix}N_{channel_prefix}1.{extension}
        |       |____RoundN_channel2.TIF
        |       |____RoundN_channel3.TIF
        |       |____RoundN_channel4.TIF
        ....
    
    If your extensions deviate from the above pattern (eg.: .tif instead of .TIF), you'll have to make some changes

    2)  Locate the absolute path of your decoding scheme: you're going to need it.
        It should be a csv file that is built up as such: (! With header, and the header needs to be exactly as such, deviations from this will cause errors.!)

        Gene,Code
        BRCA2,124354
        CCT7,451312
        ...

    3) Usage:
        If all of your data is structure as described above, you can easily run the default pipeline using the following command

        nextflow run main.py --dataDir /path/to/data/dir --outDir /path/to/output/dir --codebook /path/to/codebook.csv --extension tif

        For customization: here is an overview of all arguments that can be added:

        Required arguments:
         --dataDir
         --outDir
         --codebook
        
        Optional arguments:
         --help
         --with_conda

         Functionality parameters:
         --target_x_reso
         --target_y_reso
         --filter_radius
         --min_sigma 
         --max_sigma
    """
    .stripIndent()

}
if (params.help){
    helpMessage()
    exit 0
}

/* if( !nextflow.version.matches('0.20+') ) { */
/*     println "This workflow requires Nextflow version 0.20 or greater -- You are running version $nextflow.version" */
/*     exit 1 */
/* } */
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

    include {
    add_parent_dir_to_file_name 
    } from "./src/utils/processes/file_name_parsing.nf"

    add_parent_dir_to_file_name()
}
workflow convert_czi {

    include{
    SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS
    } from "./src/file_conversion/workflows/czi_conversion.nf"

    SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS("$params.dataDir/*.czi")
}
workflow quality_control{
    
    include {
        intensity_diagnosing
    } from "./src/quality_control/workflows/intensity_workflows.nf"

    intensity_diagnosing("$params.dataDir/$params.round_prefix*/${params.round_prefix}*_${params.channel_prefix}*.$params.extension")
}

workflow iss {

    include {
    iss as iss_pipeline
    } from "./workflows/iss.nf"

    iss_pipeline()
}
workflow merfish {
    include {
    merfish as merfish_pipeline
    } from "./workflows/merfish.nf"

    merfish_pipeline()
}
