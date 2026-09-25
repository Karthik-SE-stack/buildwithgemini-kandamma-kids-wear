package com.kandamma.kidswear.controller;

import com.kandamma.kidswear.model.Product;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "*")
public class ProductController {

    @GetMapping
    public ResponseEntity<List<Product>> getCatalog() {
        Product p1 = new Product("KKW-101", "Festive Silk Ethnic Lehenga Choli Set", "Ethnic", 49.99, Arrays.asList("2Y", "3Y", "4Y", "5Y", "6Y", "7Y-8Y"), "Handcrafted premium silk lehenga choli set with intricate embroidery.", 15, "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/lehenga.jpg");
        Product p2 = new Product("KKW-102", "Dapper Royal Silk Kurta Pyjama with Waistcoat", "Ethnic", 44.99, Arrays.asList("2Y", "3Y", "4Y", "5Y", "6Y", "7Y-8Y"), "Traditional royal silk kurta pyjama styled with a brocade waistcoat.", 20, "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/kurta.jpg");
        Product p3 = new Product("KKW-105", "Little Gentleman Tuxedo Suit with Bowtie", "Formal", 54.99, Arrays.asList("3Y", "4Y", "5Y", "6Y", "7Y"), "Premium 4-piece formal tuxedo suit including blazer, shirt, trousers, and silk bowtie.", 10, "https://storage.googleapis.com/qwiklabs-gcp-02-eb01df7117c0-kandamma-media/tuxedo.jpg");
        return ResponseEntity.ok(Arrays.asList(p1, p2, p3));
    }
}
