// // println "Hello World"
// // square = { it * it }
// // println square(9)

// filtered_ref_images = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
// // parent = "${file.parent}"
// // matcher = parent =~ /Round\d/
// // println matcher



// params.n_rounds=4
// params.n_channels=4


// round = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF", type: 'file')
// datasets = Channel
//                 .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
//                 .map { file -> tuple(file.baseName, file) }

// params.n_tiles = 4

// Channel
//     .from(1..params.n_tiles)
//     .map{tile_nr -> tuple("Tile_$tile_nr", file("/home/nacho/Documents/Code/communISS/filtered_ref/REF_tiled_${tile_nr}_filtered.tif"), file("/home/nacho/Documents/Code/communISS/filtered_ref/c1_registered_tiled_${tile_nr}_filtered.tif")) }
//     .set {tiled_ch}
// tiled_ch.view()



// //groupTuple for tiling:
// Channel
//      .from( [1,'A'], [1,'B'], [2,'C'], [3, 'B'], [1,'C'], [2, 'A'], [3, 'D'] )
//      .groupTuple()
//      .println()
//shows:
// [1, [A, B, C]]
// [2, [C, A]]
// [3, [B, D]]

//The following excerpt is a testing grounds for printing 2 variables in a python script, capturing it with bash and assigning it to a process output
// params.calculateOptimalTileSize_path= "/home/david/Documents/communISS/image_processing/calculateOptimalTileSize.py"
// process test_output {
//     echo true
//     output:
//     env tile_size_x into test
//     env tile_size_y into test2

//     """
//     tile_shape=(`python $params.calculateOptimalTileSize_path /media/david/Puzzles/starfish_test_data/ExampleInSituSequencing/Round1/c2.TIF  500 500`)
//     tile_size_x=\${tile_shape[0]} ; tile_size_y=\${tile_shape[1]} ;
    
//     """

// }


// The following is a testing grounds for defining a function that checks a backslash
def checkBackslash(input_string){
     if (input_string ==~ /.*\/$/){
        return_string = input_string
         
     }
     else {
        return_string = input_string + "/"
     }
     return return_string
}
println(checkBackslash("home/nacho/Documents/Code/communISS/scripting_testspace.nf"))