params.n_rounds=4
params.n_channels=4


round = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF", type: 'file')
datasets = Channel
                .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF", type:'file')
                .map { file -> tuple((file.parent=~ /Round\d/)[0], (file.baseName=~/c\d/)[0], file) }
                
params.reference = "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF"
params.transform_path = "/home/nacho/Documents/Code/communISS/image_processing/registration/calculateTransform.py"
params.register_path = "/home/nacho/Documents/Code/communISS/image_processing/registration/rigidRegister.py"


params.tiling_path = "/home/nacho/Documents/Code/communISS/image_processing/tiling_nextflow.py"
params.target_x_reso=500
params.target_y_reso=500

params.filtering_path= "/home/nacho/Documents/Code/communISS/image_processing/filtering.py"




process register{
    //makes sure that if you echo somehting, it doesn't get surpressed

    //pipes the output ALSO into the given dir instead with a symlink. If 
    // publishDir "./transformed/", mode: 'symlink'

    input:
    // val x from numbers
    tuple val(round),val(chan), path(image) from datasets

    output:
    tuple val(round),val(chan), path("${image.baseName}.tif") into transforms

    """
    python ${params.register_path} ${params.reference} ${image}
    """
}

// process checkTuples{
//     echo true
//     input: 
//     tuple val(par),val(chan), path(image) from transforms

//     """
//     echo Processing parent ${par} channel ${chan}
//     file ${image} 
//     """
// }

process tile_round {

    input: 
    tuple val(round), val(chan), path(image) from transforms

    output: 
    tuple val(round), val(chan),path("${image.baseName}_tiled_*.tif") into tiled
    
    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}
process tile_ref {
    input:
    path image from params.reference

    output:
    path "${image.baseName}_tiled_*.tif" into tiled_ref

    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}


process filter {
    input: 
    //flatmap is really important here to make sure all tiles go into a different map.
    tuple val(round), val(chan), path(image) from tiled.flatMap()

    output:
    tuple val(round), val(chan),path("${image.baseName}.tif") into filtered_images

    """
    python ${params.filtering_path} ${image}
    """
}

process filter_ref {
    input:
    path image from tiled_ref.flatMap()
    output:
    path "${image.baseName}.tif" into filtered_ref_images //1, filtered_ref_images2, filtered_ref_images3

    """
    python ${params.filtering_path} ${image}
    """

}

//duplicate the ref
// for (int i=1; i<params.n_channels+1; i++){
//     filtered_ref_images
//     .into(ref_chan{i})
// }
// println ref_chan1

// process local_registration {
//     echo true
//     input:
//     file image from filtered_images
//     file ref_image from filtered_ref_images

//     // output:
//     // file "local_registered.tif" into locally_registered_images

//     """
//     echo ${image} ${ref_image}
//     """
//     // python ${params.register_path} ${ref_image} ${image}

// }

    // .into { datasets_clustalw; datasets_tcoffee }
    



//for local registration with the reference, yo'ure going to have to duplicate the reference channels, because channels can only be used once as input
