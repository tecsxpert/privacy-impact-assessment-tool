// backend/src/main/java/com/internship/tool/dto/DashboardStatsResponse.java
package com.internship.tool.dto;

public class DashboardStatsResponse {

    private long totalAssessments;
    private long highRiskCount;
    private double averageScore;
    private long pendingReviews;

    public DashboardStatsResponse(long totalAssessments,
                                   long highRiskCount,
                                   double averageScore,
                                   long pendingReviews) {
        this.totalAssessments = totalAssessments;
        this.highRiskCount    = highRiskCount;
        this.averageScore     = averageScore;
        this.pendingReviews   = pendingReviews;
    }

    // Getters
    public long getTotalAssessments() { return totalAssessments; }
    public long getHighRiskCount()    { return highRiskCount; }
    public double getAverageScore()   { return averageScore; }
    public long getPendingReviews()   { return pendingReviews; }
}