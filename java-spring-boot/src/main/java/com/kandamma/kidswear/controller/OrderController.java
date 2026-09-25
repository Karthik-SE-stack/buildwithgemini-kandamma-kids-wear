package com.kandamma.kidswear.controller;

import com.kandamma.kidswear.model.Order;
import com.kandamma.kidswear.service.WhatsAppOrderService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/orders")
@CrossOrigin(origins = "*")
public class OrderController {

    private final WhatsAppOrderService whatsAppOrderService;

    public OrderController(WhatsAppOrderService whatsAppOrderService) {
        this.whatsAppOrderService = whatsAppOrderService;
    }

    @PostMapping("/whatsapp")
    public ResponseEntity<Order> createWhatsAppOrder(@RequestBody Map<String, Object> payload) {
        String customerName = (String) payload.getOrDefault("customerName", "Guest");
        String customerPhone = (String) payload.getOrDefault("customerPhone", "+919876543210");
        String itemCode = (String) payload.getOrDefault("itemCode", "KKW-101");
        String size = (String) payload.getOrDefault("size", "4Y");
        Double price = Double.parseDouble(payload.getOrDefault("price", "49.99").toString());

        Order order = whatsAppOrderService.createWhatsAppOrder(customerName, customerPhone, itemCode, size, price);
        return ResponseEntity.ok(order);
    }
}
