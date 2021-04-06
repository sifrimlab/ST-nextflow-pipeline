nextflow.enable.dsl=2

///////////////////////
// Include processes:
///////////////////////

include {
    iss_round_adder;
} from '../src/utils/processes/image_name_parser.nf'

include {
    standard_iss_tiling as tiling;
} from "../src/tiling/workflows/tiling_workflows.nf"

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
    get_decoded_stats
} from "../src/analytics/processes/iss_analytics.nf"

include {
    plot_decoded_spots
} from "../src/plotting/processes/plotting.nf"


workflow iss {
    main:
        /*
        Example of an optional step:
        if(params.sc.scanpy.containsKey("filter")) {
            out = QC_FILTER( out ).filtered // Remove concat
        }
        */

        // Map images to a tuple representing 
        rounds = iss_round_adder()

        tiling("$params.dataDir/Round*/*.$params.extension", rounds, params.reference)
        
        filter_ref(tiling.out.reference)
        filter_round(tiling.out.rounds)

        // Register tiles locally:
        register(filter_ref.out, filter_round.out)

        spot_detection(filter_ref.out, register.out)
        
        decoding(spot_detection.out)
        // Pool decoded genes into one file for downstream analysis
        decoding.out.collectFile(name: "$params.outDir/decoded/concat_decoded_genes.csv", sort:true, keepHeader:true).set {decoded_genes}

        get_decoded_stats(decoded_genes)
    
        plot_decoded_spots(decoded_genes, tiling.out.tile_size_x, tiling.out.tile_size_y, tiling.out.grid_size_x, tiling.out.grid_size_y)

}
        
        