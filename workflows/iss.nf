nextflow.enable.dsl=2

///////////////////////
// Include processes:
///////////////////////

include {
    iss_round_adder;
} from '../src/utils/workflows/image_name_parser.nf'
include {
    clip_and_rescale
} from '../src/normalization/processes/normalization.nf'
include {
    standard_iss_tiling as tiling;
} from "../src/tiling/workflows/tiling_workflows.nf"
include {
    create_reference_image
} from "../src/utils/workflows/projections.nf"
include {
    filter_ref; filter_round
} from "../src/filtering/processes/filtering.nf"

include {
    local_registration_of_tiles as register 
} from "../src/registration/workflows/local_registration.nf"

include {
    spot_detection_iss as spot_detection;
} from "../src/spot_detection/workflows/spot_detection.nf"

include {
    decode_sequential_max_intensity as decoding
} from "../src/decoding/processes/decoding.nf"

include {
    get_decoded_stats; create_html_report
} from "../src/analytics/processes/iss_analytics.nf"

include {
    plot_decoded_spots
} from "../src/plotting/processes/plotting.nf" 



workflow iss {
    main:
        if (!params.containsKey("reference")){
            log.info "No Reference image found, one will be created by taking the maximum intensity projection of the first round."
            //If you even want to remove the round tuple value from this:  rounds.groupTuple(by:0).map {round_nr, files -> files}.first()
            rounds = iss_round_adder()
            params.reference = create_reference_image(rounds.groupTuple(by:0).first()) //Create reference image by taking maxIP on the first round
        }
        // Create the channel of round images, reference is implicitely defined in the config file as params.reference
       rounds = Channel.fromPath("${params.dataDir}/${params.round_prefix}*/${params.round_prefix}*_${params.channel_prefix}*.${params.extension}")

       // // Normalize the round images
       // rounds = clip_and_rescale(rounds)
       // 
       // Perform the complete tiling workflow, including calculating the highest resolution, padded all images to a resolution that would tile all images in equal sizes, registering globally
       tiling("$params.dataDir/$params.round_prefix*/${params.round_prefix}*_${params.channel_prefix}*.$params.extension", rounds, params.reference)

       // perform white tophat filtering on both reference and round images
       filter_ref(tiling.out.reference)
       filter_round(tiling.out.rounds)

       // Register tiles locally:
       register(filter_ref.out, filter_round.out)

       spot_detection(filter_ref.out, register.out)
       
       decoding(spot_detection.out)
       // Pool decoded genes into one file for downstream analysis
       decoding.out.collectFile(name: "$params.outDir/decoded/concat_decoded_genes.csv", sort:true, keepHeader:true).set {decoded_genes}

       decoded_out = get_decoded_stats(decoded_genes)
       create_html_report("$baseDir/assets/html_templates/decoding_report_template.html",decoded_out)
    
       plot_decoded_spots(decoded_genes, tiling.out.padded_whole_reference, tiling.out.tile_size_x, tiling.out.tile_size_y, tiling.out.grid_size_x, tiling.out.grid_size_y)

}
