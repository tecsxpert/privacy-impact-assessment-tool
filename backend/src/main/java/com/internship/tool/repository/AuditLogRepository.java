package com.internship.tool.repository;

import com.internship.tool.entity.AuditLog;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AuditLogRepository
        extends JpaRepository<AuditLog, Long> {

    List<AuditLog> findByEntityTypeAndEntityIdOrderByChangedAtDesc(
        String entityType, Long entityId);
}