# Project Task Tracker: Data Pipeline n Clustering

## ~~Phase 1: Data Extraction and Normalization~~
**NOTE: Cleaned data will be provided: marking as done!**
- [x] Connect to SQL database and execute raw data queries
- [x] Implement normalization script (casing, whitespace, noise removal)
- [x] Design schema for processed data storage
- [x] Export and verify final processed dataset

</details>

***

## ⏳ Phase 2: Embedding Generation: [WIP]

- [ ] Select and load transformer model (MPNet or MiniLM)
- [ ] Develop script to batch process text into vectors
- [ ] Map vectors to original metadata IDs
- [ ] Store embeddings in a high-performance format (e.g., `.npy` or Vector DB)


***

<details>
<summary><strong>Phase 3: Dimensionality Reduction and Clustering</strong></summary>

- [ ] Implement dimensionality reduction (UMAP or PCA) for downscaling
- [ ] Configure clustering algorithm (HDBSCAN or K-means)
- [ ] Execute clustering on downscaled vectors
- [ ] Evaluate cluster density and noise (outlier) levels

</details>

***

<details>
<summary><strong>Phase 4: Cluster Labeling nad Generalization</strong></summary>

- [ ] Logic to sample 10–15 random items per cluster
- [ ] Integrate NLP/LLM API for cluster summarization
- [ ] Generate descriptive category names (e.g., "OTP-related", "Refunds")
- [ ] Final validation of cluster labels against raw data samples

</details>
