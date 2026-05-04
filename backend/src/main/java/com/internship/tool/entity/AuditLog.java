package com.internship.tool.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "audit_log")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "entity_type")
    private String entityType;

    @Column(name = "entity_id")
    private Long entityId;

    @Column(name = "action")
    private String action;

    @Column(name = "changed_by")
    private String changedBy;

    @Column(name = "changed_at")
    private LocalDateTime changedAt = LocalDateTime.now();

    @Column(name = "old_values", columnDefinition = "TEXT")
    private String oldValues;

    @Column(name = "new_values", columnDefinition = "TEXT")
    private String newValues;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getEntityType() { return entityType; }
    public void setEntityType(String entityType) {
        this.entityType = entityType;
    }

    public Long getEntityId() { return entityId; }
    public void setEntityId(Long entityId) {
        this.entityId = entityId;
    }

    public String getAction() { return action; }
    public void setAction(String action) {
        this.action = action;
    }

    public String getChangedBy() { return changedBy; }
    public void setChangedBy(String changedBy) {
        this.changedBy = changedBy;
    }

    public LocalDateTime getChangedAt() { return changedAt; }
    public void setChangedAt(LocalDateTime changedAt) {
        this.changedAt = changedAt;
    }

    public String getOldValues() { return oldValues; }
    public void setOldValues(String oldValues) {
        this.oldValues = oldValues;
    }

    public String getNewValues() { return newValues; }
    public void setNewValues(String newValues) {
        this.newValues = newValues;
    }
}