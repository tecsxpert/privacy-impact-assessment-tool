// backend/src/main/java/com/internship/tool/controller/AssessmentController.java
package com.internship.tool.controller;

import com.internship.tool.dto.*;
import com.internship.tool.service.AssessmentService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/assessments")
@CrossOrigin(origins = "http://localhost:5173")
public class AssessmentController {

    private final AssessmentService assessmentService;

    public AssessmentController(AssessmentService assessmentService) {
        this.assessmentService = assessmentService;
    }

    // ── Java Developer 2 Endpoints ──────────────────────────

    // PUT /{id} — Update assessment
    @PutMapping("/{id}")
    public ResponseEntity<AssessmentResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateAssessmentRequest request) {
        return ResponseEntity.ok(assessmentService.update(id, request));
    }

    // DELETE /{id} — Soft delete
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> softDelete(@PathVariable Long id) {
        assessmentService.softDelete(id);
        return ResponseEntity.noContent().build();
    }

    // GET /search?q= — Search assessments
    @GetMapping("/search")
    public ResponseEntity<Page<AssessmentResponse>> search(
            @RequestParam(required = false, defaultValue = "") String q,
            @RequestParam(required = false, defaultValue = "") String status,
            Pageable pageable) {
        return ResponseEntity.ok(assessmentService.search(q, status, pageable));
    }

    // GET /export — Export CSV
    @GetMapping("/export")
    public ResponseEntity<byte[]> exportCsv() {
        byte[] csv = assessmentService.exportToCsv();
        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION,
                    "attachment; filename=assessments.csv")
            .contentType(MediaType.parseMediaType("text/csv"))
            .body(csv);
    }

    // GET /stats — Dashboard statistics
    @GetMapping("/stats")
    public ResponseEntity<DashboardStatsResponse> getStats() {
        return ResponseEntity.ok(assessmentService.getDashboardStats());
    }

    // POST /{id}/upload — File upload
    @PostMapping("/{id}/upload")
    public ResponseEntity<String> uploadFile(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {
        if (file.getSize() > 5 * 1024 * 1024) {
            return ResponseEntity.badRequest()
                .body("File exceeds 5MB limit");
        }
        return ResponseEntity.ok("File uploaded successfully");
    }
}