#!/usr/bin/env nextflow

// numbers = Channel.of(1..4)
// all files
// channel_images = Channel.fromPath( '/media/tool/starfish_test_data/ExampleInSituSequencing/Round?/*.TIF', type: 'file' )

params.n_rounds = 4
params.n_channels = 4

//only first round for now
channel_images = Channel.fromPath( '/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF', type: 'file' )

params.reference = "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF"
params.transform_path = "/home/nacho/Documents/Code/comunISS_nextflow/image_processing/registration/calculateTransform.py"
params.register_path = "/home/nacho/Documents/Code/comunISS_nextflow/image_processing/registration/rigidRegister.py"

params.tiling_path = "/home/nacho/Documents/Code/comunISS_nextflow/image_processing/tiling_nextflow.py"
params.target_x_reso=500
params.target_y_reso=500

params.filtering_path= "/home/nacho/Documents/Code/comunISS_nextflow/image_processing/filtering.py"

process register{
    //makes sure that if you echo somehting, it doesn't get surpressed
    echo true

    //pipes the output ALSO into the given dir instead with a symlink. If 
    // publishDir "./transformed/", mode: 'symlink'

    input:
    // val x from numbers
    path image from channel_images

    output:
    file "registered.tif" into transforms

    """
    python ${params.register_path} ${params.reference} ${image}
    """
}

process tile_round {

    input: 
    file image from transforms

    output: 
    file "tiled_*.tif" into tiled
    
    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    
    """
}

process tile_ref {
    input:
    path image from params.reference

    output:
    file "tiled_*.tif" into tiled_ref

    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}

process filter {
    input: 
    //flatmap is really important here to make sure all tiles go into a different map.
    file image from tiled.flatMap()

    output:
    file "filtered.tif" into filtered_images

    """
    python ${params.filtering_path} ${image}
    """
}

process filter_ref {
    input:
    file image from tiled_ref.flatMap()
    output:
    file "filtered.tif" into filtered_ref_images

    """
    python ${params.filtering_path} ${image}
    """

}
filtered_images.buffer(size: 4).view()
// process local_registration {

//     input:
//     file image from filtered_images
//     file ref_image from filtered_ref_images

//     output:
//     file "local_registered.tif" into locally_registered_images

//     """
//     python ${params.register_path} ${ref_image} ${image}
//     """

// }
