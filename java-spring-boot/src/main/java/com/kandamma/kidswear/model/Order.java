package com.kandamma.kidswear.model;

import com.google.cloud.firestore.annotation.DocumentId;
import com.google.cloud.spring.data.firestore.Document;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collectionName = "orders")
public class Order {
    @DocumentId
    private String orderId;
    private String customerName;
    private String customerPhone;
    private String itemCode;
    private String size;
    private Double price;
    private String status;
    private String createdAt;
    private String whatsappUrl;
    private String paymentUrl;
}
