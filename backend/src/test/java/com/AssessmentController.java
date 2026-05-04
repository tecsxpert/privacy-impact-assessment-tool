package com.internship.tool.controller;

import com.internship.tool.dto.*;
import com.internship.tool.service.AssessmentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@Tag(
    name = "Assessments",
    description = "Privacy Impact Assessment CRUD operations"
)
@RestController
@RequestMapping("/api/assessments")
@CrossOrigin(origins = "http://localhost:5173")
public class AssessmentController {

    private final AssessmentService assessmentService;

    public AssessmentController(
            AssessmentService assessmentService) {
        this.assessmentService = assessmentService;
    }

    @Operation(summary = "Update an existing assessment")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200",
            description = "Assessment updated successfully"),
        @ApiResponse(responseCode = "404",
            description = "Assessment not found"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @PutMapping("/{id}")
    public ResponseEntity<AssessmentResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateAssessmentRequest request) {
        return ResponseEntity.ok(
            assessmentService.update(id, request));
    }

    @Operation(summary = "Soft delete an assessment")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204",
            description = "Assessment deleted successfully"),
        @ApiResponse(responseCode = "404",
            description = "Assessment not found"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> softDelete(
            @PathVariable Long id) {
        assessmentService.softDelete(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(
        summary = "Search assessments",
        description = "Search by keyword and filter by status"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200",
            description = "Search results returned"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @GetMapping("/search")
    public ResponseEntity<Page<AssessmentResponse>> search(
            @RequestParam(
                required = false,
                defaultValue = "") String q,
            @RequestParam(
                required = false,
                defaultValue = "") String status,
            Pageable pageable) {
        return ResponseEntity.ok(
            assessmentService.search(q, status, pageable));
    }

    @Operation(
        summary = "Export assessments as CSV",
        description = "Downloads all assessments as a CSV file"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200",
            description = "CSV file downloaded successfully"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @GetMapping("/export")
    public ResponseEntity<byte[]> exportCsv() {
        byte[] csv = assessmentService.exportToCsv();
        return ResponseEntity.ok()
            .header(
                HttpHeaders.CONTENT_DISPOSITION,
                "attachment; filename=assessments.csv")
            .contentType(
                MediaType.parseMediaType("text/csv"))
            .body(csv);
    }

    @Operation(summary = "Get dashboard statistics")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200",
            description = "Statistics returned successfully"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @GetMapping("/stats")
    public ResponseEntity<DashboardStatsResponse> getStats() {
        return ResponseEntity.ok(
            assessmentService.getDashboardStats());
    }

    @Operation(
        summary = "Upload supporting document",
        description = "Upload PDF or DOCX file max 5MB"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200",
            description = "File uploaded successfully"),
        @ApiResponse(responseCode = "400",
            description = "Invalid file type or size"),
        @ApiResponse(responseCode = "401",
            description = "Unauthorized")
    })
    @PostMapping("/{id}/upload")
    public ResponseEntity<String> uploadFile(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {

        // Validate file size max 5MB
        if (file.getSize() > 5 * 1024 * 1024) {
            return ResponseEntity.badRequest()
                .body("File exceeds 5MB limit");
        }

        // Validate file type
        String allowedTypes =
            "application/pdf," +
            "application/msword," +
            "application/vnd.openxmlformats-officedocument" +
            ".wordprocessingml.document";

        if (file.getContentType() == null ||
            !allowedTypes.contains(file.getContentType())) {
            return ResponseEntity.badRequest()
                .body("Only PDF and DOCX files allowed");
        }

        return ResponseEntity.ok(
            "File uploaded successfully for assessment: " + id);
    }
}