import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. CARGA Y LIMPIEZA DE DATOS
# ============================================================================
print("=" * 80)
print("PROYECTO DE PREDICCIÓN DE INCIDENCIA DELICTIVA")
print("=" * 80)

# Cargar datos
print("\n[1] Cargando datos...")
df = pd.read_csv('INM_estatal_jul25.csv')
print(f"   ✓ Datos cargados: {df.shape[0]} registros, {df.shape[1]} columnas")

# Información inicial
print(f"\n[2] Información del dataset:")
print(f"   - Columnas: {list(df.columns)}")
print(f"   - Valores nulos por columna:")
print(df.isnull().sum())

# Limpieza de datos
print("\n[3] Limpiando datos...")
df_clean = df.dropna(subset=['incidencia_delictiva', 'anio'])
df_clean['incidencia_delictiva'] = pd.to_numeric(df_clean['incidencia_delictiva'], errors='coerce')
df_clean = df_clean.dropna(subset=['incidencia_delictiva'])
print(f"   ✓ Registros después de limpieza: {df_clean.shape[0]}")

# ============================================================================
# 2. ANÁLISIS EXPLORATORIO
# ============================================================================
print("\n" + "=" * 80)
print("ANÁLISIS EXPLORATORIO")
print("=" * 80)

# Tendencia anual
print("\n[4] Tendencia anual:")
tendencia_anual = df_clean.groupby('anio')['incidencia_delictiva'].agg(['mean', 'sum', 'count'])
print(tendencia_anual)

# Top entidades
print("\n[5] Top 10 entidades con mayor incidencia promedio:")
top_entidades = df_clean.groupby('entidad')['incidencia_delictiva'].mean().sort_values(ascending=False).head(10)
print(top_entidades)

# ============================================================================
# 3. PREPARACIÓN DE DATOS PARA MACHINE LEARNING
# ============================================================================
print("\n" + "=" * 80)
print("PREPARACIÓN DE DATOS PARA ML")
print("=" * 80)

print("\n[6] Codificando variables categóricas...")

# Seleccionar todas las columnas disponibles excepto el target
columnas_disponibles = [col for col in df_clean.columns if col != 'incidencia_delictiva']
print(f"   - Columnas disponibles: {columnas_disponibles}")

# Crear DataFrame de trabajo con todas las columnas
df_ml = df_clean.copy()
df_ml = df_ml.dropna(subset=['incidencia_delictiva'])

# Identificar columnas numéricas y categóricas automáticamente
columnas_numericas = []
columnas_categoricas = []

for col in columnas_disponibles:
    if df_ml[col].dtype in ['int64', 'float64']:
        # Intentar convertir a numérico
        try:
            df_ml[col] = pd.to_numeric(df_ml[col], errors='coerce')
            columnas_numericas.append(col)
        except:
            columnas_categoricas.append(col)
    else:
        columnas_categoricas.append(col)

print(f"   - Columnas numéricas detectadas: {columnas_numericas}")
print(f"   - Columnas categóricas detectadas: {columnas_categoricas}")

# Label Encoding para variables categóricas
label_encoders = {}
for col in columnas_categoricas:
    if col in df_ml.columns:
        le = LabelEncoder()
        df_ml[col + '_encoded'] = le.fit_transform(df_ml[col].astype(str))
        label_encoders[col] = le
        print(f"   ✓ {col}: {len(le.classes_)} categorías únicas")

# Preparar X (features) e y (target)
feature_cols = [col + '_encoded' for col in columnas_categoricas if col in df_ml.columns] + columnas_numericas

# Limpiar NaN en las features
df_ml = df_ml.dropna(subset=feature_cols + ['incidencia_delictiva'])

X = df_ml[feature_cols]
y = df_ml['incidencia_delictiva']

print(f"\n[7] Features seleccionadas: {feature_cols}")
print(f"   - Shape de X: {X.shape}")
print(f"   - Shape de y: {y.shape}")

