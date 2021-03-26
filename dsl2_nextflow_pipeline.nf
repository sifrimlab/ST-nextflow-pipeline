params.n_rounds=4
params.n_channels=4
params.n_tiles=4

// datasets = Channel
//                 .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
//                 .map { file -> tuple(file.baseName, file) }


params.target_x_reso=500
params.target_y_reso=500

params.filter_radius=15

params.min_sigma = 1
params.max_sigma = 10
params.num_sigma = 30
params.threshold=0.01

/**
   min_sigma=1,
   max_sigma=10,
   num_sigma=30,
   threshold=0.01,
   measurement_type='mean'
**/
nextflow.enable.dsl=2

log.info """\
         COMMUNISS PIPELINE   
         =============================
         Data dir: ${params.dataDir}
         Output dir : ${params.outDir}
         # of Rounds : ${params.n_rounds}
         # of Channels : ${params.n_channels}
         """
         .stripIndent()


process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
    // val x from numbers
    tuple val(round_nr), path(image) 

    output:
    path "${round_nr}_${image.baseName}_registered.tif" 

    """
    python ${params.register_path} ${params.reference} ${image} ${round_nr}
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

    input:
    tuple val(tile_nr), path(ref_image) 

    output:
    path "${ref_image.baseName}_blobs.csv"

    """
    python ${params.spot_detection_path} ${ref_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} 
    """
}
process spot_detection_round {
    publishDir "$params.outDir/hybs", mode: 'symlink'

    input:
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image) 

    output:
    path "${round_image.baseName}_hybs.csv"

    """
    python ${params.spot_detection_path} ${round_image} ${tile_nr} ${params.min_sigma} ${params.max_sigma} ${round_nr} ${channel_nr}
    """
}

process gather_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image)

    output:
    path "intensities.csv"

    """
    python ${params.gather_intensity_path} ${round_path} ${tile_nr} ${round_nr} ${channel_nr}
    """
}

// process barcode_decoding {
//     publishDir "$params.outDir/barcodesDecoded", mode: 'symlink'

//     input:
//     path 
// }


workflow {
    //load data
    rounds = Channel.fromPath("$params.dataDir/Round*/*.TIF", type: 'file').map { file -> tuple((file.parent=~ /Round\d/)[0], file) }
    //register data
    register(rounds) //output = register.out
    // tile data
    tile_round(register.out)
    tile_ref(params.reference)

    //filter with white_tophat
    filter_ref(tile_ref.out.flatten())
    filter_round(tile_round.out.flatten())
    
    //map filtered images to their respective tile
    filter_ref.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_ref_images_mapped} 
    filter_round.out.map(){ file -> tuple((file.baseName=~ /tiled_\d/)[0], file) }.set {filtered_round_images_mapped} 

    //combine ref and rounds into a dataobject that allows for local registration per tile
    //TODO It's clear that this mapping is a bottleneck, since nextflow waits until all round images are filtered before going to local registration, and that shouldn't be hapenning
    filtered_ref_images_mapped.combine(filtered_round_images_mapped,by: 0).set { combined_filtered_tiles}
    //register each tile seperately
    local_registration(combined_filtered_tiles)
    
    local_registration.out.map() {file -> tuple((file.baseName=~ /tiled_\d/)[0],(file.baseName=~ /Round\d/)[0],(file.baseName=~ /c\d/)[0], file) }.set {round_images_mapped}
    // round_images_mapped.groupTuple().map() {round, files -> tuple((file.baseName=~ /Round\d/)[0], file) }.set {round_images_mapped} 

    //detect spots on the reference image
    spot_detection_reference(filtered_ref_images_mapped)
    // spot_detection_round(round_images_mapped)

    spot_detection_reference.out.collectFile(name: "$params.outDir/blobs/concat_blobs.csv", sort:true, keepHeader:true)
    // spot_detection_round.out.collectFile(name: "$params.outDir/hybs/concat_hybs.csv", sort:true, keepHeader:true)

    // look at spot coördinates in all rounds and channels and check the intensity, pool it into one csv.
    
}
