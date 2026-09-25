package com.kandammakids.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class KandammaApplication {
    public static void main(String[] args) {
        SpringApplication.run(KandammaApplication.class, args);
    }
}