# ============================================================================
# 4. DIVISIÓN DE DATOS (80% ENTRENAMIENTO, 20% PRUEBA)
# ============================================================================
print("\n[8] Dividiendo datos en entrenamiento (80%) y prueba (20%)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"   ✓ Conjunto de entrenamiento: {X_train.shape[0]} registros")
print(f"   ✓ Conjunto de prueba: {X_test.shape[0]} registros")

# ============================================================================
# 5. MODELO 1: REGRESIÓN LINEAL CLÁSICA
# ============================================================================
print("\n" + "=" * 80)
print("MODELO 1: REGRESIÓN LINEAL CLÁSICA")
print("=" * 80)

print("\n[9] Entrenando Regresión Lineal...")
modelo_lr = LinearRegression()
modelo_lr.fit(X_train, y_train)
print("   ✓ Modelo entrenado exitosamente")

# Predicciones
print("\n[10] Realizando predicciones...")
y_pred_lr_train = modelo_lr.predict(X_train)
y_pred_lr_test = modelo_lr.predict(X_test)

# Métricas
r2_train_lr = r2_score(y_train, y_pred_lr_train)
r2_test_lr = r2_score(y_test, y_pred_lr_test)
rmse_train_lr = np.sqrt(mean_squared_error(y_train, y_pred_lr_train))
rmse_test_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr_test))
mae_test_lr = mean_absolute_error(y_test, y_pred_lr_test)

print("\n[11] MÉTRICAS DE REGRESIÓN LINEAL:")
print(f"   • R² (Entrenamiento): {r2_train_lr:.4f}")
print(f"   • R² (Prueba): {r2_test_lr:.4f}")
print(f"   • RMSE (Entrenamiento): {rmse_train_lr:.2f}")
print(f"   • RMSE (Prueba): {rmse_test_lr:.2f}")
print(f"   • MAE (Prueba): {mae_test_lr:.2f}")

# ============================================================================
# 6. MODELO 2: RANDOM FOREST REGRESSOR
# ============================================================================
print("\n" + "=" * 80)
print("MODELO 2: RANDOM FOREST REGRESSOR (ML MEJORADO)")
print("=" * 80)

print("\n[12] Entrenando Random Forest...")
modelo_rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)
modelo_rf.fit(X_train, y_train)
print("   ✓ Modelo entrenado exitosamente")

# Predicciones
print("\n[13] Realizando predicciones...")
y_pred_rf_train = modelo_rf.predict(X_train)
y_pred_rf_test = modelo_rf.predict(X_test)

# Métricas
r2_train_rf = r2_score(y_train, y_pred_rf_train)
r2_test_rf = r2_score(y_test, y_pred_rf_test)
rmse_train_rf = np.sqrt(mean_squared_error(y_train, y_pred_rf_train))
rmse_test_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf_test))
mae_test_rf = mean_absolute_error(y_test, y_pred_rf_test)

print("\n[14] MÉTRICAS DE RANDOM FOREST:")
print(f"   • R² (Entrenamiento): {r2_train_rf:.4f}")
print(f"   • R² (Prueba): {r2_test_rf:.4f}")
print(f"   • RMSE (Entrenamiento): {rmse_train_rf:.2f}")
print(f"   • RMSE (Prueba): {rmse_test_rf:.2f}")
print(f"   • MAE (Prueba): {mae_test_rf:.2f}")

# Importancia de características
print("\n[15] Importancia de características (Top 5):")
importancias = pd.DataFrame({
    'Feature': feature_cols,
    'Importancia': modelo_rf.feature_importances_
}).sort_values('Importancia', ascending=False)
print(importancias.head())

# ============================================================================
# 7. TABLA COMPARATIVA DE MÉTRICAS
# ============================================================================
print("\n" + "=" * 80)
print("COMPARACIÓN DE MODELOS")
print("=" * 80)

print("\n[16] Tabla resumen de métricas:")
comparacion = pd.DataFrame({
    'Modelo': ['Regresión Lineal', 'Random Forest'],
    'R² (Train)': [r2_train_lr, r2_train_rf],
    'R² (Test)': [r2_test_lr, r2_test_rf],
    'RMSE (Train)': [rmse_train_lr, rmse_train_rf],
    'RMSE (Test)': [rmse_test_lr, rmse_test_rf],
    'MAE (Test)': [mae_test_lr, mae_test_rf]
})
print(comparacion.to_string(index=False))

