-- V3__seed_data.sql
-- Initial data for Demo Day

-- Create a demo user (password is 'password' BCrypt hashed - though for demo we might not need auth if we skip it, but better have it)
-- Note: Assuming a simple password for demo purposes if needed. 
INSERT INTO users (username, email, password, role) 
VALUES ('admin', 'admin@example.com', '$2a$10$8.UnVuG9HHgffUDAlk8Kn.2Nv5J.v.ZthS7YsnXFqLp.Z3/I.63S.', 'ADMIN');

-- Insert a few sample assessments
INSERT INTO privacy_assessments (title, description, project_name, data_types, data_subjects, processing_purpose, risk_level, status, privacy_score, created_by)
VALUES 
('Customer Loyalty Program', 'Analysis of the new loyalty program data flow.', 'Project Phoenix', 'Email, Purchase History, Location', 'Customers', 'Marketing and personalization', 'MEDIUM', 'COMPLETED', 75, 1),
('Employee Health Portal', 'Internal portal for health insurance management.', 'Project Wellness', 'Health Data, SSN, Contact Info', 'Employees', 'Benefits administration', 'HIGH', 'IN_PROGRESS', 40, 1),
('Public Feedback Survey', 'Anonymous survey for city park improvements.', 'Green City', 'Opinion, Age Group', 'General Public', 'Public service improvement', 'LOW', 'DRAFT', 95, 1);
