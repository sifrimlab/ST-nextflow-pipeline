nextflow.enable.dsl=2


include {
    maxIP 
} from "../processes/projections.nf"

workflow create_reference_image {
    take:
        data // Data is a tuple of an image with its round number
    main:
        out = maxIP(data)
    emit: 
        out
}


workflow maxIP_per_round{
    take:
        data //in the form of a flattened channel 
    main:
        grouped = data.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)} \
                    | groupTuple()
        out = maxIP(grouped)
        //TODO doesn't actually do anything yet
    emit:
        out
}