# Determinar mejor modelo
if r2_test_rf > r2_test_lr:
    mejor_modelo = "Random Forest"
    mejora = ((r2_test_rf - r2_test_lr) / abs(r2_test_lr)) * 100
else:
    mejor_modelo = "Regresión Lineal"
    mejora = ((r2_test_lr - r2_test_rf) / abs(r2_test_rf)) * 100

print(f"\n[17] CONCLUSIÓN:")
print(f"   ★ Mejor modelo: {mejor_modelo}")
print(f"   ★ Mejora en R²: {mejora:.2f}%")

# ============================================================================
# 8. PREDICCIONES FUTURAS (2025-2026)
# ============================================================================
print("\n" + "=" * 80)
print("PROYECCIONES FUTURAS")
print("=" * 80)

print("\n[18] Generando predicciones para 2025 y 2026...")

# Tomar características promedio de datos recientes
X_reciente = X_train.tail(1000).mean().to_frame().T

# Crear escenarios para 2025 y 2026
predicciones_futuras = []
for anio in [2025, 2026]:
    X_futuro = X_reciente.copy()
    X_futuro['anio'] = anio
    
    pred_lr = modelo_lr.predict(X_futuro)[0]
    pred_rf = modelo_rf.predict(X_futuro)[0]
    promedio = (pred_lr + pred_rf) / 2
    
    predicciones_futuras.append({
        'Año': anio,
        'Predicción LR': pred_lr,
        'Predicción RF': pred_rf,
        'Promedio': promedio
    })

df_predicciones = pd.DataFrame(predicciones_futuras)
print("\nPredicciones de incidencia delictiva:")
print(df_predicciones.to_string(index=False))

# ============================================================================
# 9. VISUALIZACIONES
# ============================================================================
print("\n" + "=" * 80)
print("GENERANDO VISUALIZACIONES")
print("=" * 80)

print("\n[19] Creando gráficas comparativas...")

# Crear figura con 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ANÁLISIS COMPARATIVO DE MODELOS DE PREDICCIÓN', fontsize=16, fontweight='bold')

# -------- GRÁFICA 1: Comparación de valores reales vs predicciones (muestra) --------
ax1 = axes[0, 0]
muestra = min(100, len(y_test))
indices = range(muestra)

ax1.plot(indices, y_test.values[:muestra], 'o-', label='Datos Reales', color='black', alpha=0.7, linewidth=2)
ax1.plot(indices, y_pred_lr_test[:muestra], 's--', label='Regresión Lineal', color='blue', alpha=0.6)
ax1.plot(indices, y_pred_rf_test[:muestra], '^--', label='Random Forest', color='green', alpha=0.6)
ax1.set_xlabel('Índice de Muestra', fontsize=11)
ax1.set_ylabel('Incidencia Delictiva', fontsize=11)
ax1.set_title('Comparación: Datos Reales vs Predicciones (Primeros 100)', fontsize=12, fontweight='bold')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)

# -------- GRÁFICA 2: Scatter plot - Regresión Lineal --------
ax2 = axes[0, 1]
ax2.scatter(y_test, y_pred_lr_test, alpha=0.5, s=20, color='blue', edgecolors='darkblue')
max_val = max(y_test.max(), y_pred_lr_test.max())
ax2.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Línea Perfecta (y=x)')
ax2.set_xlabel('Valores Reales', fontsize=11)
ax2.set_ylabel('Valores Predichos', fontsize=11)
ax2.set_title(f'Regresión Lineal\nR² = {r2_test_lr:.4f} | RMSE = {rmse_test_lr:.2f}', 
              fontsize=12, fontweight='bold')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)

# -------- GRÁFICA 3: Scatter plot - Random Forest --------
ax3 = axes[1, 0]
ax3.scatter(y_test, y_pred_rf_test, alpha=0.5, s=20, color='green', edgecolors='darkgreen')
max_val = max(y_test.max(), y_pred_rf_test.max())
ax3.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Línea Perfecta (y=x)')
ax3.set_xlabel('Valores Reales', fontsize=11)
ax3.set_ylabel('Valores Predichos', fontsize=11)
ax3.set_title(f'Random Forest\nR² = {r2_test_rf:.4f} | RMSE = {rmse_test_rf:.2f}', 
              fontsize=12, fontweight='bold')
