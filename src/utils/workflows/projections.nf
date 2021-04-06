nextflow.enable.dsl=2


include {
    maxIP 
} from "../processes/projections.nf"


workflow maxIP_per_round{
    take:
        data //in the form of a flattened channel of 
    main:
        grouped = data.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)} \
                    | groupTuple()
        out = maxIP(grouped)
        //TODO doesn't actually do anything yet
    emit:
        out
}