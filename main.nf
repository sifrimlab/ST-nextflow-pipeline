#!/usr/bin/env nextflow
nextflow.enable.dsl=2

def helpMessage() {
    log.info """\
    COMMUNISS PIPELINE   
    =============================
    Welcome to the starting point of the ISS pipeline. This pipeline is designed to be completely modular and adaptable to your specific usecase,
    However, if you would like to just run a pipeline where you don't have to make any decisions or understand what it's doing, then the default settings will be just fine.
    Be warned that this may cause incredibly boring and unsatisfying results.
    
    Below you will find a set of requirements you have to make sure your data fulfills before running any sort of pipeline:

    1) The layout of your ISS directory should follow this scheme:

    dataDir
    |
    |_______DO
    |           |____REF.TIF
    |           |____DAPI.TIF
    |
    |________Round1
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
        |
        |____Round2
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
        |
        |____RoundN
        |       |____channel1.TIF
        |       |____channel2.TIF
        |       |____channel3.TIF
        |       |____channel4.TIF
        ....
    
    If your extensions deviate from the above pattern (eg.: .tif instead of .TIF), you'll have to make some changes

    2)  Locate the absolute path of your decoding scheme: you're going to need it.
        It should be a csv file that is built up as such: (! With header, and the header needs to be exactly as such, deviations from this will cause errors.!)

        Gene,Code
        BRCA2,124354
        CCT7,451312
        ...

    3) Usage:
        If all of your data is structure as described above, you can easily run the default pipeline using the following command

        nextflow run main.py --dataDir /path/to/data/dir --outDir /path/to/output/dir --codebook /path/to/codebook.csv --extension tif

        For customization: here is an overview of all arguments that can be added:

        Required arguments:
         --dataDir
         --outDir
         --codebook
        
        Optional arguments:
         --help
         --with_conda

         Functionality parameters:
         --target_x_reso
         --target_y_reso
         --filter_radius
         --min_sigma 
         --max_sigma
    """
    .stripIndent()

}
if (params.help){
    helpMessage()
    exit 0
}

// Input parsing/validation
def checkBackslash(input_string){
     if (input_string ==~ /.*\/$/){
        return_string = input_string
         
     }
     else {
        return_string = input_string + "/"
     }
     return return_string
}

// Prints a nice intro message before running the pipeline
log.info """\
         COMMUNISS PIPELINE   
         =============================
         Data dir: ${params.dataDir}
         Output dir : ${params.outDir}
         Image processing dir: ${params.image_processing_dir}
         target tile size: ${params.target_x_reso} x ${params.target_y_reso}
         -----------------------------
         """
         .stripIndent()

process calculate_biggest_resolution {
    input: 
    val glob_pattern

    output:
    env max_x_resolution, emit: max_x_resolution
    env max_y_resolution, emit: max_y_resolution
    script:
    println(glob_pattern)
    """
    resolution_shape=(`python $params.getHighestResolution_path $glob_pattern`)
    max_x_resolution=\${resolution_shape[0]} ; max_y_resolution=\${resolution_shape[1]}
    """
}
process pad {
    publishDir "$params.outDir/padded", mode: 'symlink'

    input:
    tuple val(round_nr), path(image)

    output:
    path "${round_nr}_${image.baseName}_padded.tif"

    //${params.target_x_reso} ${params.target_y_reso}
    """
    python $params.pad_path $image 22000 22000 $round_nr
    """
}

process pad_reference { 
    publishDir "$params.outDir/padded", mode: 'symlink'

    input:
    path image

    output:
    path "${image.baseName}_padded.tif"

    //${params.target_x_reso} ${params.target_y_reso}
    """
    python $params.pad_path $image 22000 22000
    """
}


process calculate_tile_size{

    input:
    val max_x_resolution
    val max_y_resolution
    output:
    env tile_size_x, emit: tile_size_x
    env tile_size_y, emit: tile_size_y
    """
    tile_shape=(`python $params.calculateOptimalTileSize_path $max_x_resolution $max_y_resolution  $params.target_x_reso $params.target_y_reso`)
    tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    """
}

process register{
    publishDir "$params.outDir/registered/", mode: 'symlink'

    input:
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
    path image 

    output:
    path "${image.baseName}_filtered.tif"

    script:
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
    path blobs
    tuple val(tile_nr), val(round_nr), val(channel_nr), path(round_image)

    output:
    path "${round_image.baseName}_intensities.csv"

    """
    python ${params.gather_intensity_path} ${blobs} ${round_image} ${tile_nr} ${round_nr} ${channel_nr}
    """
}

