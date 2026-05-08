package com.internship.tool.config;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;

@Aspect
@Component
public class AuditAspect {

    private final AuditLogRepository auditLogRepository;

    public AuditAspect(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @AfterReturning(
        pointcut =
            "execution(* com.internship.tool.service.*Service.update*(..)) || " +
            "execution(* com.internship.tool.service.*Service.softDelete*(..))",
        returning = "result"
    )
    public void logAuditEvent(JoinPoint jp, Object result) {
        try {
            String method = jp.getSignature().getName();
            String action = method.startsWith("update")
                ? "UPDATE" : "DELETE";

            AuditLog log = new AuditLog();
            log.setEntityType("PrivacyAssessment");
            log.setAction(action);
            log.setChangedBy("system");
            log.setChangedAt(LocalDateTime.now());
            auditLogRepository.save(log);

        } catch (Exception e) {
            System.err.println(
                "Audit logging failed: " + e.getMessage());
        }
    }
}