ax3.legend(loc='best')
ax3.grid(True, alpha=0.3)

# -------- GRÁFICA 4: Comparación de métricas --------
ax4 = axes[1, 1]
modelos = ['Regresión\nLineal', 'Random\nForest']
r2_scores = [r2_test_lr, r2_test_rf]
rmse_scores = [rmse_test_lr / 100, rmse_test_rf / 100]  # Normalizar para visualización

x = np.arange(len(modelos))
width = 0.35

bars1 = ax4.bar(x - width/2, r2_scores, width, label='R² Score', color='steelblue', alpha=0.8)
bars2 = ax4.bar(x + width/2, rmse_scores, width, label='RMSE (÷100)', color='coral', alpha=0.8)

ax4.set_ylabel('Valor de Métrica', fontsize=11)
ax4.set_title('Comparación de Métricas por Modelo', fontsize=12, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(modelos)
ax4.legend(loc='best')
ax4.grid(True, alpha=0.3, axis='y')

# Añadir valores en las barras
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('comparacion_modelos_ml.png', dpi=300, bbox_inches='tight')
print("   ✓ Gráfica guardada como 'comparacion_modelos_ml.png'")

# ============================================================================
# 10. INTERPRETACIÓN DE RESULTADOS
# ============================================================================
print("\n" + "=" * 80)
print("INTERPRETACIÓN DE RESULTADOS")
print("=" * 80)

print("\n[20] ¿QUÉ ES R² (Coeficiente de Determinación)?")
print("   R² mide qué tan bien el modelo explica la variabilidad de los datos.")
print("   • R² = 1.0 → Predicción perfecta")
print("   • R² = 0.0 → El modelo no explica nada")
print("   • R² < 0.0 → El modelo es peor que predecir el promedio")
print(f"\n   En este proyecto:")
print(f"   - Regresión Lineal: R² = {r2_test_lr:.4f} ({r2_test_lr*100:.2f}% de varianza explicada)")
print(f"   - Random Forest: R² = {r2_test_rf:.4f} ({r2_test_rf*100:.2f}% de varianza explicada)")

print("\n[21] ¿QUÉ ES RMSE (Error Cuadrático Medio)?")
print("   RMSE mide el error promedio de las predicciones en las mismas unidades")
print("   que la variable objetivo. Un RMSE más bajo = mejores predicciones.")
print(f"\n   En este proyecto:")
print(f"   - Regresión Lineal: RMSE = {rmse_test_lr:.2f}")
print(f"   - Random Forest: RMSE = {rmse_test_rf:.2f}")
print(f"   Interpretación: En promedio, las predicciones se desvían ±{rmse_test_rf:.2f} unidades")

print("\n[22] CONCLUSIONES FINALES:")
print(f"\n   ✓ MEJOR MODELO: {mejor_modelo}")
print(f"   ✓ El {mejor_modelo} tiene un R² de {max(r2_test_lr, r2_test_rf):.4f}")
print(f"   ✓ Esto significa que explica el {max(r2_test_lr, r2_test_rf)*100:.2f}% de la variabilidad")
print(f"   ✓ El error típico de predicción es de {min(rmse_test_lr, rmse_test_rf):.2f} unidades")

print("\n[23] LIMITACIONES:")
print("   • Los modelos asumen que los patrones históricos se mantendrán")
print("   • No consideran factores externos (economía, políticas públicas, etc.)")
print("   • La calidad depende de la completitud del registro delictivo")
print("   • Las predicciones 2025-2026 son estimaciones basales, no certezas")

print("\n[24] UTILIDAD PRÁCTICA:")
print("   • Identificar tendencias y patrones generales")
print("   • Asignar recursos de seguridad de manera más eficiente")
print("   • Detectar anomalías en la incidencia delictiva")
print("   • Generar escenarios base para planificación estratégica")

print("\n" + "=" * 80)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print("\n✓ Modelos entrenados y evaluados")
print("✓ Gráficas comparativas generadas")
print("✓ Predicciones futuras calculadas")
print("✓ Análisis interpretativo incluido")

plt.show()