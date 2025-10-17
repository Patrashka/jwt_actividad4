package com.jwtauth.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class LoginResponse {
    private String message;
    
    @JsonProperty("access_token")
    private String accessToken;
    
    @JsonProperty("refresh_token")
    private String refreshToken;
    
    private User user;
    
    @JsonProperty("response_time_ms")
    private Double responseTimeMs;

    public LoginResponse() {
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Double getResponseTimeMs() {
        return responseTimeMs;
    }

    public void setResponseTimeMs(Double responseTimeMs) {
        this.responseTimeMs = responseTimeMs;
    }

    @Override
    public String toString() {
        return "LoginResponse{" +
                "message='" + message + '\'' +
                ", accessToken='" + (accessToken != null ? accessToken.substring(0, Math.min(20, accessToken.length())) + "..." : "null") + '\'' +
                ", refreshToken='" + (refreshToken != null ? refreshToken.substring(0, Math.min(20, refreshToken.length())) + "..." : "null") + '\'' +
                ", user=" + user +
                ", responseTimeMs=" + responseTimeMs +
                '}';
    }
}

