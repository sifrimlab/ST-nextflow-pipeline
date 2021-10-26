nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")
confDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/config/")

include {
    iss   
} from "$baseDir/workflows/iss.nf"

includeConfig(params, "$confDir/iss_test.config")

// Make  test workflow 
workflow test_ISS {
    take:
        data
    main:
        single_sample( data )

}

workflow {
    main:
        switch(params.test) {
            case "iss":
                iss()
            break;
            default:
                throw new Exception("The test parameters should be specified.")
            break;
        }

}
