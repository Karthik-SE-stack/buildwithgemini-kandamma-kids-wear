package com.zara.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class ZaraApplication {
    public static void main(String[] args) {
        SpringApplication.run(ZaraApplication.class, args);
    }
}