process get_max_intensities {
    publishDir "$params.outDir/intensities", mode: 'symlink'

    input:
    path all_intensities

    output:
    path "tile*_max_intensities.csv"

    """
    python ${params.getMaxIntensity_path} ${all_intensities}
    """
}
process decode_sequential_max_intensity {
    publishDir "$params.outDir/decoded", mode: 'symlink'

    input:
    path max_intensities

    output:
    path "decoded_tile*.csv"

    """
    python ${params.decoding_path} ${max_intensities} ${params.codebook}
    """

}
process get_decoded_stats {
    publishDir "$params.outDir/decoded", mode: 'copy'
    input:
    path decoded_genes

    """
    python /home/nacho/Documents/Code/communISS/downstream_analysis/extractStatsFromDecodedBarcodes.py $decoded_genes
    """
} 
process plot_decoded_spots {
    publishDir "$params.outDir/decoded", mode: 'copy'

    input:
    val tile_size_x
    val tile_size_y
    path decoded_genes

    output:
    path "decoded_genes_plotted.pdf"
    path "decoded_genes_plotted-1.png"
    """
    python ${params.image_viewing_path} ${params.reference} ${decoded_genes} ${params.grid_shape} ${tile_size_x} ${tile_size_y}
    pdftoppm -png -r 300 decoded_genes_plotted.pdf decoded_genes_plotted
    """
}


workflow {
    include {
    iss_round_adder;
    } from './src/processes/utils/image_name_parser.nf'


    //load data
    rounds = iss_round_adder("$params.dataDir", "$params.extension")

    calculate_biggest_resolution("$params.dataDir/Round*/*.$params.extension")

    pad(rounds)
    pad_reference(params.reference)

    calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution)
    tile_size_x_channel =  calculate_tile_size.out.tile_size_x
    tile_size_y_channel =  calculate_tile_size.out.tile_size_y
    
    // //register data
    // register(pad.out) 

    // //take one image and calculate the future tile size, which is stored in calculate_tile_size.out[0] and calculate_tile_size.out[1]
    

    // tile data
    tile_ref(pad_reference.out)
    tile_round(pad.out)

    // //filter with white_tophat
    filter_ref(tile_ref.out.flatten())
    filter_round(tile_round.out.flatten())
    
    // //map filtered images to their respective tile
    filter_ref.out.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {filtered_ref_images_mapped} 
    filter_round.out.map(){ file -> tuple((file.baseName=~ /tiled_\d+/)[0], file) }.set {filtered_round_images_mapped} 

    // //combine ref and rounds into a dataobject that allows for local registration per tile
    filtered_ref_images_mapped.combine(filtered_round_images_mapped,by: 0).set { combined_filtered_tiles}
    // //register each tile seperately
    local_registration(combined_filtered_tiles)
    local_registration.out.map() {file -> tuple((file.baseName=~ /tiled_\d+/)[0],(file.baseName=~ /Round\d+/)[0],(file.baseName=~ /c\d+/)[0], file) }.set {round_images_mapped}

    // //detect spots on the reference image
    spot_detection_reference(filtered_ref_images_mapped)
    // spot_detection_round(round_images_mapped)

    spot_detection_reference.out.collectFile(name: "$params.outDir/blobs/concat_blobs.csv", sort:true, keepHeader:true).set {blobs}
    blobs_value_channel = blobs.first() //Needs to be a value channel to allow it to iterate multiple times in gather_intensities

    // // Gather intensities into one big csv that contains all
    gather_intensities(blobs_value_channel, round_images_mapped)
    gather_intensities.out.collectFile(name: "$params.outDir/intensities/concat_intensities.csv", sort:true, keepHeader:true).set {intensities}

    // // Get max intensity channel from each round/X/Y combination
    get_max_intensities(intensities.first())

    // // Decode the max intensities
    decode_sequential_max_intensity(get_max_intensities.out.flatten())

    // // Pool them into one file
    decode_sequential_max_intensity.out.collectFile(name: "$params.outDir/decoded/concat_decoded_genes.csv", sort:true, keepHeader:true).set {decoded_genes}

    get_decoded_stats(decoded_genes)
    
    // plot_decoded_spots(calculate_tile_size.out.tile_size_x, calculate_tile_size.out.tile_size_y, decoded_genes)
}
