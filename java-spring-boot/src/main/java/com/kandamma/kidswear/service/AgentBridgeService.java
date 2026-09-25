package com.kandamma.kidswear.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.*;

@Service
public class AgentBridgeService {

    @Value("${kandamma.agent.engine-url:https://kandamma-kids-wear-frontend-363499579686.us-east1.run.app/chat}")
    private String agentEndpoint;

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    public AgentBridgeService() {
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(15))
                .build();
        this.objectMapper = new ObjectMapper();
    }

    public Map<String, Object> queryAgent(String userMessage) {
        try {
            Map<String, String> payload = Map.of("message", userMessage);
            String jsonRequest = objectMapper.writeValueAsString(payload);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://kandamma-kids-wear-frontend-363499579686.us-east1.run.app/chat"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonRequest))
                    .timeout(Duration.ofSeconds(30))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                return objectMapper.readValue(response.body(), Map.class);
            }
        } catch (Exception e) {
            System.err.println("Error invoking agent: " + e.getMessage());
        }

        // Fallback response if offline
        Map<String, Object> fallback = new HashMap<>();
        fallback.put("parts", List.of(Map.of("kind", "text", "text", "Welcome to Kandamma Kids Wear! How can I assist you today?")));
        return fallback;
    }
}
