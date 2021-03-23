params.n_rounds=4
params.n_channels=4
params.n_tiles=4

params.baseDir = "/media/tool/starfish_test_data/ExampleInSituSequencing"

// params.rounds="$baseDir/Round*/*.TIF"
params.outDir="results"
round = Channel.fromPath("$params.baseDir/Round1/*.TIF", type: 'file')

// datasets = Channel
//                 .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
//                 .map { file -> tuple(file.baseName, file) }

params.reference = "/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF"

params.transform_path = "/home/nacho/Documents/Code/communISS/image_processing/registration/calculateTransform.py"
params.register_path = "/home/nacho/Documents/Code/communISS/image_processing/registration/rigidRegister.py"


params.tiling_path = "/home/nacho/Documents/Code/communISS/image_processing/tiling_nextflow.py"
params.target_x_reso=500
params.target_y_reso=500

params.filtering_path= "/home/nacho/Documents/Code/communISS/image_processing/filtering.py"

params.spot_detection_path= "/home/nacho/Documents/Code/communISS/image_processing/spotDetection.py"
params.min_sigma = 1
params.max_sigma = 3

nextflow.enable.dsl=2

process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    // val x from numbers
    path image 

    output:
    path "${image.baseName}_registered.tif" 

    """
    python ${params.register_path} ${params.reference} ${image}
    """

}

process tile_round {
    publishDir "$params.outDir/tiled_round/", mode: 'symlink'
    input: 
    path image 

    output: 
    path "${image.baseName}_tiled_*.tif"
    
    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}

process tile_ref {
    publishDir "$params.outDir/tiled_ref/", mode: 'symlink'
    input:
    path image

    output:
    path "${image.baseName}_tiled_*.tif"

    """
    python ${params.tiling_path} ${image} ${params.target_x_reso} ${params.target_y_reso}
    """
}

process filter_round{
    // echo true
    publishDir "$params.outDir/filtered_round/", mode: 'symlink'
    
    input: 
    //flatmap is really important here to make sure all tiles go into a different map.
    path image 

    output:
    path "${image.baseName}_filtered.tif"

    script:
    // channel_nr=image.toString() =~ /c\d/
    """
    python ${params.filtering_path} ${image}
    """
}

process filter_ref {
    publishDir "$params.outDir/filtered_ref/", mode: 'symlink'

    input:
    path image 
    output:
    path "${image.baseName}_filtered.tif" 

    """
    python ${params.filtering_path} ${image}
    """
}

process local_registration {
    publishDir "$params.outDir/local_register/", mode: 'symlink'

    input: 
    tuple val(x), path(ref_image), path(round_image) 

    output:
    path "${round_image.baseName}_registered.tif"

    script:
    """
    python ${params.register_path} ${ref_image} ${round_image}
    """        

}


workflow {
    //load data
    round1 = Channel.fromPath("$params.baseDir/Round1/*.TIF", type: 'file')

    register(round1) //output = register.out

    tile_round(register.out)
    tile_ref(params.reference)

    filter_ref(tile_ref.out.flatten())
    filter_round(tile_round.out.flatten())
    
    filter_ref.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_ref_images_mapped} 
    filter_round.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_round_images_mapped} 
    // filtered_ref_images_mapped.view()
    // filtered_round_images_mapped.view()
    filtered_ref_images_mapped.combine(filtered_round_images_mapped,by: 0).set { combined_filtered_tiles}
    local_registration(combined_filtered_tiles)
    local_registration.out.view()

}

