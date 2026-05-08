package com.internship.tool.repository;

import com.internship.tool.entity.Assessment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AssessmentRepository extends JpaRepository<Assessment, Long> {

    List<Assessment> findByStatus(String status);

    List<Assessment> findByProjectNameContaining(String keyword);
}