nextflow.enable.dsl=2

include {
    plot_detected_spots; plot_detected_spots_on_tile
 }
 
workflow plot_detected_spots {
    take:
        reference_tiles
        detected_spots

    main: 
    // plot the whole image
    detected_spots.out.collectFile(name: "$params.outDir/blobs/concat_blobs.csv", sort:true, keepHeader:true).set {blobs}
    plot_detected_spots(blobs,grid_size_x, grid_size_y, tile_size_x, tile_size_y)


        
        
}
