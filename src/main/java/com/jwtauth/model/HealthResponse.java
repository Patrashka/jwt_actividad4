package com.jwtauth.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class HealthResponse {
    private String status;
    private String database;
    private String redis;
    private String timestamp;

    public HealthResponse() {
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getDatabase() {
        return database;
    }

    public void setDatabase(String database) {
        this.database = database;
    }

    public String getRedis() {
        return redis;
    }

    public void setRedis(String redis) {
        this.redis = redis;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "HealthResponse{" +
                "status='" + status + '\'' +
                ", database='" + database + '\'' +
                ", redis='" + redis + '\'' +
                ", timestamp='" + timestamp + '\'' +
                '}';
    }
}

