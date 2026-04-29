// backend/src/main/java/com/internship/tool/dto/AssessmentResponse.java
package com.internship.tool.dto;

import java.time.LocalDateTime;

public class AssessmentResponse {

    private Long id;
    private String title;
    private String description;
    private String projectName;
    private String dataTypes;
    private String dataSubjects;
    private String processingPurpose;
    private String riskLevel;
    private String status;
    private Integer privacyScore;
    private String aiDescription;
    private String deadline;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }

    public String getDataTypes() { return dataTypes; }
    public void setDataTypes(String dataTypes) { this.dataTypes = dataTypes; }

    public String getDataSubjects() { return dataSubjects; }
    public void setDataSubjects(String dataSubjects) { this.dataSubjects = dataSubjects; }

    public String getProcessingPurpose() { return processingPurpose; }
    public void setProcessingPurpose(String processingPurpose) { this.processingPurpose = processingPurpose; }

    public String getRiskLevel() { return riskLevel; }
    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Integer getPrivacyScore() { return privacyScore; }
    public void setPrivacyScore(Integer privacyScore) { this.privacyScore = privacyScore; }

    public String getAiDescription() { return aiDescription; }
    public void setAiDescription(String aiDescription) { this.aiDescription = aiDescription; }

    public String getDeadline() { return deadline; }
    public void setDeadline(String deadline) { this.deadline = deadline; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}