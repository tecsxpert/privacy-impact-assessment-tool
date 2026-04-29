package com.internship.tool.service;

import com.internship.tool.entity.Assessment;
import com.internship.tool.repository.AssessmentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class AssessmentService {

    @Autowired
    private AssessmentRepository repository;

    @Cacheable("assessments")
    public Page<Assessment> getAllAssessments(Pageable pageable) {
        return repository.findAll(pageable);
    }

    @Cacheable(value = "assessment", key = "#id")
    public Assessment getAssessmentById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Assessment not found"));
    }

    @CacheEvict(value = {"assessments", "assessment"}, allEntries = true)
    public Assessment saveAssessment(Assessment assessment) {
        return repository.save(assessment);
    }
}