# Fashion Finder App 👔🛍️👜

## Introduction

Have you ever browsed through photo-sharing sites like Instagram or Pinterest, spotted an outfit you loved, but had no idea where to find the clothing? This project will guide you through building an application that allows you to upload a photo of any outfit or type in a text description, and then suggests similar apparel pieces to help you recreate the look.

## Overview

In this project, you'll learn how to leverage Google Vertex AI, Weaviate vector database, Google’s multimodal embeddings, Retrieval-Augmented Generation (RAG), and Weaviate’s hybrid search feature. By combining these tools, you'll perform vector similarity searches and build a sophisticated multi-modal Recommender System, and deploy the application on Streamlit.

## Key Concepts

### Vector Database
A vector database stores data in the form of vectors and allows for efficient similarity search and retrieval. In this project, Weaviate is used as the vector database to store and query the vector embeddings of fashion items. This enables fast and accurate retrieval of similar items based on vector similarity.

### Vector Search
Vector search is a method of finding similar items in a dataset by comparing vectors. Each item is represented as a vector in a high-dimensional space, and similarity is determined by the distance between these vectors. This technique is especially useful for tasks involving images and text, where traditional keyword search methods are inadequate.

### Embeddings
Embeddings are dense vector representations of data.

#### Multimodal Embeddings
Multimodal embeddings combine different types of data (such as text and images) into a unified vector space. This allows for cross-modal retrieval and comparison. In this project, we use Google’s multimodal embeddings, which are designed to capture the semantic meaning of both visual and textual content in a shared embedding space.

Technically, these embeddings are generated using deep learning models that process images and text through separate pathways that eventually converge. For example:

Image Pathway: Convolutional Neural Networks (CNNs) or other image processing models extract features from images, which are then mapped to the embedding space.

Text Pathway: Transformers or other text processing models extract semantic information from text descriptions, which are also mapped to the same embedding space.
By training these models together, the resulting embeddings ensure that similar items (whether described textually or visually) are close to each other in the high-dimensional vector space. This enables efficient similarity search and retrieval across different modalities.

### Multimodal Recommender System
A multimodal recommender system leverages multiple types of data (e.g., images and text) to provide recommendations. In this project, both image embeddings and text embeddings are used to find and suggest similar fashion items.

### Hybrid Search
Hybrid search combines multiple search strategies to improve the accuracy and relevance of search results. In this project, both vector similarity and keyword-based search are used to enhance the recommendation system's performance.

## Running the Application

Follow the steps in the provided Jupyter notebooks to set up and run the application:

- **Part 1**: [Fashion_Finder_Part_1.ipynb](Fashion_Finder_Part_1.ipynb)
- **Part 2**: [Fashion_Finder_Part_2.ipynb](Fashion_Finder_Part_2.ipynb)

These notebooks contain detailed instructions and code snippets to help you build and run the Fashion Finder application.

### Files Included
- `mm_rag.py`: Core application file for the recommender system.
- `Logo.png`: Logo for the application.

### Deployment
Instructions for deploying the application using Streamlit and Pyngrok are provided in the tutorial notebooks.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.



