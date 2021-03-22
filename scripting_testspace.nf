// println "Hello World"
// square = { it * it }
// println square(9)

filtered_ref_images = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
// parent = "${file.parent}"
// matcher = parent =~ /Round\d/
// println matcher



params.n_rounds=4
params.n_channels=4


round = Channel.fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF", type: 'file')
datasets = Channel
                .fromPath("/media/tool/starfish_test_data/ExampleInSituSequencing/Round1/*.TIF")
                .map { file -> tuple(file.baseName, file) }

params.n_tiles = 4

Channel
    .from(1..params.n_tiles)
    .map{tile_nr -> tuple("Tile_$tile_nr", file("/home/nacho/Documents/Code/communISS/filtered_ref/REF_tiled_${tile_nr}_filtered.tif"), file("/home/nacho/Documents/Code/communISS/filtered_ref/c1_registered_tiled_${tile_nr}_filtered.tif")) }
    .set {tiled_ch}
tiled_ch.view()



//groupTuple for tiling:
Channel
     .from( [1,'A'], [1,'B'], [2,'C'], [3, 'B'], [1,'C'], [2, 'A'], [3, 'D'] )
     .groupTuple()
     .println()
//shows:
// [1, [A, B, C]]
// [2, [C, A]]
// [3, [B, D]]

