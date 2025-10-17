package com.jwtauth.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.jwtauth.model.*;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class ApiClient {
    private static final String BASE_URL = "http://localhost:5000";
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    private String accessToken;
    private String refreshToken;

    public ApiClient() {
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
        
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
    }

    // Getters y setters para tokens
    public String getAccessToken() {
        return accessToken;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    public String getRefreshToken() {
        return refreshToken;
    }

    public void setRefreshToken(String refreshToken) {
        this.refreshToken = refreshToken;
    }

    public boolean hasAccessToken() {
        return accessToken != null && !accessToken.isEmpty();
    }

    public void clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
    }

    // Health Check
    public CompletableFuture<HealthResponse> checkHealth() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/health"))
                        .GET()
                        .timeout(Duration.ofSeconds(5))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200 || response.statusCode() == 503) {
                    return objectMapper.readValue(response.body(), HealthResponse.class);
                } else {
                    throw new RuntimeException("Health check failed with status: " + response.statusCode());
                }
            } catch (Exception e) {
                throw new RuntimeException("Error checking health: " + e.getMessage(), e);
            }
        });
    }

    // Register
    public CompletableFuture<String> register(RegisterRequest registerRequest) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String jsonBody = objectMapper.writeValueAsString(registerRequest);

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/register"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 201) {
                    return "Usuario registrado exitosamente";
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error en registro: " + e.getMessage(), e);
            }
        });
    }

    // Login (SQL)
    public CompletableFuture<LoginResponse> login(LoginRequest loginRequest) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String jsonBody = objectMapper.writeValueAsString(loginRequest);

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/login"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    LoginResponse loginResponse = objectMapper.readValue(response.body(), LoginResponse.class);
                    this.accessToken = loginResponse.getAccessToken();
                    this.refreshToken = loginResponse.getRefreshToken();
                    return loginResponse;
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error en login: " + e.getMessage(), e);
            }
        });
    }

    // Login (Redis)
    public CompletableFuture<LoginResponse> loginRedis(LoginRequest loginRequest) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String jsonBody = objectMapper.writeValueAsString(loginRequest);

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api-redis/login"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    LoginResponse loginResponse = objectMapper.readValue(response.body(), LoginResponse.class);
                    this.accessToken = loginResponse.getAccessToken();
                    this.refreshToken = loginResponse.getRefreshToken();
                    return loginResponse;
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error en login Redis: " + e.getMessage(), e);
            }
        });
    }

    // Refresh Token (SQL)
    public CompletableFuture<RefreshResponse> refreshToken() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (refreshToken == null || refreshToken.isEmpty()) {
                    throw new RuntimeException("No refresh token available");
                }

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/refresh"))
                        .header("Content-Type", "application/json")
                        .header("Authorization", "Bearer " + refreshToken)
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    RefreshResponse refreshResponse = objectMapper.readValue(response.body(), RefreshResponse.class);
                    this.accessToken = refreshResponse.getAccessToken();
                    return refreshResponse;
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error refreshing token: " + e.getMessage(), e);
            }
        });
    }

    // Refresh Token (Redis)
    public CompletableFuture<RefreshResponse> refreshTokenRedis() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (refreshToken == null || refreshToken.isEmpty()) {
                    throw new RuntimeException("No refresh token available");
                }

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api-redis/refresh"))
                        .header("Content-Type", "application/json")
                        .header("Authorization", "Bearer " + refreshToken)
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    RefreshResponse refreshResponse = objectMapper.readValue(response.body(), RefreshResponse.class);
                    this.accessToken = refreshResponse.getAccessToken();
                    return refreshResponse;
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error refreshing token (Redis): " + e.getMessage(), e);
            }
        });
    }

    // Logout (SQL)
    public CompletableFuture<String> logout() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (accessToken == null || accessToken.isEmpty()) {
                    throw new RuntimeException("No access token available");
                }

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/logout"))
                        .header("Content-Type", "application/json")
                        .header("Authorization", "Bearer " + accessToken)
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    clearTokens();
                    return "Logout exitoso";
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error en logout: " + e.getMessage(), e);
            }
        });
    }

    // Logout (Redis)
    public CompletableFuture<String> logoutRedis() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (accessToken == null || accessToken.isEmpty()) {
                    throw new RuntimeException("No access token available");
                }

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api-redis/logout"))
                        .header("Content-Type", "application/json")
                        .header("Authorization", "Bearer " + accessToken)
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    clearTokens();
                    return "Logout exitoso (Redis)";
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error en logout Redis: " + e.getMessage(), e);
            }
        });
    }

    // Get Profile
    public CompletableFuture<User> getProfile() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (accessToken == null || accessToken.isEmpty()) {
                    throw new RuntimeException("No access token available");
                }

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/profile"))
                        .header("Authorization", "Bearer " + accessToken)
                        .GET()
                        .timeout(Duration.ofSeconds(10))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    var result = objectMapper.readTree(response.body());
                    return objectMapper.treeToValue(result.get("user"), User.class);
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error getting profile: " + e.getMessage(), e);
            }
        });
    }

    // Compare Performance
    public CompletableFuture<ComparisonResponse> comparePerformance(LoginRequest loginRequest) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String jsonBody = objectMapper.writeValueAsString(loginRequest);

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(BASE_URL + "/api/performance/compare"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                        .timeout(Duration.ofSeconds(15))
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() == 200) {
                    return objectMapper.readValue(response.body(), ComparisonResponse.class);
                } else {
                    ErrorResponse error = objectMapper.readValue(response.body(), ErrorResponse.class);
                    throw new RuntimeException(error.getMessage());
                }
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                throw new RuntimeException("Error comparing performance: " + e.getMessage(), e);
            }
        });
    }
}

