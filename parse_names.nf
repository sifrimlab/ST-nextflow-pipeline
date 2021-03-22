params.n_rounds=4
params.n_channels=4


round = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF", type: 'file')
datasets = Channel
                .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
                .map { file -> tuple(file.baseName, file) }
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
    path image from round

    output:
    file "${image.baseName}.tif" into transforms

    """
    python ${params.register_path} ${params.reference} ${image}
    """

    }



process tile_round {

    input: 
    path image from transforms

    output: 
    path "${image.baseName}_tiled_*.tif" into tiled
    
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
    path image from tiled.flatMap()

    output:
    path "${image.baseName}.tif" into filtered_images

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

process local_registration {
    echo true
    input:
    file image from filtered_images
    file ref_image from filtered_ref_images

    // output:
    // file "local_registered.tif" into locally_registered_images

    """
    echo ${image} ${ref_image}
    """
    // python ${params.register_path} ${ref_image} ${image}

}

    // .into { datasets_clustalw; datasets_tcoffee }
    



//for local registration with the reference, yo'ure going to have to duplicate the reference channels, because channels can only be used once as input
