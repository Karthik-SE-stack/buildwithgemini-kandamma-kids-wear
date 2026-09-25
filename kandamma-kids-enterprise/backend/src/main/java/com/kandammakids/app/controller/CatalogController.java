package com.kandammakids.app.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/public")
@Tag(name = "KAndamma Catalog & Fit Engine", description = "Public catalog, age-group categories, and kids fit recommendation wizard")
public class CatalogController {

    @GetMapping("/size-recommendation")
    @Operation(summary = "Recommend exact SKU size code based on age, height, and weight")
    public ResponseEntity<Map<String, Object>> getRecommendedSize(
            @RequestParam(required = false, defaultValue = "12") Integer ageMonths,
            @RequestParam(required = false, defaultValue = "72.0") Double heightCm,
            @RequestParam(required = false, defaultValue = "9.0") Double weightKg) {

        String recommendedSize = "6-12M";
        if (ageMonths < 3 || heightCm < 60) recommendedSize = "0-3M";
        else if (ageMonths < 6 || heightCm < 68) recommendedSize = "3-6M";
        else if (ageMonths < 12 || heightCm < 76) recommendedSize = "6-12M";
        else if (ageMonths < 18 || heightCm < 83) recommendedSize = "12-18M";
        else if (ageMonths < 24 || heightCm < 90) recommendedSize = "18-24M";
        else if (ageMonths < 36 || heightCm < 98) recommendedSize = "2-3Y";
        else if (ageMonths < 48 || heightCm < 105) recommendedSize = "3-4Y";
        else if (ageMonths < 60 || heightCm < 112) recommendedSize = "4-5Y";
        else if (ageMonths < 84 || heightCm < 125) recommendedSize = "6-7Y";
        else recommendedSize = "8-9Y";

        return ResponseEntity.ok(Map.of(
            "recommendedSize", recommendedSize,
            "ageMonthsInput", ageMonths,
            "heightCmInput", heightCm,
            "weightKgInput", weightKg,
            "fitMessage", "Recommended size for optimal comfort and growth margin: " + recommendedSize
        ));
    }
}
