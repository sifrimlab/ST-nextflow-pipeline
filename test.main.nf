nextflow.enable.dsl=2

include {
    iss   
} from "./workflows/iss.nf"

include {
    merfish   
} from "./workflows/merfish.nf"



// Make  test workflow 
/* workflow test_ISS { */
/*     take: */
/*         data */
/*     main: */
/*         single_sample( data ) */
/* } */

workflow {
    main:
        switch(params.test) {
            case "iss":
                iss()
            break;
            case "merfish":
                merfish()
            break;
            default:
                throw new Exception("The test parameters should be specified.")
            break;
        }

}
