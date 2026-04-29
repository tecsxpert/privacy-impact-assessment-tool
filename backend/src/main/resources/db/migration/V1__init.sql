-- V1__init.sql
-- Core tables for Privacy Impact Assessment Tool

CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(100) NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(50)  NOT NULL DEFAULT 'USER',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE privacy_assessments (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(255)   NOT NULL,
    description         TEXT,
    project_name        VARCHAR(255)   NOT NULL,
    data_types          VARCHAR(500),
    data_subjects       VARCHAR(255),
    processing_purpose  TEXT,
    risk_level          VARCHAR(50)    NOT NULL DEFAULT 'LOW',
    status              VARCHAR(50)    NOT NULL DEFAULT 'DRAFT',
    privacy_score       INTEGER        CHECK (privacy_score BETWEEN 0 AND 100),
    ai_description      TEXT,
    ai_recommendations  TEXT,
    ai_report           TEXT,
    is_deleted          BOOLEAN        NOT NULL DEFAULT FALSE,
    deadline            DATE,
    created_by          BIGINT         REFERENCES users(id),
    created_at          TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_assessments_status
    ON privacy_assessments(status)
    WHERE is_deleted = FALSE;

CREATE INDEX idx_assessments_risk
    ON privacy_assessments(risk_level)
    WHERE is_deleted = FALSE;

CREATE INDEX idx_assessments_created
    ON privacy_assessments(created_at DESC);

CREATE INDEX idx_assessments_created_by
    ON privacy_assessments(created_by);