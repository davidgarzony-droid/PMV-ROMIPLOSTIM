import streamlit as st
from datetime import datetime
import json

# Configurar página
st.set_page_config(page_title="PMV Romiplostim", layout="wide")
st.title("📧 Gestor de Comunicaciones - APM")

# ============================================
# DATOS REALES (extraídos de tu Sheet)
# ============================================

# Base de hematólogos (del Sheet "Segmentación")
hematologos = {
    "Dr. Juan Pérez": "Reconocimiento Profesional",
    "Dra. María García": "Prestigio Médico",
    "Dr. Carlos López": "Confianza Clínica",
    "Dr. Roberto Martínez": "Reconocimiento Profesional",
    "Dra. Ana Rodríguez": "Prestigio Médico",
    "Dr. Felipe Sánchez": "Confianza Clínica",
    "Dr. Miguel Torres": "Reconocimiento Profesional",
    "Dra. Laura Jiménez": "Prestigio Médico",
    "Dr. Andrés Díaz": "Confianza Clínica"
}

# Matriz de temas × variantes (del Sheet "Toolkit")
matriz_contenidos = {
    "Eficacia Clínica": {
        "Reconocimiento Profesional": {
            "email": "[Email-EficaciaClínica-ReconocimientoProfesional] Datos de respuesta en pacientes con ITP...",
            "whatsapp": "[WhatsApp-EficaciaClínica-ReconocimientoProfesional] ¿Viste los últimos datos de eficacia?"
        },
        "Prestigio Médico": {
            "email": "[Email-EficaciaClínica-PrestigiMédico] Publicación: Resultados en 500 pacientes...",
            "whatsapp": "[WhatsApp-EficaciaClínica-PrestigiMédico] Nueva evidencia para tus pacientes"
        },
        "Confianza Clínica": {
            "email": "[Email-EficaciaClínica-ConfianzaClínica] Seguridad demostrada en práctica clínica...",
            "whatsapp": "[WhatsApp-EficaciaClínica-ConfianzaClínica] Tranquilidad para tus pacientes"
        }
    },
    "Perfil de Seguridad": {
        "Reconocimiento Profesional": {
            "email": "[Email-PerfilSeguridad-ReconocimientoProfesional] Análisis de tolerabilidad...",
            "whatsapp": "[WhatsApp-PerfilSeguridad-ReconocimientoProfesional] Datos de seguridad clave"
        },
        "Prestigio Médico": {
            "email": "[Email-PerfilSeguridad-PrestigiMédico] Perfil favorable vs competencia...",
            "whatsapp": "[WhatsApp-PerfilSeguridad-PrestigiMédico] Mejor perfil en su clase"
        },
        "Confianza Clínica": {
            "email": "[Email-PerfilSeguridad-ConfianzaClínica] Manejo seguro en el día a día...",
            "whatsapp": "[WhatsApp-PerfilSeguridad-ConfianzaClínica] Seguro para todos tus pacientes"
        }
    },
    "Posología": {
        "Reconocimiento Profesional": {
            "email": "[Email-Posología-ReconocimientoProfesional] Esquema optimizado de dosificación...",
            "whatsapp": "[WhatsApp-Posología-ReconocimientoProfesional] Régimen simplificado"
        },
        "Prestigio Médico": {
            "email": "[Email-Posología-PrestigiMédico] Flexibilidad dosimétrica...",
            "whatsapp": "[WhatsApp-Posología-PrestigiMédico] Adaptable a cada caso"
        },
        "Confianza Clínica": {
            "email": "[Email-Posología-ConfianzaClínica] Fácil de administrar en clínica...",
            "whatsapp": "[WhatsApp-Posología-ConfianzaClínica] Simple y práctico"
        }
    },
    "Indicaciones": {
        "Reconocimiento Profesional": {
            "email": "[Email-Indicaciones-ReconocimientoProfesional] Espectro amplio de pacientes...",
            "whatsapp": "[WhatsApp-Indicaciones-ReconocimientoProfesional] Indicaciones actuales"
        },
        "Prestigio Médico": {
            "email": "[Email-Indicaciones-PrestigiMédico] Primera línea en guías internacionales...",
            "whatsapp": "[WhatsApp-Indicaciones-PrestigiMédico] Respaldado por expertos"
        },
        "Confianza Clínica": {
            "email": "[Email-Indicaciones-ConfianzaClínica] Recomendado para la mayoría...",
            "whatsapp": "[WhatsApp-Indicaciones-ConfianzaClínica] Opción confiable"
        }
    },
    "Comparativa Competitiva": {
        "Reconocimiento Profesional": {
            "email": "[Email-Comparativa-ReconocimientoProfesional] Ventajas vs alternativas...",
            "whatsapp": "[WhatsApp-Comparativa-ReconocimientoProfesional] Por qué elegir esto"
        },
        "Prestigio Médico": {
            "email": "[Email-Comparativa-PrestigiMédico] Líder en su categoría...",
            "whatsapp": "[WhatsApp-Comparativa-PrestigiMédico] La mejor opción"
        },
        "Confianza Clínica": {
            "email": "[Email-Comparativa-ConfianzaClínica] Seguro en comparación...",
            "whatsapp": "[WhatsApp-Comparativa-ConfianzaClínica] Más confiable"
        }
    },
    "Casos de Éxito": {
        "Reconocimiento Profesional": {
            "email": "[Email-CasosÉxito-ReconocimientoProfesional] Resultados en tu especialidad...",
            "whatsapp": "[WhatsApp-CasosÉxito-ReconocimientoProfesional] Casos reales"
        },
        "Prestigio Médico": {
            "email": "[Email-CasosÉxito-PrestigiMédico] Testimonios de líderes...",
            "whatsapp": "[WhatsApp-CasosÉxito-PrestigiMédico] Lo usan los mejores"
        },
        "Confianza Clínica": {
            "email": "[Email-CasosÉxito-ConfianzaClínica] Funcionó en casos como el tuyo...",
            "whatsapp": "[WhatsApp-CasosÉxito-ConfianzaClínica] Casos parecidos al tuyo"
        }
    },
    "Acceso y Cobertura": {
        "Reconocimiento Profesional": {
            "email": "[Email-Acceso-ReconocimientoProfesional] Disponibilidad en tu región...",
            "whatsapp": "[WhatsApp-Acceso-ReconocimientoProfesional] Dónde conseguirlo"
        },
        "Prestigio Médico": {
            "email": "[Email-Acceso-PrestigiMédico] Cobertura amplia...",
            "whatsapp": "[WhatsApp-Acceso-PrestigiMédico] Accesible en todas partes"
        },
        "Confianza Clínica": {
            "email": "[Email-Acceso-ConfianzaClínica] Fácil acceso para tus pacientes...",
            "whatsapp": "[WhatsApp-Acceso-ConfianzaClínica] Sin barreras"
        }
    },
    "Educación Médica": {
        "Reconocimiento Profesional": {
            "email": "[Email-Educación-ReconocimientoProfesional] Programa de capacitación...",
            "whatsapp": "[WhatsApp-Educación-ReconocimientoProfesional] Formación especializada"
        },
        "Prestigio Médico": {
            "email": "[Email-Educación-PrestigiMédico] Certificación profesional...",
            "whatsapp": "[WhatsApp-Educación-PrestigiMédico] Reconocimiento profesional"
        },
        "Confianza Clínica": {
            "email": "[Email-Educación-ConfianzaClínica] Recursos para aprender...",
            "whatsapp": "[WhatsApp-Educación-ConfianzaClínica] Aprende con nosotros"
        }
    },
    "Soporte y Servicio": {
        "Reconocimiento Profesional": {
            "email": "[Email-Soporte-ReconocimientoProfesional] Equipo dedicado...",
            "whatsapp": "[WhatsApp-Soporte-ReconocimientoProfesional] Apoyo especializado"
        },
        "Prestigio Médico": {
            "email": "[Email-Soporte-PrestigiMédico] Servicio premium...",
            "whatsapp": "[WhatsApp-Soporte-PrestigiMédico] Servicio VIP"
        },
        "Confianza Clínica": {
            "email": "[Email-Soporte-ConfianzaClínica] Siempre disponibles...",
            "whatsapp": "[WhatsApp-Soporte-ConfianzaClínica] Soporte 24/7"
        }
    }
}

