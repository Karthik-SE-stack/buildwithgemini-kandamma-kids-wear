package com.kandamma.kidswear.controller;

import com.kandamma.kidswear.model.ChatRequest;
import com.kandamma.kidswear.service.AgentBridgeService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class ChatController {

    private final AgentBridgeService agentBridgeService;

    public ChatController(AgentBridgeService agentBridgeService) {
        this.agentBridgeService = agentBridgeService;
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> chat(@RequestBody ChatRequest chatRequest) {
        Map<String, Object> response = agentBridgeService.queryAgent(chatRequest.getMessage());
        return ResponseEntity.ok(response);
    }
}
