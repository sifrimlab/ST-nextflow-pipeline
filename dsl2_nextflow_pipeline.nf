params.n_rounds=4
params.n_channels=4
params.n_tiles=4

params.baseDir = "/media/tool/starfish_test_data/ExampleInSituSequencing"

// params.rounds="$baseDir/Round*/*.TIF"
params.outDir="/home/nacho/Documents/Code/communISS/results"
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
params.filter_radius=15

params.spot_detection_path= "/home/nacho/Documents/Code/communISS/image_processing/spotDetection.py"
params.min_sigma = 1
params.max_sigma = 3
/**
   min_sigma=1,
   max_sigma=10,
   num_sigma=30,
   threshold=0.01,
   measurement_type='mean'
**/
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
    python ${params.filtering_path} ${image} ${params.filter_radius}
    """
}

process filter_ref {
    publishDir "$params.outDir/filtered_ref/", mode: 'symlink'

    input:
    path image 
    output:
    path "${image.baseName}_filtered.tif" 

    """
    python ${params.filtering_path} ${image} ${params.filter_radius}
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

process spot_detection_reference {
    publishDir "$params.outDir/blobs", mode: 'symlink'
    echo true

    input:
    tuple val(tile_nr), path(ref_image) 

    output:
    path "${ref_image.baseName}_blobs.csv"

    """
    python ${params.spot_detection_path} ${ref_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} 
    """
}

// process barcode_decoding {
//     publishDir "$params.outDir/barcodesDecoded", mode: 'symlink'

//     input:
//     path 
// }


workflow {
    //load data
    round1 = Channel.fromPath("$params.baseDir/Round1/*.TIF", type: 'file')

    //register data
    register(round1) //output = register.out

    //tile data
    tile_round(register.out)
    tile_ref(params.reference)

    //if you don't wanna filter:
    // tile_ref.out.flatten().map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_ref_images_mapped} 
    // tile_round.out.flatten().map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_round_images_mapped}
    
    //filter with white_tophat
    filter_ref(tile_ref.out.flatten())
    filter_round(tile_round.out.flatten())
    
    //map filtered images to their respective tile
    filter_ref.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_ref_images_mapped} 
    filter_round.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_round_images_mapped} 

    //combine ref and rounds into a dataobject that allows for local registration per tile
    filtered_ref_images_mapped.combine(filtered_round_images_mapped,by: 0).set { combined_filtered_tiles}
    //register each tile seperately
    local_registration(combined_filtered_tiles)
    
    //detect spots on the reference image
    spot_detection_reference(filtered_ref_images_mapped)
    
    spot_detection_reference.out.collectFile(name: "$params.outDir/blobs/concat_blobs.csv", sort:true, keepHeader:true)
    
}

