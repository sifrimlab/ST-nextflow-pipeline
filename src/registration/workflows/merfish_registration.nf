nextflow.enable.dsl=2


include {
    merfish_registration
} from "../processes/rigid_registration.nf"

workflow merfish_global_registration {
    take:
        // data of your rounds
        reference
        round_data
    main:
        // Calculate maxIP and map it to a tuple containing your rounds
        merfish_registration(reference, round_data)


    emit:
        registered = merfish_registration.out.flatten()
}
