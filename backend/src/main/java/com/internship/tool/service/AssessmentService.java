package com.internship.tool.service;

import com.internship.tool.dto.*;
import com.internship.tool.entity.Assessment;
import com.internship.tool.repository.AssessmentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import java.nio.charset.StandardCharsets;

import org.springframework.lang.NonNull;

@Service
public class AssessmentService {

    @Autowired
    private AssessmentRepository repository;

    @Cacheable("assessments")
    public Page<Assessment> getAllAssessments(@NonNull Pageable pageable) {
        return repository.findAll(pageable);
    }

    @Cacheable(value = "assessment", key = "#id")
    public Assessment getAssessmentById(@NonNull Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Assessment not found"));
    }

    @CacheEvict(value = {"assessments", "assessment"}, allEntries = true)
    public Assessment saveAssessment(@NonNull Assessment assessment) {
        return repository.save(assessment);
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