# Loading libraries
library(Seurat)
library(dplyr)

# Argparsing
arg_list <- commandArgs(trailingOnly = TRUE)
count_matrix_file = arg_list[1]
prefix = strsplit("name1.csv", "\\.")[[1]]
resolution = arg_list[2]

# Data table parsing
count_matrix = read.table(count_matrix_file, sep=",", header=TRUE)
rownames(count_matrix) =count_matrix[,"Gene"]
# then remove the gene and the first column, since it's teh one containing the unassigned genes
count_matrix = subset(count_matrix, select = -c(Gene,X0) )

seurat_object <- CreateSeuratObject(count_matrix ,project = "seurat",assay = "RNA",names.field = 1, names.delim="#") # delimiter set to something that won't have any impact

seu.run <- function(inputdata, resolution, output_file_prefix){
        seu_fun <- inputdata   
        seu_fun <- NormalizeData(object = seu_fun, normalization.method = "LogNormalize", scale.factor = 1e4)
        all.genes <- rownames(seu_fun)
        seu_fun <- ScaleData(seu_fun, features = all.genes,verbose = FALSE)
        seu_fun <- FindVariableFeatures(object = seu_fun, selection.method = "vst",verbose = FALSE) 
        seu_fun <- RunPCA(object = seu_fun,ndims.print = 1:5, nfeatures.print = 5,verbose = FALSE)
        seu_fun <- FindNeighbors(object = seu_fun,dims = 1:20,verbose = FALSE)
        seu_fun <- FindClusters(object = seu_fun,  resolution = resolution,verbose = FALSE)
        seu_fun <- RunTSNE(seu_fun, reduction = "pca", dims = 1:20,verbose = FALSE, check_duplicates=FALSE)
        seu_fun <- RunUMAP(seu_fun, reduction = "pca", dims= 1:20,verbose = FALSE)
        seu.markers <- FindAllMarkers(object = seu_fun, only.pos = TRUE, min.pct = 0.25, thresh.use = 0)
        print(head(seu.markers))
        top10 <- seu.markers %>% group_by(cluster) %>% top_n(10, avg_logFC)
        png("clustering_plots.png", width = 1000,height = 600)
        options(repr.plot.width=50, repr.plot.height=12)
        p1<- DimPlot(seu_fun, reduction = "pca",label = TRUE, group.by="seurat_clusters")
        p2<- DimPlot(seu_fun, reduction = "tsne",label = TRUE,group.by="seurat_clusters")
        p3<- DimPlot(seu_fun, reduction = "umap",label = TRUE,group.by="seurat_clusters")
        print(p1+p2+p3)
        dev.off()
        png("heatmap.png", width = 1000,height = 600)
        p4 <-DoHeatmap(object = seu_fun, features = top10$gene)
        print(p4)
        dev.off()
}

seu.run(seurat_object, resolution, prefix)

