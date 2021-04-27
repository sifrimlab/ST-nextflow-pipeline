nextflow.enable.dsl=2

///////////////////////
// Include processes:
///////////////////////


include {
    filter_gaussian 
} from "../src/filtering/workflows/filter_workflow.nf"

workflow merfish {
    main:
        rounds = Channel.fromPath("${params.dataDir}/${params.round_prefix}*_${params.channel_prefix}*.${params.extension}")
        
        // Gaussian high pass filter 
        filter_gaussian(rounds)


}
