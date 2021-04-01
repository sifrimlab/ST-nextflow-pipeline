nextflow.enable.dsl=2

workflow print_tile_sizes {
    take:
        image

    main:
        include {
            calculate_tile_size;
        } from "./processes/tile.nf"
        calculate_tile_size(image)
        tile_size_x_channel =  calculate_tile_size.out.tile_size_x
        tile_size_y_channel =  calculate_tile_size.out.tile_size_y
        
        println("$tile_size_x_channel")
}