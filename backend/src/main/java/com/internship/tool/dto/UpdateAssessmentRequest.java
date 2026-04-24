// backend/src/main/java/com/internship/tool/dto/UpdateAssessmentRequest.java
package com.internship.tool.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class UpdateAssessmentRequest {

    @NotBlank(message = "Title is required")
    @Size(max = 255, message = "Title must be less than 255 characters")
    private String title;

    private String description;

    @NotBlank(message = "Project name is required")
    private String projectName;

    private String dataTypes;
    private String dataSubjects;
    private String processingPurpose;
    private String riskLevel;
    private String status;
    private Integer privacyScore;
    private String deadline;

    // Getters and Setters
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

    public String getDeadline() { return deadline; }
    public void setDeadline(String deadline) { this.deadline = deadline; }
}