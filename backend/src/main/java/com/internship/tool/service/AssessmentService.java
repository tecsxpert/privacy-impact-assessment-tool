package com.internship.tool.service;

import com.internship.tool.dto.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import java.nio.charset.StandardCharsets;

@Service
public class AssessmentService {

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