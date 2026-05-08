package com.internship.tool.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import java.util.Map;
import java.util.HashMap;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final String AI_SERVICE_URL = System.getenv("AI_SERVICE_URL") != null 
        ? System.getenv("AI_SERVICE_URL") 
        : "http://localhost:5000";

    public AiServiceClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(10000); // 10s timeout (Day 4)
        factory.setReadTimeout(10000);
        this.restTemplate = new RestTemplate(factory);
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Map<String, Object> callAiService(String endpoint, String input) {
        String url = AI_SERVICE_URL + endpoint;
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> body = new HashMap<>();
        body.put("input", input);

        HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            return (response != null) ? (Map<String, Object>) response.getBody() : null;
        } catch (Exception e) {
            System.err.println("AI Service Error: " + e.getMessage());
            return null; // Null return on error (Day 4)
        }
    }
}
