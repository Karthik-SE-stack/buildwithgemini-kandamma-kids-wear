package com.kandamma.kidswear.service;

import com.kandamma.kidswear.model.Order;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.UUID;

@Service
public class WhatsAppOrderService {

    @Value("${kandamma.whatsapp.admin-phone:919876543210}")
    private String adminPhone;

    public Order createWhatsAppOrder(String customerName, String customerPhone, String itemCode, String size, Double price) {
        String orderId = "ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        String paymentToken = UUID.randomUUID().toString().replace("-", "");
        String paymentUrl = "https://checkout.kandammakidswear.com/pay/" + orderId + "?token=" + paymentToken;

        String rawMessage = String.format(
                "🛍️ *NEW KANDAMMA KIDS WEAR ORDER*\n" +
                "━━━━━━━━━━━━━━━━━━━━\n" +
                "📋 *Order ID*: %s\n" +
                "👤 *Customer*: %s (%s)\n" +
                "👗 *Item Code*: %s | *Size*: %s\n" +
                "💰 *Total*: $%.2f\n\n" +
                "💳 *Secured Payment Gateway Link*:\n%s\n" +
                "━━━━━━━━━━━━━━━━━━━━\n" +
                "Please confirm order fulfillment.",
                orderId, customerName, customerPhone, itemCode, size, price, paymentUrl
        );

        String encodedText = URLEncoder.encode(rawMessage, StandardCharsets.UTF_8);
        String whatsappUrl = "https://wa.me/" + adminPhone + "?text=" + encodedText;

        Order order = new Order();
        order.setOrderId(orderId);
        order.setCustomerName(customerName);
        order.setCustomerPhone(customerPhone);
        order.setItemCode(itemCode);
        order.setSize(size);
        order.setPrice(price);
        order.setStatus("PENDING_PAYMENT");
        order.setCreatedAt(Instant.now().toString());
        order.setWhatsappUrl(whatsappUrl);
        order.setPaymentUrl(paymentUrl);

        return order;
    }
}
