package com.internship.tool.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CreateAssessmentRequest {

    @NotBlank(message = "Title is required")
    @Size(max = 255, message = "Title must be less than 255 characters")
    private String title;

    @NotBlank(message = "Project name is required")
    private String projectName;

    private String description;
    private String dataTypes;
    private String dataSubjects;
    private String processingPurpose;

    // Getters and Setters
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getDataTypes() { return dataTypes; }
    public void setDataTypes(String dataTypes) { this.dataTypes = dataTypes; }

    public String getDataSubjects() { return dataSubjects; }
    public void setDataSubjects(String dataSubjects) { this.dataSubjects = dataSubjects; }

    public String getProcessingPurpose() { return processingPurpose; }
    public void setProcessingPurpose(String processingPurpose) { this.processingPurpose = processingPurpose; }
}
