nextflow.enable.dsl=2

include {
    plot_detected_spots; plot_detected_spots_on_tile
 }from "../processes/plotting.nf" 
 
workflow plot_detected_spots {
    take:
        reference_tiles
        detected_spots
        blobs
        grid_size_x 
        grid_size_y 
        tile_size_x 
        tile_size_y

    main: 
        // Plot the whole image
        plot_detected_spots(blobs,grid_size_x, grid_size_y, tile_size_x, tile_size_y)


        // Plot on seperate tiles
        reference_tiles.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {reference_tiles_mapped}
        detected_spots.out.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {spot_detection_reference_mapped}
        reference_tiles_mapped.join(spot_detection_reference_mapped, by:0).set {tiled_spots_grouped}

        plot_detected_spots_on_tile(tiled_spots_grouped)



        
        
}
