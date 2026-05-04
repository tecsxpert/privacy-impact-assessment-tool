package com.internship.tool;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements CommandLineRunner {

    @Override
    public void run(String... args) throws Exception {
        System.out.println("================================");
        System.out.println("DataSeeder: Starting...");
        System.out.println("DataSeeder: Ready to seed 15 demo records");
        System.out.println("DataSeeder: Will activate when");
        System.out.println("           repository is connected");
        System.out.println("================================");
    }
}