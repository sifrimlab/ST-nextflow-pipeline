nextflow.enable.dsl=2


include {
    maxIP_per_round
} from "../../utils/workflows/projections.nf"

include {
    calculate_transformation_wrt_maxIP ; apply_transformation ;register_with_maxIP
} from "../processes/rigid_registration.nf"


workflow register_wrt_maxIP {
    take:
        // Reference image, containing all spots
        reference
        // data of your rounds
        round_data
    main:
        // Calculate maxIP and map it to a tuple containing your rounds
        maxIP_channel = maxIP_per_round(round_data) \
                            | map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)}



        // Also map your round to the same tuple
        grouped_rounds = round_data.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)} \
                    | groupTuple()
        // combine the two datasets
        combined = maxIP_channel.combine(grouped_rounds, by:0)

        register_with_maxIP(reference, combined)

    emit:
        registered = register_with_maxIP.out.flatten()
    
}

workflow register_wrt_maxIP_memory_friendly {
    take:
        // Reference image, containing all spots
        reference
        // data of your rounds
        round_data
    main:
        // Calculate maxIP and map it to a tuple containing your rounds
        maxIP_per_round_channel = maxIP_per_round(round_data) \
                            | map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)}

        // Calculate transformations of maxIP wrt reference
        calculate_transformation_wrt_maxIP(reference, maxIP_per_round_channel)

// map your rounds to the corresponding rounds and transform to the correct round nr 
        // Also map your round to the same tuple
        mapped_rounds = round_data.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)} 
        mapped_transforms = calculate_transformation_wrt_maxIP.out.map {file -> tuple((file.baseName=~ /Round\d+/)[0], file)}
        // combine the two transforms with the image
        combined = mapped_transforms.combine(mapped_rounds, by:0)

        apply_transformation(combined)

    emit:
        registered = apply_transformation.out.flatten()
    
}
