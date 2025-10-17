package com.jwtauth.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

@JsonIgnoreProperties(ignoreUnknown = true)
public class ComparisonResponse {
    private User user;
    private Map<String, ComparisonResult> comparison;
    
    @JsonProperty("performance_analysis")
    private PerformanceAnalysis performanceAnalysis;

    public ComparisonResponse() {
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Map<String, ComparisonResult> getComparison() {
        return comparison;
    }

    public void setComparison(Map<String, ComparisonResult> comparison) {
        this.comparison = comparison;
    }

    public PerformanceAnalysis getPerformanceAnalysis() {
        return performanceAnalysis;
    }

    public void setPerformanceAnalysis(PerformanceAnalysis performanceAnalysis) {
        this.performanceAnalysis = performanceAnalysis;
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ComparisonResult {
        private Boolean success;
        
        @JsonProperty("response_time_ms")
        private Double responseTimeMs;
        
        private String error;

        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public Double getResponseTimeMs() {
            return responseTimeMs;
        }

        public void setResponseTimeMs(Double responseTimeMs) {
            this.responseTimeMs = responseTimeMs;
        }

        public String getError() {
            return error;
        }

        public void setError(String error) {
            this.error = error;
        }
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class PerformanceAnalysis {
        @JsonProperty("faster_system")
        private String fasterSystem;
        
        @JsonProperty("time_difference_ms")
        private Double timeDifferenceMs;
        
        @JsonProperty("percentage_difference")
        private Double percentageDifference;
        
        @JsonProperty("redis_advantage")
        private String redisAdvantage;

        public String getFasterSystem() {
            return fasterSystem;
        }

        public void setFasterSystem(String fasterSystem) {
            this.fasterSystem = fasterSystem;
        }

        public Double getTimeDifferenceMs() {
            return timeDifferenceMs;
        }

        public void setTimeDifferenceMs(Double timeDifferenceMs) {
            this.timeDifferenceMs = timeDifferenceMs;
        }

        public Double getPercentageDifference() {
            return percentageDifference;
        }

        public void setPercentageDifference(Double percentageDifference) {
            this.percentageDifference = percentageDifference;
        }

        public String getRedisAdvantage() {
            return redisAdvantage;
        }

        public void setRedisAdvantage(String redisAdvantage) {
            this.redisAdvantage = redisAdvantage;
        }
    }
}

