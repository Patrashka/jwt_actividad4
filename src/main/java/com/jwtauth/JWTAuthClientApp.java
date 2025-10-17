package com.jwtauth;

import com.jwtauth.model.*;
import com.jwtauth.service.ApiClient;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class JWTAuthClientApp extends Application {
    
    private ApiClient apiClient;
    private TextArea logArea;
    private Label statusLabel;
    private Label healthStatusLabel;
    
    // Auth fields
    private TextField usernameField;
    private PasswordField passwordField;
    private TextField emailField;
    private ComboBox<String> modeComboBox;
    
    // Session info
    private Label sessionLabel;
    private TextArea tokenInfoArea;
    
    // Buttons
    private Button loginButton;
    private Button registerButton;
    private Button refreshButton;
    private Button logoutButton;
    private Button profileButton;
    private Button compareButton;
    private Button healthCheckButton;
    private Button clearButton;

    @Override
    public void start(Stage primaryStage) {
        apiClient = new ApiClient();
        
        primaryStage.setTitle("JWT Auth Client - JavaFX");
        
        // Main layout
        BorderPane mainLayout = new BorderPane();
        mainLayout.setPadding(new Insets(10));
        
        // Top: Header
        VBox header = createHeader();
        mainLayout.setTop(header);
        
        // Center: Main content
        VBox centerContent = new VBox(15);
        centerContent.setPadding(new Insets(10));
        
        // Health Check Section
        VBox healthSection = createHealthSection();
        
        // Authentication Section
        VBox authSection = createAuthSection();
        
        // Session Section
        VBox sessionSection = createSessionSection();
        
        // Comparison Section
        VBox comparisonSection = createComparisonSection();
        
        // Log Section
        VBox logSection = createLogSection();
        
        centerContent.getChildren().addAll(
            healthSection,
            new Separator(),
            authSection,
            new Separator(),
            sessionSection,
            new Separator(),
            comparisonSection,
            new Separator(),
            logSection
        );
        
        ScrollPane scrollPane = new ScrollPane(centerContent);
        scrollPane.setFitToWidth(true);
        mainLayout.setCenter(scrollPane);
        
        // Bottom: Status bar
        HBox statusBar = createStatusBar();
        mainLayout.setBottom(statusBar);
        
        Scene scene = new Scene(mainLayout, 900, 800);
        primaryStage.setScene(scene);
        primaryStage.show();
        
        // Initial state
        updateSessionUI(false);
        log("Aplicación iniciada. Backend: http://localhost:5000");
    }

    private VBox createHeader() {
        VBox header = new VBox(5);
        header.setPadding(new Insets(10));
        header.setStyle("-fx-background-color: #2c3e50;");
        
        Label titleLabel = new Label("🔐 JWT Authentication Client");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 24));
        titleLabel.setTextFill(Color.WHITE);
        
        Label subtitleLabel = new Label("Cliente JavaFX para API JWT (SQL/Redis)");
        subtitleLabel.setFont(Font.font("Arial", 14));
        subtitleLabel.setTextFill(Color.LIGHTGRAY);
        
        header.getChildren().addAll(titleLabel, subtitleLabel);
        return header;
    }

    private VBox createHealthSection() {
        VBox section = new VBox(10);
        section.setPadding(new Insets(10));
        section.setStyle("-fx-border-color: #3498db; -fx-border-width: 2; -fx-border-radius: 5;");
        
        Label titleLabel = new Label("🏥 Health Check");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        healthStatusLabel = new Label("Estado: Desconocido");
        healthStatusLabel.setFont(Font.font("Arial", 12));
        
        healthCheckButton = new Button("Verificar Estado del Servidor");
        healthCheckButton.setStyle("-fx-background-color: #3498db; -fx-text-fill: white;");
        healthCheckButton.setOnAction(e -> checkHealth());
        
        HBox buttonBox = new HBox(10);
        buttonBox.getChildren().addAll(healthCheckButton, healthStatusLabel);
        buttonBox.setAlignment(Pos.CENTER_LEFT);
        
        section.getChildren().addAll(titleLabel, buttonBox);
        return section;
    }

    private VBox createAuthSection() {
        VBox section = new VBox(10);
        section.setPadding(new Insets(10));
        section.setStyle("-fx-border-color: #27ae60; -fx-border-width: 2; -fx-border-radius: 5;");
        
        Label titleLabel = new Label("🔑 Autenticación");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        // Mode selection
        HBox modeBox = new HBox(10);
        Label modeLabel = new Label("Modo:");
        modeComboBox = new ComboBox<>();
        modeComboBox.getItems().addAll("SQL", "Redis");
        modeComboBox.setValue("SQL");
        modeBox.getChildren().addAll(modeLabel, modeComboBox);
        modeBox.setAlignment(Pos.CENTER_LEFT);
        
        // Username
        HBox usernameBox = new HBox(10);
        Label usernameLabel = new Label("Username:");
        usernameLabel.setPrefWidth(100);
        usernameField = new TextField("testuser");
        usernameField.setPrefWidth(200);
        usernameBox.getChildren().addAll(usernameLabel, usernameField);
        usernameBox.setAlignment(Pos.CENTER_LEFT);
        
        // Password
        HBox passwordBox = new HBox(10);
        Label passwordLabel = new Label("Password:");
        passwordLabel.setPrefWidth(100);
        passwordField = new PasswordField();
        passwordField.setText("password123");
        passwordField.setPrefWidth(200);
        passwordBox.getChildren().addAll(passwordLabel, passwordField);
        passwordBox.setAlignment(Pos.CENTER_LEFT);
        
        // Email (for registration)
        HBox emailBox = new HBox(10);
        Label emailLabel = new Label("Email:");
        emailLabel.setPrefWidth(100);
        emailField = new TextField();
        emailField.setPrefWidth(200);
        emailField.setPromptText("usuario@ejemplo.com");
        emailBox.getChildren().addAll(emailLabel, emailField);
        emailBox.setAlignment(Pos.CENTER_LEFT);
        
        // Buttons
        HBox buttonBox = new HBox(10);
        loginButton = new Button("🔓 Login");
        loginButton.setStyle("-fx-background-color: #27ae60; -fx-text-fill: white;");
        loginButton.setOnAction(e -> login());
        
        registerButton = new Button("📝 Registrar");
        registerButton.setStyle("-fx-background-color: #2980b9; -fx-text-fill: white;");
        registerButton.setOnAction(e -> register());
        
        buttonBox.getChildren().addAll(loginButton, registerButton);
        
        section.getChildren().addAll(titleLabel, modeBox, usernameBox, passwordBox, emailBox, buttonBox);
        return section;
    }

    private VBox createSessionSection() {
        VBox section = new VBox(10);
        section.setPadding(new Insets(10));
        section.setStyle("-fx-border-color: #e67e22; -fx-border-width: 2; -fx-border-radius: 5;");
        
        Label titleLabel = new Label("👤 Sesión Actual");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        sessionLabel = new Label("Estado: No autenticado");
        sessionLabel.setFont(Font.font("Arial", FontWeight.BOLD, 12));
        sessionLabel.setTextFill(Color.RED);
        
        tokenInfoArea = new TextArea();
        tokenInfoArea.setPrefRowCount(3);
        tokenInfoArea.setEditable(false);
        tokenInfoArea.setPromptText("Información de tokens aparecerá aquí...");
        
        // Session buttons
        HBox buttonBox = new HBox(10);
        
        refreshButton = new Button("🔄 Refresh Token");
        refreshButton.setStyle("-fx-background-color: #f39c12; -fx-text-fill: white;");
        refreshButton.setOnAction(e -> refreshToken());
        
        profileButton = new Button("👤 Ver Perfil");
        profileButton.setStyle("-fx-background-color: #9b59b6; -fx-text-fill: white;");
        profileButton.setOnAction(e -> getProfile());
        
        logoutButton = new Button("🔒 Logout");
        logoutButton.setStyle("-fx-background-color: #c0392b; -fx-text-fill: white;");
        logoutButton.setOnAction(e -> logout());
        
        buttonBox.getChildren().addAll(refreshButton, profileButton, logoutButton);
        
        section.getChildren().addAll(titleLabel, sessionLabel, tokenInfoArea, buttonBox);
        return section;
    }

    private VBox createComparisonSection() {
        VBox section = new VBox(10);
        section.setPadding(new Insets(10));
        section.setStyle("-fx-border-color: #9b59b6; -fx-border-width: 2; -fx-border-radius: 5;");
        
        Label titleLabel = new Label("⚡ Comparación de Rendimiento");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        Label descLabel = new Label("Compare el rendimiento entre SQL (MariaDB) y Redis");
        descLabel.setFont(Font.font("Arial", 12));
        descLabel.setTextFill(Color.GRAY);
        
        compareButton = new Button("🔬 Comparar SQL vs Redis");
        compareButton.setStyle("-fx-background-color: #9b59b6; -fx-text-fill: white;");
        compareButton.setOnAction(e -> comparePerformance());
        
        section.getChildren().addAll(titleLabel, descLabel, compareButton);
        return section;
    }

    private VBox createLogSection() {
        VBox section = new VBox(10);
        section.setPadding(new Insets(10));
        section.setStyle("-fx-border-color: #34495e; -fx-border-width: 2; -fx-border-radius: 5;");
        
        Label titleLabel = new Label("📋 Registro de Actividad");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        logArea = new TextArea();
        logArea.setPrefRowCount(10);
        logArea.setEditable(false);
        logArea.setWrapText(true);
        logArea.setStyle("-fx-font-family: 'Courier New'; -fx-font-size: 11px;");
        
        clearButton = new Button("🗑️ Limpiar Log");
        clearButton.setStyle("-fx-background-color: #95a5a6; -fx-text-fill: white;");
        clearButton.setOnAction(e -> logArea.clear());
        
        section.getChildren().addAll(titleLabel, logArea, clearButton);
        return section;
    }

    private HBox createStatusBar() {
        HBox statusBar = new HBox();
        statusBar.setPadding(new Insets(5));
        statusBar.setStyle("-fx-background-color: #ecf0f1;");
        
        statusLabel = new Label("Listo");
        statusLabel.setFont(Font.font("Arial", 11));
        
        statusBar.getChildren().add(statusLabel);
        return statusBar;
    }

    // API Methods

    private void checkHealth() {
        setStatus("Verificando estado del servidor...");
        log("Verificando health check...");
        
        apiClient.checkHealth().thenAccept(health -> {
            Platform.runLater(() -> {
                String statusText = String.format(
                    "Estado: %s | DB: %s | Redis: %s",
                    health.getStatus().toUpperCase(),
                    health.getDatabase(),
                    health.getRedis()
                );
                healthStatusLabel.setText(statusText);
                
                if ("healthy".equalsIgnoreCase(health.getStatus())) {
                    healthStatusLabel.setTextFill(Color.GREEN);
                    log("✅ Servidor saludable - DB: " + health.getDatabase() + ", Redis: " + health.getRedis());
                } else {
                    healthStatusLabel.setTextFill(Color.RED);
                    log("⚠️ Servidor no saludable - " + statusText);
                }
                setStatus("Health check completado");
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                healthStatusLabel.setText("Estado: ERROR");
                healthStatusLabel.setTextFill(Color.RED);
                log("❌ Error en health check: " + ex.getMessage());
                setStatus("Error en health check");
                showError("Error de Conexión", "No se pudo conectar al servidor. Asegúrate de que Flask esté ejecutándose en http://localhost:5000");
            });
            return null;
        });
    }

    private void register() {
        String username = usernameField.getText().trim();
        String password = passwordField.getText();
        String email = emailField.getText().trim();
        
        if (username.isEmpty() || password.isEmpty() || email.isEmpty()) {
            showError("Campos Requeridos", "Por favor, completa todos los campos para registrarte");
            return;
        }
        
        setStatus("Registrando usuario...");
        log("Registrando usuario: " + username);
        
        RegisterRequest request = new RegisterRequest(username, email, password);
        apiClient.register(request).thenAccept(message -> {
            Platform.runLater(() -> {
                log("✅ " + message);
                setStatus("Usuario registrado");
                showInfo("Registro Exitoso", message + "\nAhora puedes iniciar sesión.");
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error en registro: " + ex.getMessage());
                setStatus("Error en registro");
                showError("Error de Registro", ex.getMessage());
            });
            return null;
        });
    }

    private void login() {
        String username = usernameField.getText().trim();
        String password = passwordField.getText();
        String mode = modeComboBox.getValue();
        
        if (username.isEmpty() || password.isEmpty()) {
            showError("Campos Requeridos", "Por favor, ingresa username y password");
            return;
        }
        
        setStatus("Iniciando sesión (" + mode + ")...");
        log("Iniciando sesión con modo: " + mode);
        
        LoginRequest request = new LoginRequest(username, password);
        
        var loginFuture = "SQL".equals(mode) ? 
            apiClient.login(request) : 
            apiClient.loginRedis(request);
        
        loginFuture.thenAccept(response -> {
            Platform.runLater(() -> {
                log("✅ " + response.getMessage());
                log("   Usuario: " + response.getUser().getUsername());
                log("   Email: " + response.getUser().getEmail());
                log("   Tiempo de respuesta: " + response.getResponseTimeMs() + " ms");
                
                updateTokenInfo(response.getAccessToken(), response.getRefreshToken());
                updateSessionUI(true);
                setStatus("Sesión iniciada (" + mode + ")");
                
                showInfo("Login Exitoso", 
                    "Bienvenido " + response.getUser().getUsername() + "!\n" +
                    "Tiempo de respuesta: " + response.getResponseTimeMs() + " ms");
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error en login: " + ex.getMessage());
                setStatus("Error en login");
                showError("Error de Login", ex.getMessage());
            });
            return null;
        });
    }

    private void refreshToken() {
        String mode = modeComboBox.getValue();
        setStatus("Renovando token (" + mode + ")...");
        log("Renovando access token...");
        
        var refreshFuture = "SQL".equals(mode) ? 
            apiClient.refreshToken() : 
            apiClient.refreshTokenRedis();
        
        refreshFuture.thenAccept(response -> {
            Platform.runLater(() -> {
                log("✅ Token renovado exitosamente");
                if (response.getResponseTimeMs() != null) {
                    log("   Tiempo de respuesta: " + response.getResponseTimeMs() + " ms");
                }
                updateTokenInfo(apiClient.getAccessToken(), apiClient.getRefreshToken());
                setStatus("Token renovado");
                showInfo("Token Renovado", "El access token ha sido renovado exitosamente");
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error renovando token: " + ex.getMessage());
                setStatus("Error renovando token");
                showError("Error de Refresh", ex.getMessage());
            });
            return null;
        });
    }

    private void logout() {
        String mode = modeComboBox.getValue();
        setStatus("Cerrando sesión (" + mode + ")...");
        log("Cerrando sesión...");
        
        var logoutFuture = "SQL".equals(mode) ? 
            apiClient.logout() : 
            apiClient.logoutRedis();
        
        logoutFuture.thenAccept(message -> {
            Platform.runLater(() -> {
                log("✅ " + message);
                updateSessionUI(false);
                tokenInfoArea.clear();
                setStatus("Sesión cerrada");
                showInfo("Logout Exitoso", message);
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error en logout: " + ex.getMessage());
                setStatus("Error en logout");
                showError("Error de Logout", ex.getMessage());
            });
            return null;
        });
    }

    private void getProfile() {
        setStatus("Obteniendo perfil...");
        log("Obteniendo información del perfil...");
        
        apiClient.getProfile().thenAccept(user -> {
            Platform.runLater(() -> {
                log("✅ Perfil obtenido:");
                log("   ID: " + user.getId());
                log("   Username: " + user.getUsername());
                log("   Email: " + user.getEmail());
                log("   Activo: " + user.getIsActive());
                setStatus("Perfil obtenido");
                
                showInfo("Perfil de Usuario",
                    "ID: " + user.getId() + "\n" +
                    "Username: " + user.getUsername() + "\n" +
                    "Email: " + user.getEmail() + "\n" +
                    "Estado: " + (user.getIsActive() ? "Activo" : "Inactivo"));
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error obteniendo perfil: " + ex.getMessage());
                setStatus("Error obteniendo perfil");
                showError("Error de Perfil", ex.getMessage());
            });
            return null;
        });
    }

    private void comparePerformance() {
        String username = usernameField.getText().trim();
        String password = passwordField.getText();
        
        if (username.isEmpty() || password.isEmpty()) {
            showError("Campos Requeridos", "Por favor, ingresa username y password para comparar");
            return;
        }
        
        setStatus("Comparando rendimiento SQL vs Redis...");
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        log("🔬 COMPARACIÓN DE RENDIMIENTO: SQL vs Redis");
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        
        LoginRequest request = new LoginRequest(username, password);
        apiClient.comparePerformance(request).thenAccept(comparison -> {
            Platform.runLater(() -> {
                var sqlResult = comparison.getComparison().get("sql");
                var redisResult = comparison.getComparison().get("redis");
                var analysis = comparison.getPerformanceAnalysis();
                
                log("📊 Resultados:");
                log("");
                log("  SQL (MariaDB):");
                log("    ✓ Estado: " + (sqlResult.getSuccess() ? "Exitoso" : "Fallido"));
                log("    ⏱️ Tiempo: " + sqlResult.getResponseTimeMs() + " ms");
                log("");
                log("  Redis:");
                log("    ✓ Estado: " + (redisResult.getSuccess() ? "Exitoso" : "Fallido"));
                log("    ⏱️ Tiempo: " + redisResult.getResponseTimeMs() + " ms");
                log("");
                
                if (analysis != null) {
                    log("📈 Análisis:");
                    log("    🏆 Sistema más rápido: " + analysis.getFasterSystem().toUpperCase());
                    log("    ⏱️ Diferencia: " + Math.abs(analysis.getTimeDifferenceMs()) + " ms");
                    log("    📊 Diferencia porcentual: " + Math.abs(analysis.getPercentageDifference()) + "%");
                    log("    💡 " + analysis.getRedisAdvantage());
                }
                
                log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                setStatus("Comparación completada");
                
                // Show visual comparison dialog
                showComparisonDialog(sqlResult, redisResult, analysis);
            });
        }).exceptionally(ex -> {
            Platform.runLater(() -> {
                log("❌ Error en comparación: " + ex.getMessage());
                log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                setStatus("Error en comparación");
                showError("Error de Comparación", ex.getMessage());
            });
            return null;
        });
    }

    // UI Helper Methods

    private void updateSessionUI(boolean authenticated) {
        Platform.runLater(() -> {
            refreshButton.setDisable(!authenticated);
            profileButton.setDisable(!authenticated);
            logoutButton.setDisable(!authenticated);
            loginButton.setDisable(authenticated);
            
            if (authenticated) {
                sessionLabel.setText("Estado: ✅ Autenticado");
                sessionLabel.setTextFill(Color.GREEN);
            } else {
                sessionLabel.setText("Estado: ❌ No autenticado");
                sessionLabel.setTextFill(Color.RED);
            }
        });
    }

    private void updateTokenInfo(String accessToken, String refreshToken) {
        Platform.runLater(() -> {
            StringBuilder info = new StringBuilder();
            info.append("Access Token: ").append(truncateToken(accessToken)).append("\n");
            info.append("Refresh Token: ").append(truncateToken(refreshToken)).append("\n");
            info.append("Tokens almacenados y listos para usar");
            tokenInfoArea.setText(info.toString());
        });
    }

    private String truncateToken(String token) {
        if (token == null) return "null";
        return token.length() > 50 ? token.substring(0, 50) + "..." : token;
    }

    private void log(String message) {
        Platform.runLater(() -> {
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
            logArea.appendText("[" + timestamp + "] " + message + "\n");
        });
    }

    private void setStatus(String status) {
        Platform.runLater(() -> statusLabel.setText(status));
    }

    private void showError(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showInfo(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showComparisonDialog(
            ComparisonResponse.ComparisonResult sqlResult,
            ComparisonResponse.ComparisonResult redisResult,
            ComparisonResponse.PerformanceAnalysis analysis) {
        
        Dialog<Void> dialog = new Dialog<>();
        dialog.setTitle("Comparación SQL vs Redis");
        dialog.setHeaderText("📊 Resultados de la Comparación de Rendimiento");
        
        VBox content = new VBox(15);
        content.setPadding(new Insets(20));
        
        // SQL Result
        VBox sqlBox = new VBox(5);
        sqlBox.setStyle("-fx-border-color: #3498db; -fx-border-width: 2; -fx-padding: 10; -fx-border-radius: 5;");
        Label sqlTitle = new Label("SQL (MariaDB)");
        sqlTitle.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        Label sqlTime = new Label("Tiempo: " + sqlResult.getResponseTimeMs() + " ms");
        sqlTime.setFont(Font.font("Arial", 16));
        sqlBox.getChildren().addAll(sqlTitle, sqlTime);
        
        // Redis Result
        VBox redisBox = new VBox(5);
        redisBox.setStyle("-fx-border-color: #e74c3c; -fx-border-width: 2; -fx-padding: 10; -fx-border-radius: 5;");
        Label redisTitle = new Label("Redis");
        redisTitle.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        Label redisTime = new Label("Tiempo: " + redisResult.getResponseTimeMs() + " ms");
        redisTime.setFont(Font.font("Arial", 16));
        redisBox.getChildren().addAll(redisTitle, redisTime);
        
        HBox resultsBox = new HBox(20);
        resultsBox.getChildren().addAll(sqlBox, redisBox);
        
        // Analysis
        if (analysis != null) {
            VBox analysisBox = new VBox(5);
            analysisBox.setStyle("-fx-border-color: #2ecc71; -fx-border-width: 2; -fx-padding: 10; -fx-border-radius: 5;");
            Label analysisTitle = new Label("🏆 " + analysis.getFasterSystem().toUpperCase() + " es más rápido");
            analysisTitle.setFont(Font.font("Arial", FontWeight.BOLD, 16));
            Label difference = new Label("Diferencia: " + Math.abs(analysis.getTimeDifferenceMs()) + " ms (" + 
                                         Math.abs(analysis.getPercentageDifference()) + "%)");
            difference.setFont(Font.font("Arial", 14));
            Label advantage = new Label(analysis.getRedisAdvantage());
            advantage.setFont(Font.font("Arial", 12));
            advantage.setTextFill(Color.GRAY);
            analysisBox.getChildren().addAll(analysisTitle, difference, advantage);
            
            content.getChildren().addAll(resultsBox, analysisBox);
        } else {
            content.getChildren().add(resultsBox);
        }
        
        dialog.getDialogPane().setContent(content);
        dialog.getDialogPane().getButtonTypes().add(ButtonType.OK);
        dialog.showAndWait();
    }

    public static void main(String[] args) {
        launch(args);
    }
}

