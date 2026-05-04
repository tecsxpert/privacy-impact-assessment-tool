package com.internship.tool;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import com.internship.tool.controller.AssessmentController;
import com.internship.tool.service.AssessmentService;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(AssessmentController.class)
@AutoConfigureMockMvc
class AssessmentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AssessmentService assessmentService;

    // Test 1
    @Test
    void getAll_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/all"))
            .andExpect(status().isUnauthorized());
    }

    // Test 2
    @Test
    void search_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/search?q=test"))
            .andExpect(status().isUnauthorized());
    }

    // Test 3
    @Test
    void export_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/export"))
            .andExpect(status().isUnauthorized());
    }

    // Test 4
    @Test
    void stats_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/stats"))
            .andExpect(status().isUnauthorized());
    }

    // Test 5
    @Test
    void update_withoutToken_returns401() throws Exception {
        mockMvc.perform(put("/api/assessments/1")
            .contentType(MediaType.APPLICATION_JSON)
            .content(
                "{\"title\":\"Test\"," +
                "\"projectName\":\"Test\"}"))
            .andExpect(status().isUnauthorized());
    }

    // Test 6
    @Test
    void delete_withoutToken_returns401() throws Exception {
        mockMvc.perform(delete("/api/assessments/1"))
            .andExpect(status().isUnauthorized());
    }

    // Test 7
    @Test
    void upload_withoutToken_returns401() throws Exception {
        mockMvc.perform(
            post("/api/assessments/1/upload"))
            .andExpect(status().isUnauthorized());
    }

    // Test 8
    @Test
    void createAssessment_withoutToken_returns401()
            throws Exception {
        mockMvc.perform(post("/api/assessments/create")
            .contentType(MediaType.APPLICATION_JSON)
            .content(
                "{\"title\":\"Test\"," +
                "\"projectName\":\"Test\"}"))
            .andExpect(status().isUnauthorized());
    }

    // Test 9
    @Test
    void getById_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/999"))
            .andExpect(status().isUnauthorized());
    }

    // Test 10
    @Test
    void exportCsv_withoutToken_returns401() throws Exception {
        mockMvc.perform(get("/api/assessments/export"))
            .andExpect(status().isUnauthorized());
    }
}