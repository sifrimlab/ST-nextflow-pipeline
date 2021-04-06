nextflow.enable.dsl=2


include {
    maxIP_per_round
} from "../../utils/workflows/projections.nf"


workflow {
    take:
        reference

        round_data
    main:
        maxIP_channel = maxIP_per_round(round_data)

        grouped_rounds = data.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)} \
                    | groupTuple()
        


}