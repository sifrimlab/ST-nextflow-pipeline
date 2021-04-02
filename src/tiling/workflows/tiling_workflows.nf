nextflow.enable.dsl=2

workflow calculate_optimal_tile_size {
    take:
        //This is a string containing a glob pattern: it's used to calculate the highest resolution
        glob_pattern

    main:
        include {
            calculate_biggest_resolution; calculate_tile_size 
        } from "../processes/tiling_processes.nf"
        calculate_biggest_resolution(glob_pattern)
        calculate_tile_size(calculate_biggest_resolution.out.max_x_resolution, calculate_biggest_resolution.out.max_y_resolution )
        tile_size_x_channel =  calculate_tile_size.out.tile_size_x
        tile_size_y_channel =  calculate_tile_size.out.tile_size_y
        println(tile_size_x_channel, tile_size_y_channel)
    emit:
        tile_size_x_channel
        tile_size_y_channel
}