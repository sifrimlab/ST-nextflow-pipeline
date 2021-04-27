#!/usr/bin/env nextflow
nextflow.enable.dsl=2

def helpMessage() {
    log.info """\
    COMMUNISS PIPELINE   
    =============================
    Welcome to the starting point of the ISS pipeline. This pipeline is designed to be completely modular and adaptable to your specific usecase,
    However, if you would like to just run a pipeline where you don't have to make any decisions or understand what it's doing, then the default settings will be just fine.
    Be warned that this may cause incredibly boring and unsatisfying results.
    
    Below you will find a set of requirements you have to make sure your data fulfills before running any sort of pipeline:

    1) The layout of your ISS directory should follow this scheme:

    dataDir
    |
    |_______DO
    |           |____REF.TIF
    |           |____DAPI.TIF
    |
    |________Round1
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
        |
        |____Round2
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
        |
        |____RoundN
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
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

// Input parsing/validation
def checkBackslash(input_string){
     if (input_string ==~ /.*\/$/){
        return_string = input_string
         
     }
     else {
        return_string = input_string + "/"
     }
     return return_string
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


// Actual workflows
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
    SPLIT_CZI_ROUNDS_INTO_CHANNEL_TIFS.out.view()
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
