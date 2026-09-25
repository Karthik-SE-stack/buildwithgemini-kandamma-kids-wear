package com.kandamma.kidswear.model;

import com.google.cloud.firestore.annotation.DocumentId;
import com.google.cloud.spring.data.firestore.Document;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collectionName = "products")
public class Product {
    @DocumentId
    private String id;
    private String name;
    private String category; // Ethnic, Formal, Casual
    private Double price;
    private List<String> sizes;
    private String description;
    private Integer stock;
    private String imageUrl;
}
