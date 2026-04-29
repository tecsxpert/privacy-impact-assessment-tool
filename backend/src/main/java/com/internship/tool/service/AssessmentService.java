package com.internship.tool.service;

import com.internship.tool.dto.*;
import com.internship.tool.entity.Assessment;
import com.internship.tool.repository.AssessmentRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Async;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.List;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class AssessmentService {

    private final AssessmentRepository assessmentRepository;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;

    public AssessmentService(AssessmentRepository assessmentRepository, AiServiceClient aiServiceClient) {
        this.assessmentRepository = assessmentRepository;
        this.aiServiceClient = aiServiceClient;
        this.objectMapper = new ObjectMapper();
    }

    public AssessmentResponse create(CreateAssessmentRequest request) {
        Assessment assessment = new Assessment();
        assessment.setProjectName(request.getProjectName());
        assessment.setDescription(request.getDescription());
        assessment.setStatus("DRAFT");
        
        assessment = assessmentRepository.save(assessment);

        // Build input for AI
        String aiInput = "Project: " + request.getProjectName() + 
                         ", Desc: " + request.getDescription() + 
                         ", DataTypes: " + request.getDataTypes() + 
                         ", Subjects: " + request.getDataSubjects() + 
                         ", Purpose: " + request.getProcessingPurpose();

        triggerAiEvaluation(assessment.getId(), aiInput);

        AssessmentResponse response = new AssessmentResponse();
        response.setId(assessment.getId());
        response.setTitle(request.getTitle());
        response.setProjectName(request.getProjectName());
        response.setStatus(assessment.getStatus());
        return response;
    }

    @Async
    public void triggerAiEvaluation(Long assessmentId, String aiInput) {
        try {
            // 1. Get Description
            Map<String, Object> describeResult = aiServiceClient.callAiService("/describe", aiInput);
            
            // 2. Get Recommendations
            List<Map<String, Object>> recommendResult = aiServiceClient.callAiServiceForList("/recommend", aiInput);

            assessmentRepository.findById(assessmentId).ifPresent(assessment -> {
                boolean updated = false;

                if (describeResult != null) {
                    if (describeResult.containsKey("risk_level")) {
                        assessment.setRiskLevel((String) describeResult.get("risk_level"));
                    }
                    updated = true;
                }

                if (recommendResult != null) {
                    try {
                        assessment.setAiRecommendations(objectMapper.writeValueAsString(recommendResult));
                        updated = true;
                    } catch (Exception e) {
                        System.err.println("Failed to serialize AI recommendations: " + e.getMessage());
                    }
                }

                if (updated) {
                    assessmentRepository.save(assessment);
                    System.out.println("Async AI evaluation completed and saved for Assessment ID: " + assessmentId);
                }
            });

        } catch (Exception e) {
            System.err.println("Error during async AI evaluation: " + e.getMessage());
        }
    }

    public AssessmentResponse update(Long id, UpdateAssessmentRequest request) {
        AssessmentResponse response = new AssessmentResponse();
        response.setId(id);
        response.setTitle(request.getTitle());
        response.setProjectName(request.getProjectName());
        response.setRiskLevel(request.getRiskLevel());
        response.setStatus(request.getStatus());
        return response;
    }

    public void softDelete(Long id) {
        System.out.println("Soft deleting assessment: " + id);
    }

    public Page<AssessmentResponse> search(
            String q, String status, Pageable pageable) {
        return Page.empty();
    }

    public byte[] exportToCsv() {
        StringBuilder csv = new StringBuilder();
        csv.append("ID,Title,Project,Risk Level,Status,Score\n");
        csv.append("1,Sample,Sample Project,LOW,DRAFT,75\n");
        return csv.toString().getBytes(StandardCharsets.UTF_8);
    }

    public DashboardStatsResponse getDashboardStats() {
        return new DashboardStatsResponse(0L, 0L, 0.0, 0L);
    }
}