# ============================================
# INTERFAZ STREAMLIT
# ============================================

col1, col2 = st.columns(2)

with col1:
    cliente = st.selectbox("👨‍⚕️ Selecciona el hematólogo:", list(hematologos.keys()))

with col2:
    tema = st.selectbox("📋 Selecciona el tema:", list(matriz_contenidos.keys()))

# ============================================
# LÓGICA DE RECOMENDACIÓN
# ============================================

if cliente and tema:
    fuerza_impulsora = hematologos[cliente]
    
    contenido = matriz_contenidos[tema][fuerza_impulsora]
    
    st.divider()
    st.subheader("📧 Recomendaciones personalizadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📨 Email")
        st.info(contenido["email"])
    
    with col2:
        st.markdown("### 💬 WhatsApp")
        st.success(contenido["whatsapp"])
    
    st.divider()
    
    # Botón para registrar
    if st.button("✅ Registrar envío", key="register"):
        # Guardar en historial (sesión temporal)
        if "historial" not in st.session_state:
            st.session_state.historial = []
        
        registro = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hematólogo": cliente,
            "Tema": tema,
            "Fuerza Impulsora": fuerza_impulsora,
            "Email": contenido["email"],
            "WhatsApp": contenido["whatsapp"]
        }
        
        st.session_state.historial.append(registro)
        st.success(f"✅ Envío registrado a {cliente}")

# ============================================
# HISTORIAL
# ============================================

st.divider()
st.subheader("📊 Historial de envíos")

if "historial" in st.session_state and st.session_state.historial:
    # Mostrar como tabla simple sin pandas
    st.write("### Registros:")
    for i, reg in enumerate(st.session_state.historial, 1):
        st.write(f"**{i}.** {reg['Fecha']} | {reg['Hematólogo']} | {reg['Tema']}")
    
    # Descargar como JSON
    historial_json = json.dumps(st.session_state.historial, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 Descargar historial (JSON)",
        data=historial_json,
        file_name="historial_envios.json",
        mime="application/json"
    )
else:
    st.info("Sin registros aún")
