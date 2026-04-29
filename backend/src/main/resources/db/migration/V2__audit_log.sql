-- V2__audit_log.sql
-- Audit log table for tracking all changes

CREATE TABLE audit_log (
    id            BIGSERIAL PRIMARY KEY,
    entity_type   VARCHAR(100) NOT NULL,
    entity_id     BIGINT       NOT NULL,
    action        VARCHAR(50)  NOT NULL,
    changed_by    VARCHAR(100),
    changed_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    old_values    TEXT,
    new_values    TEXT,
    ip_address    VARCHAR(45)
);

CREATE INDEX idx_audit_entity
    ON audit_log(entity_type, entity_id);

CREATE INDEX idx_audit_user
    ON audit_log(changed_by);

CREATE INDEX idx_audit_time
    ON audit_log(changed_at DESC);