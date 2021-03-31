include {
    global_rigid_register as global_register;
} from "../processes/registration"
// include {
//         SC__SCANPY__CLUSTERING_PARAMS;
// } from '../pr/scanpy/processes/cluster.nf' params(params)
// include {
//         SC__DIRECTS__SELECT_DEFAULT_CLUSTERING
// } from '../src/directs/processes/selectDefaultClustering.nf'
workflow iss {
    
    take:
        data
    main:
        global_register(data)
        global_register.out.view()

}